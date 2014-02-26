# -*- coding: utf-8 -*-

# 从教务处全校课表获取所有的课程信息的Spider
# URL: http://xk.urp.seu.edu.cn/jw_service/service/academyClassLook.action

import requests
import MySQLdb
import sys
import copy
import urllib2
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')

# 去除无用的信息
def beautyText(text):
    text = text.replace('&nbsp;', '').strip()
    return text

# 切割混合字串得到具体的课程时间地点信息
def getTimeAndPlaceDetail(mixedStr):
    # 典型的类型
    # [1-16周] 周一(3-4)中大-309,周四(3-4)中大-求是堂
    # [1-16周]
    # [9-16周] 周四(6-7)东南-104
    # [1-16周] 周一(6-8),周四(6-8)
    # [1-16周] 周二(单6-7)教二-400,周四(6-7)教二-400
    # [1-16周] 周二(3-4)教七-30A,周四(双3-4)教七-30A

    # 一门课程由于需要会被切割为多条，故提供一标准，方便只对不同的信息进行修改
    # 比如 [1-16周] 周二(3-4)教七-30A,周四(双3-4)教七-30A 会解析成如下两条：
    # 1, 16, 2, 3, 4, 0, 教七-30A
    # 1, 16, 4, 3, 4, -1, 教七-30A
    # 存在信息必然是相同的，只用拷贝一份并修改不同的即可
    formattedInfo = {
        'beginWeekNum': -1,  # 课程开始的周
        'endWeekNum': -1,  # 课程结束的周
        'classWeek': -1,  # 星期几上课
        'beginTime': -1,  # 第几节课开始
        'endTime': -1,  # 第几节课结束
        'classType': 0,  # 0为不分单双周的课，单周为1，双周为-1
        'place': "",  # 上课地点
    }

    result = []  # 保存用于返回的结果

    # 分段解析混合串
    part1 = mixedStr[0: mixedStr.find(']') + 1].strip()  # 第一段 [x-y]周
    part2 = mixedStr[mixedStr.find(']') + 1:].strip()  # 剩余部分

    # 字段1不为空，保存关于周次的信息，相同部分，直接修改formattedInfo
    if len(part1) != 0:
        part1 = part1.replace('[', '').replace('周]', '').strip()
        dashPos = part1.find('-')
        formattedInfo['beginWeekNum'] = part1[0: dashPos].strip()
        formattedInfo['endWeekNum'] = part1[dashPos + 1:].strip()

    # 字段2不为空，保存关于上课时间与地点的信息
    if len(part2) != 0:
        splitedParts = part2.split(',')  # 根据逗号分隔开
        # 针对每一部分处理
        for part in splitedParts:
            part = part.strip()
            if len(part) != 0:
                copyInfo = copy.deepcopy(formattedInfo)  # 拷贝一份

                # 填充信息
                copyInfo['place'] = part[
                    part.find(')') + 1:].strip()

                if part.find('单') != -1:  # 单周上课
                    copyInfo['beginTime'] = part[
                        part.find(u'单') + len(u"单"): part.find('-')].strip()
                    copyInfo['endTime'] = part[
                        part.find('-') + 1: part.find(')')].strip()
                    copyInfo['classType'] = 1
                elif part.find('双') != -1:  # 双周上课
                    copyInfo['beginTime'] = part[
                        part.find(u'双') + len(u"双"): part.find('-')].strip()
                    copyInfo['endTime'] = part[
                        part.find('-') + 1: part.find(')')].strip()
                    copyInfo['classType'] = -1
                else:
                    copyInfo['beginTime'] = part[
                        part.find('(') + 1: part.find('-')].strip()
                    copyInfo['endTime'] = part[
                        part.find('-') + 1: part.find(')')].strip()

                # 将字符串转化成整型
                for (k, v) in copyInfo.items():
                    if v.__class__ == "".__class__ and v.isdigit():
                        copyInfo[k] = int(v)

                w = part[0: part.find('(')].strip()
                if w == '周一':
                    copyInfo['classWeek'] = 1
                elif w == '周二':
                    copyInfo['classWeek'] = 2
                elif w == '周三':
                    copyInfo['classWeek'] = 3
                elif w == '周四':
                    copyInfo['classWeek'] = 4
                elif w == '周五':
                    copyInfo['classWeek'] = 5
                elif w == '周六':
                    copyInfo['classWeek'] = 6
                elif w == '周日':
                    copyInfo['classWeek'] = 7

                # 测试。。
                # if len(copyInfo['beginTime']) == 0:
                #     print "传入的参数:", mixedStr
                #     print "分割后的数组:", splitedParts
                #     for i in splitedParts:
                #         print i
                #     print "出现bug的part:", part
                #     print "是否一致", right == mixedStr
                    # exit()

                result.append(copyInfo)

    return result


def main():
    # setup
    term = '13-14-3'
    termPrefix = '13143'
    
    conn = MySQLdb.connect(
        host="localhost", user="goclis", passwd="qqqqqq", db="goclis", charset="utf8")
    cursor = conn.cursor()

    entryUrl = "http://xk.urp.seu.edu.cn/jw_service/service/academyClassLook.action"
    entryPageSource = requests.get(entryUrl).text
    html = etree.HTML(entryPageSource)
    departmentNodes = html.xpath('//a[@target]')  # 所有院系的节点

    urlPrefix = "http://xk.urp.seu.edu.cn/jw_service/service/"  # 链接的前缀

    for node in departmentNodes:
        url = urlPrefix + node.attrib['href']  # 院系对应的课程链接
        text = node.text
        dpmId = text[text.find('[') + 1: text.find(']')]  # 院系的编号

        dpmPageSource = requests.get(url).text 
        
        dpmHtml = etree.HTML(dpmPageSource)

        # 得到符合学期条件的课程节点
        s =  "//tr[@onmouseover]/td[2][contains(text(), '%s')]/parent::*" % term
        coursesInThisTerm = dpmHtml.xpath(s)
        for course in coursesInThisTerm:
            # 课程细节
            tds = course.xpath('.//td')

            courseId = termPrefix + dpmId \
                        + beautyText(tds[0].text)  # 以 学期编码+院系编号+课程序号作为其【课程编号】
            courseTerm = term  # 同查询的学期
            courseName = beautyText(tds[2].text)  # 课程名
            courseTeacher = beautyText(tds[4].text)  # 授课老师
            courseTimeAndPlace = beautyText(tds[5].text)  # 上课的时间和地点

            timeAndPlaceInfos = getTimeAndPlaceDetail(courseTimeAndPlace)
            for item in timeAndPlaceInfos:
                # 存入数据库
                sql = "INSERT INTO course (beginWeekNum, endWeekNum, classWeek, classBeginTime, \
                            classEndTime, classPlace, classType, term, courseName, teacher, courseId) \
                                VALUES (%s, %s, %s, %s, %s, '%s', %s, '%s', '%s', '%s', '%s')" % \
                    (item[
                     'beginWeekNum'], item['endWeekNum'],
                     item['classWeek'], item[
                     'beginTime'], item[
                     'endTime'], item['place'],
                     item['classType'], courseTerm, courseName, 
                     courseTeacher, courseId)
                print sql
                n = cursor.execute(sql)

                conn.commit()



def testTimeAndPlaceDetail():
    r = getTimeAndPlaceDetail(u'[1-16周]周四(双3-4)教二-403')
    for item in r:
        for (k, v) in item.items():
            print k, v
    print r

# testTimeAndPlaceDetail()
main()