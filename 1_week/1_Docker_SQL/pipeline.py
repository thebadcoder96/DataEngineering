import sys
import pandas as pd

print(f'Hello from Docker. You are using Pandas Version: {pd.__version__}')

print(sys.argv)

day = sys.argv[1]

print(f'Today is {day}')