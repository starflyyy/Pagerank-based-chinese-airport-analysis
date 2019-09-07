# encoding: utf-8
from prettytable import PrettyTable
import requests
import json
import pymysql
import time
import sqlite3
import random
import telnetlib  # 测试ip是否能用的模块
import re
import csv

global count
global city_cnt
import numpy as np
import random

city_list = ['阿拉善右旗', '安庆', '鞍山',
 '包头', '保山', '北京', '重庆', '昌都', '常德', '常州',
 '成都', '揭阳', '长沙', '长治', '沧源', '达县', '大理',
 '丹东', '敦煌', '芒市', '额济纳旗', '佛山', '福州', '阜阳',
 '赣州', '广元', '广州', '桂林', '哈密', '海口', '海拉尔', '汉中',
 '合肥', '黑河', '呼和浩特', '淮安', '黄山', '佳木斯', '嘉峪关',
 '金门', '锦州', '嘉义', '井冈山', '景德镇', '九江',
 '库车', '库尔勒', '昆明', '拉萨', '黎平', '丽江', '荔波', '临汾',
 '柳州', '洛阳', '梅州', '马祖', '南昌',
 '南京', '南宁', '南通', '宁波', '宁蒗', '攀枝花', '且末', '秦皇岛', '青岛', '庆阳',
 '日照', '三亚', '厦门', '深圳', '神农架', '塔城', '台州', '太原', '扬州',
 '腾冲', '铜仁', '吐鲁番', '万州', '温州',
 '无锡', '梧州', '武夷山', '西安', '锡林浩特',
 '香港', '盐城', '伊春', '宜宾', '宜春', '义乌', '玉树', '运城',
 '张掖', '昭通', '郑州', '中卫', '舟山', '遵义(茅台)', '遵义(新舟)']



city = {'阿尔山': 'YIE', '阿克苏': 'AKU', '阿拉善右旗': 'RHT', '阿拉善左旗': 'AXF', '阿勒泰': 'AAT', '阿里': 'NGQ', '澳门': 'MFM',
        '安庆': 'AQG', '安顺': 'AVA', '鞍山': 'AOG', '巴彦淖尔': 'RLK', '百色': 'AEB', '包头': 'BAV', '保山': 'BSD', '北海': 'BHY',
        '北京': 'BJS', '白城': 'DBC', '白山': 'NBS', '毕节': 'BFJ', '博乐': 'BPL', '重庆': 'CKG', '昌都': 'BPX', '常德': 'CGD',
        '常州': 'CZX', '朝阳': 'CHG', '成都': 'CTU', '池州': 'JUH', '赤峰': 'CIF', '揭阳': 'SWA', '长春': 'CGQ', '长沙': 'CSX',
        '长治': 'CIH', '承德': 'CDE', '沧源': 'CWJ', '达县': 'DAX', '大理': 'DLU', '大连': 'DLC', '大庆': 'DQA', '大同': 'DAT',
        '丹东': 'DDG', '稻城': 'DCY', '东营': 'DOY', '敦煌': 'DNH', '芒市': 'LUM', '额济纳旗': 'EJN', '鄂尔多斯': 'DSN', '恩施': 'ENH',
        '二连浩特': 'ERL', '佛山': 'FUO', '福州': 'FOC', '抚远': 'FYJ', '阜阳': 'FUG', '赣州': 'KOW', '格尔木': 'GOQ', '固原': 'GYU',
        '广元': 'GYS', '广州': 'CAN', '贵阳': 'KWE', '桂林': 'KWL', '哈尔滨': 'HRB', '哈密': 'HMI', '海口': 'HAK', '海拉尔': 'HLD',
        '邯郸': 'HDG', '汉中': 'HZG', '杭州': 'HGH', '合肥': 'HFE', '和田': 'HTN', '黑河': 'HEK', '呼和浩特': 'HET', '淮安': 'HIA',
        '怀化': 'HJJ', '黄山': 'TXN', '惠州': 'HUZ', '鸡西': 'JXA', '济南': 'TNA', '济宁': 'JNG', '加格达奇': 'JGD', '佳木斯': 'JMU',
        '嘉峪关': 'JGN', '金昌': 'JIC', '金门': 'KNH', '锦州': 'JNZ', '嘉义': 'CYI', '西双版纳': 'JHG', '建三江': 'JSJ', '晋江': 'JJN',
        '井冈山': 'JGS', '景德镇': 'JDZ', '九江': 'JIU',  # '九寨沟': 'JZH',
        '喀什': 'KHG', '凯里': 'KJH', '康定': 'KGT', '克拉玛依': 'KRY',
        '库车': 'KCA', '库尔勒': 'KRL', '昆明': 'KMG', '拉萨': 'LXA', '兰州': 'LHW', '黎平': 'HZH', '丽江': 'LJG', '荔波': 'LLB',
        '连云港': 'LYG', '六盘水': 'LPF', '临汾': 'LFQ', '林芝': 'LZY', '临沧': 'LNJ', '临沂': 'LYI', '柳州': 'LZH', '泸州': 'LZO',
        '洛阳': 'LYA', '吕梁': 'LLV', '澜沧': 'JMJ', '龙岩': 'LCX', '满洲里': 'NZH', '梅州': 'MXZ', '绵阳': 'MIG', '漠河': 'OHE',
        '牡丹江': 'MDG', '马祖': 'MFK', '南昌': 'KHN', '南充': 'NAO', '南京': 'NKG', '南宁': 'NNG', '南通': 'NTG', '南阳': 'NNY',
        '宁波': 'NGB', '宁蒗': 'NLH', '攀枝花': 'PZI', '普洱': 'SYM', '齐齐哈尔': 'NDG', '黔江': 'JIQ', '且末': 'IQM', '秦皇岛': 'BPE',
        '青岛': 'TAO', '庆阳': 'IQN', '衢州': 'JUZ', '日喀则': 'RKZ', '日照': 'RIZ', '三亚': 'SYX', '厦门': 'XMN', '上海': 'SHA',
        '深圳': 'SZX', '神农架': 'HPG', '沈阳': 'SHE', '石家庄': 'SJW', '塔城': 'TCG', '台州': 'HYN', '太原': 'TYN', '扬州': 'YTY',
        '唐山': 'TVS', '腾冲': 'TCZ', '天津': 'TSN', '天水': 'THQ', '通辽': 'TGO', '铜仁': 'TEN', '吐鲁番': 'TLQ', '万州': 'WXN',
        '威海': 'WEH', '潍坊': 'WEF', '温州': 'WNZ', '文山': 'WNH', '乌海': 'WUA', '乌兰浩特': 'HLH', '乌鲁木齐': 'URC', '无锡': 'WUX',
        '梧州': 'WUZ', '武汉': 'WUH', '武夷山': 'WUS', '西安': 'SIA', '西昌': 'XIC', '西宁': 'XNN', '锡林浩特': 'XIL', '香格里拉(迪庆)': 'DIG',
        '襄阳': 'XFN', '兴义': 'ACX', '徐州': 'XUZ', '香港': 'HKG', '烟台': 'YNT', '延安': 'ENY', '延吉': 'YNJ', '盐城': 'YNZ',
        '伊春': 'LDS',
        '伊宁': 'YIN', '宜宾': 'YBP', '宜昌': 'YIH', '宜春': 'YIC', '义乌': 'YIW', '银川': 'INC', '永州': 'LLF', '榆林': 'UYN',
        '玉树': 'YUS',
        '运城': 'YCU', '湛江': 'ZHA', '张家界': 'DYG', '张家口': 'ZQZ', '张掖': 'YZY', '昭通': 'ZAT', '郑州': 'CGO', '中卫': 'ZHY',
        '舟山': 'HSN',
        '珠海': 'ZUH', '遵义(茅台)': 'WMT', '遵义(新舟)': 'ZYI'}


def get_ip():
    ip_list = []
    port_list = []
    conn = sqlite3.connect(r"C:\Users\12592\Documents\GitHub\IP\IPProxyPool\data\proxy.db")
    cur = conn.cursor()
    cur.execute("""
    select ip from proxys;
    """)
    cursor = cur.fetchall()
    for row in cursor:
        ip_list.append(row[0])

    cur.execute("""
    select port from proxys;
    """)
    port = cur.fetchall()
    for row in port:
        port_list.append(row[0])
    # 提交修改
    conn.commit()

    # 关闭数据库连接
    conn.close()
    l = len(ip_list)
    i = random.randint(0, l - 1)
    try:
        telnetlib.Telnet(ip_list[i], port='%s' % port_list[i], timeout=5)
    except:
        ip = get_ip()
    else:
        ip = ip_list[i]
    return ip


def table_exists(con, table_name):  # 这个函数用来判断表是否存在

    sql = "show tables;"
    con.execute(sql)

    tables = [con.fetchall()]

    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:

        return 1  # 存在返回1

    else:

        return 0  # 不存在返回0


def xiecheng(dcity, acity, date, string):
    date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'Referer': 'http://flights.ctrip.com/itinerary/oneway/szx-hak?date=2019-05-20',  # 5-20
        "Content-Type": "application/json",  # 声明文本类型为 json 格式,
        # 'Cookie':'DomesticUserHostCity: BJS|%b1%b1%be%a9'
    }
    # ip = get_ip()
    # print (ip)
    # proxies = {'http': 'http://61.163.247.10' }
    url = 'http://flights.ctrip.com/itinerary/api/12808/products'
    request_payload = {"flightWay": "Oneway",
                       "classType": "ALL",
                       "hasChild": 'false',
                       "hasBaby": 'false',
                       "searchIndex": 1,
                       "portingToken": "3fec6a5a249a44faba1f245e61e2af88",
                       "airportParams": [
                           {"dcity": city.get(dcity), "acity": city.get(acity), "dcityname": dcity, "acityname": acity,
                            "date": date}]}
    # 这里传进去的参数必须为 json 格式
    Flag = False
    while not Flag:
        try:
            response = requests.post(url, data=json.dumps(request_payload), headers=headers).text
        except:
            print("网络请求失败")
            time.sleep(5)
        else:
            try:
                msg = json.loads(response).get('msg')
            except:
                print("json读取错误1")
                return
            else:
                if (msg != 'success'):
                    print("当前页面被封了")
                    time.sleep(60)
                    return
            try:
                routeList = json.loads(response).get('data').get('routeList')
            except:
                print("json读取错误2")
                return
            else:
                Flag = True
    table = PrettyTable(["Airline", "FlightNumber", "DepartureDate", 'ArrivalDate', 'PunctualityRate', 'LowestPrice', 'CraftTypeName', 'CraftTypeKindDisplayName'])
    print (response)
    # 如果没有直达飞机，直接返回不进行计算
    print("%s->%s " % (dcity, acity))
    if (routeList == None):
        print("无相关信息")
    else:
        print(routeList[0].get('routeType'))
        if (routeList[0].get('routeType') == 'Transit' or routeList[0].get('routeType') == 'FlightTrain'):
            print("非直达1")
    # if (table_exists(cursor, string) == 1):
    # print ("impossible error")
    # 使用预处理语句创建表
    sql = """CREATE TABLE %s(
             ID_NUM INT UNSIGNED AUTO_INCREMENT,
             Airline  VARCHAR(20) NOT NULL,
             FlightNumber  VARCHAR(20) NOT NULL,
             DepartureDate VARCHAR(20) NOT NULL,  
             ArrivalDate VARCHAR(20) NOT NULL,
             PuntualityRate VARCHAR(20) NOT NULL,
             LowestCost INT NOT NULL, 
             CraftTypeName VARCHAR(20) NOT NULL,
             CraftTypeKindDisplayName VARCHAR(20) NOT NULL,
             PRIMARY KEY(ID_NUM))""" % string

    cursor.execute(sql)
    if (routeList == None):
        return
        
    for route in routeList:
        if len(route.get('legs')) == 1:
            info = {}
            legs = route.get('legs')[0]
            flight = legs.get('flight')
            info['Airline'] = flight.get('airlineName')
            info['FlightNumber'] = flight.get('flightNumber')
            info['DepartureDate'] = flight.get('departureDate')[-8:-3]
            info['ArrivalDate'] = flight.get('arrivalDate')[-8:-3]
            info['PunctualityRate'] = flight.get('punctualityRate')
            info['LowestPrice'] = legs.get('characteristic').get('lowestPrice')
            info['CraftTypeName'] = flight.get('craftTypeName')
            info['CraftTypeKindDisplayName'] = flight.get('craftTypeKindDisplayName')
            table.add_row(info.values())
            # SQL 插入语句
            # SQL 插入语句
            sql = "INSERT INTO %s(Airline, \
                   FlightNumber, DepartureDate, ArrivalDate, PuntualityRate, LowestCost, CraftTypeName, CraftTypeKindDisplayName) \
                   VALUES ('%s', '%s',  '%s',  '%s', '%s', %s, '%s', '%s')" % \
                  (string, info['Airline'], info['FlightNumber'], info['DepartureDate'], info['ArrivalDate'],
                   info['PunctualityRate'], info['LowestPrice'], info['CraftTypeName'], info['CraftTypeKindDisplayName'])
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 执行sql语句
                db.commit()
            except:
                # 发生错误时回滚
                db.rollback()

    print(table)


if __name__ == "__main__":
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "Huzi19980614", "test")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    finished_citys = []
    csv_file = csv.reader(open('finished_citys.csv', 'r'))
    for stu in csv_file:
        finished_citys.append(stu[0])
    print(finished_citys)
    global city_cnt
    city_cnt = 0

    city_list = city_list[0:31]
    for c1 in city_list:
        if (c1 in finished_citys):
            continue
        for c2 in city.keys():
            string = str(city[c1] + city[c2])
            string = string.lower()
            if (c1 == c2):
                continue
            elif (table_exists(cursor, string) == 1):  # 表在数据库中,不用再进行更新了
                print("%s->%s没有更新" % (c1, c2))
                continue
            else:
                dcity = c1
                acity = c2
                date = "20190530"
                xiecheng(dcity, acity, date, string)
                time.sleep(5)
        finished_citys.append(c1)
        print("finished_citys:", finished_citys)
        city_cnt = city_cnt + 1
        # 每新增两个城市写入一次
        if (city_cnt == 1):
            city_cnt = 0
            # 将finished_citys写入
            out = open('finished_citys.csv', 'w+', newline='')
            # 设定写入模式
            csv_write = csv.writer(out, dialect='excel')
            for cityone in finished_citys:
                stu = [cityone]
                # 写入具体内容
                csv_write.writerow(stu)
            out.close()
            print('write over')


    db.close()

