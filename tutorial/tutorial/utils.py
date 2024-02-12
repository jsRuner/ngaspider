import json
import re
import redis
def serialize_json(value):
    return json.dumps(value, ensure_ascii=False).encode('utf-8')

def get_dict_list_from_redis(redis_host, redis_port, redis_db, redis_password, list_key):
    # 连接到Redis服务器
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)

    # 从Redis中获取列表
    list_data = r.lrange(list_key, 0, -1)

    # 将列表中的字典数据转换为Python字典对象
    dict_list = []
    for item in list_data:
        dict_list.append(json.loads(item))

    return dict_list

def get_dict_set_from_redis(redis_host, redis_port, redis_db, redis_password, set_key):
    # 连接到Redis服务器
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)

    # 从Redis中获取集合
    set_data = r.smembers(set_key)

    # 将集合中的字典数据转换为Python字典对象
    dict_set = []
    for item in set_data:
        dict_set.append(json.loads(item))

    return dict_set

def filter_chinese(text):
    # 使用正则表达式匹配中文字符
    filtered_text = ""
    try:
        if text:
            chinese_characters = re.findall(r'[\u4e00-\u9fff]+', text)
            # 将匹配到的中文字符连接起来
            filtered_text = ''.join(chinese_characters)
    except Exception as e:
        print("filter_chinese text = {}".format(text))
    return filtered_text

import redis

def store_url_in_redis(redis_host, redis_port, redis_db, redis_password, set_key,url):
    # 连接到Redis服务器
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
    # 存储URL到Redis的列表中
    r.sadd(set_key, url)

def get_urls_from_redis(redis_host, redis_port, redis_db, redis_password, set_key):
    # 连接到Redis服务器
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
    # 从Redis集合中获取所有URL
    urls = r.smembers(set_key)
    # 将URL转换为字符串，并返回结果
    return [url.decode('utf-8') for url in urls]

def delete_key_from_redis(redis_host, redis_port, redis_db, redis_password,key):
    # 连接到Redis服务器
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
    # 删除给定键
    r.delete(key)
