import timeit

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

    map_time = timeit.timeit(
        stmt='map_example(emails)',
        setup='from __main__ import map_example, emails',
        number=n
    )

    times = {
        'loop': loop_time,
        'list comprehension': list_time,
        'map': map_time
    }
    best = min(times, key=times.get)

    if best == 'map':
        print("it is better to use a map")
    elif best == 'list comprehension':
        print("it is better to use a list comprehension")
    else:
        print("it is better to use a loop")
    print(f'{loop_time} vs {list_time} vs {map_time}')
    
if __name__ == '__main__':
    main()


