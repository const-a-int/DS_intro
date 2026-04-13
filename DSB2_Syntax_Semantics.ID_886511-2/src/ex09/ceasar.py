import sys

def check_str(text):
    try:
        text.encode('ascii')
    except UnicodeEncodeError:
        return False
    return True

def ceasar(string, shift, mode):
    output_str = ""
    for c in string:
        if ((ord(c) > 96 and ord(c) < 123) or (ord(c) > 64  and ord(c) < 91)):
            base = 97 if ord(c) > 96 else 65
            c = (ord(c) - base + mode*shift) % 26 + base
            output_str+=chr(c)
        else: output_str+=c
    return output_str

def main():
    if len(sys.argv) != 4:
        raise Exception("Invalid number of arguments")
    if sys.argv[1] == 'decode': mode = -1 
    elif sys.argv[1] == 'encode': mode = 1 

    string = sys.argv[2]
    if not check_str(string):
        raise Exception("The script does not support your language yet.")
    
    try:
        shift = int(sys.argv[3])
    except ValueError:
        raise Exception("Shift must be an integer")

    print(ceasar(string, shift, mode))


if __name__ == "__main__":
    main()