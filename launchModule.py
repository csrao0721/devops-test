import boto3
from boto3.s3.transfer import S3Transfer
import json
import sys
import time

action = sys.argv[1]
filename = sys.argv[2]
environment = sys.argv[3]
stage = sys.argv[4]

s3_client = boto3.client('s3')
if "s3://" in filename:
    filename = filename.replace("s3://", "")
    filename_split = filename.split("/", 1)
    file_object = s3_client.get_object(Bucket=filename_split[0], Key=filename_split[1])
    config_content = file_object['Body'].read().decode('utf-8')
    config_json = json.loads(config_content)
else:
    with open(filename, 'r') as fileContent:
        config_json = json.loads(fileContent.read())

# Get environment JSON.
env_json = config_json['environment'][environment]
config_parameters = {}
for key in env_json:
    config_parameters[key] = env_json[key]
parameters_list = []
parameter = {}
parameters_dic = {}

region_name='us-east-1'
if 'region' in config_json:
    region_name=config_json['region']
if 'region' in env_json:
    region_name=env_json['region']

if 'keypair_name' in env_json:
    parameter['ParameterKey'] = 'KeyPairName'
    parameter['ParameterValue'] = env_json['keypair_name']
    parameters_list.append(parameter)

master_cft_name = config_json['module']

# Get artifact location from stage name.
try:
    artifacts_bucket = env_json['stage'][stage]
except Exception as e:
    artifacts_bucket = 'artifacts_bucket'

# Relative path in case CFT location is not in the current directory.
try:
    cft_location = config_json['cft_location']
except Exception as e:
    print "Could not find key cft_location in config file. Using default."
    cft_location = ""

# HTTPS URL for S3 CFT path; the s3_path is adjusted to accomodate
# different stage launches.
s3 = boto3.client('s3')
try:
    s3_path = config_json['cft_s3_path']
    s3_path = s3_path.replace("{bucket_name}", artifacts_bucket)
    key = s3_path.replace("https://s3.amazonaws.com/" + artifacts_bucket + "/", "")
    file_content = ''
    s3_object = s3.get_object(Bucket=artifacts_bucket, Key=key)
    file_content = s3_object['Body'].read().decode('utf-8')
except Exception as e:
    print "Could not find key cft_s3_path in config file. Using default."
    s3_path = "https://s3.amazonaws.com/artifacts_bucket/hw-cli/SkillCFT.json"

# This series of try-except statements sets the necessary parameters.
try:
    parameter = {}
    parameter['ParameterKey'] = 'BucketName'
    parameter['ParameterValue'] = env_json['app_bucket_name']
    parameters_list.append(parameter)
except:
    print "app_bucket_name not found in config file"

try:
    parameter = {}
    parameter['ParameterKey'] = 'BucketName'
    parameter['ParameterValue'] = env_json['BucketName']
    parameters_list.append(parameter)
except:
    print "BucketName not found not found in config file"

try:
    parameter = {}
    parameter['ParameterKey'] = 'DataBucketName'
    parameter['ParameterValue'] = env_json['DataBucketName']
    parameters_list.append(parameter)
except:
    print "DataBucketName not found in config file"

try:
    template = json.loads(file_content)
    cft_parameters = template['Parameters']
    for key in cft_parameters:
        if key in config_parameters:
         parameters_dic[key] = config_parameters[key]
    for key in parameters_dic:
        parameter= {}
        parameter['ParameterKey'] = key
        parameter['ParameterValue'] = parameters_dic[key]
        parameters_list.append(parameter)
    print parameters_list
except:
    print "Params not found in config file"



flag = 0
break_flag = 0

# CFT bucket at the account level.
try:
    cft_bucket_name = config_json['cft_bucket_name']
except Exception as e:
    print "Could not find key cft_bucket_name in config file. Using default."
    cft_bucket_name = "hw-cftbucket"

client = boto3.setup_default_session(region_name=region_name)
client = boto3.client('cloudformation')
local_path = cft_location + master_cft_name + '.json'
sts_client = boto3.client('sts')

if 'assume_role' in env_json.keys() and env_json['assume_role'] != '':
    if 'external_id' in env_json['assume_role'].keys():
        assumed_role_object = sts_client.assume_role(
            RoleArn=env_json['assume_role']['role_arn'],
            RoleSessionName=env_json['assume_role']['role_session_name'],
            ExternalId=env_json['assume_role']['external_id']
        )
    else:
        assumed_role_object = sts_client.assume_role(
            RoleArn=env_json['assume_role']['role_arn'],
            RoleSessionName=env_json['assume_role']['role_session_name']
        )
    credentials = assumed_role_object['Credentials']
    client = boto3.client('cloudformation',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

if(action == "launch"):
    response = client.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'CREATE_IN_PROGRESS', 'UPDATE_COMPLETE'])
    summary = response['StackSummaries']
    print type(summary)
    print len(summary)
    for stack in summary:
        print stack
        print type(stack)
        if stack['StackName'] == master_cft_name:
            print "Master CFT Running"
            flag = 1

    if flag == 0:
        try:
            response = client.create_stack(
                StackName=master_cft_name,
                TemplateURL=s3_path,
                Capabilities=['CAPABILITY_NAMED_IAM'],
                OnFailure='ROLLBACK',
                Parameters=parameters_list,
            )
            while True:
                response = client.list_stacks(StackStatusFilter=['CREATE_COMPLETE'])
                summary = response['StackSummaries']
                for stack in summary:
                    if stack['StackName'] == master_cft_name:
                        print stack
                        break_flag = 1
                        break
                if break_flag == 0:
                    print 'creating CFT'
                    time.sleep(40)
                else:
                    break
        except Exception as e:
            print e

    print 'Resources Created successfully'

# Delete the CFT.
elif(action == "teardown"):
    print master_cft_name
    stack_name = master_cft_name.strip()
    try:
        stack_id = client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackId']
        waiter = client.get_waiter('stack_delete_complete')
        response = client.delete_stack(StackName=stack_id)
    except Exception as e:
        print e
    else:
        print "Waiting for %s to teardown..." % master_cft_name
        waiter.wait(StackName=stack_id)
        print "%s successfully torn down." % master_cft_name
