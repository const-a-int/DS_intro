import sys
import resource
import time

def read_and_write():
    filename = sys.argv[1]
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines

if __name__ == '__main__':
    start_ = time.time()

    lines = read_and_write()
    for line in lines:
        pass
    
    end_ = time.time()

    peak_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)
    print(f"Peak Memory Usage = {peak_memory:.3f} GB")
    print(f"User Mode Time + System Mode Time = {end_- start_:.2f}s")