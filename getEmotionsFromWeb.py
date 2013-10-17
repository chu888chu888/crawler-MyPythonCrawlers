# encoding: UTF-8
# 抓取表情

import urllib2, urllib, random

# 人人表情
def getFromRenRen():
	url = "http://a.xnimg.cn/imgpro/emotions/tie/%s.gif?ver=1"
	for i in range(40):
		data = urllib.urlopen(url % i).read()
		if data.find("404") == -1:
			f = open("renren/%s.gif" % i, 'w')
			f.write(data)
			f.close()

# -.- 对付百度还得伪装成浏览器。。
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

# 获取兔斯基的表情
def getTsjFromTieba():
	url = "http://static.tieba.baidu.com/tb/editor/images/tsj/t_%s.gif"
	
	for i in [j + 1 for j in range(50)]:
		s = str(i)
		if len(s) == 1:
			s = "000" + s
		elif len(s) == 2:
			s = "00" + s
		
		request = urllib2.Request(url % s)
		index = random.randint(0, 9)
		user_agent = user_agents[index]
		request.add_header('User-agent', user_agent)
		data = urllib2.urlopen(request).read()

		if data.find("html") == -1:
			f = open("tsj/%s.gif" % s, 'w')
			f.write(data)
			f.close()
		else:
			print data[0 : 100]

# 获取泡泡
def getPaopaoFromTieba():
	url = "http://static.tieba.baidu.com/tb/editor/images/client/image_emoticon%s.png"

	for i in [j + 1 for j in range(80)]:
		request = urllib2.Request(url % i)
		index = random.randint(0, 9)
		user_agent = user_agents[index]
		request.add_header('User-agent', user_agent)
		data = urllib2.urlopen(request).read()

		if data.find("html") == -1:
			f = open("paopao/%s.png" % i, 'w')
			f.write(data)
			f.close()

# 获取气泡熊
def getQpxFromTieba():
	url = "http://static.tieba.baidu.com/tb/editor/images/qpx_n/b%s.gif"

	for i in [j + 1 for j in range(60)]:
		s = str(i)
		if len(s) == 1:
			s = "0" + s

		request = urllib2.Request(url % s)
		index = random.randint(0, 9)
		user_agent = user_agents[index]
		request.add_header('User-agent', user_agent)
		data = urllib2.urlopen(request).read()

		if data.find("html") == -1:
			f = open("qpx/%s.gif" % s, 'w')
			f.write(data)
			f.close()

# 获取阿狸
def getAliFromTieba():
	url = "http://static.tieba.baidu.com/tb/editor/images/ali/ali_0%s.gif"

	for i in [j + 1 for j in range(60)]:
		s = str(i)
		if len(s) == 1:
			s = "0" + s

		request = urllib2.Request(url % s)
		index = random.randint(0, 9)
		user_agent = user_agents[index]
		request.add_header('User-agent', user_agent)
		data = urllib2.urlopen(request).read()

		if data.find("html") == -1:
			f = open("ali/%s.gif" % s, 'w')
			f.write(data)
			f.close()

# 获取影子
def getYzFromTieba():
	url = "http://static.tieba.baidu.com/tb/editor/images/shadow/yz_0%s.gif"

	for i in [j + 1 for j in range(60)]:
		s = str(i)
		if len(s) == 1:
			s = "0" + s

		request = urllib2.Request(url % s)
		index = random.randint(0, 9)
		user_agent = user_agents[index]
		request.add_header('User-agent', user_agent)
		data = urllib2.urlopen(request).read()

		if data.find("html") == -1:
			f = open("yz/%s.gif" % s, 'w')
			f.write(data)
			f.close()

