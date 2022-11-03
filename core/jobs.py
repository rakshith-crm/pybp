import sys
import time
import os
import numpy as np
from multiprocessing import Process

from .utility import *


def spawn_jobs(function, job_batches):
    jobs = []
    for batch in job_batches:
        job = Process(target=function, args=tuple(batch))
        jobs.append(job)
    return jobs


def monitor_jobs(monitors, verbose, refresh, timer):
    completed = 100 * len(monitors)
    columns = os.get_terminal_size().columns // box_size
    rows = ceil(len(monitors) / columns)
    while True:
        tabular_display(monitors, columns)
        print("\033[F" * (2 + 2 * rows))        
        if sum(monitors) == completed:
            break
        time.sleep(refresh)
    print('\n' * (1 + 2 * rows), end='')
