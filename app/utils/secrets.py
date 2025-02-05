import os
import boto3
from dotenv import load_dotenv
import json

load_dotenv()


def get_secret():
    cloud_env = os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
    if cloud_env:
        secret_name = os.environ.get("SECRET_NAME")
        region_name = "ap-southeast-1"
        session = boto3.session.Session()

        client = session.client(service_name="secretsmanager", region_name=region_name)
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response["SecretString"])

        msql_ei = json.loads(secret["DB_MSQL_MAIN"])["DB_EI_RO"]
        msql_acl = json.loads(secret["DB_MSQL_MAIN"])["DB_MSQL"]
        gims_ro = json.loads(secret["DB_URI"])["GIMS_RO"]
        oracle_w = json.loads(secret["DB_URI"])["GIMS_W"]
        microsoft_auth = secret["AUTH_URL"]
        finance_db = json.loads(secret["DB_MSQL_MAIN"])["DB_FINANCE"]

        return msql_acl, msql_ei, gims_ro, oracle_w, microsoft_auth, finance_db
    else:
        msql_acl = os.environ.get("DB_MSQL_ACL")
        msql_ei = os.environ.get("DB_MSQL_EI")
        gims_ro = os.environ.get("GIMS_RO")
        oracle_w = os.environ.get("GIMS_W")
        microsoft_auth = os.environ.get("AUTH_URL")
        finance_db = os.environ.get("DB_MSQL_MAIN")

        return msql_acl, msql_ei, gims_ro, oracle_w, microsoft_auth, finance_db
