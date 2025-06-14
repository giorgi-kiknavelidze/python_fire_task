#!/usr/bin/env python
from typer import Typer
from features.my_auto.my_auto_downloader import MyAutoDownloader
from features.s3.s3_service import S3Service

app = Typer()


@app.command()
def download_from_myauto(page_number: int, output_folder: str) -> None:
    my_auto_downloader = MyAutoDownloader()
    my_auto_downloader.download_images(page_number, output_folder)


app()
