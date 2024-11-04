import boto3

class DynamoDBShelf:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = dynamodb.Table('bookshelf')  # Ensure this matches your table name

    def save_book(self, title, author, page_count, isbn):
        try:
            self.table.put_item(
                Item={
                    'BookID': isbn,  # Use the unique identifier for the partition key
                    'Title': title,
                    'Author': author,
                    'PageCount': page_count,
                }
            )
            return {'message': 'Book saved successfully!'}
        except Exception as e:
            return {'error': str(e)}

