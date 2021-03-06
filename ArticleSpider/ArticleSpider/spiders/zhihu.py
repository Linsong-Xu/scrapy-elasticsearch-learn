# -*- coding: utf-8 -*-
import scrapy
import re
import os
from urllib import parse
from scrapy.loader import ItemLoader
import datetime
import json
from ArticleSpider.items import ZhihuQuestionItem, ZhihuAnswerItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_answer_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={1}&offset={2}&platform=desktop&sort_by=default'

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
        提取出html页面中的所有url， 并跟踪这些url进行下一步爬取
        如果提取的url中的格式为/question/xxxk就下载之后直接进入解析函数
        :param response:
        :return:
        """
        all_urls = response.css('a::attr(href)').extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x : True if x.startswith('https') else False, all_urls)
        for url in all_urls:
            match_obj = re.match('(.*zhihu.com/question/(\d+))(/|$).*', url)
            if match_obj:
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
                #break
            else:
                #pass
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        # 处理question页面， 从页面中提取出具体的question item
        if 'QuestionHeader-title' in response.text:
            #处理新版本
            match_obj = re.match('(.*zhihu.com/question/(\d+))(/|$).*', response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_xpath('title', '//main//h1[@class="QuestionHeader-title"]//text()')
            item_loader.add_xpath('content', '//div[@class="QuestionHeader-detail"]')
            item_loader.add_value('url', response.url)
            item_loader.add_value('zhihu_id', question_id)
            item_loader.add_xpath('answer_num', '//div[@class="List"]/div/h4/span/text()')
            item_loader.add_xpath('comments_num', '//div[@class="QuestionHeader-Comment"]//button//text()')
            item_loader.add_xpath('watch_user_num', '//strong[@class="NumberBoard-itemValue"]//text()')
            item_loader.add_xpath('topics', '//div[@class="QuestionHeader-topics"]//div[@class="Popover"]//text()')

            # item_loader.add_css('title', 'h1.QuestionHeader-title::text')
            # item_loader.add_css('content', '.QuestionHeader-detail')
            # item_loader.add_value('url', response.url)
            # item_loader.add_value('zhihu_id', question_id)
            # item_loader.add_css('answer_num', '.List-headerText span::text')
            # item_loader.add_css('comments_num', '.QuestionHeader-Comment button::text')
            # item_loader.add_css('watch_user_num', '.NumberBoard-itemValue::text')
            # item_loader.add_css('topics', '.QuestionHeader-topics .Popover div::text')

            question_item = item_loader.load_item()

        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers, callback=self.parse_answer)
        yield question_item

        pass

    def parse_answer(self, reponse):
        # 处理question的answer
        ans_json = json.loads(reponse.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        # 提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["praise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)

    def start_requests(self):
        from selenium import webdriver
        import time
        import pickle

        cookie_dict = {}

        if(os.path.exists('./ArticleSpider/cookies/zhihu_cookie.pickle')):
            with open('./ArticleSpider/cookies/zhihu_cookie.pickle', 'rb') as file:
                cookie_dict = pickle.load(file)
            return [scrapy.Request(url=self.start_urls[0], headers=self.headers, dont_filter=True, cookies=cookie_dict)]

        browser = webdriver.Chrome()
        browser.get("https://www.zhihu.com/signup?next=%2F")

        time.sleep(20)

        Cookies = browser.get_cookies()

        for cookie in Cookies:
            cookie_dict[cookie['name']] = cookie['value']
        f = open('./ArticleSpider/cookies/zhihu_cookie.pickle', 'wb')
        pickle.dump(cookie_dict, f)
        f.close()
        browser.close()


        return [scrapy.Request(url=self.start_urls[0], headers = self.headers, dont_filter=True, cookies=cookie_dict)]
