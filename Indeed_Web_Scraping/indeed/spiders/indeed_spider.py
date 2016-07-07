from scrapy import Spider
from scrapy.selector import Selector
from indeed.items import IndeedItem

class IndeedSpider(Spider):
    name = "indeed"
    allowed_domains = ["indeed.com"]
    start_urls = [
        "http://www.indeed.com/jobs?q=data+scientist&l=San+Francisco+Bay+Area%2C+CA",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="row  result"]')
        for question in questions:
            item = IndeedItem()
            item['title'] = question.xpath(
                'a/@title').extract()[0]
            item['url'] = question.xpath(
                'a/@href').extract()[0]
            item['company'] = " ".join(question.xpath(
                'div[@class="sjcl"]/span[@class="company"]/text()').extract()[0].split())
            if not item['company']:
                item['company'] = " ".join(question.xpath(
                    'div[@class="sjcl"]/span[@class="company"]/a/text()').extract()[0].split())
            yield item

        questions = Selector(response).xpath('//div[@class="  row  result"]')
        for question in questions:
            item = IndeedItem()
            item['title'] = question.xpath(
                'h2/a/@title').extract()[0]
            item['url'] = question.xpath(
                'h2/a/@href').extract()[0]
            item['company'] = " ".join(question.xpath(
                'span[@class="company"]/span/text()').extract()[0].split())
            if not item['company']:
                item['company'] = " ".join(question.xpath(
                    'span[@class="company"]/span/a/text()').extract()[0].split())
            yield item

        questions = Selector(response).xpath('//div[@class="row sjlast result"]')
        for question in questions:
            item = IndeedItem()
            item['title'] = question.xpath(
                'a/@title').extract()[0]
            item['url'] = question.xpath(
                'a/@href').extract()[0]
            item['company'] = " ".join(question.xpath(
                'div[@class="sjcl"]/span/text()').extract()[0].split())
            if not item['company']:
                item['company'] = " ".join(question.xpath(
                    'div[@class="sjcl"]/span/a/text()').extract()[0].split())
            yield item

        questions = Selector(response).xpath('//div[@class="lastRow  row  result"]')
        for question in questions:
            item = IndeedItem()
            item['title'] = question.xpath(
                'h2/a/@title').extract()[0]
            item['url'] = question.xpath(
                'h2/a/@href').extract()[0]
            item['company'] = " ".join(question.xpath(
                'span[@class="company"]/span/text()').extract()[0].split())
            if not item['company']:
                item['company'] = " ".join(question.xpath(
                    'span[@class="company"]/span/a/text()').extract()[0].split())
            yield item


# from scrapy.selector import HtmlXPathSelector
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.spider import BaseSpider
# from scrapy.http import Request
# import time
# import sys
# from indeed.items import IndeedItem
#
#
# class IndeedSpider(CrawlSpider):
#     name = "indeed"
#     allowed_domains = ["indeed.com"]
#     start_urls = [
#         "http://www.indeed.com/jobs?q=linux&l=Chicago&sort=date?",
#     ]
#
#     rules = (
#         Rule(SgmlLinkExtractor(
#             allow=('/jobs.q=linux&l=Chicago&sort=date$', 'q=linux&l=Chicago&sort=date&start=[0-9]+$',),
#             deny=('/my/mysearches', '/preferences', '/advanced_search', '/my/myjobs')), callback='parse_item',
#              follow=True),
#
#     )
#
#     def parse_next_site(self, response):
#
#         item = response.request.meta['item']
#         item['source_url'] = response.url
#         item['source_page_body'] = response.body
#         item['crawl_timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
#
#         return item
#
#     def parse_item(self, response):
#         self.log('\n Crawling  %s\n' % response.url)
#         hxs = HtmlXPathSelector(response)
#         sites = hxs.select("//div[@class='row ' or @class='row lastRow']")
#         # sites = hxs.select("//div[@class='row ']")
#         items = []
#         for site in sites:
#             item = IndeedItem(company='none')
#
#             item['job_title'] = site.select('h2/a/@title').extract()
#             link_url = site.select('h2/a/@href').extract()
#             item['link_url'] = link_url
#             item['crawl_url'] = response.url
#             item['location'] = site.select("span[@class='location']/text()").extract()
#
#             # Not all entries have a company
#             if site.select("span[@class='company']/text()").extract() == []:
#                 item['company'] = [u'']
#             else:
#                 item['company'] = site.select("span[@class='company']/text()").extract()
#
#             item['summary'] = site.select("//table/tr/td/span[@class='summary']").extract()
#             item['source'] = site.select("table/tr/td/span[@class='source']/text()").extract()
#             item['found_date'] = site.select("table/tr/td/span[@class='date']/text()").extract()
#             # item['source_url'] = self.get_source(link_url)
#             request = Request("http://www.indeed.com" + item['link_url'][0], callback=self.parse_next_site)
#             request.meta['item'] = item
#             yield request
#
#             items.append(item)
#         return
#
#
# SPIDER = IndeedSpider()
