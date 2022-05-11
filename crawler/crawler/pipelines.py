# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class CrawlerPipeline:
    def process_item(self, item, spider: scrapy.Spider):
        article = ItemAdapter(item)
        article_text = article.get('text', '')
        text_length = len(article_text)
        if text_length > 0:
            item['length'] = text_length
        else:
            raise DropItem(f"No text in article {item['title']}")
