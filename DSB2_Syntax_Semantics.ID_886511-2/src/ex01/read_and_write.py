def read_and_write():
    INPUT = 'ds.csv'
    lines = []
    with open(INPUT, 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.replace(",", "\t"))
    with open('ds.tsv', 'w', encoding='utf-8') as file:
        file.writelines(lines)

if __name__ == '__main__':
    read_and_write()