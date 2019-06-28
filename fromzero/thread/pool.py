from multiprocessing import Pool, Process
import os
import time


class SubProcess(Process):
    """使用multiprocessing模块创建进程"""
    def __init__(self, interval, name=""):
        Process.__init__(self)
        self.interval = interval
        if name:
            self.name = name

    def run(self):
        print("子进程（%s）开始执行，父进程为（%s）" %(os.getpid(), os.getppid()))
        t_start = time.time()
        time.sleep(self.interval)
        print("子进程（%s）结束执行，耗时（%0.2f秒）" %(os.getpid(), time.time() - t_start))


def task(name):
    print("子进程（%s）执行task %s ..." % (os.getpid(), name))
    time.sleep(1)


if __name__ == '__main__':
    print("父进程（%s） ." % os.getpid())
    # 进程池 Pool，开始三个任务
    process = Pool(3)
    for i in range(10):
        # 使用非阻塞方式调用task，并行执行
        # apply() 阻塞，必须等待上一进程退出才能执行下一个进程
        process.apply_async(task, args=(i,))

    print("等待所有子进程结束...")
    process.close()
    process.join()
    print("所有子进程结束.")