import sys
import os 
from random import randint
import config

class Research:
    def __init__(self, filename):
        self.filename = filename

    def file_reader(self, has_header=True):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = []
                lines = file.readlines()
                header = lines[0].strip()
                if (has_header and header != "head,tail"):
                    raise ValueError("Wrong header")
                start_i = 1 if has_header else 0
                if len(lines) > 2:
                    for i in range(start_i, len(lines)):
                        values = lines[i].strip().split(',')
                        if len(values) != 2:
                            raise ValueError("Wrong structure")
                        if values[0] == values[1]:
                            raise ValueError("Wrong data")
                        data.append(values)
                    return data
                else:
                    raise ValueError("Wrong structure")
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.filename} is not found") from None
        except Exception as e:
            raise ValueError(f"Error reading file: {e}") from None

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


