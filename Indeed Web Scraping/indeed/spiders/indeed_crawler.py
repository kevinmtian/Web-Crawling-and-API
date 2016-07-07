# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from indeed.text_cleaner import *
from indeed.items import IndeedItem

class IndeedCrawlerSpider(CrawlSpider):
    name = 'indeed_crawler'
    allowed_domains = ['indeed.com']

    start_urls = ['http://indeed.com/jobs?q=data+scientist&sort=date']

    rules = (
        Rule(LinkExtractor(allow='&start='), callback='parse_item', follow=True),
    )



    def parse_item(self, response):
        questions = Selector(response).xpath('//div[@class="row  result"]')
        for question in questions:
            item = IndeedItem()
            item['title'] = question.xpath(
                'a/@title').extract()[0]
            item['url'] = 'http://indeed.com' + question.xpath(
                'a/@href').extract()[0]
            item['company'] = " ".join(question.xpath(
                'div[@class="sjcl"]/span[@class="company"]/text()').extract()[0].split())
            if not item['company']:
                item['company'] = " ".join(question.xpath(
                    'div[@class="sjcl"]/span[@class="company"]/a/text()').extract()[0].split())
            item['words'] = text_cleaner(item['url'])
            item['city'] = question.xpath(
                'div[@class="sjcl"]/span[@class="location"]/text()').extract()[0]
            item['city'], item['state'] = state_extract(item['city'], )
            yield item

        questions = Selector(response).xpath('//div[@class="  row  result"]')
        for question in questions:
            item = IndeedItem()
            item['title'] = question.xpath(
                'h2/a/@title').extract()[0]
            item['url'] = 'http://indeed.com' + question.xpath(
                'h2/a/@href').extract()[0]
            item['company'] = " ".join(question.xpath(
                'span[@class="company"]/span/text()').extract()[0].split())
            if not item['company']:
                item['company'] = " ".join(question.xpath(
                    'span[@class="company"]/span/a/text()').extract()[0].split())
            item['words'] = text_cleaner(item['url'])
            item['city'] = question.xpath(
                'span[@itemprop="jobLocation"]/span/span/text()').extract()[0]
            item['city'], item['state'] = state_extract(item['city'], )
            yield item

        questions = Selector(response).xpath('//div[@class="row sjlast result"]')
        for question in questions:
            item = IndeedItem()
            item['title'] = question.xpath(
                'a/@title').extract()[0]
            item['url'] = 'http://indeed.com' + question.xpath(
                'a/@href').extract()[0]
            item['company'] = " ".join(question.xpath(
                'div[@class="sjcl"]/span/text()').extract()[0].split())
            if not item['company']:
                item['company'] = " ".join(question.xpath(
                    'div[@class="sjcl"]/span/a/text()').extract()[0].split())
            item['words'] = text_cleaner(item['url'])
            item['city'] = question.xpath(
                'div[@class="sjcl"]/span[@class="location"]/text()').extract()[0]
            item['city'], item['state'] = state_extract(item['city'], )
            yield item

        questions = Selector(response).xpath('//div[@class="lastRow  row  result"]')
        for question in questions:
            item = IndeedItem()
            item['title'] = question.xpath(
                'h2/a/@title').extract()[0]
            item['url'] = 'http://indeed.com' + question.xpath(
                'h2/a/@href').extract()[0]
            item['company'] = " ".join(question.xpath(
                'span[@class="company"]/span/text()').extract()[0].split())
            if not item['company']:
                item['company'] = " ".join(question.xpath(
                    'span[@class="company"]/span/a/text()').extract()[0].split())
            item['words'] = text_cleaner(item['url'])
            item['city'] = question.xpath(
                'span[@itemprop="jobLocation"]/span/span/text()').extract()[0]
            item['city'], item['state'] = state_extract(item['city'], )
            yield item






