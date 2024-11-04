import boto3

class DynamoDBShelf:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = dynamodb.Table('bookshelf')  # Ensure this matches your table name

    def save_book(self, book_id, title, author, page_count, isbn):
        try:
            self.table.put_item(
                Item={
                    'BookID': book_id,  # Use the unique identifier for the partition key
                    'Title': title,
                    'Author': author,
                    'PageCount': page_count,
                    'ISBN': isbn
                }
            )
            return {'message': 'Book saved successfully!'}
        except Exception as e:
            return {'error': str(e)}

