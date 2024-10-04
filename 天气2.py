import pandas as pd
import requests
import time
import base64
from lxml import etree
from openpyxl import Workbook
url = "http://127.0.0.1:5000/city_weather?city="
citys = ['青岛', '开封', '苏州', '扬州', '烟台', '丽江','桂林', '三亚', '厦门','大理']
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Referer': 'http://127.0.0.1:5000/',
    'Cookie': 'salt="\302\210D\303\2609\302\221\007\302\230\302\211f9\303\254J:U\027\303\205V\302\276\302\213\303\257\303\227\303\230\303\223\303\246\302\230*4"'
}
# t = str(int(time.time() * 1000))
# print(t)
# t64 = base64.b64encode(t.encode('utf8')).decode('utf8')
# url2 = url+citys[0]+"&page="+str(1)+"&TOKEN="+t64
# res = requests.get(url=url2, headers=headers)
# print(res.text)
# html_ds = res.content  # .decode('utf-8')
# print(html_ds)
# html_ds = etree.HTML(html_ds)
# parts = html_ds.xpath('//li')
# l = xp(parts)
# print(l)
def get_bs64():
    t = str(int(time.time() * 1000))
    t64 = base64.b64encode(t.encode('utf8')).decode('utf8')
    return t64
def get_xp(parts):
    avg_high = str(parts[0].xpath('.//text()')[1])
    avg_low = str(parts[0].xpath('.//text()')[3])
    ex_high = str(parts[1].xpath('.//text()')[0])
    ex_low = str(parts[2].xpath('.//text()')[0])
    quality_air = str(parts[3].xpath('.//text()')[0])
    good_air = str(parts[4].xpath('.//text()')[0])
    good_air_date = str(parts[4].xpath('.//text()')[1])
    bad_air = str(parts[5].xpath('.//text()')[0])
    bad_air_date = str(parts[5].xpath('.//text()')[1])
    return [avg_high,avg_low,ex_high,ex_low,quality_air,good_air,good_air_date,bad_air,bad_air_date]
for city in citys:
    wb = Workbook()
    ws = wb.active
    h = ['城市', '月份', '平均高温', '平均低温', '极端高温', '极端低温', '平均空气质量指数', '空气最好', '空气最好日期', '空气最差', '空气最差日期']
    ws.append(h)
    for month in range(1,13):
        one_line = [city,month]
        # one_line.append(city)
        # one_line.append(month)
        # res = None
        # while True:
        #     print(res.status_code)
        #     if res.status_code == 200 :
        #         break
        #     elif res.status_code == 429:
        #         t = res.headers.get('Retry-After')
        #         print(t)
        #         time.sleep(t)
        url2 = url + city + "&page=" + str(month) + "&TOKEN=" + get_bs64()
        res = requests.get(url=url2, headers=headers)
        html_ds = etree.HTML(res.content)
        time.sleep(0.5)
        html_parts = html_ds.xpath('//li')
        back = get_xp(html_parts)
        one_line.extend(back)#使用 one_line.extend(back)，这种方法直接在 one_line 的原始列表上进行操作，不会创建新的列表对象
        print(one_line)
        ws.append(one_line)
    time.sleep(10)
    wb.save(city + "_month.csv")
