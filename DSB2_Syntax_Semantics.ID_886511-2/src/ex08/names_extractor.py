import sys

def open_file():
    INPUT = 'mails.txt'
    OUTPUT = 'employees.tsv'
    with open(OUTPUT, 'w', encoding='utf-8') as file:
        file.write("Name\tSurname\tE-Mail\n")
        with open(INPUT, 'r', encoding='utf-8') as file_in:
            for mail in file_in:
                name = mail.split(sep='.', maxsplit=1)
                surname = name[1].split(sep='@', maxsplit=1)
                line = f"{name[0].capitalize()}\t{surname[0].capitalize()}\t{mail}"
                file.writelines(line)
    return

if __name__ == '__main__':
    open_file()