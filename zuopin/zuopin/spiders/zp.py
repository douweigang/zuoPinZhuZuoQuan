# -*- coding: utf-8 -*-
import pymongo
import scrapy
import requests
from wit.util import get_md5

from zuopin.items import ZuopinItem


class ZpSpider(scrapy.Spider):
    name = 'zp'
    # allowed_domains = ['zuopin']
    start_urls = ['http://203.207.196.210:8080/user/allWorkinfo.do?pageNumber=1&pageSize=20&sortColumns=']

    def __init__(self):
        super().__init__()
        self.client = pymongo.MongoClient()
        self.db = self.client["zhuzuoquan"]["zuopin"]

    def start_requests(self):
        for i in range(int(8798373 // 20)):
            yield scrapy.Request(
                url='http://203.207.196.210:8080/user/allWorkinfo.do?pageNumber={}&pageSize=20&sortColumns='.format(
                    i + 1))

    def parse(self, response):
        li_list = response.xpath('//*[@id="all_link"]/ul/li')
        for li in li_list:
            url = li.xpath('./a/@href').extract_first()
            if url:
                url = response.urljoin(url)
                is_exist = self.db.find_one({"uuid":get_md5(url)})
                if not is_exist:
                    yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        infos = response.xpath('//*[@id="text_real"]/table')
        """相关公司	company
       登记号	registration_number
       作品名称	work_name
       作者	name
       作品类别	type
       著作权人	copyright_owner
       创作完成时间	create_at
       首次发表时间	publish_at
       登记日期	register
       是个人还是公司（0个人 1公司）	private  （整形）
       发布日期	release_date"""
        item = ZuopinItem()
        item["work_name"] = infos.xpath('./tr[1]/td[2]/text()').extract_first()
        item["name"] = infos.xpath('./tr[6]/td[2]/text()').extract_first()
        item["registration_number"] = infos.xpath('./tr[8]/td[2]/text()').extract_first()
        item["type"] = infos.xpath('./tr[3]/td[2]/text()').extract_first()
        item["copyright_owner"] = infos.xpath('./tr[3]/td[4]/text()').extract_first()
        item["create_at"] = infos.xpath('./tr[7]/td[2]/text()').extract_first()
        item["publish_at"] = infos.xpath('./tr[7]/td[4]/text()').extract_first()
        item["register"] = infos.xpath('./tr[8]/td[4]/text()').extract_first()
        item["private"] = 1 if len(item["copyright_owner"]) > 5 else 0
        item["release_date"] = infos.xpath('./tr[9]/td[2]/text()').extract_first()
        item["uuid"] = get_md5(response.url)
        yield item


if __name__ == '__main__':
    from scrapy import Selector
    import re

    # url = "http://203.207.196.210:8080/user/allWorkinfo.do?pageNumber=439918&pageSize=20&sortColumns="
    url = "http://203.207.196.210:8080/registerinfo/worksDetail.do?id=6297020"
    resp = requests.get(url)
    # print(resp.content.decode())
    # response = re.sub(r"<!--.*?-->","" ,resp.content.decode())
    # resp = Selector(text=response).xpath('//*[@id="content_small"]/table/tr/td/div/div[2]/a[12]/img/@src').extract_first()
    # if resp:
    #     print(resp)
    # else:
    #     print("no 下一頁")

    infos = Selector(text=resp.content.decode()).xpath('//*[@id="text_real"]/table')
    # for li in li_list:
    #     url = li.xpath('./a/@href').extract_first()
    #     print(url)
    item = {}
    item["work_name"] = infos.xpath('./tr[2]/td[2]/text()').extract_first()
    item["name"] = infos.xpath('./tr[6]/td[2]/text()').extract_first()
    item["registration_number"] = infos.xpath('./tr[8]/td[2]/text()').extract_first()
    item["type"] = infos.xpath('./tr[3]/td[2]/text()').extract_first()
    item["copyright_owner"] = infos.xpath('./tr[3]/td[4]/text()').extract_first()
    item["create_at"] = infos.xpath('./tr[7]/td[2]/text()').extract_first()
    item["publish_at"] = infos.xpath('./tr[7]/td[4]/text()').extract_first()
    item["register"] = infos.xpath('./tr[8]/td[4]/text()').extract_first()
    item["private"] = 1 if len(item["copyright_owner"]) > 5 else 0
    item["release_date"] = infos.xpath('./tr[9]/td[2]/text()').extract_first()
    print(item)