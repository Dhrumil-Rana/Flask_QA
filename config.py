from dotenv import load_dotenv
import os
import json
from urllib.parse import quote_plus
load_dotenv()

def get_secret_from_aws(secret_name, region_name="us-east-1"):
    import boto3
    from botocore.exceptions import ClientError
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    try:
        #print(f"Retrieving secret: {secret_name} from region: {region_name}")
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        return get_secret_value_response['SecretString']
    except ClientError as e:
        print(f"Error retrieving secret: {e}")
        return None

class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Get DB credentials from AWS or env
    db_secret = (
        get_secret_from_aws(os.getenv('AWS_SECRET_NAME'), os.getenv('AWS_REGION'))
        or os.getenv('SECRET_KEY', 'very secret key')
    )
    db_secret = json.loads(db_secret) if isinstance(db_secret, str) else db_secret

    # Use a separate secret key for Flask session
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'super-secret-flask-key')

    if not isinstance(db_secret, dict):
        raise ValueError("DB secret must be a dictionary with 'username', 'password', 'host', 'port', and 'dbname' keys.")

    encoded_password = quote_plus(db_secret['password'])
    UPLOAD_FOLDER = 'static/upload/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{db_secret['username']}:{encoded_password}@{db_secret['host']}:{db_secret['port']}/{db_secret['dbname']}"
    )