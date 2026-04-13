import timeit

emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
emails = emails * 5

def loop_example(emails):
    gmails = []
    for email in emails:
        if email.endswith('gmail.com'):
            gmails.append(email)
    return gmails

def list_example(emails):
    return [email for email in emails if email.endswith('gmail.com')]

def main():
    n = 90000

    loop_time = timeit.timeit(
        stmt='loop_example(emails)',
        setup='from __main__ import loop_example, emails',
        number=n
    )

    list_time = timeit.timeit(
        stmt='list_example(emails)',
        setup='from __main__ import list_example, emails',
        number=n
    )

    if loop_time > list_time:
        print("it is better to use a list comprehension")
    else:
        print("it is better to use a loop")
    
    print(f'{loop_time} vs {list_time}')
    
if __name__ == '__main__':
    main()


