# 函数 -> 装饰器

# 在 Python 中，函数是一等公民，
# 函数也是对象。可以把函数当作参数，传入另一个函数中
def get_message(message):
    print('Got a message: {}'.format(message))

def root_call(func, message):
    print(func(message))

root_call(get_message, 'hi anzi')


# 装饰器的简单例子：
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print('wrapper of decorator')
        func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(message):
    print(message)

greet('hi anzi')

# 类装饰器