# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class UserItem(Item):
    collection = 'users'
    id = Field()
    name = Field()
    avatar = Field()
    gender = Field()
    cover = Field()
    verified = Field()
    description = Field()  # 简介
    #Certified = Field()  #微博认证
    fans_count = Field()
    follows_count = Field()
    weibos_count = Field()
    #fans = Field()
    #follows = Field()
    #location = Field()   # 所在地


class WeiboItem(Item):
    collection = 'weibos'
    id = Field()
    created_at = Field()  #创建时间
    text = Field()
    pictures = Field()
    reposts_count = Field()  #分享
    comments_count = Field()
    attitudes_count = Field()  # 点赞
    user = Field()