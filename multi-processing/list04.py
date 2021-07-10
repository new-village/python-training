""" list04.py
apply_async使ったマルチプロセスのサンプルコード
"""
from multiprocessing import Pool

def count_char(word):
    print("call with %s" % word)
    return len(word)

def main():
    # マルチプロセス処理
    with Pool() as p:
        result1 = p.apply_async(count_char, args=("大谷翔平",))
        result2 = p.apply_async(count_char, args=("前健",))
        result3 = p.apply_async(count_char, args=("ダルビッシュ有",))

        print(result1.get())
        print(result2.get())
        print(result3.get())

if __name__ == "__main__":
    main()
