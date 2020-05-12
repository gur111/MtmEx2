import hw2
import os
import sys
from io import StringIO
from termcolor import colored

if __name__ == '__main__':
    stdout_stream = StringIO()

    with open("out1.txt") as f:
        expected  = f.read()

    stdout, sys.stdout = sys.stdout, stdout_stream

    hw2.partA("test1.txt")
    sys.stdout = stdout
    stdout_stream.seek(0)
    actual = stdout_stream.read()

    print(f'Test 1: {colored("passed", "green") if actual == expected[:len(actual)] else colored("failed", "red")}')
    print('Hello world')
