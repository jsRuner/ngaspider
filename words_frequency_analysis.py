import os
import jieba
import jieba.analyse
import codecs
import re
from collections import Counter


class WordCounter(object):

    def count_from_file(self, file, top_limit=0):
        with codecs.open(file, 'r', 'utf-8') as f:
            content = f.read()
            content = re.sub(r'\s+', r' ', content)
            content = re.sub(r'\.+', r' ', content)
            return self.count_from_str(content, top_limit=top_limit)

    def count_from_str(self, content, top_limit=0):
        if top_limit <= 0:
            top_limit = 100
        tags = jieba.analyse.extract_tags(content, topK=100)

        words = jieba.cut(content)
        counter = Counter()
        for word in words:
            if word in tags:
                counter[word] += 1

        return counter.most_common(top_limit)


def split_list(lst, size):
    """将列表拆分成多个大小为size的子列表"""
    result = []
    for i in range(0, len(lst), size):
        result.append(lst[i:i+size])
    return result


def get_files_info(directory):
    files_info = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            files_info.append({'filename': filename, 'size': file_size})
    return files_info

def gen_analysis_report(counter, files):
    for file_info in files:
        print(f"File: {file_info['filename']}, Size: {file_info['size']} bytes")
        if file_info['size'] < 100:
            continue
        uid = file_info['filename'].replace(".txt", "")
        full_path = f"./data/uid/{uid}.txt"
        file_size = os.path.getsize(full_path)
        if file_size < 100:
            continue
        result = counter.count_from_file(full_path, top_limit=10)
        # 将分析报告写入 .txt 文件中
        output_file = f'data/analysis/{uid}.txt'
        for i, j in result:
            with open(output_file, "a") as f:
                f.write(str(i)+'\t'+str(j)+'\n')
counter = WordCounter()
directory = 'data/uid'
files_info = get_files_info(directory)

n = 200  # 线程数
datas = split_list(files_info, n)
import threading
# 创建并启动线程
threads = []
for item in datas:
    thread = threading.Thread(target=gen_analysis_report, args=(counter,item,))
    thread.start()
    threads.append(thread)

# 等待所有线程结束
for thread in threads:
    thread.join()

print("All threads have finished execution.")
        
