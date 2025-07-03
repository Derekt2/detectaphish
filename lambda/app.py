import json
import base64

def handler(event, context):
    """
    A Lambda function that processes a file sent in the request body.
    """
    try:
        # The body will be base64 encoded by API Gateway
        file_content = base64.b64decode(event['body'])
        
        # Here you can add your logic to process the file_content
        # For example, you could save it to S3, or analyze it.
        # For now, we'll just return a success message with the file size.
        
        file_size = len(file_content)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'File processed successfully!',
                'fileSize': file_size
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
