# coding:utf-8

import requests
import json
import time


class GZH(object):
    def __init__(self):
        self.url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5MzI5MTQ1Mg==&f=json&offset={}&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=cQfaZ0JaohZiPviQdAdcS0G70iubt9%2Bp%2FNgqT20dsaij6ckUL3GfFgd5YlGouqvn&wxtoken=&appmsg_token=963_4Hyc4ukRBuA8gDvHIeDalky8NczbDYBX7zyHaQ~~&x5=0&f=json"
        self.headers = {
            'Host':'mp.weixin.qq.com',
            'Accept-Encoding':'br, gzip, deflate',
            'Cookie':'devicetype=iOS11.2.5; lang=zh_CN; pass_ticket=cQfaZ0JaohZiPviQdAdcS0G70iubt9+p/NgqT20dsaij6ckUL3GfFgd5YlGouqvn; version=16060622; wap_sid2=CIDVhIkBElxDXzhWVVc1MTVMZTUtMVFObWZfSGxFY1V5SGdCRUEzbWpPR2RFMGhWWU1Jc2FRbG1ROEl2RW9tRWVuUUF5UVU4ZFg2alpPLTJHTmhBMGt6dUZEenZMOE1EQUFBfjDqg+3ZBTgNQJVO; wxuin=287386240; wxtokenkey=777; rewardsn=',
            'Connection':'keep-alive',
            'Accept':'*/*',
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D60 MicroMessenger/6.6.6 NetType/WIFI Language/zh_CN',
            'Referer':'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MzI5MTQ1Mg==&scene=124&devicetype=iOS11.2.5&version=16060622&lang=zh_CN&nettype=WIFI&a8scene=3&fontScale=100&pass_ticket=cQfaZ0JaohZiPviQdAdcS0G70iubt9%2Bp%2FNgqT20dsaij6ckUL3GfFgd5YlGouqvn&wx_header=1',
            'Accept-Language':'zh-cn',
            'X-Requested-With':'XMLHttpRequest',
        }
        self.offset = 11
        self.item = {
            'title': "",
            'digest':"",
            'fileid':"",
            'content_url':"",
            'cover':"",
            'author':"",
        }


    def request_data(self):
        """
        爬取url
        :return:
        """
        try:
            response = requests.get(self.url.format(self.offset),headers=self.headers)
            if response.status_code == 200:
                self.parse_data(response.text)
                print(self.url.format(self.offset))
        except Exception as e:
            print(e)


    def parse_data(self,jsonText):
        """
        解析数据
        :param jsonText:
        :return:
        """
        datas = json.loads(jsonText)
        if datas['ret'] == 0:

            self.offset = datas['next_offset']
            print(self.offset)
            msg_list = datas['general_msg_list']
            result = json.loads(msg_list)['list']
            #print(result)
            for data in result:
                try:
                    self.item['title'] = data['app_msg_ext_info']['title']
                    self.item['digest'] = data['app_msg_ext_info']['digest']
                    self.item['fileid'] = data['app_msg_ext_info']['fileid']
                    self.item['content_url'] = data['app_msg_ext_info']['content_url']
                    self.item['cover'] = data['app_msg_ext_info']['cover']
                    self.item['author'] = data['app_msg_ext_info']['author']
                    self.write_datas(self.item)
                except Exception as e:
                    print(e)
                    continue
            time.sleep(5) # 设置延迟防止爬取间隔太短
            self.request_data()
        else:
            print('数据错误')

    def write_datas(self,data):
        with open(r'data.json','a') as file:
            file.write(json.dumps(data))


if __name__ == "__main__":
    a = GZH()
    a.request_data()
