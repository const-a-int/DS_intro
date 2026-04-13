import sys

def get_mail():
    if len(sys.argv) != 2:
        return
    mail = sys.argv[1]
    return mail

def letter_sender(mail):
    INPUT = 'employees.tsv'
    with open(INPUT, 'r', encoding='utf-8') as file:
        for line in file:
            separated_line = line.strip().split('\t')
            if mail == separated_line[2]:
                print(f"Dear, {separated_line[0]}, welcome to our team! We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires.")
    return

if __name__ == "__main__":
    mail = get_mail()
    letter_sender(mail)