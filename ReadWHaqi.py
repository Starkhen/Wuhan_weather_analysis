# -*- coding: utf-8 -*-
# @Time    : 2022/5/11 21:08
# @Author  : 自动化2005陈富昌0122004950804
# @Site    : 
# @File    : ReadWHaqi.py
# @Software: PyCharm

import requests
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


# 爬取武汉空气质量数据
def ExtractAQIWHWeather():
    WHWeatherExcel = xlsxwriter.Workbook('武汉空气质量.xlsx')  # 创建Excel表格武汉空气质量.xlsx,之后每年添加一个sheet
    motherurl = 'http://www.tianqihoubao.com/aqi/wuhan-'  # URL共有的部分
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39',
        'Connection': 'close'}  # head伪装，请求完成后连接立马关闭
    # 爬取的区间
    openyear = 2010
    endyear = 2022
    WorkSheet = WHWeatherExcel.add_worksheet('aqi')  # sheet名称
    row = 0
    col = 0
    # 表格第一行
    WorkSheet.write(row, col, '日期')
    WorkSheet.write(row, col + 1, '质量等级')
    WorkSheet.write(row, col + 2, 'AQI指数')
    WorkSheet.write(row, col + 3, '当天AQI排名')
    WorkSheet.write(row, col + 4, 'PM2.5')
    WorkSheet.write(row, col + 5, 'PM10')
    WorkSheet.write(row, col + 6, 'So2')
    WorkSheet.write(row, col + 7, 'No2')
    WorkSheet.write(row, col + 8, 'Co')
    WorkSheet.write(row, col + 9, 'O3')
    for year in range(openyear, endyear + 1):
        for month in range(1, 13):
            # url的合成处理
            if month <= 9:
                realurl = motherurl + str(year) + '0' + str(month) + '.html'
            else:
                realurl = motherurl + str(year) + str(month) + '.html'
            try:  # 请求过度频繁的处理
                Aqi_HTML = requests.get(realurl, headers=head)  # 跳转的页面再执行一次爬取操作
                AMonthObj = BeautifulSoup(Aqi_HTML.content, 'lxml')  # 网页请求
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
                        for info in ALine:  # 遍历行的各项信息
                            AnInfo = str(info.get_text())  # 获取行数据下的文本内容
                            AnInfo = CleanData(AnInfo)  # 除去数据中的\n、\r、空格，以及变换日期格式
                            WorkSheet.write(row, col, AnInfo)  # 数据写入表格
                            col += 1  # 列增加
            except:  # 请求过快时，按5s休息处理
                print("requests speed so high,need sleep!")
                time.sleep(5)
                print("continue...")
                continue

        print('...爬完 ' + str(year) + ' 年...')
    WHWeatherExcel.close()
    print('爬取结束')
    return f'爬取结束'


if __name__ == '__main__':
    ExtractAQIWHWeather()  # 爬取AQI数据

    # 去重处理
    WHWeatherAQIExcel = pd.ExcelFile('武汉空气质量.xlsx')
    realWHWeatherAQIpath = "武汉质量数据.xlsx"
    WHWeatherAQIdf = pd.DataFrame(pd.read_excel('武汉空气质量.xlsx'))
    deleteRe = WHWeatherAQIdf.drop_duplicates()
    if not os.path.exists(realWHWeatherAQIpath):
        deleteRe.to_excel(realWHWeatherAQIpath, encoding='GBK')
    else:
        with pd.ExcelWriter(realWHWeatherAQIpath, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            deleteRe.to_excel(writer)
    WHWeatherAQIExcel.close()

