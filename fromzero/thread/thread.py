import threading
import time


def coding():
    for x in range(3):
        print("啦啦啦", threading.current_thread())


def multi_thread():
    t1 = threading.Thread(target=coding) #传递函数而不是返回值

    t1.start()


class CodingThread(threading.Thread):
    def run(self) -> None:
        for x in range(3):
            print("I'm coding %s" % threading.current_thread())
            time.sleep(2)


gLock = threading.Lock()


if __name__ == '__main__':
    print(threading.enumerate())
    multi_thread()
    print("-" * 30)
    t = CodingThread()
    t.start()
