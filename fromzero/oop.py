# *_*coding: UTF-8 *_*

import time
import prettytable

# 初始化余额
balance = 1000
# 初始化交易日志
account_log = []


class Bank:
    def __init__(self) -> None:
        global balance
        self.balance = balance
        self.account_log = account_log

    def deposit(self):
        """存款"""
        amount = float(input("请输入存款金额："))
        self.balance += amount
        self.write_log("转入", amount)
        print("已转入", amount)

    def withdrawl(self):
        """"取款"""
        amount = float(input("请输入取款金额："))
        # 判断余额
        if amount > self.balance:
            print("余额不足")
        else:
            self.balance -= amount
            self.write_log("消费", amount)
            print("消费", amount)

    def print_log(self):
        """打印交易日志"""
        table = prettytable.PrettyTable()
        # 表头
        table.field_names = ["交易日期", "摘要", "金额", "币种", "余额"]
        for info in self.account_log:
            # 判断转入还是消费，为金额前添加"+"或"-"
            if info[1] == "转入":
                amount = "+{}".format(info[2])
            else:
                amount = "-{}".format(info[2])
            table.add_row([info[0], info[1], amount, "￥", info[3]])
        print(table)

    def write_log(self, handle, amount):
        """'写入日志"""
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        data = [create_time, handle, amount, self.balance]
        self.account_log.append(data)


def show_menu():
    """"显示菜单"""
    meun = "菜单 0: 退出 1：存款 2：取款 3：打印交易详情"
    print(meun)


if __name__ == '__main__':
    show_menu()
    num = float(input("请根据菜单输入操作编号："))
    bank = Bank()
    while num != 0:
        if num == 1:
            bank.deposit()
        elif num == 2:
            bank.withdrawl()
        elif num == 3:
            bank.print_log()
        else:
            print("输入有误")
        num = float(input("请根据菜单输入操作编号："))
    print("您已退出系统")
