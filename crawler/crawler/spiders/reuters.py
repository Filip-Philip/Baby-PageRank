from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field
from scrapy.http import Response
from scrapy.selector import Selector
from w3lib.url import url_query_cleaner
import re
import os
import extruct
from crawler.items import CrawlerItem


class ArticleItem(Item):
    title = Field()
    date = Field()
    author = Field()
    tags = Field()
    category = Field()
    text = Field()
    length = Field()


def process_links(links):
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link


class BloombergCrawler(CrawlSpider):
    name = 'reuters'
    allowed_domains = ['www.reuters.com']

    start_urls = ['https://www.reuters.com/']
    rules = (
        Rule(LinkExtractor(
            deny=[
                re.escape('https://www.reuters.com/offsite'),
                re.escape('https://www.reuters.com/whitelist-offsite'),
            ],
        ),
            process_links=process_links,
            callback='parse',
            follow=True
        ),
    )

    def parse(self, response: Response, **kwargs):
        article = CrawlerItem()
        response = Selector(response=response)
        article['title'] = response.xpath('//title/text()').get()

        article['date'] = response.xpath('.//span[@class="posted-on"]//text()').get()
        article['author'] = response.xpath('.//a[@class="url fn n"]//text()').get()
        article['tags'] = response.xpath(
            './/meta[@property="article:tag"]//@content').getall()
        article_text = response.xpath('.//p//text()').getall()
        article['text'] = ''.join(article_text)
        directory_up = os.path.dirname(__file__)
        directory_up = os.path.dirname(directory_up)
        directory_up = os.path.dirname(directory_up)
        article['title'] = article['title'][:-10] # get rid of the " | Reuters " at the end of every article title
        article_path = os.path.join(directory_up, 'articles', article['title'] + '.txt')
        with open(article_path, 'w', encoding='utf-8') as file:
            file.write("Date: %s\n" % article['date'])
            file.write("Author: %s\n" % article['author'])
            file.write("Tags: %s\n\n" % article['tags'])
            file.write("%s" % article['text'])


