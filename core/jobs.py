import sys

import numpy as np
from multiprocessing import Process


def spawn_jobs(function, job_batches):
    jobs = []
    for batch in job_batches:
        job = Process(target=function, args=tuple(batch))
        jobs.append(job)
    return jobs


def monitor_jobs(monitors, verbose):
    return
