# -*- coding: utf-8 -*-
# @Time    : 2022/5/12 10:25
# @Author  : 自动化2005陈富昌0122004950804
# @Site    :
# @File    : MergeTwoExcel.py
# @Software: PyCharm
import pandas as pd
from string import digits


def Merge(AllWHAirQualityData, AllWHWeatherData):
    AllWHAirQualityDatRows = len(AllWHAirQualityData)  # aqi总行数
    AllWHWeatherDataRows = len(AllWHWeatherData)  # 总行数

    MergedDate = []  # 存储两表共同的日期数据
    MergedWeatherCondition = []  # 天气状况
    MergedTemperature = []  # 气温
    MergedWindDirection = []  # 风力风向
    MergedAQI = []
    MergedQuaLevel = []
    MergedPM25 = []
    MergedPM10 = []
    MergedSO2 = []
    MergedCO = []
    MergedNO2 = []
    MergedO3 = []

    # 处理日期的数据
    for i in AllWHAirQualityData['日期']:
        for j in AllWHWeatherData['日期']:
            if i == j and i not in MergedDate and j not in MergedDate:  # 相同的日期，存储起来
                MergedDate.append(i)
                break
    for i in range(0, AllWHAirQualityDatRows):  # 遍历所有行
        OneLineData = AllWHAirQualityData[i:i + 1]
        # Date = str(OneLineData['日期']).replace('Name: 日期, dtype: object', '')[-11: -1]
        Date = str(OneLineData['日期']).replace('Name: 日期, dtype: object', '')[-11:-1]  # 进行删选，选取需要的部分
        if Date in MergedDate:
            AQIData = str(OneLineData['AQI指数']).replace('\nName: AQI指数, dtype: int64', '')[-4:].replace(' ', '')
            MergedAQI.append(AQIData)
            QuaLevelData = str(OneLineData['质量等级']).replace('\nName: 质量等级, dtype: object', '')[-5:].replace(' ', '')
            MergedQuaLevel.append(QuaLevelData)

            PM25Data = str(OneLineData['PM2.5']).replace('\nName: PM2.5, dtype: int64', '')[-4:].replace(' ', '')
            MergedPM25.append(PM25Data)

            PM10Data = str(OneLineData['PM10']).replace('\nName: PM10, dtype: int64', '')[-4:].replace(' ', '')
            MergedPM10.append(PM10Data)

            SO2Data = str(OneLineData['So2']).replace('\nName: So2, dtype: int64', '')[-4:].replace(' ', '')
            MergedSO2.append(SO2Data)

            COData = str(OneLineData['Co']).replace('\nName: Co, dtype: float64', '')[-6:].replace(' ', '')
            MergedCO.append(COData)

            NO2Data = str(OneLineData['No2']).replace('\nName: No2, dtype: int64', '')[-4:].replace(' ', '')
            MergedNO2.append(NO2Data)

            O3 = str(OneLineData['O3']).replace('\nName: O3, dtype: int64', '')[-4:].replace(' ', '')
            MergedO3.append(O3)

    remove_digits = str.maketrans('', '', digits)
    for i in range(0, AllWHWeatherDataRows):
        OneLineData = AllWHWeatherData[i:i + 1]
        # Date = str(OneLineData['日期']).replace('\nName: 日期, dtype: datetime64[ns]', '')[-11: ].replace(' ', '')
        Date = str(OneLineData['日期']).replace('Name: 日期, dtype: object', '')[-11:-1]
        if Date in MergedDate:
            WeatherConditionData = str(OneLineData['天气状况']).translate(remove_digits)
            WeatherConditionData = WeatherConditionData.replace('\nName: 天气状况, dtype: object', '')[-10:].replace(' ',
                                                                                                                 '')
            MergedWeatherCondition.append(WeatherConditionData)

            TemperatureData = str(OneLineData['气温']).replace('\nName: 气温, dtype: object', '')[-10:].replace(' ', '')
            MergedTemperature.append(TemperatureData)

            WindDirectionData = str(OneLineData['风力风向']).replace('\nName: 风力风向, dtype: object', '')[-20:].replace(' ',
                                                                                                                  '')
            while WindDirectionData[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:  # 修正格式
                WindDirectionData = WindDirectionData[1:]

            MergedWindDirection.append(WindDirectionData)

    df1 = pd.DataFrame({'日期': MergedDate})
    df2 = pd.DataFrame({'AQI': MergedAQI})
    df3 = pd.DataFrame({'质量等级': MergedQuaLevel})
    df4 = pd.DataFrame({'PM2.5': MergedPM25})
    df5 = pd.DataFrame({'PM10': MergedPM10})
    df6 = pd.DataFrame({'So2': MergedSO2})
    df7 = pd.DataFrame({'Co': MergedCO})
    df8 = pd.DataFrame({'No2': MergedNO2})
    df9 = pd.DataFrame({'O3': MergedO3})
    df10 = pd.DataFrame({'天气状况': MergedWeatherCondition})
    df11 = pd.DataFrame({'气温': MergedTemperature})
    df12 = pd.DataFrame({'风力风向': MergedWindDirection})

    result = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12], axis=1)
    result.to_excel('武汉合并数据.xlsx', sheet_name='合并数据', startcol=0, index=False)
    return


if __name__ == '__main__':
    AllWHAirQualityData = pd.read_excel(r'武汉质量数据.xlsx')  # 读取空气质量数据
    WHWeatherData = pd.ExcelFile(r'武汉天气数据.xlsx')  # 读取天气数据
    # 因为爬取的时候为了显示好看，将数据按年份分了sheet存储
    # 这里为了合并方便需要先把天气数据合并到一起
    SheetNames = WHWeatherData.sheet_names  # 获取武汉天气爬虫工作区的工作表名称
    AllWHWeatherData = pd.DataFrame()
    for i in SheetNames:
        OneYearData = pd.read_excel('武汉天气数据.xlsx', sheet_name=i)  # 武汉天气爬虫的sheetname
        AllWHWeatherData = pd.concat([AllWHWeatherData, OneYearData])  # 不同sheet数据级联
    Merge(AllWHAirQualityData, AllWHWeatherData)
