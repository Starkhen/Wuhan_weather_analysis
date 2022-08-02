# -*- coding: utf-8 -*-
# @Time    : 2022/5/11 22:04
# @Author  : 自动化2005陈富昌0122004950804
# @Site    :
# @File    : ReadWHWeather.py
# @Software: PyCharm

import requests  # 网页请求
from bs4 import BeautifulSoup
import xlsxwriter
import time
import pandas as pd
import os


# 除去数据中的\n、\r、空格，以及变换日期格式
def CleanData(InfoString):
    InfoString = InfoString.replace('\n', '', )  # 这里爬下来的文本里面有很多\n\r的字符，把它们去掉
    InfoString = InfoString.replace('\r', '', )  # 第三个参数默认，替换全部
    InfoString = InfoString.replace(' ', '', )
    InfoString = InfoString.replace('年', '-', 1)  # 日期格式调整
    InfoString = InfoString.replace('月', '-', 1)
    InfoString = InfoString.replace('日', '', 1)
    return InfoString


# 爬取武汉天气数据
def ExtractWHWeather():
    WHWeatherExcel = xlsxwriter.Workbook('武汉天气爬虫.xlsx')  # 创建Excel表格武汉天气爬虫.xlsx,之后每年添加一个sheet
    url = 'http://www.tianqihoubao.com/lishi/wuhan.html'
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'Connection': 'close'}  # head,防止网站知道我们是爬虫，并且请求完要关闭
    html = requests.get(url, headers=head)  # 网页数据
    bsObj = BeautifulSoup(html.content, 'lxml')  # 网页请求
    AllYearWeather = bsObj.find_all('div', class_="wdetail")  # 所有的天气数据在此
    OneYearWeather = AllYearWeather[0].find_all('div', attrs={'class': 'box pcity'})  # 每一年的天气数据
    Year = 2010
    for Quarter in OneYearWeather:  # 一个季度的数据
        Year += 1
        # if Year <= 2022:  # 首先底部还有许多冗余信息会被爬进去，加上年份限制
        WorkSheet = WHWeatherExcel.add_worksheet(str(Year))  # 创建sheet,并以年份命名，worksheet指向WHWeatherExcel
        row = 0
        col = 0
        # 表格第一行
        WorkSheet.write(row, col, '日期')
        WorkSheet.write(row, col + 1, '天气状况')
        WorkSheet.write(row, col + 2, '气温')
        WorkSheet.write(row, col + 3, '风力风向')
        AQuarterData = Quarter.find_all('ul')  # 一个季度的全部数据在一个<ul>标签
        for AMonth in AQuarterData:  # 一个季度内遍历每个月的数据
            ThreeMonthLink = AMonth.find_all('a')  # 每个月的链接都在一个a标签内
            for Link in ThreeMonthLink:  # 遍历一个季度（三个月）的链接，分别爬取数据
                AMonthLink = Link['href']
                if '/lishi' in str(AMonthLink):  # 2016年及之后某些年份的链接存在缺省
                    AMonthurl = 'http://www.tianqihoubao.com' + AMonthLink
                else:  # 缺省处理
                    AMonthurl = 'http://www.tianqihoubao.com/lishi/' + AMonthLink

                try:  # 请求过度频繁的处理
                    AMonth_HTML = requests.get(AMonthurl, headers=head)  # 跳转的页面再执行一次爬取操作
                    AMonthObj = BeautifulSoup(AMonth_HTML.content, 'lxml')  # 网页请求
                    AMonthData = AMonthObj.find_all('tr')  # 表格中的一行,即为某一天的天气数据，存储一个月的所有行
                    i = 1
                    for ADay in AMonthData:  # 遍历一个月数据的所有行，ADay即为一行
                        if i == 1:  # 表格的第一行是表头，不是天气数据，排除
                            i = 2
                            continue
                        else:
                            ALine = ADay.find_all('td')  # 找出表格一行内容
                            col = 0  # 从0列开始写入
                            row += 1  # 比起上一次写入时，行+1
                            for info in ALine:  # 遍历行的四项信息
                                AnInfo = str(info.get_text())  # 获取行数据下的文本内容
                                AnInfo = CleanData(AnInfo)  # 除去数据中的\n、\r、空格，以及变换日期格式
                                WorkSheet.write(row, col, AnInfo)  # 数据写入表格
                                col += 1  # 列增加
                except:  # 请求过快时，按5s休息处理
                    print("requests speed so high,need sleep!")
                    time.sleep(5)
                    print("continue...")
                    continue
        print('...爬完 ' + str(Year) + ' 年...')  # 交互内容
    WHWeatherExcel.close()  # 关闭EXCEL
    print('爬取结束')  # 提示爬取结束
    return f'爬取结束'


if __name__ == '__main__':
    ExtractWHWeather()  # 爬取天气数据

    # 去除重复行的数据
    WHWeatherExcel = pd.ExcelFile('武汉天气爬虫.xlsx')
    for sheetnames in WHWeatherExcel.sheet_names:
        realWHWeatherpath = "武汉天气数据.xlsx"
        WHWeatherdf = pd.DataFrame(pd.read_excel('武汉天气爬虫.xlsx', sheet_name=sheetnames))
        deleteRe = WHWeatherdf.drop_duplicates()
        if not os.path.exists(realWHWeatherpath):
            deleteRe.to_excel(realWHWeatherpath, encoding='GBK', sheet_name=sheetnames)
        else:
            with pd.ExcelWriter(realWHWeatherpath, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                deleteRe.to_excel(writer, sheet_name=sheetnames)
    WHWeatherExcel.close()
