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

# Route to save a selected book to DynamoDB
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
