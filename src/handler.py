"""Lambda function for uploading files to S3"""
import json

from src.utils import get_last_month_edit_counts, get_latest_date_time, upload_file_to_s3


def main(event, context):
    parameters = event['queryStringParameters']
    if not isinstance(parameters, dict) or 'title' not in parameters:
        response = {'statusCode': 400, 'body': {'message': 'ERROR : Bad Request.'}}
        return response

    title = parameters['title'].strip()
    date = get_latest_date_time(title)
    month_last_updates = get_last_month_edit_counts(title)
    upload_file_to_s3(date, month_last_updates, title)

    body = {
        'message': 'File with title - {} Upload Successful'.format(title),
    }

    response = {
        'statusCode': 200,
        'body': json.dumps(body)
    }

    return response
