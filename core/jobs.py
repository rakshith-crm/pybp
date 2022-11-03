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
    table_rows = 2 * rows + 2
    estimate_completion_time_rows = 2
    total_rows = 0
    if verbose == 1:
        total_rows = estimate_completion_time_rows
    if verbose == 2:
        total_rows = table_rows + estimate_completion_time_rows

    while True:
        if verbose >= 2:
            tabular_display(monitors, columns)
            print()
        if verbose >= 1:
            elapsed = time.time() - timer
            print('Estimated Completion in', expected_completion_time(monitors, elapsed=elapsed))
        print("\033[F" * (total_rows))
        if sum(monitors) == completed:
            break
        time.sleep(refresh)
    print('\n' * (total_rows - 1), end='')
