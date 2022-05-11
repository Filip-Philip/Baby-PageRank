# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CrawlerItem(Item):
    title = Field()
    date = Field()
    author = Field()
    tags = Field()
    category = Field()
    text = Field()
    length = Field()
