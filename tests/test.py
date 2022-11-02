import multiprocessing
import os

from core import Handle
import numpy as np

batcher = Handle(cores=5, verbose=1)


def sum_of_array(array):
    sum_value = 0.0
    for times in batcher.monitor(range(100000)):
        sum_value = 0.0
        for value in array:
            sum_value += value
    print(sum_value, os.getpid())



if __name__ == '__main__':
    array1 = np.arange(0, 30)

    batcher.launch(sum_of_array, array1)
