# -*- coding: utf-8 -*-
# @Time    : 2022/5/12 22:54
# @Author  : 自动化2005陈富昌0122004950804
# @Site    :
# @File    : WeatherPie.py
# @Software: PyCharm
import matplotlib.pyplot as plt
import pandas as pd
import numpy


def StatisticOneYear(OneYearData):
    label = ['晴', '雨', '多云', '阴']
    WeatherConditionDict = {}
    AllWeatherConditionDict = {}

    for WeatherConditionName in label:
        WeatherConditionDict[WeatherConditionName] = 0

    for OneDayData in OneYearData:
        DayData = OneDayData.split('/')[0]  # 拆分天气，只保留左边，即白天
        if DayData in AllWeatherConditionDict:
            AllWeatherConditionDict[DayData] += 1
        else:
            AllWeatherConditionDict[DayData] = 1

    for WeatherConditionName in AllWeatherConditionDict:
        if WeatherConditionName == '晴':
            WeatherConditionDict['晴'] += AllWeatherConditionDict[WeatherConditionName]
        # elif '雾' in WeatherConditionName or '霾' in WeatherConditionName:
        #     WeatherConditionDict['雾霾'] += AllWeatherConditionDict[WeatherConditionName]#雾霾数据太少，不算
        elif '雨' in WeatherConditionName:
            WeatherConditionDict['雨'] += AllWeatherConditionDict[WeatherConditionName]
        elif WeatherConditionName == '多云':
            WeatherConditionDict['多云'] += AllWeatherConditionDict[WeatherConditionName]
        # elif '雪' in WeatherConditionName and WeatherConditionName != '雨夹雪':
        #     WeatherConditionDict['雪'] += AllWeatherConditionDict[WeatherConditionName]#雪的数据太少
        elif WeatherConditionName == '阴':
            WeatherConditionDict['阴'] += AllWeatherConditionDict[WeatherConditionName]

    WeatherConditionList = []
    for WeatherConditionName in label:
        WeatherConditionList.append(WeatherConditionDict[WeatherConditionName])
    return WeatherConditionList


def absolute_value(val):
    a = numpy.round(val / 100. * 365, 0)
    return a






if __name__ == '__main__':
    WHWeatherData = pd.ExcelFile(r'武汉天气数据.xlsx')  # 读取天气数据
    # 数据按年份分了sheet存储,每次提取一个sheet即可
    SheetNames = WHWeatherData.sheet_names  # 获取武汉天气爬虫工作区的工作表名称，一年一个工作区
    plt.figure(1)

    label = [u'晴', u'雨', u'多云', u'阴']
    color = ['green', 'purple', 'lightskyblue', 'red']

    k = 1
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    for i in SheetNames:  # i为年份
        OneYearData = pd.read_excel('武汉天气数据.xlsx', sheet_name=i)
        OneYearData = list(OneYearData['天气状况'])
        PieData = StatisticOneYear(OneYearData)  # 获得天数统计的list
        ax = plt.subplot(3, 4, k)  # 选中子区域
        plt.pie(PieData, radius=1, labels=label, labeldistance=1.2, colors=color, startangle=90, shadow=True,
                autopct=absolute_value)
        # 标签存在重叠问题，加入labeldistance参数
        ax.set_title(str(i) + '年天气状况统计',fontsize=10)
        k += 1
        if k == 13:
            break
    plt.savefig('./WeatherPie.jpg')
    plt.show()


