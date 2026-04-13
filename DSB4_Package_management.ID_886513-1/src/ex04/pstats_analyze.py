import pstats
import cProfile
import financial_enhanced
import sys

#python -m cProfile -o profile_stats.prof financial.py 'MSFT' 'Total Revenue'

def analyze():
    stats = pstats.Stats('profile_stats.prof')
    stats.sort_stats('cumulative')
    with open('pstats-cumulative.txt', 'w') as f:
        stats.stream = f
        stats.print_stats(5)

if __name__ == '__main__':
    analyze()