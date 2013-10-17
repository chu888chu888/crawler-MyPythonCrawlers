# encoding: UTF-8

''' 通过Google搜索关键字并获取结果页 '''

import urllib, urllib2, random

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
        (KHTML, like Gecko) Element Browser 5.0', \
        'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
        Version/6.0 Mobile/10A5355d Safari/8536.25', \
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/28.0.1468.0 Safari/537.36', \
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

queryStr = 'c++ site:seu.edu.cn'
queryStr = urllib2.quote(queryStr)
# ----- url description ------- 
# hl -- language used
# q -- keyword to search
# start -- selected page, 20 for page 3, 10 for page 2, 0 for page 1
url = 'https://www.google.com.hk/search?hl=cn&q=%s&start=10' % queryStr
#url = 'https://www.google.com.hk/#bav=on.2,or.&fp=45ba06928bde91f4&newwindow=1&q=%s&safe=strict' % queryStr
request = urllib2.Request(url)
index = random.randint(0, 9)
user_agent = user_agents[index]
request.add_header('User-agent', user_agent)
response = urllib2.urlopen(request)
html = response.read()
open('google_result.html', 'w').write(html)