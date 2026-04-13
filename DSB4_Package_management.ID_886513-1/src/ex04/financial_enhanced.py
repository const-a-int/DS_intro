from bs4 import BeautifulSoup
import requests
import time
import sys
import re
import httpx

def input_data():
    ticker = sys.argv[1].replace("'", "")
    field = sys.argv[2].replace("'", "")
    return ticker, field

def send_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    }

    with httpx.Client() as client:
        answer = client.get(url, headers=headers, timeout=10.0)
    if answer.status_code != 200:
        raise Exception(f"Page not found. Status code: {answer.status_code}")

    page = BeautifulSoup(answer.text, "html.parser")

    return answer

def parsing_page(answer, field):
    soup = BeautifulSoup(answer.text, "html.parser")

    rows = soup.find_all('div', {'class': re.compile('row lv-0')})
    if not rows:
        raise Exception('Unable to find a table for a ticker')

    for row in rows:
        label = row.find('div', {'class': re.compile('rowTitle')})
        if label and label.text.strip().lower() == field.lower():
                values = row.find_all('div', {'class': re.compile('column yf-')})
                values_list = [value.text.strip() for value in values]
                return (values_list)

if __name__ == '__main__':
    ticker, field = input_data()
    url = f'https://finance.yahoo.com/quote/{ticker.upper()}/financials/'
    try:
        page = send_request(url)
        print(parsing_page(page, field))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
