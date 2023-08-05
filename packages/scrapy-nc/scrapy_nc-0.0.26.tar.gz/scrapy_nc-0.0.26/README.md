## scrapy_nc

### 安装

```
pip install scrapy_nc
```

### 使用

目前提供以下基础数据:

- scrapy_nc.item.BaseItem 基础 item
- scrapy_nc.pipelines.AMQPPipeline 发送队列 pipeline
- scrapy_nc.pipelines.OSSPipeline 保存 OSS pipeline
  <!-- - scrapy_nc.pipelines.RedisDuplicatesPipeline Redis 去重 Pipeline -->

### BaseItem

目前由以下三个 Field 是默认包含的

```

crawled_at = scrapy.Field()  #爬虫时间
oss_filename = scrapy.Field() # oss 路径
unique_id = scrapy.Field()   # 资源唯一id
```

示例：

```

from scrapy_nc.item import BaseItem

class XiaoyusanItem(BaseItem):
    pass
```

### OSSPipeline

OSSPipeline 会将 item 内容保存在 oss 中，如果 oss_filename 如果为空则使用默认规则 {spider_name}/{url_host}/{md5(url)}

安装 oss2

```
pip install oss2
```

settings 配置

```
ITEM_PIPELINES = {
    'scrapy_nc.pipelines.OSSPipeline': 600,
}
```

### AMQPPipeline

安装 pika

```
pip install pika
```

settings 配置

```
ITEM_PIPELINES = {
    'scrapy_nc.pipelines.AMQPPipeline': 700,
}
```

配置 items.py 添加 queue_names 函数

```

from scrapy_nc.item import BaseItem

class XiaoyusanItem(BaseItem):
    test = scrapy.Field()

    def queue_names(self):
        return ['spider.medical.ncov_community.xiaoyusan'] # 默认发送到线上和线下两个队列，'.dev'或'.prod'结尾的队列只会发送其中一个

```
