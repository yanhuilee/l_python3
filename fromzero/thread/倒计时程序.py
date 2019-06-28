# *_* coding:UTF-8 *_*

import datetime

now = datetime.datetime.today()

print("Today：", now)
count_down = datetime.datetime.strptime("2019-6-7", "%Y-%m-%d")
detla = count_down - now
print(str(detla.days))
