import pandas as pd
import requests
import time
import base64
from lxml import etree
from openpyxl import Workbook

url = "http://127.0.0.1:5000/city_weather?city="
citys = ['青岛', '开封', '苏州', '扬州', '烟台', '丽江', '桂林', '三亚', '厦门', '大理']
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Referer': 'http://127.0.0.1:5000/',
    'Cookie': 'salt="\302\210D\303\2609\302\221\007\302\230\302\211f9\303\254J:U\027\303\205V\302\276\302\213\303\257\303\227\303\230\303\223\303\246\302\230*4"'
}
def get_bs64():
    t = str(int(time.time() * 1000))
    t64 = base64.b64encode(t.encode('utf8')).decode('utf8')
    return t64

def get_xp(parts):
    data = str(parts[0].xpath('.//text()'))
    high = str(parts[1].xpath('.//text()'))
    low = str(parts[2].xpath('.//text()'))
    weather = str(parts[3].xpath('.//text()'))
    trend = str(parts[4].xpath('.//text()'))
    return [data, high, low, weather, trend]
for city in citys:
    wb = Workbook()
    ws = wb.active
    h = ['城市', '日期', '最高气温', '最低气温', '天气', '风向']
    ws.append(h)

    for month in range(1, 13):
        one_line = [city]


        url2 = url + city + "&page=" + str(month) + "&TOKEN=" + get_bs64()
        res = requests.get(url=url2, headers=headers)
        html_ds = etree.HTML(res.content)
        time.sleep(2)

        html_parts = html_ds.xpath('//tr/td')
        back = get_xp(html_parts)
        one_line.extend(back)#使用 one_line.extend(back)，这种方法直接在 one_line 的原始列表上进行操作，不会创建新的列表对象
        print(one_line)
        ws.append(one_line)
    # time.sleep(10)
    wb.save(city + "_day.csv")
    #     for f in weather_f[1:]:
    #         weather_l = []
    #         data = f.xpath('.//text()')
    #         weather_l.append(city)
    #         weather_l.append(data[0])
    #         weather_l.append(data[1])
    #         weather_l.append(data[2])
    #         weather_l.append(data[3])
    #         weather_l.append(data[4])
    #         weather_list.append(weather_l)
    #         ws.append(weather_l)
    #
    # wb.save(c + "_day.csv")
    # df = pd.DataFrame(weather_list)
    # df.columns = h
    # print(df)

