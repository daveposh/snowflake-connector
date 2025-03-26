#!/usr/bin/env python3
import boto3
import base64
import os
from dotenv import load_dotenv

def encrypt_value(kms_client, key_id, value):
    """Encrypt a value using AWS KMS and return base64 encoded string."""
    try:
        response = kms_client.encrypt(
            KeyId=key_id,
            Plaintext=value.encode('utf-8')
        )
        return base64.b64encode(response['CiphertextBlob']).decode('utf-8')
    except Exception as e:
        print(f"Error encrypting value: {str(e)}")
        return None

def main():
    # Load environment variables
    load_dotenv()
    
    # AWS Configuration
    region = os.getenv('AWS_REGION', 'us-west-2')
    key_id = os.getenv('AWS_KMS_KEY_ID')
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    if not all([key_id, aws_access_key, aws_secret_key]):
        print("Error: AWS credentials not found in .env file")
        return
    
    # Initialize KMS client
    kms_client = boto3.client(
        'kms',
        region_name=region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    
    # Dictionary of credentials to encrypt
    credentials = {
        'KMS_ENCRYPTED_ACCOUNT': input("Enter Snowflake Account: "),
        'KMS_ENCRYPTED_USER': input("Enter Snowflake User: "),
        'KMS_ENCRYPTED_PASSWORD': input("Enter Snowflake Password: "),
        'KMS_ENCRYPTED_ROLE': input("Enter Snowflake Role: "),
        'KMS_ENCRYPTED_WAREHOUSE': input("Enter Snowflake Warehouse: "),
        'KMS_ENCRYPTED_DATABASE': input("Enter Snowflake Database: "),
        'KMS_ENCRYPTED_SCHEMA': input("Enter Snowflake Schema: ")
    }
    
    # Encrypt each credential
    encrypted_credentials = {}
    for key, value in credentials.items():
        if value:
            encrypted_value = encrypt_value(kms_client, key_id, value)
            if encrypted_value:
                encrypted_credentials[key] = encrypted_value
    
    # Update .env file with encrypted values
    with open('.env', 'r') as f:
        env_lines = f.readlines()
    
    # Create new .env content
    new_env_content = []
    for line in env_lines:
        if line.startswith('#'):
            new_env_content.append(line)
        else:
            key = line.split('=')[0].strip()
            if key in encrypted_credentials:
                new_env_content.append(f"{key}={encrypted_credentials[key]}\n")
            else:
                new_env_content.append(line)
    
    # Write updated content back to .env
    with open('.env', 'w') as f:
        f.writelines(new_env_content)
    
    print("\nCredentials have been encrypted and updated in .env file")
    print("Please verify the .env file contents and ensure it's properly secured")

if __name__ == "__main__":
    main() 