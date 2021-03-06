import json

params = {
    'symbol': '123456',
    'type': 'limit',
    'price': 123.4,
    'amount': 23
}

if __name__ == '__main__':
    # 序列化为 string
    params_str = json.dumps(params)
    # with open('params.json', 'w') as fout:
    #     params_str = json.dump(params, fout)

    print('after json serialization')
    print('type of params_str = {}, params_str = {}'.format(type(params_str), params))

    # 反序列化为 Python 的基本数据类型
    original_params = json.loads(params_str)

    print('after json deserialization')
    print('type of original_params = {}, original_params = {}'.format(type(original_params), original_params))
