from features.rekognition.rekognition_result_repository import (
    RekognitionResultRepository,
)
import boto3
import json

from typing import Any


def lambda_handler(event: Any, context: Any) -> None:
    rekognition = boto3.client("rekognition")
    dynamodb_client = boto3.client("dynamodb")

    repo = RekognitionResultRepository(dynamodb_client, "rekognitionAnalysesDB")

    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        try:
            response = rekognition.detect_labels(
                Image={"S3Object": {"Bucket": bucket, "Name": key}},
                MaxLabels=20,
                MinConfidence=75,
            )

            response_str = json.dumps(response)

            repo.update_result(key, response_str)

        except Exception as e:
            print(f"Error processing image {key}: {str(e)}")
