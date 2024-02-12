
## 使用教程

- 进入目录
  
  cd tutorial/tutorial

- 爬取板块帖子列表   624 怀旧  510428 探索

scrapy crawl quotes -a fid=510428

- 爬取板块帖子评论

scrapy crawl spider2 -a list_redis_key=quotes:20240212095815

list_redis_key是帖子列表的redis的key值

- 分析数据

    cd tutorial
    python app.py
    结果在data目录




## 环境配置
```
conda create --name ngaspider python=3.10.9
conda activate ngaspider 
pip install -r requirements.txt
```

## 其他

```
pip config list -v  
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
<!-- 爬虫 -->
pip install Scrapy

<!-- 文档 -->
https://docs.scrapy.org/en/latest/intro/tutorial.html

scrapy startproject tutorial

<!-- 运行爬虫 -->
cd tutorial
scrapy crawl quotes

# 调试

scrapy shell

url='https://bbs.nga.cn/thread.php?fid=510428&order_by=postdatedesc&page=1'
url="https://bbs.nga.cn/read.php?tid=39244916&page=1"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
cookies = {"key_1": "value_1", "key_2": "value_2", "key_3": "value_3"}
req = scrapy.Request(url, cookies=cookies, headers=headers)
fetch(req)
view(response)


response.css(".topicrow").get()
#标题
response.css("title::text").get()
#帖子标题
response.css(".topic::text").getall()


#帖子链接
response.css(".topic::attr(href)").getall()
#帖子作者
response.css(".author::text").getall()
#帖子作者id
response.css(".author::attr(title)").getall()

帖子时间
response.css("span.postdate::text").getall()
response.css(".replyer::text").getall()

response.css(".replydate").get()
response.css(".replies::text").getall()
response.xpath('//a[@title="下一页"]').xpath('./@href').get()
```
词频统计Ok
词云图片ok

回帖时间分析。例如集中在啥时间。
评论次数排行榜。哪个人话最多。
感情色彩分析。
统计下整体的数据集规模。


期望的是分析出xx是 刷子，水军。




