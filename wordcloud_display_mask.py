import jieba
import wordcloud
from matplotlib.pyplot import imread
import os

def split_list(lst, size):
    """将列表拆分成多个大小为size的子列表"""
    result = []
    for i in range(0, len(lst), size):
        result.append(lst[i:i+size])
    return result

def get_files_info(directory):
    files_info = []
    for filename in os.listdir(directory):
        if  not filename.startswith('0'):
            continue
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            files_info.append({'filename': filename, 'size': file_size})
    return files_info

directory = 'data/uid'
files_info = get_files_info(directory)
# 创建文件夹存储报告
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'data/wordcloudpics')
if not os.path.exists(final_directory):
    os.makedirs(final_directory)


def generate_wordcloud(data,name):
    # 忽略掉不符合的词
    excludes = {"div", "h5", "class", "h4", "h3",
                        "h2", "h1", "conlun2_box_text", "p", "id", "span"}
    # 设置字体,否则汉字会变为全是方框框，显示不出来
    font = 'STHeiti Light.ttc'
    mask = imread("China.jpg")
    w = wordcloud.WordCloud(
        width=1000,  # 设置图片宽度
        height=700,  # 设置图片高度
        background_color="white",  # 设置图片背景颜色
        font_path=font,  # 指定字体文件的完整路径，如果不设置可能显示不了中文
        max_words=100,  # 词云中最大词数
        max_font_size=80,  # 词云中最大的字体号数
        mask=mask,  # 使用遮照
        stopwords=excludes  # 被排除的词列表
    )
    
    for file_info in data:
        print(f"theadname: {name} File: {file_info['filename']}, Size: {file_info['size']} bytes")

        if file_info['size'] < 100:
            continue
        
        uid = file_info['filename'].replace(".txt", "")
       
        f = open(f"./data/uid/{uid}.txt", "r", encoding="utf-8")
        
        t = f.read()
        f.close()
        ls = jieba.lcut(t)  # 使用精确分词模式进行分词
        txt = " ".join(ls)  # 利用空格连接精确分词后的词语
        w.generate(txt)
        # 生成图片写入文件夹内
        w.to_file(f"{final_directory}/{uid}-词云.png")

n = 300  # 线程数

datas = split_list(files_info, n)


import threading
# 创建并启动线程
threads = []
for key in range(len(datas)):
    thread = threading.Thread(target=generate_wordcloud, args=(datas[key],key))
    thread.start()
    threads.append(thread)

# 等待所有线程结束
for thread in threads:
    thread.join()

print("All threads have finished execution.")

