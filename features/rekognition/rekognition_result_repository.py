from types_boto3_dynamodb import DynamoDBClient


class RekognitionResultRepository:
    __dynamodb_client: DynamoDBClient
    __table_name: str

    def __init__(self, dynamodb_client: DynamoDBClient, table_name: str):
        self.__dynamodb_client = dynamodb_client
        self.__table_name = table_name

    def __does_table_exist(self) -> bool:
        return self.__table_name in self.__dynamodb_client.list_tables()

    def __initialize_table(self) -> None:
        self.__dynamodb_client.create_table(
            TableName=self.__table_name,
            KeySchema=[
                {
                    "AttributeName": "filename",
                    "KeyType": "HASH",
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "filename",
                    "AttributeType": "S",
                }
            ],
        )
        waiter = self.__dynamodb_client.get_waiter("table_exists")
        waiter.wait(TableName=self.__table_name)

    def update_result(self, filename: str, value: str) -> None:
        if not self.__does_table_exist():
            self.__initialize_table()
        self.__dynamodb_client.put_item(
            TableName=self.__table_name,
            Item={filename: {"S": filename}, value: {"S", value}},
        )
