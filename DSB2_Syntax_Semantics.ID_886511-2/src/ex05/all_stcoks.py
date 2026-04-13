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
    words = get_string()
    for word in words:
        if (company_check(word)):
            continue
        if (ticker_check(word)):
            continue
        print(word, "is an unknown company or an unknown ticker symbol")

def get_string():
    output = []
    for item in sys.argv[1:]:
        item = item.replace(',', '')
        if item != '': output.append(item)
    return output

def company_check(company):
    company = company.lower().capitalize()
    if company in COMPANIES:
        ticker = COMPANIES[company]
        price = STOCKS[ticker]
        print(company, "stock price is", price)
        return True
    else:
        return False

def ticker_check(ticker):
    ticker = ticker.upper()
    if ticker in STOCKS:
        company = find_keys_by_value(ticker)
        print(ticker, "is ticker symbol for", company[0])
        return True
    else:
        return False

def find_keys_by_value(target):
    return [key for key, value in COMPANIES.items() if value == target]

if __name__ == '__main__':
    main()