from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError
import json

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
CORS(app)


# Backend route to call Google Books API
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query')  # Get the query from the search form

    secret_name = "reading_test_key"
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    google_books_api_key = json.loads(get_secret_value_response['SecretString'])['googlebooks']
    
    google_books_api = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={google_books_api_key}"
    
    response = requests.get(google_books_api)
    data = response.json()
    return jsonify(data)  # Return Google Books API data as JSON to frontend

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
