from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS
import boto3
import json
from dynamo_shelf import DynamoDBShelf

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
CORS(app)

shelf = DynamoDBShelf()  # Instantiate the DynamoDBShelf class

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

@app.route('/save_book', methods=['POST'])
def save_book():
    book_data = request.get_json()
    
    book_id = book_data.get("book_id")
    title = book_data.get("title")
    author = book_data.get("author", "Unknown Author")
    page_count = book_data.get("page_count", 0)
    isbn = book_data.get("isbn", "N/A")

    result = shelf.save_book(book_id, title, author, page_count, isbn)
    return jsonify(result)

@app.route('/get_books', methods=['GET'])
def get_books():
    response = shelf.table.scan()  # Scan the bookshelf table
    return jsonify(response.get('Items', []))  # Return the items or an empty list if none



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)



