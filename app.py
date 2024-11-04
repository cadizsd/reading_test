from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS
import json
import boto3

# Import the DynamoDBShelf class
from dynamo_shelf import DynamoDBShelf  # Assuming your class is saved in dynamo_shelf.py

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
CORS(app)

# Initialize DynamoDBShelf
shelf = DynamoDBShelf()  # This initializes the bookshelf table

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

    # Check if ISBN is provided
    if not data.get('BookID') or data['BookID'] == 'No ISBN available':
        return jsonify({'error': 'Cannot save book without a valid ISBN.'}), 400

    # Use DynamoDBShelf's save_book method
    result = shelf.save_book(
        title=data['Title'],
        author=data['Author'],
        page_count=data['PageCount'],
        isbn=data['BookID']
    )

    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result), 201

# Endpoint to retrieve shelved books
@app.route('/shelved_books', methods=['GET'])
def shelved_books():
    try:
        response = shelf.table.scan()  # Scan the bookshelf table
        return jsonify(response['Items'])  # Return the items in JSON format
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)






