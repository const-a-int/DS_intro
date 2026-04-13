class Must_Read:
    INPUT = 'data.csv'

    with open(INPUT, 'r', encoding='utf-8') as file:
        for line in file:
            print(line, end='')

if __name__ == "__main__":
    Must_Read()