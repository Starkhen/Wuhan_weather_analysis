# WuHanClimateDataAnalysis
爬虫爬取武汉天气数据，pandas和numpy处理数据，matplot可视化展示数据，sklearn机器学习方法预测空气状况。


ReadWHWeather.py
从 http://www.tianqihoubao.com/lishi/beijing.html 网站上通过爬虫把武汉2011年-至今的天气数据爬下来，并保存为 武汉天气爬虫.xlsx。并且在 武汉天气爬虫.xlsx的基础上进行去重操作报错数据为 武汉天气数据.xlsx。

ReadWHaqi.py
从 http://www.tianqihoubao.com/aqi/wuhan-xxxx.html 网站上爬虫把武汉能查询到的最前的空气质量数据-至今的天气数据爬下来，并保存为 武汉空气质量爬虫.xlsx。并且在 武汉空气质量爬虫.xlsx的基础上进行去重操作报错数据为 武汉空气质量数据.xlsx。


MergeTwoExcel.py
读入武汉空气质量数据（武汉空气质量数据.xlsx），并把该数据和第1步中得到的武汉天气数据进行融合，得到一个同时包含天气和空气质量的表格数据，保存为 武汉合并数据.xlsx


WeatherPie.py
对2011-2022年的每一年，统计这一年中白天为晴、雨、多云、阴、雪、雾霾、扬沙的天数，并绘制成饼图.


ContinuePollution.py
对2014-2021年的每一年，统计这一年中持续1天污染的次数、持续2天污染的次数、持续3天污染的次数、持续4天污染的次数和持续5天及以上有污染的次数，把所有年份的统计结果绘制成一幅柱状图.


Prediction.py
在武汉历史天气和空气质量数据的基础上，根据当天的天气情况以及前两天的天气及空气质量情况，预测当天的空气质量等级，比较线性预测以及SVM两种算法，从中选出较优的算法并确定最优超参数.
