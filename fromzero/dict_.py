# append()/insert()/ pop(index=-1) / remove(obj)
# 将元组转换为列表 list(seq)
# list.append(obj) / list.extend(seq) / clear()
# list.sort(cmp=None, key=None, reverse=False)
# copy()

# 日期和时间
# 文件操作

# 比起os模块的path方法，python3标准库的pathlib模块的Path处理起路径更加的容易
import os
print(os.path.dirname(__file__)) #/
print(os.getcwd()) #\

import pathlib
cwd = pathlib.Path.cwd()
# os.getcwd()
print(cwd)
# 获取上两级文件目录
print(cwd.parent.parent)

# 枚举
import enum
@enum.unique
class Sex(enum.Enum):
    man = 0
    woman = 1

for item in Sex:
    print(item.name, item.value)

# 原地交换两个数字
x, y = 10, 20
x, y = y, x

print([i for i in range(1, 10) if i % 2 != 0])