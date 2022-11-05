import time
import sys
import os
from math import ceil

box_size = 13
box = lambda value: '| Proc-%-4s |' % (value,)
lines = lambda size: '=' * size 

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d:%02d" % (hour, minutes, seconds)

def time_this(function, *args):
    start_time = time.time()
    function(*args)
    end_time = time.time()
    return convert(end_time - start_time)

def tabular_display(values, columns):
    current_column = 0
    current_row = 1
    print(lines(min(columns, len(values)) * box_size))
    for value in values:
        sys.stdout.write(box(value=value))
        current_column += 1
        if (current_column % columns) == 0:
            current_column = 0
            print()
            print(lines(columns * box_size))
            current_row += 1
    print()
    print(lines( (len(values) % columns)  * box_size))

def expected_completion_time(monitor, elapsed):
    mean_completion_percent = sum(monitor) // len(monitor)
    if mean_completion_percent == 0:
        return convert(0)
    return convert((100 - mean_completion_percent) * elapsed / mean_completion_percent)