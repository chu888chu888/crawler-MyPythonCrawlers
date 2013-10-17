# encoding: UTF-8
''' 从教务处获取学生信息 '''

import urllib, urllib2, re
import MySQLdb

# 学生信息（数据库model）
class Student(object):
	def __init__(self, name = '', ID = 1, stu_num = '', depart = '', major = ''):
		self.name = name  # 姓名
		self.ID = ID  # 一卡通
		self.stu_num = stu_num  # 学号
		self.depart = depart  # 院系
		self.major = major  # 专业

# 以字符串形式返回一卡通为ID，学期为term的课表的源代码
def getCourseTableSource(ID, term):
	url = "http://xk.urp.seu.edu.cn/jw_service/service/stuCurriculum.action"
	data = {'returnStr': '',
			'queryStudentId': str(ID),
			'queryAcademicYear': term}
	data_encoded = urllib.urlencode(data)
	content = urllib2.urlopen(url, data_encoded)

	return decorateSource(content.read())

# 处理源代码格式方便后续解析
def decorateSource(html_src):
	# 替换不规则代码
	html_src = html_src.replace('<td rowspan="5" class="line_topleft"" align="center">',
			 '<td rowspan="5" class="line_topleft" align="center">')
	# 去除&nbsp;
	html_src = html_src.replace('&nbsp;', '')

	return html_src

# 返回Student对象
def getStudentInfo(html_src):
	ptrn = r'<td width="20%" align="left">.*?</td>'  # 开头是<td ...>结尾是</td>的非贪婪的匹配
	result = re.findall(ptrn, html_src)

	student = Student()
	for info in result:
		info = info.strip('<td width="20%" align="left">').strip(r'</td>')  # 去除头尾html标签
		if info.find('院系') != -1:
			student.depart = info[info.find(':') + 1 : ]
		if info.find('专业') != -1:
			student.major = info[info.find(':') + 1 : ]
		if info.find('学号') != -1:
			student.stu_num = info[info.find(':') + 1 : ]
		if info.find('一卡通') != -1:
			student.ID = int(info[info.find(':') + 1 : ])
		if info.find('姓名') != -1:
			student.name = info[info.find(':') + 1 : ]
	return student

# 连接数据库
def connectMySQLdb(db_name):
	conn = MySQLdb.connect(host = 'localhost', user = '***', passwd = '***')  # 连接数据库
	conn.select_db(db_name)  # 选择数据库
	return conn.cursor()

def dealStudentInfo(ID, term):
	html_src = getCourseTableSource(ID, term)
	student = getStudentInfo(html_src)

	db_name = 'db_name'
	conn = MySQLdb.connect(host = 'localhost', user = '***', passwd = '***', db = db_name,
				charset='utf8')
	dbCursor = conn.cursor()  # 数据库cursor
	info = (student.ID, student.stu_num, student.name, student.depart, student.major)
	if student.name: 
		try:
			dbCursor.execute("INSERT INTO student VALUES (%s, %s, %s, %s, %s)", info)
			conn.commit()  # 添加此语句实现数据真正写入数据库
		except:
			pass
	dbCursor.close()

# 主函数
def main():
	term = '13-14-1'
	IDs = [i + 213130001 for i in range(4250)]
	notify = 0
	for ID in IDs:
		dealStudentInfo(ID, term)
		notify += 1
		if notify >= 5:
			print str((ID - 213130001) / 4250.0 * 100) + "%"
			notify = 0

def test():
	dealStudentInfo(213116000, '13-14-2')
	print getCourseTableSource(213116000, '13-14-2')

if __name__ == '__main__':
	main()

