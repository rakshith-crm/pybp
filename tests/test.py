import os
import time
from math import ceil
from tqdm import tqdm
import sys
from core import Handle
import numpy as np

handle = Handle(cores=5, verbose=1)

box_size = 13
box = lambda value: '| Proc-%-4s |' % (value,)
lines = lambda size: '-' * size 


def sum_of_array(array):
    sum_value = 0.0
    for times in handle.monitor(range(1000000)):
        sum_value = 0.0
        for value in array:
            sum_value += value



if __name__ == '__main__':
    array1 = np.arange(0, 30)
    # sum_of_array(array1)
    handle.launch(sum_of_array, array1)
    # array2 = np.arange(0, 4+1)
    # table(array2)
