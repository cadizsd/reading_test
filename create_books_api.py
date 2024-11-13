import boto3
import json
import sys

# Initialize Boto3 clients
client = boto3.client('apigateway', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')
iam_client = boto3.client('iam', region_name='us-east-1')

# Step 1: Check if API already exists
response = client.get_rest_apis()
apis = response.get('items', [])

for api in apis:
    if api.get('name') == 'BookshelfAPI':
        print('API already exists')
        sys.exit(0)

# Step 2: Create the API Gateway
response = client.create_rest_api(
    name='BookshelfAPI',
    description='API to interact with Google Books and DynamoDB for book tracking.',
    endpointConfiguration={'types': ['REGIONAL']}
)
api_id = response["id"]

# Get the root resource ID
resources = client.get_resources(restApiId=api_id)
root_id = [resource for resource in resources["items"] if resource["path"] == "/"][0]["id"]

# Step 3: Create /search resource
search_resource = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='search'
)
search_resource_id = search_resource["id"]

# Step 4: Create GET method for /search
client.put_method(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)

# Get the ARN for the 'searchBooks' Lambda function
search_lambda_arn = lambda_client.get_function(FunctionName='searchBooksFunction')['Configuration']['FunctionArn']
search_uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{search_lambda_arn}/invocations'

# Step 5: Integrate /search with Lambda
client.put_integration(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='GET',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=search_uri
)

# Enable CORS for /search
client.put_method_response(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Origin': True
    }
)

client.put_integration_response(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    }
)

# Step 6: Create /save_book resource
save_book_resource = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='save_book'
)
save_book_resource_id = save_book_resource["id"]

# Step 7: Create POST method for /save_book
client.put_method(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='POST',
    authorizationType='NONE'
)

# Get the ARN for the 'saveBook' Lambda function
save_lambda_arn = lambda_client.get_function(FunctionName='saveBookFunction')['Configuration']['FunctionArn']
save_uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{save_lambda_arn}/invocations'

# Step 8: Integrate /save_book with Lambda
client.put_integration(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='POST',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=save_uri
)

# Enable CORS for /save_book
client.put_method_response(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Origin': True
    }
)

client.put_integration_response(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    }
)

# Step 9: Deploy the API
deployment = client.create_deployment(
    restApiId=api_id,
    stageName='prod'
)

print(f"API Gateway 'BookshelfAPI' created with ID: {api_id}")
print("API Gateway deployment complete.")
