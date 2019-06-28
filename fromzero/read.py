import threading
import time


class SubThread(threading.Thread):
    def run(self) -> None:
        for i in range(3):
            time.sleep(1)
            msg = "子线程{}执行，i={}".format(self.name, str(i))
            print(msg)


if __name__ == '__main__':
    thread_a = SubThread()
    thread_b = SubThread()
    thread_a.start()
    thread_b.start()
    thread_a.join()
    thread_b.join()
