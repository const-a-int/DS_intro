import timeit
import sys

emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
emails = emails * 5

def find_gmail(email):
    if email.endswith('gmail.com'):
        return email

def loop_example(emails):
    gmails = []
    for email in emails:
        if find_gmail(email):
            gmails.append(email)
    return gmails

def list_example(emails):
    return [email for email in emails if find_gmail]

def map_example(emails):
    return list(map(find_gmail, emails))

def filter_example(emails):
    return list(filter(find_gmail, emails))

def main():
    n = 900000
    command = sys.argv[1].lower()
    if command == 'loop':
        result = timeit.timeit(
            stmt='loop_example(emails)',
            setup='from __main__ import loop_example, emails',
            number=n
        )

    elif command == 'list_comprehension':
        result = timeit.timeit(
            stmt='list_example(emails)',
            setup='from __main__ import list_example, emails',
            number=n
        )

    elif command == 'map':
        result = timeit.timeit(
            stmt='map_example(emails)',
            setup='from __main__ import map_example, emails',
            number=n
        )

    elif command == 'filter':
        result = timeit.timeit(
            stmt='filter_example(emails)',
            setup='from __main__ import filter_example, emails',
            number=n
        )

    else:
        print('Worng command')
        sys.exit(1)
        
    print(result)

if __name__ == '__main__':
    main()


