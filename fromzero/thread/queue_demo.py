from queue import Queue
import threading
import random
import time


class Producer(threading.Thread):
    """生产者类"""
    def __init__(self, name, queue):
        threading.Thread.__init__(self, name=name)
        self.data = queue

    def run(self):
        for i in range(5):
            print("生产者将{}产品{}加入队列！".format(self.getName(), i))
            self.data.put(i)
            time.sleep(random.random())
        print("生产者{}完成".format(self.getName()))


class Consumer(threading.Thread):
    """消费者类"""
    def __init__(self, name, queue):
        threading.Thread.__init__(self, name=name)
        self.data = queue

    def run(self):
        for i in range(5):
            val = self.data.get()

            print("消费者将{}产品{}从队列取出！".format(self.getName(), val))
            time.sleep(random.random())

        print("消费者{}完成".format(self.getName()))


if __name__ == '__main__':
    print("---主线程开始---")
    queue = Queue()
    producer = Producer("Producer", queue)
    consumer = Consumer("Consumer", queue)
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()
    print("---主线程结束---")


