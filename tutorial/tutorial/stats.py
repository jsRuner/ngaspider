from scrapy.statscollectors import StatsCollector
import pytz

class CustomStatsCollector(StatsCollector):
    def __init__(self, crawler):
        print('CustomStatsCollector initialized')
        super().__init__(crawler)
        self.timezone = pytz.timezone('Asia/Shanghai')  # 设置时区为上海

    def set_value(self, key, value, spider=None):
        # 在设置统计数据值之前，将当前时间转换为指定时区
        if key == 'timestamp':
            value = value.astimezone(self.timezone)
        super().set_value(key, value, spider)