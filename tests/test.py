from bp import Handle
import numpy as np
import time

handle = Handle(cores=5, verbose=2)

def compute_bound_function_bp(array):
    sum_value = 0.0
    for times in handle.monitor(range(10000)):
        for i in range(len(array)):
            sum_value += array[i]

def compute_bound_function_normal(array):
    sum_value = 0.0
    start = time.time()
    for times in range(10000):
        percent = int((times + 1) / 10000 * 100)
        elapsed = time.time() - start
        if percent != 0 and percent % 2 == 0:
            print(percent, 'Estimated completion in', int((100 - percent) * elapsed / percent), end='\r')
        for i in range(len(array)):
            sum_value += array[i]
    end = time.time()
    print('Normal Elapsed Time:', (end - start))

if __name__ == '__main__':
    array = np.arange(0, 300000)

    handle.launch(compute_bound_function_bp, array)

    compute_bound_function_normal(array)
