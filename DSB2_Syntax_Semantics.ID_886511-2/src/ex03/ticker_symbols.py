import sys

COMPANIES = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Netflix': 'NFLX',
    'Tesla': 'TSLA',
    'Nokia': 'NOK'
}

STOCKS = {
    'AAPL': 287.73,
    'MSFT': 173.79,
    'NFLX': 416.90,
    'TSLA': 724.88,
    'NOK': 3.37
}

def main():
    if len(sys.argv) != 2:
        return
    ticker = sys.argv[1].upper()
    if ticker in STOCKS:
        company = find_keys_by_value(ticker)
        price = STOCKS[ticker]
        print(company[0], price)
    else:
        print("Unknown ticker")

def find_keys_by_value(target):
    return [key for key, value in COMPANIES.items() if value == target]

if __name__ == '__main__':
    main()