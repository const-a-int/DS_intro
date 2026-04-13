import sys
import os

class Reasearch:
    def __init__(self, filename):
        self.filename = filename

    def file_reader(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                header = lines[0].strip()
                if header != "head,tail":
                    raise ValueError("Wrong header")
                if len(lines) > 2:
                    for i in range(1, len(lines)):
                        values = lines[i].strip().split(',')
                        if len(values) != 2:
                            raise ValueError("Wrong structure")
                        if values[0] == values[1]:
                            raise ValueError("Wrong data")
                    return "".join(lines)
                else:
                     raise ValueError("Wrong structure")
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.filename} is not found") from None
        except Exception as e:
            raise ValueError(f"Error reading file: {e}") from None

if __name__ == "__main__":
    if len(sys.argv) != 2: 
        print("Wrong argument") 
        sys.exit(1)
    filename = sys.argv[1]
    r = Reasearch(filename)
    try:
        print(r.file_reader())
    except Exception as e:
        print(e)
        sys.exit(1)