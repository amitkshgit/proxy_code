import re
import os
import boto3
import requests


def path_to_call():
    file_path = "/etc/systemd/system/gunicorn.service"
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = r'--reload\s*(.*?)\s*-b'
    match = re.search(pattern, content)

    if match:
        result = match.group(1).replace(' ', '')
        return result
    else:
        return None

def read_ddb_env_variable():
    ssm_client = boto3.client('ssm', region_name='us-east-2')
    response = ssm_client.get_parameter(Name='proxy_env', WithDecryption=True)
    proxy_db = response['Parameter']['Value']
    return(proxy_db)

def get_public_ipv4(token):
    url = "http://169.254.169.254/latest/meta-data/public-ipv4"
    headers = {"X-aws-ec2-metadata-token": token}
    response = requests.get(url, headers=headers)
    public_ipv4 = response.text
    return public_ipv4

def get_aws_token():
    url = "http://169.254.169.254/latest/api/token"
    headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
    response = requests.put(url, headers=headers)
    token = response.text
    return token

def insert_public_ip_dynamodb():
    # Get the AWS metadata token
    token = get_aws_token()

    # Get the public IPv4 address
    public_ipv4 = get_public_ipv4(token)

    # Create a DynamoDB client with the specified region
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    # Specify the table name
    table_name = read_ddb_env_variable()
    table = dynamodb.Table(table_name)

    # Create the item to be inserted
    url_path = path_to_call()
    item = {
        'ipaddress': public_ipv4,
        'health': 'ok',
        'url': url_path
    }

    # Insert the item into the DynamoDB table
    table.put_item(Item=item)

    print(f"Public IP address {public_ipv4} inserted into DynamoDB table {table_name}")

if __name__ == "__main__":
    insert_public_ip_dynamodb()
