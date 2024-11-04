# app.py

from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS
import boto3
import json
from botocore.exceptions import ClientError
from dynamo_shelf import DynamoDBShelf

app = Flask(__name__)
load_dotenv()
CORS(app)

shelf = DynamoDBShelf()

# Route to call Google Books API
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    secret_name = "reading_test_key"
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        # Retrieve the API key from AWS Secrets Manager
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        google_books_api_key = json.loads(get_secret_value_response['SecretString'])['googlebooks']

        # Make a request to the Google Books API
        google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={google_books_api_key}"
        response = requests.get(google_books_api_url)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)  # Return Google Books API data as JSON to frontend
    except ClientError as e:
        return jsonify({"error": "Failed to retrieve Google Books API key", "details": str(e)}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error fetching data from Google Books API", "details": str(e)}), 500

# Route to save a selected book to DynamoDB
@app.route('/save_book', methods=['POST'])
def save_book():
    book_data = request.get_json()
    
    book_id = book_data.get("book_id")
    title = book_data.get("title")
    author = book_data.get("author", "Unknown Author")
    page_count = book_data.get("page_count", 0)
    isbn = book_data.get("isbn", "N/A")
    description = book_data.get("description", "No description available")

    result = shelf.save_book(book_id, title, author, page_count, isbn, description)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)  # Ensuring it runs on port 8080


