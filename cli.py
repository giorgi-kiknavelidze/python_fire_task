#!/usr/bin/env python
import boto3
from typer import Typer
from features.my_auto.my_auto_downloader import MyAutoDownloader
from features.s3.s3_service import S3Service

app = Typer()
s3_client = boto3.client("s3")


@app.command()
def download_from_myauto(page_number: int, output_folder: str) -> None:
    my_auto_downloader = MyAutoDownloader()
    my_auto_downloader.download_images(page_number, output_folder)


@app.command()
def upload_to_bucket(bucket_name: str, source_folder: str) -> None:
    my_bucket_uploader = S3Service(s3_client, bucket_name)
    my_bucket_uploader.upload_folder(source_folder)


app()
