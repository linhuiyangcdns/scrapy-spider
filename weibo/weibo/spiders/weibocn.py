# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request,Spider
import json
from ..items import *

class WeibocnSpider(scrapy.Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']
    start_urls = ['http://m.weibo.cn/']
    user_url = "https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}"
    follower_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}" # 博主的关注url
    weibo_url = "https://m.weibo.cn/api/container/getIndex?uid={uid}&value={uid}&containerid=107603{uid}&page={page}"
    fans_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}"
    start_users = ['359703040', '3167735565', '2282991915','1784537661']

    def start_requests(self):
        for i in self.start_users:
            yield Request(self.user_url.format(uid=i),callback= self.parse_user)

    def parse_user(self,response):
        """
        作用：解析用户信息
        :return:
        """
        self.logger.debug(response)
        result = json.loads(response.text)
        if result.get('data').get('userInfo'):
            user_info = result.get('data').get('userInfo')
            user_item = UserItem()
            # collection = 'users'
            # id = Field()
            # name = Field()
            # avatar = Field()
            # gender = Field()
            # cover = Field()
            # verified = Field()
            # description = Field()  # 简介
            # Certified = Field()  # 微博认证
            # fans_count = Field()
            # follows_count = Field()
            # weibos_count = Field()
            # fans = Field()
            # follows = Field()
            # location = Field()  # 所在地
            field_map = {
                "id": 'id','name':'screen_name','gender':'gender','description':'description',
                'fans_count': 'followers_count', 'follows_count':'follow_count', 'weibos_count':'statuses_count',
                'avatar': 'profile_image_url', 'cover':'cover_image_phone', 'verified':'verified',

            }
            for field,attr in field_map.items():
                user_item[field] = user_info.get(attr)
            yield user_item
            uid = user_info.get('id')
            yield Request(self.follower_url.format(uid=uid,page=1),callback=self.parse_follower,meta={'uid':uid,'page':1})
            yield Request(self.fans_url.format(uid=uid,page=1),callback=self.parse_fans,meta={"uid":uid,"page":1})
            yield Request(self.weibo_url.format(uid=uid,page=1),callback=self.parse_weibo,meta={'uid':uid,'page':1})


    def parse_follower(self,response):
        """
               解析博主关注
               :param response:
               :return:
               """
        result = json.loads(response.text)
        #print(result)
        # if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and result.get(
        #         'data').get('cards''card_group'):
        try:
            fans = result.get('data').get('cards')[-1].get('card_group')
            for fan in fans:
                if fan.get('user'):
                    uid = fan.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
            # 下一页关注
            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1
            yield Request(self.fans_url.format(uid=uid, page=page), callback=self.parse_follower,
                          meta={'uid': uid, 'page': page})
        except:
            print('shibai')



    def parse_fans(self,response):
        """
        解析粉丝关注
        :param response:
        :return:
        """
        result = json.loads(response.text)
        #if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and result.get('data').get('cards''card_group'):
        try:
            fans = result.get('data').get('cards')[-1].get('card_group')
            #print(fans)
            for fan in fans:
                if fan.get('user'):
                    uid = fan.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid),callback=self.parse_user)
            # 下一页关注
            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1
            yield Request(self.fans_url.format(uid=uid,page=page),callback=self.parse_fans,meta={'uid':uid,'page':page})
        except:
            print('123')


    def parse_weibo(self,response):
        result = json.loads(response.text)
        #if result.get('ok') and result.get('data').get('cards'):
        try:
            weibos = result.get('data').get('cards')
            #print(weibos)
            for weibo in weibos:
                mblog = weibo.get('mblog')
                if mblog:
                    weibo_item = WeiboItem()
                    # id = Field()
                    # created_at = Field()  # 创建时间
                    # text = Field()
                    # pictures = Field()
                    # reposts_count = Field()  # 分享
                    # comments_count = Field()
                    # attitudes_count = Field()  # 点赞
                    # user = Field()
                    field_map = {
                        'id':'id','created_at':'created_at','text':'text','pictures':'original_pic','reposts_count':'reposts_count',
                        'comments_count':'comments_count','attitudes_count':'attitudes_count',
                    }
                    for field,attr in field_map.items():
                        weibo_item[field] = weibos.get(attr)
                    weibo_item['user'] = response.meta.get('uid')
            # 下一页微博                                     
            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1
            yield Request(self.weibo_url.format(uid=uid,page=page),callback=self.parse_weibo,meta={'uid':'uid','page':page})
        except:
            print('456')

