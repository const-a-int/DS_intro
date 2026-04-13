import timeit
import sys
from functools import reduce

def loop_counter(num):
    sum_ = 0
    for i in range(1, num+1):
        sum_ = sum_ + i*i
    return sum_

def reduce_counter(num):
    return reduce(lambda sum_, i: sum_ + i*i, range(1, 1+num), 0)

def main():
    command = sys.argv[1].lower()
    n = int(sys.argv[2])
    input_num = int(sys.argv[3])

    if command == 'loop':
        result = timeit.timeit(
            stmt=f'loop_counter({input_num})',
            setup='from __main__ import loop_counter',
            number=n
        )
    elif command == 'reduce':
        result = timeit.timeit(
            stmt=f'reduce_counter({input_num})',
            setup='from __main__ import reduce_counter',
            number=n
        )
    else:
        print('Wrong command')    
        sys.exit(1)
    
    print(result)

if __name__ == '__main__':
    main()