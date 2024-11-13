import json
import boto3


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('bookshelf') 


def lambda_handler(event, context):
    try:
        # Extract book details from the incoming request (assuming JSON body)
        body = json.loads(event.get('body', '{}'))
        
        isbn = body.get('isbn')
        title = body.get('title')
        author = body.get('author')
        page_count = body.get('page_count')
        
        # Validate required fields
        if not all([isbn, title, author, page_count]):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing required fields'})
            }
        
        # Insert the book into DynamoDB
        table.put_item(
            Item={
                'BookID': isbn,        # Use ISBN as the unique identifier (partition key)
                'Title': title,
                'Author': author,
                'PageCount': page_count,
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Book logged successfully'})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error: {str(e)}'})
        }
