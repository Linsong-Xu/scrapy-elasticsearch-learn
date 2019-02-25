# -*- coding: utf-8 -*-
import re
import json
import datetime

import scrapy
from scrapy.loader import ItemLoader


class ZhihuSelSpider(scrapy.Spider):
    name = 'zhihu_sel'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        """
        提取出html页面中的所有url 并跟踪这些url进行一步爬取
        如果提取的url中格式为 /question/xxx 就下载之后直接进入解析函数
        """
        pass

    def parse_question(self, response):
        # 处理question页面， 从页面中提取出具体的question item
        pass

    def parse_answer(self, reponse):
        pass

    def start_requests(self):
        from selenium import webdriver
        import time
        import pickle

        browser = webdriver.Chrome()
        browser.get("https://www.zhihu.com/signup?next=%2F")

        time.sleep(20)

        Cookies = browser.get_cookies()
        cookie_dict = {}

        for cookie in Cookies:
            f = open('./ArticleSpider/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()

        return [scrapy.Request(url=self.start_urls[0], headers = self.headers, dont_filter=True, cookies=cookie_dict)]


