import boto3
import json

SNS_TOPIC_ARN = "arn:aws:sns:us-east-2:379660073266:students"

class SNSService:
    def __init__(self):
        self.sns = boto3.client("sns")

    def send_notification(self, subject, message):
        """Send a notification to SNS topic"""
        self.sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=json.dumps(message),
            Subject=subject
        )
