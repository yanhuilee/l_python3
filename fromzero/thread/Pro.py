import threading
import random
import time


gMoney = 100
gLock = threading.Lock()
g_condition = threading.Condition()


class Producer(threading.Thread):
    def run(self) -> None:
        global gMoney
        while True:
            money = random.randint(1, 50)
            g_condition.acquire()
            gMoney += money
            print("%s 生产了： %d 元，剩余：%d 元" % (threading.current_thread(), money, gMoney))

            if gMoney < 10:
                print("%s 正在生产，请等待。。。" % threading.current_thread())
                g_condition.release()
                continue

            g_condition.notify_all()
            g_condition.release()
            if gMoney > 1000:
                return

        time.sleep(1)


class Consumer(threading.Thread):
    def run(self) -> None:
        global gMoney
        while True:
            money = random.randint(10, 100)
            g_condition.acquire()
            while gMoney < money:
                print("%s 准备消费： %d 元，剩余：%d 元，余额不足！" % (threading.current_thread(), money, gMoney))
                g_condition.wait(3)

            gMoney -= money
            print("%s 消费了： %d 元，剩余：%d 元" % (threading.current_thread(), money, gMoney))
            g_condition.release()
            time.sleep(1)


def main():
    for x in range(2):
        t = Consumer(name="消费者%d" % x)
        t.start()

    producer = Producer(name="生产者0")
    producer.start()


if __name__ == '__main__':
    main()