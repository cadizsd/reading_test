# dynamo_shelf.py

import boto3

class DynamoDBShelf:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = dynamodb.Table('bookshelf')

    def save_book(self, book_id, title, author, page_count, isbn):
        try:
            self.table.put_item(
                Item={
                    'BookID': book_id,      # Partition Key
                    'Title': title,
                    'Author': author,
                    'PageCount': page_count,
                    'ISBN': isbn            # ISBN attribute
                }
            )
            return {"message": "Book saved successfully"}
        except Exception as e:
            return {"error": str(e)}

    def get_books(self):
        try:
            response = self.table.scan()
            return response.get('Items', [])
        except Exception as e:
            return {"error": str(e)}
