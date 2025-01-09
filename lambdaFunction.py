import json
import boto3

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    # Add logging for debugging
    print(f"Received event: {json.dumps(event)}")
    
    # Ensure the 'detail' key exists
    event_details = event.get('detail', {})
    
    # Get the resources and event information, default to empty list or "Unknown" if missing
    resource_ids = event_details.get('resources', [])
    event_name = event_details.get('eventName', 'Unknown Event')
    user_identity = event_details.get('userIdentity', {}).get('arn', 'Unknown User')
    
    # Prepare the message for the SNS notification
    message = (f"Tags were modified on the following resources: {resource_ids}\n"
               f"Event Name: {event_name}\n"
               f"Modified by: {user_identity}")
    
    # Publish the message to the SNS topic
    sns_client.publish(
        TopicArn='arn:aws:sns:<region>:<account_id>:EBS-Tag-Change-Notifications',
        Message=message,
        Subject='EBS Tag Change Detected'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent successfully!')
    }
