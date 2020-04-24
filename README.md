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

Should you choose to accept it ... We have provided an [AWS Sam](https://github.com/awslabs/serverless-application-model) project that recieves an image over an API, resizes it and drops it into an s3 bucket. Right now its just 30 lines of actual source code, but it can already perform a task and every day it isnt in production clients cant resize images! You need to develop tooling to enable developers to iterate on this project and get changes to production as fast as possible. 

At heavywater, in addition to writing source code, deveopers are responsible for writing infrastructure as code so tooling you develop must consider that developers may want to make changes on the cloudformation templates in addition to source.

---

## Outcomes
- A latest and gratest master is live in production
- Another developer can pull request a code change on this project
- Before the change can be merged into master:
  - Their infrastructure is validated according to security policies
  - Their dev branch is unit tested
  - Their dev branch integration tested
  - The dev code does not interfere with running master and its infrastructure
- After their change is merged to master:
  - Master infrastructure is validated according to security policies
  - Master code is unit tested
  - The live production version is updated without downtime
  - Production is tested post update
  - An alarm is raised if something is wrong

---

## Tasks

**Unordered list of possible tasks to complete**
- [ ] create a github repository for this project
- [ ] create an aws free teir account
- [ ] write unit tests for python script
- [ ] write integration tests against the launched stack
- [ ] write codebuild spec file for unit tests
- [ ] trigger code pipeline and publish from github webhooks/github actions
- [ ] validate the template before launch
- [ ] make the repo installable through some package manager
- [ ] add linting/static analysis to cloudformation template
- [ ] add linting/static analysis to python script
- [ ] evaluate best practices on the project from a security context
- [ ] comment on and remediate security issues present in the template and source code
 
---

## Measurement Criteria

The interview will be conducted as a code review. It is not required that you perform all tasks or achieve all the outcomes, but *you should be prepared to explain the tradeoffs that you made* from a priority and security standpoint. 

We will clone your repo and checkout the appropriate branch. We will then try to run your code on our machine against one of our AWS account. If we "accept" that branch/PR we will approve the PR and you will merge your branch to master. We will then move on to the next branch.

Your score will be the number of the above tasks which "accepted" and able to be run from the master branch at the end of this process.

Due to the public nature of this repo, forking will share you work with other candidates. Please do no fork this repo. Clone it and init your own new git repo.


Best of luck. We look forward to your submission!
