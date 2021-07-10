""" list02.py
マルチプロセス用並列処理サンプルコード
"""
from concurrent import futures

def count_char(word):
    print("call with %s" % word)
    return len(word)

def main():
    # マルチプロセス処理
    with futures.ProcessPoolExecutor() as executor:
        future1 = executor.submit(count_char, "大谷翔平")
        future2 = executor.submit(count_char, "前健")
        future3 = executor.submit(count_char, "ダルビッシュ有")

        print(future1.result())
        print(future2.result())
        print(future3.result())

if __name__ == "__main__":
    main()
