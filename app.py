from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS
import boto3
import json

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
CORS(app)

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
shelf = dynamodb.Table('bookshelf')  # Ensure this matches your DynamoDB table name

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

# Endpoint to save a book to DynamoDB
@app.route('/save_book', methods=['POST'])
def save_book():
    data = request.get_json()
    try:
        shelf.put_item(
            Item={
                'BookID': data['ISBN'],
                'Title': data['Title'],
                'Author': data['Author'],
                'PageCount': data['PageCount'],
                # Remove description from being saved
            }
        )
        return jsonify({'message': 'Book saved successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to retrieve shelved books
@app.route('/shelved_books', methods=['GET'])
def shelved_books():
    try:
        response = shelf.scan()  # Scan the bookshelf table
        return jsonify(response['Items'])  # Return the items in JSON format
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)





