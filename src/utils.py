import json
import logging
from datetime import datetime

import boto3
import requests
from bs4 import BeautifulSoup
from botocore.exceptions import ClientError

URL_PAGE_WIKI = 'https://en.wikipedia.org/w/index.php'
URL_PAGE_STATS = 'https://xtools.wmflabs.org/articleinfo/en.wikipedia.org/{}#month-counts'
BUCKET_NAME = 'getupsidewiki'

s3_client = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_latest_date_time(title):
    params = {'title': title, 'action': 'history'}
    page = get_page(URL_PAGE_WIKI, params=params)
    return parse_page(page)


def get_last_month_edit_counts(title):
    page = get_page(URL_PAGE_STATS.format(title))
    return parse_page(page)


def get_page(url, params=None):
    response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}, params=params)
    return response.text


def parse_page(page):
    soup = BeautifulSoup(page, "html.parser")
    if 'Wikipedia' in soup.title.contents[0].strip():
        return soup.find_all(class_="mw-changeslist-date")[0].contents[0]
    else:
        # 8 index geting Month counts table
        table = soup.find_all('table')[8]
        values = []
        for i in table.find_all('tr'):
            cols = i.findAll("td")
            if cols:
                values.append([ele.text.strip() for ele in cols])

        # velue for previous month
        return values[-2][1]



def upload_file_to_s3(date, month_last_updates, title):
    date = datetime.strptime(date, '%H:%M, %d %B %Y').isoformat()
    file_name = '{}.json'.format(title)
    data = {'number_updates_last_month': month_last_updates,
            'latest_update_time': date}

    try:
        s3_client.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=json.dumps(data))
    except ClientError as e:
        logging.error(e)
