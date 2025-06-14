from types_boto3_s3 import S3Client
import os
from pathlib import Path

class S3Service:
    __s3_client: S3Client
    __bucket_name: str

    def __init__(self, s3_client: S3Client, bucket_name: str):
        self.__s3_client = s3_client
        self.__bucket_name = bucket_name

    def upload_file(self, source: str, dest: str) -> None:
        self.__s3_client.upload_file(source, self.__bucket_name, dest)

    def __get_file_list_recursive(self, source_folder: str) -> list[str]:
        full_path_to_source_folder = os.path.realpath(source_folder)
        files = []

        for (dirpath, dirnames, filenames) in os.walk(source_folder):
            for filename in filenames:
                full_path = os.path.realpath(os.path.join(dirpath, filename))
                relative_path = Path(full_path).relative_to(full_path_to_source_folder)
                files.append(str(relative_path))
        return files

    def upload_folder(self, source_folder: str) -> None:
        source_folder_path = Path(source_folder)
        files = self.__get_file_list_recursive(source_folder)
        for files in files:
            self.upload_file(os.path.join(source_folder, file), file)
        