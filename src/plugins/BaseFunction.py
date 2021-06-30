import random
import datetime
import linecache

from plugins import dataManage


# ==========================================================
# 硬币
def coin():
    ran = random.randint(1, 6)
    if ran % 2 == 0:
        return '你抛出的硬币是：正面'
    else:
        return '你抛出的硬币是：反面'


# 骰子
def dice():
    return '你丢出的点数是：' + str(random.randint(1, 6))


# ==========================================================
# 运势
class luck:
    def __init__(self):
        self.luck = {}
        self.luck_file = 'luck'
        self.load_file()

    def load_file(self):
        self.luck = dataManage.load_obj(self.luck_file)

        clockDate = self.luck["luckDate"]
        today = str(datetime.date.today())
        if clockDate != today:
            self.luck["luck"].clear()
            self.luck["luckDate"] = today

    def write_file(self):
        dataManage.save_obj(self.luck, self.luck_file)

    def get_luck(self, qq):
        self.load_file()
        if self.luck["luck"].__contains__(qq):
            return '你今天的运势是：' + str(self.luck["luck"][qq])

        number = random.normalvariate(50, 16)
        if number < 0:
            number = 0
        elif number > 100:
            number = 100
        self.luck["luck"][qq] = int(number)
        self.write_file()
        return '你今天的运势是：' + str(int(number))


# ==========================================================
# 单词
def loop_step(index, total):
    index += 1
    if index > total:
        index = 1
    return index


def get_vocabulary4(number):
    if number > 20:
        return '贪心可不是好事哦~请输入一个小于等于20的数字'
    lineNumber = 1
    with open('data/vocabulary-4-index.txt', 'r+', encoding='utf-8') as f:
        lineNumber = int(f.readline())

    totalNumber = int(linecache.getline(r'data/vocabulary-4.txt', 1))
    reply = ''
    for i in range(0, number):
        reply += linecache.getline(r'data/vocabulary-4.txt', lineNumber + 1)
        lineNumber = loop_step(lineNumber, totalNumber)

    print('lineNumber：', lineNumber)

    with open('data/vocabulary-4-index.txt', 'w+', encoding='utf-8') as f:
        f.write(str(lineNumber))

    return reply[:-1]


def get_vocabulary6(number):
    if number > 20:
        return '贪心可不是好事哦~请输入一个小于等于20的数字'
    lineNumber = 1
    with open('data/vocabulary-6-index.txt', 'r+', encoding='utf-8') as f:
        lineNumber = int(f.readline())

    totalNumber = int(linecache.getline(r'data/vocabulary-6.txt', 1))
    reply = ''
    for i in range(0, number):
        reply += linecache.getline(r'data/vocabulary-6.txt', lineNumber + 1)
        lineNumber = loop_step(lineNumber, totalNumber)

    with open('data/vocabulary-6-index.txt', 'w+', encoding='utf-8') as f:
        f.write(str(lineNumber))
    return reply[:-1]


# ==========================================================
