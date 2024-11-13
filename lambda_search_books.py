import json
import boto3
import requests

def get_secret():
    secret_name = "reading_test_key"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])
        return secret['googlebooks']
    except Exception as e:
        print(f"Error retrieving secret: {str(e)}")
        raise e

def lambda_handler(event, context):
    # Extract query parameter
    query = event['queryStringParameters'].get('query', '')

    if not query:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Query parameter is required'})
        }

    # Get the Google Books API key from Secrets Manager
    api_key = get_secret()

    # Call the Google Books API
    google_books_api = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
    response = requests.get(google_books_api)
    data = response.json()

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(data)
    }
