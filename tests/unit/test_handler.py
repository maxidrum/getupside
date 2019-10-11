"""Unit tests for Lambda handler."""

import json
import unittest
from mock import patch

from src.handler import main


LATEST_DATE_TIME = '00:00, 0 October 2019'
LAST_MONTH_EDIT_COUNTS = '22'
BODY = {'message': 'File with title - Test title Upload Successful'}


class TestHandler(unittest.TestCase):
    """
    Test lambda handler
    """
    def test_handler_error(self):
        """Test handler main function for bad response"""
        response = main({"queryStringParameters": {"test": "test_parameter"}}, {})
        self.assertIsInstance(response, dict)
        self.assertEqual(400, response["statusCode"])
        self.assertEqual('ERROR : Bad Request.', response['body']['message'])


    @patch('src.handler.get_latest_date_time')
    @patch('src.handler.get_last_month_edit_counts')
    @patch('src.handler.upload_file_to_s3')
    def test_handler_response(self, mocked_get_latest_date_time, mocked_get_last_month_edit_counts,
                              mocked_upload_file_to_s3):
        """Test handler main function for successfully response"""
        mocked_get_latest_date_time.return_value = LATEST_DATE_TIME
        mocked_get_last_month_edit_counts.return_value = LAST_MONTH_EDIT_COUNTS
        mocked_upload_file_to_s3.return_value = False
        response = main({"queryStringParameters": {'title': 'Test title'}}, {})
        self.assertIsInstance(response, dict)
        self.assertEqual(200, response['statusCode'])
        self.assertEqual(json.loads(response['body'])['message'], BODY['message'])
