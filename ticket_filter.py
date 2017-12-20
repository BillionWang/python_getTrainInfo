from prettytable import PrettyTable
from stationsMap import stations
from colorama import init, Fore

''' 12306 一个火车数据 每个item对应的内容
a[1] = 预定
a[3] = 车次
a[8] = 始发时间
a[9] = 到达时间
a[10] = 历时
a[14] = 火车是否排期。如果这个位置是3 有车 如果是空。无发车时间
a[21] = 高级软卧
a[23] = 软卧
a[22] = 其他
a[26]= 无座
a[27]=软座
a[28] = 硬卧
a[29] = 硬座
a[30] = 二等座
a[31] = 一等座
a[32] = 特等座
a[33]= 动卧
'''


class TrainsFilter:
    def __init__(self, available_trains, options):
        """查询到的火车班次集合

                :param available_trains: 一个列表, 包含可获得的火车班次, 每个火车班次是一个list
                :param options: 查询的选项, 如高铁, 动车, etc... gdzk什么的
                """
        self.available_trains = available_trains
        self.options = options
        # 这个是表头
        self.header = ('车次 车站 时间 历时 特等座 一等 二等 高级软卧 软卧 动卧 硬卧 '
                       + '软座 硬座 无座 其他 备注').split()

    # zip函数把两个list组合成一个tuple list - > zip([1,2,3],[4,5,6]) = [(1,4),(2,5),(3,6)]
    # 这里用zip(stations.value(),stations.keys()) 目的是翻转原始dic
    stations_re = dict(zip(stations.values(), stations.keys()))

    # 时间做一下转换
    @staticmethod
    def get_duration(raw_train):
        duration = raw_train.replace(':', '小时') + '分钟'
        return duration

    def generate_train(self, initial_train):
        train_no = initial_train[3]
        begin_station = self.stations_re.get(initial_train[4])
        end_station = self.stations_re.get(initial_train[5])
        from_station = self.stations_re.get(initial_train[6])
        to_station = self.stations_re.get(initial_train[7])
        # 判断是否始发和终到站
        begin_flag = self.__check_equals(begin_station, from_station, True)
        end_flag = self.__check_equals(end_station, to_station, False)
        train = [
            train_no,
            '\n'.join([begin_flag + ' ' + self.__get_color(Fore.GREEN, from_station),
                       end_flag + ' ' + self.__get_color(Fore.RED, to_station)]),
            '\n'.join([self.__get_color(Fore.GREEN, initial_train[8]),
                       self.__get_color(Fore.RED, initial_train[9])]),

            self.get_duration(initial_train[10]),

            # 特等座
            self.__show_color(initial_train[32]),
            # 一等
            self.__show_color(initial_train[31]),
            # 二等
            self.__show_color(initial_train[30]),
            # 高级软卧
            self.__show_color(initial_train[31]),
            # 软卧
            self.__show_color(initial_train[23]),
            # 动卧
            self.__show_color(initial_train[33]),
            # 硬卧
            self.__show_color(initial_train[28]),
            # 软座
            self.__show_color(initial_train[27]),
            # 硬座
            self.__show_color(initial_train[29]),
            # 无座
            self.__show_color(initial_train[26]),
            # 其他
            self.__show_color(initial_train[22]),
            # 备注
            self.__show_color(initial_train[1])
        ]
        for i, item in enumerate(train):
            if not item:
                train[i] = '--'
        return train

    def __get__trains(self):
        train_list = []
        for raw_train in self.available_trains:
            train_no = raw_train[3]
            initial = train_no[0].lower()

            # 车种筛选 这是判空  我在这里想了一会儿 这里会调用对应类的 __nonzero__ 或者 __length
            if not self.options or initial in self.options:
                train_list.append(self.generate_train(raw_train))
        return train_list

    @staticmethod
    def __check_equals(from_station, to_station, begin):
        if from_station == to_station:
            if begin:
                return '始'
            else:
                return '终'
        else:
            return '过'

    @staticmethod
    def __show_color(content):

        if content == '有':
            return Fore.GREEN + content + Fore.RESET
        else:
            return content

    @staticmethod
    def __get_color(color, content):
        return color + content + Fore.RESET

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.__get__trains():
            pt.add_row(train)
        print(pt)
