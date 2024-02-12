conda create --name ngaspider python=3.10.9
conda activate ngaspider 
conda deactivate

<!-- 找到pip配置文件。修改清华源 -->
pip config list -v  

[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple


<!-- 爬虫 -->
pip install Scrapy

<!-- 快速入手 -->
https://docs.scrapy.org/en/latest/intro/tutorial.html

scrapy startproject tutorial

<!-- 运行爬虫 -->
cd tutorial
scrapy crawl quotes

<!-- 尝试定位元素 -->
scrapy shell 'https://bbs.nga.cn/thread.php?fid=510428&order_by=postdatedesc'

<!-- 进入shell -->
scrapy shell

# 指定请求目标的 URL 链接
url='https://bbs.nga.cn/thread.php?fid=510428&order_by=postdatedesc&page=1'
url="https://bbs.nga.cn/read.php?tid=39244916&page=1"
# 自定义 Headers 请求头(一般建议在调试时使用自定义 UA，以绕过最基础的 User-Agent 检测)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
# 构造需要附带的 Cookies 字典
cookies = {"key_1": "value_1", "key_2": "value_2", "key_3": "value_3"}
# 构造 Request 请求对象
req = scrapy.Request(url, cookies=cookies, headers=headers)
# 发起 Request 请求
fetch(req)
# 在系统默认浏览器查看请求的页面（主要为了检查是否正常爬取到内页）
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
<!-- 评论者 -->
response.css(".replyer::text").getall()

<!-- 评论时间 -->
response.css(".replydate").get()
<!-- 评论数 -->
response.css(".replies::text").getall()
<!--下一页 -->
response.xpath('//a[@title="下一页"]').xpath('./@href').get()

创建新的爬虫
scrapy genspider spider2 example.com
爬虫帖子
scrapy crawl quotes 
爬虫帖子内容  
scrapy crawl spider2  

帖子内容缺少一些信息。是js渲染的应该




词频统计Ok
词云图片ok

回帖时间分析。例如集中在啥时间。
评论次数排行榜。哪个人话最多。
感情色彩分析。
统计下整体的数据集规模。


期望的是分析出xx是 刷子，水军。

# 爬取板块帖子列表   624 怀旧  510428 探索
scrapy crawl quotes -a fid=510428

# 爬取板块帖子评论
scrapy crawl spider2 -a list_redis_key=quotes:20240212095815



