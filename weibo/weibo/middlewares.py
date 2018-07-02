# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# -*- coding: utf-8 -*-
import random
import scrapy
from scrapy import log
import time
from .cookie import cookies


# logger = logging.getLogger()

class ProxyMiddleWare(object):
    """
     z作用：代理Ip中间件
    """

    def process_request(self, request, spider):
        '''对request对象加上proxy'''
        proxy = self.get_random_proxy()
        print("this is request ip:" + proxy)
        request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):
        '''
        对返回的response处理
        '''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            proxy = self.get_random_proxy()
            print("this is response ip:" + proxy)
            # 对当前reque加上代理
            request.meta['proxy'] = proxy
            return request
        return response

    def get_random_proxy(self):
        '''
        随机从文件中读取proxy
        '''
        while 1:
            with open(r'/home/lhy/Desktop/scrapy/weibo/weibo/proxies.txt', 'r') as f:
                proxies = f.readlines()
            if proxies:
                break
            else:
                time.sleep(1)
        proxy = random.choice(proxies).strip()
        return proxy



class CookiesMiddleware(object):
    """ 换Cookie """

    def process_request(self, request, spider):
        #cookie = random.choice(cookies)
        if cookies != None:
            cookie =random.choice(cookies)
        else:
            print("cookie池没有cookie")