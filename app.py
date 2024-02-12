
'''
去重
统计数量
为词云准备数据
为词频准备数据
时间柱形图




'''
import subprocess
import shutil

import json
import re
import redis
import os
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

def remove_duplicates(lst):
    seen = set()
    unique_list = []
    for d in lst:
        # 将字典转换为不可变的元组，以便进行哈希比较
        dict_tuple = tuple(sorted(d.items()))
        if dict_tuple not in seen:
            seen.add(dict_tuple)
            unique_list.append(d)
    return unique_list
threadInfos = get_dict_list_from_redis('localhost', 6379, 0, '3xozcZLFDNU0gNL4', 'quotes:20240209155240')
replyInfos = get_dict_list_from_redis('localhost', 6379, 0, '3xozcZLFDNU0gNL4', 'spider2:20240209163653')
unique_thread = remove_duplicates(threadInfos)
unique_reply = remove_duplicates(replyInfos)

print("帖子数{},去重后{}".format(len(threadInfos), len(unique_thread)))
print("评论数{},去重后{}".format(len(replyInfos), len(unique_reply)))



out_dirs = ['data/uid','data/postdate','data/wordcloudpics',"data/analysis"]
#清理文件夹
for directory_path in out_dirs:
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.mkdir(directory_path)


# 评论写入文本
uids=[]

for threadItem in unique_reply:
    uid = threadItem['author_id']
    text = threadItem['text']
    with open(f'data/uid/{uid}.txt', 'a') as f:
            f.write(str(text))
            f.write('\n')
    with open(f'data/uid/0.txt', 'a') as f:
            f.write(str(text))
            f.write('\n')
    if uid not in uids:
        uids.append(uid)
print("用户数{}".format(len(uids)))


countInfo = "帖子数{},评论数{},用户数{}".format(len(unique_thread), len(unique_reply),len(uids))
with open(f'data/count.txt', 'w') as f:
    f.write(countInfo)


subprocess.run(["python", "./wordcloud_display_mask.py"])
subprocess.run(["python", "./words_frequency_analysis.py"])

# 计算每个人评论时间的发布
hour_count = {key: 0 for key in range(24)}
hour_count_uid = {}
import datetime
for threadItem in unique_reply:
    date_string = threadItem['post_date']
    hour = int(date_string.split()[1].split(":")[0])  # 提取日期字符串中的小时数字
    if hour in hour_count:
        hour_count[hour] += 1
    #是否存在uid
    author_id = threadItem['author_id']
    if author_id in hour_count_uid:
        hour_count_uid[author_id][hour] += 1
    else:
        hour_count_uid[author_id] = {key: 0 for key in range(24)}
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
def hour_img(dataDict,uid):
    # 指定中文字体文件的路径
    font_path = 'STHeiti Light.ttc'
    # 创建自定义字体对象
    custom_font = FontProperties(fname=font_path)
    # 提取键和值
    categories = list(dataDict.keys())
    values = list(dataDict.values())

    # 创建柱形图
    plt.bar(categories, values)

    # 添加标题和标签
    plt.title("nga用户{}评论时间分布".format(uid),fontproperties=custom_font)
    plt.xlabel('时间',fontproperties=custom_font)
    plt.ylabel('评论数',fontproperties=custom_font)
    plt.xticks(range(len(categories)), categories)
    # 保存为图片
    plt.savefig('data/postdate/{}.png'.format(uid))
    plt.cla()
hour_img(hour_count,0)
for key in hour_count_uid:
    hour_img(hour_count_uid[key],key)






