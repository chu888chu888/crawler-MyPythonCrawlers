# encoding: UTF-8
# 刷人人墙脚本

import sys, urllib2, urllib, cookielib, random

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

# 通过人人登录测试，登录人人并返回个人主页的源代码
loginUrl = 'http://www.renren.com/PLogin.do'  # 登录的表单的action
post_data = {'email': '387251968@qq.com',  # httpfox抓到的post_data
		'origURL:': 'http://www.renren.com/home',
		'domain': 'renren.com',
		'password': '135790',
		'captcha_type': 'web_login'}
myCookie = urllib2.HTTPCookieProcessor(cookielib.CookieJar())  # 创建一个HttpCookie处理器并绑定一个CookieJar
opener = urllib2.build_opener(myCookie)
urllib2.install_opener(opener)  # 13 -14 将httpcookie处理器与urllib2绑定
req = urllib2.urlopen(loginUrl, urllib.urlencode(post_data))  # 模拟登录！

def main():
	contents = ['预祝晚会圆满结束～～～～', '~~~']
	for i in range(1200):
		content = '只给电源不给线？'
		post_content = {'content': content,
						'requestToken': 311188297,
						'_rtk': 'de4d59a3'}
		url = 'http://w.renren.com/wall/24333/publish'
		request = urllib2.Request(url, data=urllib.urlencode(post_content))
		index = random.randint(0, 9)
		user_agent = user_agents[index]
		request.add_header('User-agent', user_agent)

		rs = urllib2.urlopen(request)
		print i / 1200.0

main()