""" list09.py
マンデルブロー集合をマルチプロセスで描画するスクリプト
"""
import time
import numpy as np
import matplotlib

matplotlib.use('agg')
from concurrent import futures
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize

STEP_COUNT = 100
MESH = 1000
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

def create_jpg(mandelbrot_data):
    # imshowで画像が反転するので、先にデータを反転させる
    mandelbrot_data = mandelbrot_data[::-1]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('real')
    ax.set_ylabel('imag')

    ax.imshow(
        mandelbrot_data, cmap='jet',
        norm=Normalize(vmin=0, vmax=STEP_COUNT),
        extent=[REAL_MIN, REAL_MAX, IMAG_MIN, IMAG_MAX]
    )

    plt.tight_layout()
    plt.savefig('mandelbrot.jpg')
    plt.close()

def main():
    # 開始時間の記録
    start = time.perf_counter()
    # マンデルブロ集合データの計算
    mandelbrot_data = create_mandelbrot_data()
    create_jpg(mandelbrot_data)
    # 終了時間の記録と出力
    end = time.perf_counter()
    print('elapsed time: {:.8} sec'.format(end - start))

if __name__ == "__main__":
    main()
