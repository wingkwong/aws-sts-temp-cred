#!/usr/bin/python3
import sys
import configparser
import json
import os
import boto3

sts = boto3.client("sts")
fp = os.path.expanduser("~/")


def read_ini(config_or_creds):
    config = configparser.ConfigParser()
    config.read("{}/.aws/{}".format(fp, config_or_creds))
    return config

profile_name, token, duration_in_seconds = sys.argv[1:]
response = sts.get_session_token(
    DurationSeconds=duration_in_seconds,
    TokenCode=token,
    SerialNumber="arn:aws:iam::<IAM/Users/MFA something>",
)
aws_cred = read_ini(config_or_creds="credentials")
prof_name = "MFA_{}".format(profile_name)
if prof_name in aws_cred.sections():
    print("{} already exists, writing temporary credentials".format(prof_name))
    pass
else:
    aws_cred.add_section(section=prof_name)
aws_cred[prof_name]["aws_access_key_id"] = response["Credentials"]["AccessKeyId"]
aws_cred[prof_name]["aws_secret_access_key"] = response["Credentials"]["SecretAccessKey"]
aws_cred[prof_name]["aws_session_token"] = response["Credentials"]["SessionToken"]
with open("{}/.aws/{}".format(fp, "credentials"), "w") as awsCredfile:
    aws_cred.write(awsCredfile)
