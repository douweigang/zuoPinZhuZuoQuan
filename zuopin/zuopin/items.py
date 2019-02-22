# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZuopinItem(scrapy.Item):
    # define the fields for your item here like:
    collection = "zuopin"
    work_name = scrapy.Field()
    name = scrapy.Field()
    registration_number = scrapy.Field()
    type = scrapy.Field()
    copyright_owner = scrapy.Field()
    create_at = scrapy.Field()
    publish_at = scrapy.Field()
    register = scrapy.Field()
    private = scrapy.Field()
    release_date = scrapy.Field()
    uuid = scrapy.Field()


