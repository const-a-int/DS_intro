import timeit
import random
from collections import Counter

def my_function(list_numbers):
    res_dict = {}
    for n in list_numbers:
        res_dict[n] = res_dict.get(n, 0) + 1
    return res_dict

def my_top(list_numbers):
    temp_dict = my_function(list_numbers)
    sorted_items = sorted(temp_dict.items(), 
                             key=lambda kv: (-kv[1]))
    return dict(sorted_items[0:10])

def counter_function(list_numbers):
    return Counter(list_numbers)

def counter_top(list_numbers):
    counter = Counter(list_numbers)
    return counter.most_common(10)

def main():
    list_numbers = [random.randint(1, 100) for _ in range(100)]

    my_function_time = timeit.timeit(
        stmt=f'my_function({list_numbers})',
        setup='from __main__ import my_function',
    )

    my_top_time = timeit.timeit(
        stmt=f'my_top({list_numbers})',
        setup='from __main__ import my_top',
    )

    counter_function_time = timeit.timeit(
        stmt=f'counter_function({list_numbers})',
        setup='from __main__ import counter_function',
    )

    counter_top_time = timeit.timeit(
        stmt=f'counter_top({list_numbers})',
        setup='from __main__ import counter_top',
    )

    print(f'my function: {my_function_time}\n'
          f'Counter: {counter_function_time}\n'
          f'my top: {my_top_time}\n'
          f"Counter's top: {counter_top_time}")

if __name__ == '__main__':
    main()