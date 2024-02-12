import jieba
import wordcloud
from matplotlib.pyplot import imread
import os

def get_files_info(directory):
    files_info = []
    for filename in os.listdir(directory):
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

for file_info in files_info:
    print(f"File: {file_info['filename']}, Size: {file_info['size']} bytes")

    if file_info['size'] < 100:
        continue
    
    uid = file_info['filename'].replace(".txt", "")
    mask = imread("China.jpg")
    f = open(f"./data/uid/{uid}.txt", "r", encoding="utf-8")
    # 忽略掉不符合的词
    excludes = {"div", "h5", "class", "h4", "h3",
                "h2", "h1", "conlun2_box_text", "p", "id", "span"}
    t = f.read()
    f.close()
    ls = jieba.lcut(t)  # 使用精确分词模式进行分词
    txt = " ".join(ls)  # 利用空格连接精确分词后的词语

    # 设置字体,否则汉字会变为全是方框框，显示不出来
    font = 'STHeiti Light.ttc'

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
    w.generate(txt)

    
    # 生成图片写入文件夹内
    w.to_file(f"{final_directory}/{uid}-词云.png")
