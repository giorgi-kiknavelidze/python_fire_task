import boto3
import json
import uuid
from datetime import datetime

def lambda_handler(event, context):
    rekognition = boto3.client('rekognition')
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')

    table = dynamodb.Table('rekogintionAnalysesDB')

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        try:
            response = rekognition.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                },
                MaxLabels=20,
                MinConfidence=75
            )

            analysis_id = str(uuid.uuid4())
            current_time = datetime.now().isoformat()

            item = {
                'AnalysisID': analysis_id,
                'ImageBucket': bucket,
                'ImageKey': key,
                'RekognitionResponse': json.dumps(response), 
                'AnalysisDate': current_time
            }

            table.put_item(Item=item)

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Rekognition analysis saved successfully',
                    'analysis_id': analysis_id
                })
            }

        except Exception as e:
            print(f"Error processing image {key}: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': f"Error processing image {key}",
                    'error': str(e)
                })
            }
