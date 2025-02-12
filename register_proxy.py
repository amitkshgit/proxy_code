import re
import os
import boto3
import requests


def path_to_call(file_name="proxy.py"):
    try:
        # Read the contents of the file
        with open(file_name, 'r') as file:
            text = file.read()
        
        # Search for the pattern
        pattern = r'app_\w{10}'
        match = re.search(pattern, text)
        
        if match:
            return match.group()
        else:
            return None
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None
    except IOError:
        print(f"Error: Unable to read file '{file_name}'.")
        return None


def read_ddb_env_variable():
    ssm_client = boto3.client('ssm', region_name='us-east-2')
    response = ssm_client.get_parameter(Name='proxy_env', WithDecryption=True)
    proxy_db = response['Parameter']['Value']
    return(proxy_db)

def get_region(token):
    url = "http://169.254.169.254/latest/meta-data/placement/region"
    headers = {"X-aws-ec2-metadata-token": token}
    response = requests.get(url, headers=headers)
    region = response.text
    return region

def get_instance_id(token):
    url = "http://169.254.169.254/latest/meta-data/instance-id"
    headers = {"X-aws-ec2-metadata-token": token}
    response = requests.get(url, headers=headers)
    instance_id = response.text
    return instance_id


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
    # Get the region 
    ec2_region = get_region(token)
    # Get the instance-id
    instance_id = get_instance_id(token)

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
        'url': url_path,
        'region': ec2_region,
        'instanceid': instance_id
    }

    # Insert the item into the DynamoDB table
    table.put_item(Item=item)

    print(f"Public IP address {public_ipv4} inserted into DynamoDB table {table_name}")

if __name__ == "__main__":
    insert_public_ip_dynamodb()
