# -*- coding: utf-8 -*-
# @Time    : 2022/5/14 13:55
# @Author  : 自动化2005陈富昌0122004950804
# @Site    :
# @File    : Prediction.py
# @Software: PyCharm
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt


# 天气状况编码
def EncodeWeatherCondition(StringData):
    flag = 0
    if StringData == '晴':
        flag = 1
    elif StringData == '多云':
        flag = 2
    elif StringData == '阴':
        flag = 3
    elif '雨' in StringData:
        flag = 4
    elif '雪' in StringData and StringData != '雨夹雪':
        flag = 5
    elif '雾' in StringData or '霾' in StringData:
        flag = 6
    elif StringData == '扬沙':
        flag = 7
    return flag


def EncodeAirQualityLevel(StringData):
    # 空气质量情况编码
    flag = 0
    if StringData == '优':
        flag = 1
    elif StringData == '良':
        flag = 2
    elif StringData == '轻度污染':
        flag = 3
    elif StringData == '中度污染':
        flag = 4
    elif StringData == '重度污染':
        flag = 5
    elif StringData == '严重污染':
        flag = 6
    elif StringData == '无':
        flag = 2
    return flag

    # 某一天的所需数据提取


def ExtractNeededData(i, WHMergedData_Dict):
    OneDayData = []
    OneDayData.append(WHMergedData_Dict[i]['AQI'])
    OneDayData.append(WHMergedData_Dict[i]['PM2.5'])
    OneDayData.append(WHMergedData_Dict[i]['PM10'])
    OneDayData.append(WHMergedData_Dict[i]['So2'])
    OneDayData.append(WHMergedData_Dict[i]['Co'])
    OneDayData.append(WHMergedData_Dict[i]['No2'])
    OneDayData.append(WHMergedData_Dict[i]['O3'])

    DayNight = WHMergedData_Dict[i]['天气状况'].split('/')  # 将白天晚上的天气状况数据分开
    DayCoder = EncodeWeatherCondition(DayNight[0])
    NightCoder = EncodeWeatherCondition(DayNight[1])  # 天气状况中文用数字来分类编码
    #  晴：1，多云：2，阴：3，雨：4，雪：5，雾霾：6，扬沙：7
    OneDayData.append(DayCoder)
    OneDayData.append(NightCoder)
    return OneDayData


# 当天+前两天数据编码放入一个list
def EncodeData(WHMergedData):
    EncodedList = []
    WHMergedData_Dict = WHMergedData.to_dict('records')  # dataframe转化为dict数据
    DayLength = len(WHMergedData_Dict)  # 一共多少天的数据
    for i in range(0, DayLength):
        if i >= 2:
            TheDayData = ExtractNeededData(i, WHMergedData_Dict)  # 当天数据
            #  预测某一天等级的全部数据，包括当天及前两天的空气数据和天气状况
            Last1DayData = ExtractNeededData(i - 1, WHMergedData_Dict)  # 前一天数据
            Last2DayData = ExtractNeededData(i - 2, WHMergedData_Dict)  # 前二天数据
            PredictOneDayData = TheDayData + Last1DayData + Last2DayData

            QuaLevFlag = EncodeAirQualityLevel(WHMergedData_Dict[i]['质量等级'])
            # 分类编码，共6种类别
            # 优：1，良：2，轻度污染：3，中度污染：4，重度污染：5.严重污染：6，无：2
            PredictOneDayData.append(QuaLevFlag)  # 最后放入y，即标签值
            EncodedList.append(PredictOneDayData)
    return EncodedList

    # 测试获得的结果不是整数，执行向下取整处理，
    # 得到分类1、2、3、4、5、6


def y_testToInteger(y_test):
    y_test_to_integer = []
    for y in y_test:
        if y < 1.5:
            y_test_to_integer.append(1)
        elif y < 2.5:
            y_test_to_integer.append(2)
        elif y < 3.5:
            y_test_to_integer.append(3)
        elif y < 4.5:
            y_test_to_integer.append(4)
        elif y < 5.5:
            y_test_to_integer.append(5)
        else:
            y_test_to_integer.append(6)
    return y_test_to_integer


def LinearRegPre(EncodedList):  # 线性回归
    Data = np.array(EncodedList)
    X = Data[:, :-1]  # 某一天的除最后一位为预测值
    Y = Data[:, -1]  # 最后一位数为标签值
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=1)  # 训练数据、测试数据7：3划分

    # 线性回归训练
    regr = linear_model.LinearRegression()
    regr.fit(X_train, Y_train)
    print('coefficients(w1,w2...):', regr.coef_)  # 系数
    print('intercept(b):', regr.intercept_)  # 截距

    # 预测，获得的标签整数化，向下取整
    y_test = regr.predict(X_test)
    y_test_to_integer = y_testToInteger(y_test)  # 测试获得的结果不是整数，执行向下取整处理，
    print('Linear训练结束！')
    print('多元线性回归结果：')
    print('准确率：', metrics.accuracy_score(Y_test, y_test_to_integer))
    print('精确率：', metrics.precision_score(Y_test, y_test_to_integer, average='weighted'))
    print('召回率：', metrics.recall_score(Y_test, y_test_to_integer, average='weighted'))
    # weighted’: 为每个标签计算指标，并通过各类占比找到
    # 它们的加权均值（每个标签的正例数）.它解决了’macro’的标签不平衡问题；
    print('Linear预测结束！')
    return


def SVMPre(EncodedList):  # 支持向量机
    Data = np.array(EncodedList)
    X = Data[:, :-1]
    Y = Data[:, -1]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=1)
    # 训练数据、测试数据7：3划分

    # 构建SVM模型，并确定最优超参数
    svc = SVC()
    param = {'kernel': ['linear', 'poly', 'rbf'], 'C': np.linspace(0.01, 1, 10), 'gamma': np.linspace(0.01, 1, 11)}
    gs = GridSearchCV(svc, param, cv=5, n_jobs=-1, scoring='neg_mean_absolute_error')
    gs.fit(X_train, Y_train)  # 训练并获得最优超参数

    # 使用最优超参数确定的模型预测
    # 获得的标签整数化，向下取整
    y_test = gs.predict(X_test)
    y_test_to_integer = y_testToInteger(y_test)
    print('SVM训练结束！')
    print('支持向量机结果：')
    print('最优超参数：', gs.best_params_)  # 输出最优超参数
    print('准确率：', metrics.accuracy_score(Y_test, y_test_to_integer))
    print('精确率：', metrics.precision_score(Y_test, y_test_to_integer, average='weighted'))
    print('召回率：', metrics.recall_score(Y_test, y_test_to_integer, average='weighted'))
    # weighted’: 为每个标签计算指标，并通过各类占比找到
    # 它们的加权均值（每个标签的正例数）.它解决了’macro’的标签不平衡问题；
    print('SVM预测结束！')
    return


if __name__ == '__main__':
    WHMergedData = pd.read_excel(r'武汉合并数据.xlsx')  # 读取武汉合并数据,得到DataFrame
    EncodedList = EncodeData(WHMergedData)  # 当天+前两天数据编码放入一个list
    LinearRegPre(EncodedList)  # 多元线性回归预测
    SVMPre(EncodedList)  # 支持向量机分类预测

