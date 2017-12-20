# coding: utf-8


"""命令行火车票查看器

Usage:
    [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
     北京 上海 2016-10-10
     -dg 成都 南京 2016-10-10
"""
from stationsMap import stations
import requests
from docopt import docopt
from ticket_filter import TrainsFilter

trains_list = []


def get_train():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    get_station_url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station)
    station_response = requests.get(get_station_url, headers=headers, verify=False)

    # 获取查询的乘车类别 .join是把后面list里的数据用冒号里的连接起来。返回一个string arguments是一个dic字典
    # key for key, value in arguments.items() if value is True
    # 遍历arguments， 获得里面的key，如果key值是Ture，加在list中
    options = ''.join([key for key, value in arguments.items() if value is True])

    # 获得json结果数据，我们需要其中的result部分。这个可能查询没有结果。用try except套住处理异常
    try:
        available_trains = (station_response.json()['data']['result'])
    except:
        print('查询错误')
    # 查询结果是以 | 来分割的。 split方法获得分割后的list，插入trains中
    for x in available_trains:
        result = x.split('|')
        trains_list.append(result)

    TrainsFilter(trains_list, options).pretty_print()


if __name__ == '__main__':
    get_train()
