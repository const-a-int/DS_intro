import sys
import os 
from random import randint

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
            if value[0] == "1": head+=1
            if value[1] == "1": tail+=1
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

if __name__ == "__main__":
    if len(sys.argv) != 2: 
        print("Wrong argument") 
        sys.exit(1)
    filename = sys.argv[1]
    r = Research(filename)
    try:
        data = r.file_reader()
    except Exception as e:
        print(e)
        sys.exit(1)
    c = Calculations(data)
    a = Analytics(data)
    head, tail = c.counts()
    h_per, t_per = c.fractions(head, tail)
    predictions = a.predict_random(3)
    pred_last = a.predict_last()
    print(data)
    print(head, tail)
    print(h_per, t_per)
    print(predictions)
    print(pred_last)