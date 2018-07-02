# encoding:utf-8

"""
获取cookie，建cookies池
"""
import requests
import time
from selenium import webdriver


myWeiBo = [
    {'no':'ps808085@163.com','psw':'a1234560'},
    #{'no':'15867287705','psw':'a1234560'},
]




def getCookie(account,password):
    try:
        url = 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F'
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(2)

        driver.find_element_by_id('loginName').send_keys(account)
        driver.find_element_by_id('loginPassword').send_keys(password)
        driver.find_element_by_id('loginAction').click()
        time.sleep(5)

        try:
            cookie = {}
            for ck in driver.get_cookies():
                cookie[ck['name']] = ck['value']
            driver.quit()
            print("Get the cookie of Weibo:%s successfully!(共%d个键值对)" % (account, len(cookie)))
            return cookie
        except Exception:
            print("出错")
    except Exception:
        print("网址出错")

def getCookies(weibo):
    """
    获取cookies
    :param weibo:
    :return:
    """
    cookies = []
    for elem in weibo:
        accont = elem['no']
        password = elem['psw']
        cookie = getCookie(accont,password)
        if cookie != None:
            cookies.append(cookie)
    return cookies


cookies = getCookies(myWeiBo)
if __name__ == "__main__":
    cookie = getCookies(myWeiBo)