""" list06.py
マルチプロセスで共有しているデータを更新するプログラム
"""
from concurrent import futures
from multiprocessing import Manager


def count_up(index, counter):
    tmp = counter.value
    # 共通変数（tmp）と並び順（index）を表示
    print("read counter %d by %d" % (tmp, index))
    # 共通変数のカウントアップ
    counter.value = tmp + 1
    # カウントアップ後の共通変数（tmp）と並び順（index）を再表示
    print("read counter %d by %d again" % (counter.value, index))
    return index


def main():
    with Manager() as manager:
        # 共有する変数'i'を作成
        counter = manager.Value('i', 0)
        with futures.ProcessPoolExecutor() as executor:
            future1 = executor.submit(count_up, 1, counter)
            future2 = executor.submit(count_up, 2, counter)
            future3 = executor.submit(count_up, 3, counter)

            future1.result()
            future2.result()
            future3.result()


if __name__ == "__main__":
    main()
