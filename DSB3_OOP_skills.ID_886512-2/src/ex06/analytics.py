import sys
import os 
from random import randint
import config
import logging
import json
import requests

logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.DEBUG,
    format=config.LOG_FORMAT
)

class Research:
    def __init__(self, filename):
        self.filename = filename
        logging.debug(f'Research class initialized with filename: {filename}')

    def file_reader(self, has_header=True):
        logging.debug(f'Start file_reader method')
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = []
                lines = file.readlines()
                header = lines[0].strip()
                if (has_header and header != "head,tail"):
                    logging.error('Wrong file header')
                    raise ValueError("Wrong header")
                start_i = 1 if has_header else 0
                if len(lines) > 2:
                    for i in range(start_i, len(lines)):
                        values = lines[i].strip().split(',')
                        if len(values) != 2:
                            logging.error('Wrong structure')
                            raise ValueError("Wrong structure")
                        if values[0] == values[1]:
                            logging.error('Wrong data')
                            raise ValueError("Wrong data")
                        data.append(values)
                    return data
                    logging.debug('File read successful')
                else:
                    logging.error('Wrong structure')
                    raise ValueError("Wrong structure")
        except FileNotFoundError:
            logging.error(f"File {self.filename} is not found")
            raise FileNotFoundError(f"File {self.filename} is not found") from None
        except Exception as e:
            logging.error(f'Error reading file: {e}')
            raise ValueError(f"Error reading file: {e}") from None

    def sendMessage_TG(self, success=True):
        logging.debug('Sending TG message')
        try:
            if success:
                message = "The report has been successfully created"
            else:
                message = "The report hasn't been created due to an error"

            payload = {
                'chat_id': config.TELEGRAM_CHAT_ID,
                'text': message
            }

            response = requests.post(config.TELEGRAM_URL, data=payload)
            logging.debug(f'TG response: {response.status_code}')

            if response.status_code == 200:
                logging.info('TG message sent succsessfully')
            else:
                logging.error(f'TG message sent failed: {response.text}')
        except Exception as e:
            logging.error(f'Error sending Telegram message: {e}')

class Calculations:
    def __init__(self, data):
        self.data = data

    def counts(self):
        head = 0
        tail = 0
        for value in self.data:
            if str(value[0]) == "1": head+=1
            if str(value[1]) == "1": tail+=1
        return head, tail

    def fractions(self, head, tail):
        total = head + tail
        h_per = (head / total) * 100
        t_per = (tail / total) * 100
        return h_per, t_per

class Analytics(Calculations):
    def predict_random(self, num_predictions):
        predictions = []
        for i in range(num_predictions):
            n = randint(0, 1)
            prediction = [n, 1 - n]
            predictions.append(prediction)
        return predictions

    def predict_last(self):
        return self.data[-1]

    def save_file(self, data, filename, ext):
        full_filename = f"{filename}.{ext}"
        with open(full_filename, 'w', encoding='utf-8') as file:
            file.write(str(data))
        return full_filename


