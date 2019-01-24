# HeavyWater DevOps Test

## Purpose

The purpose of this test is to evaluate your abilities in several dimensions at once.

  1. Do you understand the principles of DevSecOps and GitOps
  1. Can you build something that works
  1. Do you have a grasp of the tool chain from code on your local to code in production
  1. Can you explain your design and thinking process
  1. Are you excited by learning and challenges

---

## Your Mission

Should you choose to accept it ... We have given you a CloudFormation template, a config file and a python script. The python script reads the config file, reads the CFT from S3 then launches the stack with the appropriate configuration based on the config file and commandline variables. Complete as many of the tasks below as you can. The goal is to complete as many as you can. There is no order and no preference from us on which to tackle first.

---
## Tasks

**Unordered list of possible tasks to complete**

- [ ] write unit tests for python script
- [ ] write integration tests against the launched stack
- [ ] write code build spec file for unit tests
- [ ] write code pipeline that executes build spec and unit tests
- [ ] trigger code pipeline and publish from github webhooks
- [ ] validate the cloudformation template before launch
- [ ] write a config file validator
  - needs to be easily extensible aka via some sort of config
- [ ] make the repo installable through some package manager
  - examples: homebrew private tap, npm private repo, github releases, etc
- [ ] allow for S3 upload of CloudFormation template
- [ ] add yaml support for the cloudformation template
- [ ] add yaml support for the config file
- [ ] add commandline flags (example: -f {input} / --file {input})
- [ ] add linting/static analysis to cloudformation template
- [ ] add linting/static analysis to python script
- [ ] add linting/static analysis to the config file

---
## Measurement Criteria

The interview will be conducted as a code review. We will clone your repo and checkout the appropriate branch. We will then try to run your code on our machine against one of our AWS account. If we "accept" that branch/PR we will approve the PR and you will merge your branch to master. We will then move on to the next branch.

Your score will be the number of the above tasks which "accepted" and able to be run from the master branch at the end of this process.

Due to the public nature of this repo, forking will share you work with other candidates. Please do no fork this repo. Clone it and init your own new git repo.


Best of luck. We look forward to your submission!
