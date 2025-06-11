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

            car_details = {
                'Make': None,
                'Model': None,
                'Type': None,
                'Color': None,
                'Year': None,
                'OtherFeatures': []
            }

            for label in response['Labels']:
                label_name = label['Name'].lower()
                confidence = label['Confidence']

                if label_name in ['car', 'vehicle', 'automobile']:
                    for parent in label.get('Parents', []):
                        parent_name = parent['Name'].lower()
                        if parent_name not in ['vehicle', 'transportation']:
                            car_details['Make'] = parent['Name']
                            break


                elif label_name in ['sedan', 'suv', 'truck', 'coupe', 'hatchback']:
                    car_details['Type'] = label['Name']
                elif 'model' in label_name and confidence > 85:
                    car_details['Model'] = label['Name']


                elif label_name in ['red', 'blue', 'black', 'white', 'silver', 'gray', 'green']:
                    car_details['Color'] = label['Name']


                elif label_name.isdigit() and len(label_name) == 4 and 1900 < int(label_name) < 2025:
                    car_details['Year'] = label['Name']


                elif label_name in ['wheel', 'tire', 'headlight', 'taillight', 'license plate', 'sunroof']:
                    car_details['OtherFeatures'].append(label['Name'])

            analysis_id = str(uuid.uuid4())

            current_time = datetime.now().isoformat()

            item = {
                'AnalysisID': analysis_id,
                'ImageBucket': bucket,
                'ImageKey': key,
                'CarDetails': car_details,
                'AllLabels': response['Labels'],
                'AnalysisDate': current_time,
                'Metadata': {
                    'LabelCount': len(response['Labels']),
                    'CarRecognized': any([car_details['Make'], car_details['Model']])
                }
            }

            table.put_item(Item=item)

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Car analysis completed and saved successfully',
                    'analysis_id': analysis_id,
                    'car_details': car_details
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