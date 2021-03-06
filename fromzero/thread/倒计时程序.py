# *_* coding:UTF-8 *_*

import datetime

now = datetime.datetime.today()

print("Today：", now)
count_down = datetime.datetime.strptime("2021-1-1", "%Y-%m-%d")
detla = count_down - now
print(str(detla.days))
