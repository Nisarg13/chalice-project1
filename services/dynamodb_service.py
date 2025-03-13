import boto3

TABLE_NAME = "Students"

class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self._get_or_create_table()

    def _get_or_create_table(self):
        """Ensure table exists or create a new one"""
        try:
            table = self.dynamodb.Table(TABLE_NAME)
            table.load()
            return table
        except:
            table = self.dynamodb.create_table(
                TableName=TABLE_NAME,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            table.wait_until_exists()
            return table

    def save_student(self, student):
        self.table.put_item(Item=student.to_dict())

    def get_all_students(self):
        response = self.table.scan()
        return response.get("Items", [])

    def get_student(self, student_id):
        response = self.table.get_item(Key={"id": student_id})
        return response.get("Item")

    def update_student(self, student_id, updated_data):
        update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in updated_data.keys())
        expression_attribute_values = {f":{k}": v for k, v in updated_data.items()}

        response = self.table.update_item(
            Key={"id": student_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW",
        )
        return response.get("Attributes")

    def delete_student(self, student_id):
        self.table.delete_item(Key={"id": student_id})
