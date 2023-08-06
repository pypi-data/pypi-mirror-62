# botoless
A smaller view of boto3, intended for serverless application development

Botoless is no more and no less than **the interface to various AWS services that I repeatedly find myself wanting when I am developing serverless functionality on AWS in python using Chalice**. Boto3 is a huge library, with lots of legacy commitments, that must cover all of AWS; runtime operations in serverless apps is just one small usage profile, so it's no surprise that boto3 can feel clunky in this context.

Botoless makes a few assumptions about how it's being used that allow it to present a much simpler interface than boto3:

1. It assumes that you are building a serverless web app or microservice, so it concentrates on the AWS services and usage patterns that are most relevant to that scenario
2. It assumes that it is being used in the context of a Lambda function runtime; this means, for example, that boto3 will be available and that it will be invoked with the credentials of the AWS account under which that Lambda is deployed

## Installation

```
pip install botoless
```

## Usage


