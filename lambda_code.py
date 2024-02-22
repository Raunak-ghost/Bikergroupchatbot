import boto3 as 
import json

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Parse the event data
    body = json.loads(event["body"])
    message = body["message"]["text"]

    # Process the message
    if message == "/rider_details":
        response = get_rider_details(body["rider_id"])
    elif message == "/rider_stats":
        response = get_rider_stats(body["rider_id"])
    else:
        response = "Invalid command"

    # Return the response
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": response
        })
    }

def get_rider_details(rider_id):
    # Query DynamoDB to get rider details
    response = dynamodb.get_item(
        TableName='RiderDetails',
        Key={
            'rider_id': {'S': rider_id}
        }
    )

    # Extract rider details from the response
    rider_details = response['Item']

    # Format the rider details
    formatted_rider_details = {
        'rider_id': rider_details['rider_id']['S'],
        'name': rider_details['name']['S'],
        'email': rider_details['email']['S'],
        'phone': rider_details['phone']['S']
    }

    return formatted_rider_details

def get_rider_stats(rider_id):
    # Query DynamoDB to get rider stats
    response = dynamodb.get_item(
        TableName='RiderStats',
        Key={
            'rider_id': {'S': rider_id}
        }
    )

    # Extract rider stats from the response
    rider_stats = response['Item']

    # Format the rider stats
    formatted_rider_stats = {
        'rider_id': rider_stats['rider_id']['S'],
        'total_trips': rider_stats['total_trips']['N'],
        'total_distance': rider_stats['total_distance']['N'],
        'total_duration': rider_stats['total_duration']['N']
    }

    return formatted_rider_stats
