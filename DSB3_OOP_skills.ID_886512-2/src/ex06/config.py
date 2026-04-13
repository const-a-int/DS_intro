NUM_STEPS = 3 
REPORT_FILENAME = "report.txt"

TELEGRAM_BOT_TOKEN = '8325873509:AAHaxQDUPeu6fjwLM3EVVB9-H5Be53nLsAQ'
TELEGRAM_CHAT_ID = '768862170'
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

LOG_FILE = 'analytics.log'
LOG_FORMAT = '%(asctime)s %(message)s'

REPORT_TEMPLATE = """
We conducted {observations} observations by tossing a coin: {tail_count} were tails and {head_count} were heads.
The probabilities are {tail_percentage:.2f}% and {head_percentage:.2f}% respectively.
Our forecast is that the next three observations will be: {prediction}.
"""