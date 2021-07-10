""" list03.py
multiprocessingを使ったマルチプロセスのサンプルコード
"""
from multiprocessing import Pool

def count_char(word):
    print("call with %s" % word)
    return len(word)

def main():
    # マルチプロセス処理
    with Pool() as p:
        print(p.map(count_char, ["大谷翔平","前健","ダルビッシュ有"]))

if __name__ == "__main__":
    main()
