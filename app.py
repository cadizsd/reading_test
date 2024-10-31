from flask import Flask, jsonify, request
import requests
import json
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for cross-origin requests

    @app.route('/search', methods=['GET'])
    def search():
        query = request.args.get('query')  # Get the query from the request parameters
        google_books_api_key = os.getenv('API_KEY')  # Get API key from environment variable

        # Call the Google Books API with the query
        google_books_api = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={google_books_api_key}"
        response = requests.get(google_books_api)

        if response.status_code == 200:
            data = response.json()
            return jsonify(data)  # Return JSON response to the frontend
        else:
            return jsonify({"error": "Failed to retrieve data"}), 500  # Handle API errors

    return app


def launch_app():
    return create_app()


if __name__ == '__main__':
    app = launch_app()
    app.run(host="0.0.0.0", port=8080)
