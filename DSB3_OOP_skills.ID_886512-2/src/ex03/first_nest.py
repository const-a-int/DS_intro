import sys
import os 

class Reasearch:
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
                        if not values[0] or not values[1]:
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
        def counts(data):
            head = 0
            tail = 0
            for value in data:
                if value[0] == "1": tail+=1
                if value[1] == "1": head+=1
            return tail, head
        def fractions(head, tail):
            total = head + tail
            h_per = (head / total) * 100
            t_per = (tail / total) * 100
            return h_per, t_per

if __name__ == "__main__":
    if len(sys.argv) != 2: 
        print("Wrong argument") 
        sys.exit(1)
    filename = sys.argv[1]
    r = Reasearch(filename)
    try:
        data = r.file_reader()
    except Exception as e:
        print(e)
        sys.exit(1)
    c = r.Calculations
    head, tail = c.counts(data)
    h_per, t_per = c.fractions(head, tail)
    print(data)
    print(head, tail)
    print(h_per, t_per)