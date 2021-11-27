""" azure-container-registry/main.py
This scipt process mandelbrot set.
"""
import logging
import os
import sys
import time
from concurrent import futures

import numpy as np

STEP_COUNT = 100
REAL_MIN = -2
REAL_MAX = 0.5
IMAG_MIN = -1.2
IMAG_MAX = 1.2
PROCESS_COUNT = 2


def check_mandelbrot(c):
    z = complex(0, 0)
    n = 0
    while np.abs(z) <= 2 and n < STEP_COUNT:
        z = z ** 2 + c
        n += 1
    return n


def calc_sub_part(real, imag, start_index, end_index):
    results = []
    for i in range(start_index, end_index):
        c = complex(real.ravel()[i], imag.ravel()[i])
        n = check_mandelbrot(c)
        if n < STEP_COUNT:
            results.append(n)
        else:
            results.append(0)
    return results


def create_mandelbrot_data():
    real, imag = np.meshgrid(
        np.linspace(REAL_MIN, REAL_MAX, MESH),
        np.linspace(IMAG_MIN, IMAG_MAX, MESH)
    )
    n_grid = len(real.ravel())
    mandelbrot_data = np.zeros(n_grid)
    n_grid_per_sub_part = int(n_grid / PROCESS_COUNT)

    with futures.ProcessPoolExecutor() as executor:
        processes = []
        for index in range(PROCESS_COUNT):
            start_index = n_grid_per_sub_part * index
            end_index = n_grid_per_sub_part * (index + 1)
            process = executor.submit(calc_sub_part, real, imag, start_index, end_index)
            processes.append(process)

        for index in range(len(processes)):
            start_index = n_grid_per_sub_part * index
            sub_part = processes[index].result()
            for i in range(len(sub_part)):
                mandelbrot_data[start_index + i] = sub_part[i]

    mandelbrot_data = np.reshape(mandelbrot_data, real.shape)
    return mandelbrot_data


if __name__ == "__main__":
    # Load logger config & Set Logger
    logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()

    # Set Parameter if define on environment variables
    try:
        MESH = int(os.getenv('MESH'))
        logger.info('Set MESH value: {0}.'.format(MESH))
    except TypeError:
        MESH = 500
        logger.warning('Invalid MESH value. Set default: {0}.'.format(MESH))

    # Set start time
    logger.info('Start mandelbrot processing.')
    start = time.perf_counter()
    # Caliculate mandelbrot set
    mandelbrot_data = create_mandelbrot_data()
    # Caliculate elapsed time
    logger.info('Finish processing. Elapsed time: {:.8} sec'.format(time.perf_counter() - start))

    # Exit
    sys.exit()
