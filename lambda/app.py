import json

def handler(event, context):
    """
    A simple Lambda function that returns a success message.
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': 'Hello from Lambda!'})
    }
