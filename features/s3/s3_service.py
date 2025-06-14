from types_boto3_s3 import S3Client


class S3Service:
    __s3_client: S3Client
    __bucket_name: str

    def __init__(self, s3_client: S3Client, bucket_name: str):
        self.__s3_client = s3_client
        self.__bucket_name = bucket_name

    def upload_file(self, source: str, dest: str) -> None:
        self.__s3_client.upload_file(source, self.__bucket_name, dest)

    def download_file(self, source: str, dest: str) -> None:
        self.__s3_client.download_file(self.__bucket_name, source, dest)

    def download_file_bytes(self, source: str) -> bytes:
        response = self.__s3_client.get_object(Bucket=self.__bucket_name, Key=source)
        return response["Body"].read()
