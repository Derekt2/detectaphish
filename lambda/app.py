import json
import base64

def handler(event, context):
    """
    A Lambda function that processes a file sent in the request body.
    """
    body = json.loads(event['body'])
    file_content = base64.b64decode(body['body'])
    
    file_size = len(file_content)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'File processed successfully!',
            'fileSize': file_size
        })
    }
