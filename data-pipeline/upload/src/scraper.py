import io
import os
import requests
import zipfile
from bs4 import BeautifulSoup
from datetime import datetime

# get directory of this file
DIR = os.path.dirname(os.path.abspath(__file__))
OUTFILE = 'eurofxref-hist.csv'
OUTDIR = os.path.join(DIR, 'data')

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
        if 'eurofxref-hist.zip' in a['href']:
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

def download_csv():
    # Create the output directory if it doesn't exist
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)
    # Find and download the zip file
    try:
        zip_url = get_csv_zip_url()
        resp = requests.get(zip_url)
        resp.raise_for_status()
        # Unzip the file in memory
        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            for filename in z.namelist():
                if filename.endswith('.csv'):
                    csv_bytes = z.read(filename)
                    # output the csv to a file
                    with open(os.path.join(OUTDIR, OUTFILE), 'wb') as f:
                        f.write(csv_bytes)
                    print(f'INFO: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Downloaded {filename} to {OUTDIR}')
        return {'status': 'success'}
    except Exception as e:
        print(f'ERROR: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {str(e)}')
        return {'status': 'error', 'message': str(e)}
