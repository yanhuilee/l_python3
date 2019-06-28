# -*- coding: utf-8 -*-


class Fruit:
    color = ""

    def __init__(self, color="green"):
        Fruit.color = color

    def harvest(self):
        print("水果是" + Fruit.color + "的")


class Apple(Fruit):
    def __init__(self):
        print("我是苹果")
        super().__init__() #不放在第一行？


if __name__ == '__main__':
    apple = Apple()
    apple.harvest()
