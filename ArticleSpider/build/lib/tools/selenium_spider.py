from selenium import webdriver
from scrapy.selector import Selector
import time
from requests import Session
import pickle

req = Session()
req.headers.clear()
browser = webdriver.Chrome()
browser.get("https://www.zhihu.com/signup?next=%2F")

time.sleep(20)

cookies = browser.get_cookies()
# for cookie in cookies:
#     req.cookies.set(cookie['name'],cookie['value'])
#
# test = req.get('https://www.zhihu.com')

cookie_dict = {}

for cookie in cookies:
    # 写入文件
    f = open('../cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb')
    pickle.dump(cookie, f)
    f.close()
    cookie_dict[cookie['name']] = cookie['value']
browser.close()





# browser.find_element_by_xpath('//div[contains(@class, "SignFlow-accountInputContainer")]//input[@name="username"]').send_keys('18392077175')
# browser.find_element_by_xpath('//div[contains(@class, "SignFlow-password")]//input[@name="password"]').send_keys('xulinsong')
# browser.find_element_by_xpath('//button[contains(@class, "SignFlow-submitButton")]').click()

# browser = webdriver.Chrome()
#
# browser.get("https://www.zhihu.com/signin")
# browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
#             "18392077175")
# browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
#             "xulinsong")
# time.sleep(5)
# browser.find_element_by_css_selector(
#             ".Button.SignFlow-submitButton").click()
#browser.quit()


#selenium 完成微博模拟登陆
# browser = webdriver.Chrome()
# browser.get('https://www.weibo.com')


#模拟鼠标下拉
# browser = webdriver.Chrome()
# browser.get("https://www.oschina.net/blog")
# import time
# time.sleep(20)
#
# for i in range(3):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(3)

#设置chromedriver不加载图片
#chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images":2}
# chrome_opt.add_experimental_option("prefs", prefs)
# browser = webdriver.Chrome(chrome_options=chrome_opt)
# browser.get("https://www.taobao.com")

# browser = webdriver.PhantomJS(executable_path="/Users/uvo9ono/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
# browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.3.yYBVG6&id=538286972599&cm_id=140105335569ed55e27b&abbucket=15&sku_properties=10004:709990523;5919063:6536025")
#
# print (browser.page_source)
# browser.quit()
