import os
import numpy as np
from math import ceil
from multiprocessing import Manager, Lock

from .jobs import *
from .utility import *

class Handle:
    def __init__(self, cores, verbose, refresh=2):
        self.manager = Manager()
        self.size = None
        self.cores = cores
        self.verbose = verbose
        self.job_ids = self.manager.list()
        self.monitors = self.manager.list()
        self.main_lock = Lock()
        self.refresh = refresh
        self.timer = None

    def monitor(self, range_values):
        unique_key = self.job_ids.index(os.getpid())
        for i in range(len(range_values)):
            process_completion = (i + 1) / len(range_values) * 100
            if (process_completion % 4) == 0:
                self.monitors[unique_key] = int(process_completion)
            yield range_values[i]

    def launch(self, function, *args):
        if len(args[0]) == 0:
            print('required at least one array for batch processing')
            return

        self.size = len(args[0])
        sizes = [self.size == len(args[i]) for i in range(len(args))]

        if not all(sizes):
            print('required len(arg[i]) == len(args[j]) in args')
            return

        compute_core = ceil(self.size / self.cores)
        print(f'Using {self.cores}/{os.cpu_count()} cores, compute per core {compute_core}')
        batches = [[arg[i * compute_core: (i + 1) * compute_core] for arg in args] for i in range(0, self.cores)]
        jobs = spawn_jobs(function, batches)
        self.timer = time.time()
        duaration = time_this(self.launch_jobs, jobs)
        print('\nCompleted in', duaration)
        

    
    def launch_jobs(self, jobs):
        for i in range(len(jobs)):
            jobs[i].start()
            self.job_ids.append(jobs[i].pid)
            self.monitors.append(0)
        monitor_process = None
        if self.verbose != 0:
            monitor_process = Process(target=monitor_jobs, args=(self.monitors, self.verbose, self.refresh, self.timer))
            print('\n-----------\n| Monitor |\n-----------')
            monitor_process.start()

        for job in jobs:
            job.join()
        if self.verbose != 0:
            monitor_process.join()