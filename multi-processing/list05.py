""" list05.py
processオブジェクトを使ったマルチプロセスのサンプルコード
"""
from multiprocessing import Process, Queue

def count_char(word, queue):
    print("call with %s" % word)
    queue.put(len(word))

def main():
    q = Queue()
    jobs = []

    # List処理をマルチプロセスで実行
    for word in ["大谷翔平","前健","ダルビッシュ有"]:
        # Process オブジェクトのインスタンス化
        p = Process(target=count_char, kwargs={'word': word, 'queue': q})
        # インスタンスの実行
        p.start()
        # 実行結果をlistに格納
        jobs.append(p)
    
    # join関数でマルチプロセスが完了したことを確認（ループで全プロセスの完了を確認）
    for proc in jobs:
        proc.join()

    # Queueインスタンスから戻り値を取得
    result = [q.get(i) for i in range(3)]
    print(result)

if __name__ == "__main__":
    main()
