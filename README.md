# aws-sts-temp-cred
Request temporary credentials for a MFA-enabled AWS account or IAM user

## Usage

Update ``SerialNumber`` in Line 21 and then run

```py
python3 main.py <profile_name:str> <mfa_token:int> <duration_in_seconds:int>
```