import os
import io
import zipfile
import boto3
import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime

S3_BUCKET = os.environ.get('S3_BUCKET', 'your-s3-bucket-name')
S3_KEY_PREFIX = os.environ.get('S3_KEY_PREFIX', 'ecb-exchange-rates/')

def get_csv_zip_url():
    # ECB reference rates page
    url = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html'
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Find the CSV zip link (look for href ending with .zip and containing 'csv')
    href = None
    links = soup.find_all('a', href=True)
    for a in links:
        if 'eurofxref.zip' in a['href']:
            href = a['href']
            print(f'INFO: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Found CSV zip link: {href}')
            # ECB links are often relative
            if href.startswith('http'):
                href = href
            else:
                href = 'https://www.ecb.europa.eu' + href
            # take the first link that meets criteria
            break
    if href is None:
        raise Exception('CSV zip link not found on ECB page.')
    else:
        return href

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    # Step 1: Find and download the zip file
    try:
        zip_url = get_csv_zip_url()
        resp = requests.get(zip_url)
        resp.raise_for_status()
        # Step 2: Unzip the file in memory
        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            for filename in z.namelist():
                if filename.endswith('.csv'):
                    csv_bytes = z.read(filename)
                    s3_filename = f'{datetime.now().strftime("%Y-%m-%d")}_{filename}'
                    # Step 3: Upload to S3
                    s3_key = f'{S3_KEY_PREFIX}{s3_filename}'
                    s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=csv_bytes)
                    log_message = f'Uploaded {filename} to s3://{S3_BUCKET}/{s3_key}'
                    # add timestamp to the printed message
                    print(f'INFO: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {log_message}')
        return {'status': 'success'}
    except Exception as e:
        print(f'ERROR: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {str(e)}')
        return {'status': 'error', 'message': str(e)}
