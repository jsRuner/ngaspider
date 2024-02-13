
## 使用教程
- 需要准备cookie
  需要配置cookie。需要安装redis ，修改redis配置。一共2个爬虫，第二个爬虫需要第一个爬虫的帖子列表的key值。分析脚本需要2个key 。分别是2个爬虫的结果key
  如果爬虫设备,需要修改setting.py中 DOWNLOAD_DELAY

  爬虫可以多次执行,直到没有失败的url为止。没有失败的url的标识是redis中不存在quotes:urls 和 spider2:urls

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

# 部署
```
conda info --envs
/Users/ft521/anaconda3/envs/ngaspider
/Users/ft521/anaconda3/envs/ngaspider/lib/python3.10/site-packages/scrapyd/default_scrapyd.conf

~/.scrapyd.conf

 cp /Users/ft521/anaconda3/envs/ngaspider/lib/python3.10/site-packages/scrapyd/default_scrapyd.conf ~/.scrapyd.conf

 修改配置，增加账号和密码

 cd tutorial                                            scrapyd-deploy -p tutorial                                 git:main*

Packing version 1707725550
Deploying to project "tutorial" in http://127.0.0.1:6800/addversion.json
Server response (200):
{"node_name": "ft521deMacBook-Pro.local", "status": "ok", "project": "tutorial", "version": "1707725550", "spiders": 2}

curl -u admin:123456 http://127.0.0.1:6800/schedule.json -d project=tutorial -d spider=quotes
```
打包发布文件
scrapyd-deploy --build-egg tutorial.egg

可视化
scrapydweb

不推荐docker-compose部署。理论上应该是先启动多个scrapyd 再启动scrapydweb 
compose部署带来ip访问的问题。需要增加代理来访问。

docker run 参考
https://github.com/libaibuaidufu/scrapyd_web_log









