""" list08.py
マンデルブロー集合を計算するスクリプト（悲マルチプロセス）
"""
import numpy as np
import matplotlib

matplotlib.use('agg')
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize

STEP_COUNT = 100
MESH = 1000
REAL_MIN = -2
REAL_MAX = 0.5
IMAG_MIN = -1.2
IMAG_MAX = 1.2

def check_mandelbrot(c):
    z = complex(0, 0)
    n = 0
    while np.abs(z) <= 2 and n < STEP_COUNT:
        z = z ** 2 + c
        n += 1
    return n

def create_mandelbrot_data():
    real, imag = np.meshgrid(
        np.linspace(REAL_MIN, REAL_MAX, MESH),
        np.linspace(IMAG_MIN, IMAG_MAX, MESH)
    )
    length = len(real.ravel())
    mandelbrot_data = np.zeros(length)

    for i in range(length):
        c = complex(real.ravel()[i], imag.ravel()[i])
        n = check_mandelbrot(c)
        if n < STEP_COUNT:
            mandelbrot_data[i] = n
    
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
    mandelbrot_data = create_mandelbrot_data()
    create_jpg(mandelbrot_data)

if __name__ == "__main__":
    main()
