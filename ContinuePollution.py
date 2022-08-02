# -*- coding: utf-8 -*-
# @Time    : 2022/5/14 14:14
# @Author  : 自动化2005陈富昌0122004950804
# @Site    :
# @File    : ContinuePollution.py
# @Software: PyCharm
import pandas as pd
import matplotlib.pyplot as plt


## 按年份把污染情况数据提取出来,因为2013和2022数据不完整，所以不需要
def SplitToOneYear(WHAirData):
    WHAirData_Dict = WHAirData.to_dict('records')  # dataframe转化为dict数据
    YearAirData = {}
    for i in range(2014, 2022):  # 14-21年数据Dict，年份为key
        YearAirData[str(i)] = []  # 不同index的存放不同year的数据

    # 按年份提取每一天的质量等级
    for OneDay in WHAirData_Dict:
        Year = OneDay['日期'].split('-')[0].replace('\ufeff', '', 1)  # 把年份单独取出来， 便于按照年份分割，‘\ufeff’是数据中的一个乱码
        if Year != '2013' and Year != '2022':  # 因为2013和2022数据不完整，所以不需要
            YearAirData[Year].append(OneDay['质量等级'])
    return YearAirData


def SplitToOneYear1(WHAirData):
    WHAirData_Dict = WHAirData.to_dict('records')  # dataframe转化为dict数据
    YearAirData = {}
    for i in range(2014, 2022):  # 14-21年数据Dict，年份为key
        YearAirData[str(i)] = []  # 不同index的存放不同year的数据

    # 按年份提取每一天的质量等级
    for OneDay in WHAirData_Dict:
        Year = OneDay['日期'].split('-')[0].replace('\ufeff', '', 1)  # 把年份单独取出来， 便于按照年份分割，‘\ufeff’是数据中的一个乱码
        if Year != '2013' and Year != '2022':  # 因为2013和2022数据不完整，所以不需要
            YearAirData[Year].append(OneDay['质量等级'])
    return YearAirData


# 统计污染情况
def PolluDaysStatistic(YearAirData):
    AllYearStatistic = []
    for OneYearData in YearAirData:
        DaysNum = len(YearAirData[OneYearData])
        OneYearStatistic = {'连续一天': 0, '连续两天': 0, '连续三天': 0,
                            '连续四天': 0, '连续五天及以上': 0}
        #  [1]	该年的第一天：当前天有污染，之后一天无污染；
        #  [2]	该年最后一天：当前天有污染，前面一天无污染；
        #  [3]	该年中间：当前天有污染，前面一天无污染，之后一天无污染。
        # -------------------------------------连续一天------------------------------------------
        for i in range(0, DaysNum):
            if i == 0 and ('污染' in YearAirData[OneYearData][i]) and \
                    ('污染' not in YearAirData[OneYearData][i + 1]):
                OneYearStatistic['连续一天'] += 1
            elif i == DaysNum - 1 and ('污染' in YearAirData[OneYearData][i]) and \
                    ('污染' not in YearAirData[OneYearData][i - 1]):
                OneYearStatistic['连续一天'] += 1
            elif ('污染' in YearAirData[OneYearData][i]) and \
                    ('污染' not in YearAirData[OneYearData][i - 1]) and \
                    ('污染' not in YearAirData[OneYearData][i + 1]):
                OneYearStatistic['连续一天'] += 1
            #  [1]	非该年的最后一天：当前天有污染，前一天有污染，前二天无污染，后一天无污染；
            #  [2]	该年的最后一天：当前天有污染，前一天有污染，前二天无污染。
            # -------------------------------------连续两天------------------------------------------
            elif i == DaysNum - 1 and ('污染' in YearAirData[OneYearData][i]) and \
                    ('污染' in YearAirData[OneYearData][i - 1]) and \
                    ('污染' not in YearAirData[OneYearData][i - 2]):
                OneYearStatistic['连续两天'] += 1
            elif i >= 1 and ('污染' in YearAirData[OneYearData][i]) and \
                    ('污染' in YearAirData[OneYearData][i - 1]) and \
                    ('污染' not in YearAirData[OneYearData][i - 2]) and \
                    ('污染' not in YearAirData[OneYearData][i + 1]):
                OneYearStatistic['连续两天'] += 1
            #  [1]  非该年的最后一天：当前天有污染，前一天有污染，前二天有污染，前三天无污染，后一天无污染；
            #  [2]  该年的最后一天：当前天有污染，前一天有污染，前二天有污染，前三天无污染。
            # -------------------------------------连续三天------------------------------------------
            elif i == DaysNum - 1 and ('污染' in YearAirData[OneYearData][i]) and \
                    ('污染' in YearAirData[OneYearData][i - 1]) and \
                    ('污染' in YearAirData[OneYearData][i - 2]) and \
                    ('污染' not in YearAirData[OneYearData][i - 3]):
                OneYearStatistic['连续三天'] += 1
            elif i >= 2 and ('污染' in YearAirData[OneYearData][i]) and \
                    ('污染' in YearAirData[OneYearData][i - 1]) and \
                    ('污染' in YearAirData[OneYearData][i - 2]) and \
                    ('污染' not in YearAirData[OneYearData][i - 3]) and \
                    ('污染' not in YearAirData[OneYearData][i + 1]):
                OneYearStatistic['连续三天'] += 1
            #  [1]	非该年的最后一天：当前天有污染，前一天有污染，前二天有污染，前三天有污染，前四天无污染，后一天无污染；
            #  [2]	该年的最后一天：当前天有污染，前一天有污染，前二天有污染，前三天有污染，前四天无污染。
            # -------------------------------------连续四天------------------------------------------
            elif i == DaysNum - 1 and ('污染' in YearAirData[OneYearData][i]) and \
                    ('污染' in YearAirData[OneYearData][i - 1]) and \
                    ('污染' in YearAirData[OneYearData][i - 2]) and \
                    ('污染' in YearAirData[OneYearData][i - 3]) and \
                    ('污染' not in YearAirData[OneYearData][i - 4]):
                OneYearStatistic['连续四天'] += 1
            elif i >= 3 and ('污染' in YearAirData[OneYearData][i]) and \
                    ('污染' in YearAirData[OneYearData][i - 1]) and \
                    ('污染' in YearAirData[OneYearData][i - 2]) and \
                    ('污染' in YearAirData[OneYearData][i - 3]) and \
                    ('污染' not in YearAirData[OneYearData][i - 4]) and \
                    ('污染' not in YearAirData[OneYearData][i + 1]):
                OneYearStatistic['连续四天'] += 1
            #  [1]	非该年的最后一天：当前天有污染，前一天有污染，前二天有污染，前三天有污染，前四天有污染，后一天无污染；
            #  [2]	该年的最后一天：当前天有污染，前一天有污染，前二天有污染，前三天有污染，前四天有污染。
            # -------------------------------------连续五天及以上------------------------------------------
            elif i == DaysNum - 1 and ('污染' in YearAirData[OneYearData][i]) and \
                    ('污染' in YearAirData[OneYearData][i - 1]) and \
                    ('污染' in YearAirData[OneYearData][i - 2]) and \
                    ('污染' in YearAirData[OneYearData][i - 3]) and \
                    ('污染' in YearAirData[OneYearData][i - 4]):
                OneYearStatistic['连续五天及以上'] += 1
            elif i >= 4 and ('污染' in YearAirData[OneYearData][i]) and \
                    ('污染' in YearAirData[OneYearData][i - 1]) and \
                    ('污染' in YearAirData[OneYearData][i - 2]) and \
                    ('污染' in YearAirData[OneYearData][i - 3]) and \
                    ('污染' in YearAirData[OneYearData][i - 4]) and \
                    ('污染' not in YearAirData[OneYearData][i + 1]):
                OneYearStatistic['连续五天及以上'] += 1

        AllYearStatistic.append(OneYearStatistic)
    return AllYearStatistic
def PolluDaysStatistic1(YearAirData):
    AllYearStatistic = []
    for OneYearData in YearAirData:
        OneYearStatistic = {'优': 0, '良': 0, '轻度污染': 0,
                            '中度污染': 0, '重度污染': 0, '严重污染': 0}
        for quality in YearAirData[OneYearData]:
            if quality == '优':
                OneYearStatistic['优'] += 1
            elif quality == '良':
                OneYearStatistic['良']+=1
            elif quality == '轻度污染':
                OneYearStatistic['轻度污染']+=1
            elif quality == '中度污染':
                OneYearStatistic['中度污染']+=1
            elif quality == '重度污染':
                OneYearStatistic['重度污染']+=1
            elif quality == '严重污染':
                OneYearStatistic['严重污染']+=1
        AllYearStatistic.append(OneYearStatistic)

    return AllYearStatistic



# 绘制柱状图
def DrawConPollution(AllYearStatistic):
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    for OneYearData in AllYearStatistic:
        y1.append(OneYearData['连续一天'])
        y2.append(OneYearData['连续两天'])
        y3.append(OneYearData['连续三天'])
        y4.append(OneYearData['连续四天'])
        y5.append(OneYearData['连续五天及以上'])
    width = 0.16  # 设置柱与柱之间的宽度

    x1 = range(len(y1))  # 横坐标
    x2 = [i + width for i in x1]
    x3 = [i + width for i in x2]
    x4 = [i + width for i in x3]
    x5 = [i + width for i in x4]
    # Bar的属性
    Bar1 = plt.bar(x1, y1, width=0.16, alpha=0.9, color='purple')
    Bar2 = plt.bar(x2, y2, width=0.16, alpha=0.9, color='red')
    Bar3 = plt.bar(x3, y3, width=0.16, alpha=0.9, color='blue')
    Bar4 = plt.bar(x4, y4, width=0.16, alpha=0.9, color='green')
    Bar5 = plt.bar(x5, y5, width=0.16, alpha=0.9, color='yellow')

    Year = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']#需要的年份
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xticks([i + 2 * width for i in x1], Year)
    plt.yticks([0, 5, 10, 15, 20, 25])
    plt.legend(['连续一天', '连续两天', '连续三天', '连续四天', '连续五天及以上'],
               loc="upper left")
    plt.title('持续污染天数按年份统计情况')

    # 下面对所有柱子进行数字标注
    for rect in Bar1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=12, ha='center', va='bottom')
    for rect in Bar2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=12, ha='center', va='bottom')
    for rect in Bar3:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=12, ha='center', va='bottom')
    for rect in Bar4:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=12, ha='center', va='bottom')
    for rect in Bar5:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=12, ha='center', va='bottom')
    plt.savefig('./ContinuePollution.jpg')
    plt.show()
    return

#折线图
def DrawConPollution1(AllYearStatistic):
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    y6 = []
    for OneYearData in AllYearStatistic:
        y1.append(OneYearData['优'])
        y2.append(OneYearData['良'])
        y3.append(OneYearData['轻度污染'])
        y4.append(OneYearData['中度污染'])
        y5.append(OneYearData['重度污染'])
        y6.append(OneYearData['严重污染'])
    Year = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']  # 需要的年份
    plt.figure('broken_line')

    ax = plt.subplot(2, 3, 1)  # 选中子区域
    plt.plot(Year,y1,label='Frist line',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=5)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xticks(Year,size=7)
    plt.yticks([ 25, 50, 75, 100, 125,150,175])
    ax.set_title('优的天数按年份统计情况',fontsize=7)

    ax = plt.subplot(2, 3, 2)  # 选中子区域
    plt.plot(Year,y2,label='Frist line',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=5)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xticks(Year,size=7)
    plt.yticks([  160, 170, 180, 190,200,210,220],size=8)
    ax.set_title('良的天数按年份统计情况',fontsize=7)

    ax = plt.subplot(2, 3, 3)  # 选中子区域
    plt.plot(Year, y3, label='Frist line', linewidth=3, color='r', marker='o', markerfacecolor='blue', markersize=5)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xticks(Year,size=7)
    plt.yticks([ 20, 40, 60, 80, 100,120])
    ax.set_title('轻度污染的天数按年份统计情况',fontsize=7)

    ax = plt.subplot(2, 3, 4)  # 选中子区域
    plt.plot(Year,y4,label='Frist line',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=5)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xticks(Year,size=7)
    plt.yticks([ 5, 10, 15, 20, 25,30,35,40])
    ax.set_title('中度污染的天数按年份统计情况',fontsize=7)

    ax = plt.subplot(2, 3, 5)  # 选中子区域
    plt.plot(Year,y5,label='Frist line',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=5)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xticks(Year,size=7)
    plt.yticks([ 5,10,15,20,25])
    ax.set_title('重度污染的天数按年份统计情况',fontsize=7)

    ax = plt.subplot(2, 3, 6)  # 选中子区域
    plt.plot(Year,y6,label='Frist line',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=5)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xticks(Year,size=7)
    plt.yticks([ 5,10,15,20,25])
    ax.set_title('严重污染的天数按年份统计情况',fontsize=7)

    plt.savefig('./ContinuePollution1.jpg')
    plt.show()





if __name__ == '__main__':
    WHAirData = pd.read_excel(r'武汉合并数据.xlsx')  # 读取武汉合并数据,得到DataFrame
    YearAirData = SplitToOneYear(WHAirData)  # 按年份把污染情况数据提取出来,因为2013和2022数据不完整，所以不需要
    AllYearStatistic = PolluDaysStatistic(YearAirData)  # 统计污染情况
    DrawConPollution(AllYearStatistic)  # 绘制柱状图
    YearAirData1 = SplitToOneYear1(WHAirData)# 按年份把空气质量数据提取出来,因为2013和2022数据不完整，所以不需要
    AllYearStatistic1 = PolluDaysStatistic1(YearAirData1)# 统计空气质量情况
    DrawConPollution1(AllYearStatistic1)# 绘制折线图


