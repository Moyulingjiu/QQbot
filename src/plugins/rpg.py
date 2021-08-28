

import random
import datetime
import linecache
import os
import copy

from plugins import dataManage
from plugins import logManage
from plugins import getNow
from plugins import BaseFunction

user_path = 'data/RPG/user/information'

rpg_config_path = 'data/RPG/system'
system_path = 'data/RPG/system/system'
rank_path = 'data/RPG/system/rank'

goods_path = 'data/RPG/goods/goods'
shop_path = 'data/RPG/goods/shop'
soul_shop_path = 'data/RPG/goods/soul_shop'
conversion_path = 'data/RPG/goods/conversion/'

monster_path = 'data/RPG/monster/monster'
map_path = 'data/RPG/monster/map/'

# ============================================
# 明日方舟抽卡模拟器

def MRFZ_card():
    card1 = []
    card2 = []
    card3 = []
    card4 = []
    card5 = []
    card6 = []
    information = []
    with open('data/Function/Arknights/PersonaCard.txt', 'r+', encoding='utf-8') as f:
        information = f.readlines()
    for i in information:
        i = i.strip()
        if len(i) > 0:
            tmp = i.split(' ')
            if tmp[0] == '1':
                card1.append(tmp[1])
            elif tmp[0] == '2':
                card2.append(tmp[1])
            elif tmp[0] == '3':
                card3.append(tmp[1])
            elif tmp[0] == '4':
                card4.append(tmp[1])
            elif tmp[0] == '5':
                card5.append(tmp[1])
            elif tmp[0] == '6':
                card6.append(tmp[1])
    random.shuffle(card1)
    random.shuffle(card2)
    random.shuffle(card3)
    random.shuffle(card4)
    random.shuffle(card5)
    random.shuffle(card6)
    card = starProbability()
    result = ''

    if card == 3:
        result += star2string(card) + random.choice(card3) + '\n'
    elif card == 4:
        result += star2string(card) + random.choice(card4) + '\n'
    elif card == 5:
        result += star2string(card) + random.choice(card5) + '\n'
    elif card == 6:
        result += star2string(card) + random.choice(card6) + '\n'
    result += '-------------\n以上数据由夜煞提供，如有错误，请使用命令\"*send 错误内容\"告知'
    return result


def MRFZ_card10():
    card1 = []
    card2 = []
    card3 = []
    card4 = []
    card5 = []
    card6 = []
    information = []
    with open('data/Function/Arknights/PersonaCard.txt', 'r+', encoding='utf-8') as f:
        information = f.readlines()
    for i in information:
        i = i.strip()
        if len(i) > 0:
            tmp = i.split(' ')
            if tmp[0] == '1':
                card1.append(tmp[1])
            elif tmp[0] == '2':
                card2.append(tmp[1])
            elif tmp[0] == '3':
                card3.append(tmp[1])
            elif tmp[0] == '4':
                card4.append(tmp[1])
            elif tmp[0] == '5':
                card5.append(tmp[1])
            elif tmp[0] == '6':
                card6.append(tmp[1])
    random.shuffle(card1)
    random.shuffle(card2)
    random.shuffle(card3)
    random.shuffle(card4)
    random.shuffle(card5)
    random.shuffle(card6)
    cards = []
    for i in range(10):
        cards.append(starProbability())
    result = ''
    for card in cards:
        if card == 3:
            result += star2string(card) + ' ' + random.choice(card3) + '\n'
        elif card == 4:
            result += star2string(card) + ' ' + random.choice(card4) + '\n'
        elif card == 5:
            result += star2string(card) + ' ' + random.choice(card5) + '\n'
        elif card == 6:
            result += star2string(card) + ' ' + random.choice(card6) + '\n'
    result += '-------------\n以上数据由夜煞提供，如有错误，请使用命令\"*send 错误内容\"告知'
    return result


def starProbability():
    ran = random.randrange(0, 100)
    if ran < 2:
        return 6
    elif ran < 10:
        return 5
    elif ran < 60:
        return 4
    else:
        return 3


def star2string(star):
    if star == 1:
        return '★☆☆☆☆☆'
    elif star == 2:
        return '★★☆☆☆☆'
    elif star == 3:
        return '★★★☆☆☆'
    elif star == 4:
        return '★★★★☆☆'
    elif star == 5:
        return '★★★★★☆'
    elif star == 6:
        return '★★★★★★'


# ============================================
# 辅助函数
def is_yesterday(date):
    today = str(datetime.date.today())
    list1 = today.split('-')
    for i in range(len(list1)):
        if list1[i].isdigit():
            list1[i] = int(list1[i])
        else:
            return False

    list2 = date.split('-')
    for i in range(len(list2)):
        if list2[i].isdigit():
            list2[i] = int(list2[i])
        else:
            return False
    if len(list2) != 3:
        return False

    leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    no_leap = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    is_leap = False
    if (list1[0] % 100 != 0 and list1[0] % 4 == 0) or list1[0] % 400 == 0:
        is_leap = True

    if list1[0] == list2[0]:
        if list1[1] == list2[1]:
            if list1[2] - list2[2] == 1:
                return True
        elif list1[1] - list2[1] == 1:
            if is_leap:
                if list2[2] == leap[list2[1] - 1] and list1[2] == 1:
                    return True
            else:
                if list2[2] == no_leap[list2[1] - 1] and list1[2] == 1:
                    return True
    elif list1[0] - list2[0] == 1:
        if list1[1] == 1 and list1[2] == 1 and list2[1] == 12 and list2[2] == 31:
            return True

    return False

def get_number(string):
    if string[0] == '-' and string[1:].isdigit():
        return -1 * int(string[1:])
    elif string.isdigit():
        return int(string)
    else:
        return 0

def analysis_name(string):
    enchanting = {
        'sharp': 0,
        'rapid': 0,
        'strong': 0
    }

    index = string.find('（')
    if not (index != -1 and string[-1] == '）'):
        return string, enchanting
    if string[0] == '（':
        return string, enchanting
    
    name = string[:index]
    information = string[index + 1:-1]
    if '，' in information:
        information_list = information.split('，')
    else:
        information_list = information.split('、')

    for section in information_list:
        if section[:2] == '锋利' and section[2:].isdigit():
            enchanting['sharp'] = int(section[2:])
        elif section[:2] == '迅捷' and section[2:].isdigit():
            enchanting['rapid'] = int(section[2:])
        elif section[:2] == '坚固' and section[2:].isdigit():
            enchanting['strong'] = int(section[2:])

    return name, enchanting

def get_name_with_enchanting(item):
    reply = item['name']

    enchanting = False
    if item['enchanting']['sharp'] != 0:
        reply += '（锋利' + str(item['enchanting']['sharp'])
        enchanting = True
    if item['enchanting']['rapid'] != 0:
        if not enchanting:
            reply += '（迅捷' + str(item['enchanting']['rapid'])
            enchanting = True
        else:
            reply += '，迅捷' + str(item['enchanting']['rapid'])
    if item['enchanting']['strong'] != 0:
        if not enchanting:
            reply += '（坚固' + str(item['enchanting']['strong'])
            enchanting = True
        else:
            reply += '，坚固' + str(item['enchanting']['strong'])
    if enchanting:
        reply += '）'
        
    if item['number'] > 1:
        reply += 'x' + str(item['number'])
    return reply

# 在日期上增加多少分钟
def addition_minute(date, minute):
    temp_list = date.split(' ')
    date_list = temp_list[0].split('-')
    for i in range(len(date_list)):
        date_list[i] = int(date_list[i])
    time_list = temp_list[1].split(':')
    for i in range(len(time_list)):
        time_list[i] = int(time_list[i])

    time_list[1] += minute
    
    if time_list[1] > 59:
        time_list[0] += int(time_list[1] / 60)
        time_list[1] = time_list[1] % 60

        if time_list[0] > 23:
            date_list[2] += int(time_list[0] / 24)
            time_list[0] = time_list[0] % 24

            
            leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            no_leap = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
            is_continue = True
            while is_continue:
                is_continue = False

                is_leap = False
                if (date_list[0] % 100 != 0 and date_list[0] % 4 == 0) or date_list[0] % 400 == 0:
                    is_leap = True
                
                if is_leap:
                    while date_list[2] > leap[date_list[1] - 1]:
                        date_list[2] -= leap[date_list[1] - 1]
                        date_list[1] += 1
                        if date_list[1] > 12:
                            date_list[0] += 1
                            date_list[1] %= 12
                            is_continue = True
                            break
                else:
                    while date_list[2] > no_leap[date_list[1] - 1]:
                        date_list[2] -= no_leap[date_list[1] - 1]
                        date_list[1] += 1
                        if date_list[1] > 12:
                            date_list[0] += 1
                            date_list[1] %= 12
                            is_continue = True
                            break
    
    return "%d-%02d-%02d %02d:%02d:%02d" % (date_list[0], date_list[1], date_list[2], time_list[0], time_list[1], time_list[2])

# 比较两个日期的大小，第一个是否大于第二
def is_greater_date(date1, date2):
    temp_list = date2.split(' ')
    date_list = temp_list[0].split('-')
    for i in range(len(date_list)):
        date_list[i] = int(date_list[i])
    time_list = temp_list[1].split(':')
    for i in range(len(time_list)):
        time_list[i] = int(time_list[i])

    temp_list = date1.split(' ')
    date_list2 = temp_list[0].split('-')
    for i in range(len(date_list2)):
        date_list2[i] = int(date_list2[i])
    time_list2 = temp_list[1].split(':')
    for i in range(len(time_list2)):
        time_list2[i] = int(time_list2[i])
    
    if date_list2[0] > date_list[0]:  # 年大于
        return True
    elif date_list2[0] == date_list[0]:  
        if date_list2[1] > date_list[1]:  # 月大于
            return True
        elif date_list2[1] == date_list[1]: 
            if date_list2[2] > date_list[2]:  # 日大于
                return True
            elif date_list2[2] == date_list[2]:
                if time_list2[0] > time_list[0]:  # 小时大于
                    return True
                elif time_list2[0] == time_list[0]:
                    if time_list2[1] > time_list[1]:  # 分钟大于
                        return True
                    elif time_list2[1] == time_list[1]:
                        if time_list2[2] > time_list[2]:  # 秒大于
                            return True
    return False

# 现在的时间是否已经超过对应日期
def is_beyond_deadline(date):
    return is_greater_date(getNow.toString(), date)

# 日期相减（暂不可用）
def subtract_date(date1, date2):
    if not is_greater_date(date1, date2):
        return -1

    temp_list = date2.split(' ')
    date_list = temp_list[0].split('-')
    for i in range(len(date_list)):
        date_list[i] = int(date_list[i])
    time_list = temp_list[1].split(':')
    for i in range(len(time_list)):
        time_list[i] = int(time_list[i])

    temp_list = date1.split(' ')
    date_list2 = temp_list[0].split('-')
    for i in range(len(date_list2)):
        date_list2[i] = int(date_list2[i])
    time_list2 = temp_list[1].split(':')
    for i in range(len(time_list2)):
        time_list2[i] = int(time_list2[i])
    
    seconds = time_list2[2] - time_list[2]
    if seconds < 0:
        seconds += 60
        time_list2[1] -= 1
    minute = time_list2[1] - time_list[1]
    if minute < 0:
        minute += 60
        time_list2[0] -= 1
    hour = time_list2[0] - time_list[0]
    if hour < 0:
        hour += 24
        date_list2[2] -= 1
    
    day = date_list2[2] - date_list[2]
    if day < 0:
        day += 30
        date_list2[1] -= 1
    
    day = date_list2[2] - date_list[2]
    if day < 0:
        day += 30
        date_list2[1] -= 1

# 级别转为罗马数字
def get_roman_numerals(number):
    if number == 1:
        return 'Ⅰ'
    elif number == 2:
        return 'Ⅱ'
    elif number == 3:
        return 'Ⅲ'
    elif number == 4:
        return 'Ⅳ'
    elif number == 5:
        return 'Ⅴ'
    elif number == 6:
        return 'Ⅵ'
    elif number == 7:
        return 'Ⅶ'
    elif number == 8:
        return 'Ⅷ'
    elif number == 9:
        return 'Ⅸ'
    elif number == 10:
        return 'Ⅹ'
    elif number == 11:
        return 'Ⅺ'
    elif number == 12:
        return 'Ⅻ'
    return ''
    
# ============================================
# 核心

class Result:
    def __init__(self):
        super().__init__()
        self.init = False
        self.name = ''
        self.sign = {
            'init': False,
            'state': 'success',  # 签到成功
            'gold': 0,  # 现在的积分
            'gold_sign': 0,  # 签到所获得的积分
            'gets': {},  # 签到所获得的物品
            'consecutive': 0,  # 连续签到天数
            'sum': 0  # 总计签到天数
        }
        self.PVP = {
            'init': False,
            'state': 'win',
            'is_fencing': False,  # 是否是击剑
            'name1': '',  # 胜利者名字
            'name2': '',  # 失败者名字
            'gold': 0
        }
        self.PVE = {
            'init': False,
            'state': 'win',
            'hp': 0,  # 损失生命值
            'monsters': [],  # 怪物
            'gets': []  # 掉落物
        }
        self.change_occupation = {
            'init': False,
            'state': 'success',  # 转职状态
            'type': 0,
            'from': '',
            'to': '',
            'need': {}
        }
        self.level_up_occupation = {
            'init': False,
            'state': 'success',  # 转职状态
            'mode': 0,  # 0生活职业，1：战斗职业
            'name': '',
            'from': 1,
            'to': 2,
            'need': {}
        }

        self.introduction = {
            'init': False,
            'state': '',
            'name': '',
            'id': 0,
            'type': 0,
            'limit': 0,
            'cost': -1,
            'sell': -1,
            'enchanting': {
                'sharp': 0,
                'rapid': 0,
                'strong': 0
            },
            'attribute': {  # 装备带来的属性
                'attack': 0,
                'armor': 0,
                'speed': 0,
                'hp': {
                    'number': 0,
                    'recovery': 0,
                    'max': 0
                },
                'san': {
                    'number': 0,
                    'recovery': 0,
                    'max': 0
                },
                'strength': {
                    'number': 0,
                    'recovery': 0,
                    'max': 0
                },
                'knapsack': 0,
                'resurrection': 0,
                'gold': 0
            },
            'comments': '',
            'decompose': {  # 分解路线
                'number': 0,
                'path': []
            },
            'synthesis': {  # 合成路线
                'number': 0,
                'path': []
            },
            'forger_synthesis': {  # 锻造师合成路线
                'number': 0,
                'level': 0,
                'path': []
            },
            'enchanter_synthesis': {  # 附魔师合成路线
                'number': 0,
                'level': 0,
                'path': []
            },
            'nurturer_synthesis': {  # 培育师合成路线
                'number': 0,
                'level': 0,
                'time': 0,
                'additional': [],
                'path': []
            }
        }
        self.monster_introduction = {
            'init': False,
            'name': '',
            'level': 0,
            'attack': 0,
            'armor': 0,
            'speed': 0,
            'hp': 0,
            'element': '',  # 元素
            'comments': '',
            'spoils': []
        }
        self.purchase = {
            'init': False,
            'state': 'success',
            'type': 0,  # 0表示正常商店购买，1表示灵商店购买
            'cost_soul': [],
            'cost': 0,
            'name': '',
            'number': 0
        }
        self.discard = {
            'init': False,
            'state': 'success',
            'goods': []
        }
        self.sell = {
            'init': False,
            'state': 'success',
            'sell': 0,
            'goods': []
        }
        self.give = {
            'init': False,
            'state': 'success',
            'name': '',
            'goods': []
        }
        self.use = {
            'init': False,
            'state': 'success',
            'goods': [],
            'mode': 0,  # 0：使用，1：装备
            'gold': 0,
            'hp': 0,
            'hp-recovery': 0,
            'hp-max': 0,
            'san': 0,
            'san-recovery': 0,
            'san-max': 0,
            'strength': 0,
            'strength-recovery': 0,
            'strength-max': 0,
            'resurrection': 0,
            'comments': ''
        }
        self.remove_equipment = {
            'init': False,
            'state': 'success',
            'name': ''
        }
        self.poisoning = {  # 中毒
            'init': False,
            'state': 'success',
            'level': 0,
            'hp': 0
        }
        self.paralysis = {  # 麻痹
            'init': False,
            'state': 'success',
            'level': 0,
            'strength': 0
        }
        self.double_gold = {  # 双倍积分收益
            'init': False,
            'state': 'success',
            'level': 0,
            'gold': 0
        }
        self.half_gold = {  # 减半积分收益
            'init': False,
            'state': 'success',
            'level': 0,
            'gold': 0
        }
        self.achievement = {  # 达成成就
            'init': False,
            'state': 'success',
            'achievement': {
                'synthesis': 0,  # 这是什么（合成物品数）
                'decompose': 0,  # 湮灭（分解物品数）
                'fully_armed': 0,  # 全副武装
                'human_sovereigns': 0,  # 人皇
                'boss_killer': 0,  # BOSS杀手
                'monster_kill': 0,  # 怪物杀手（击杀怪物数量）
                'almighty': 0,  # 全能达人
                'hunting_moment': 0,  # 猎杀时刻
                'miner': 0,  # 黄金矿工
                'lumberjack': 0,  # 伐木工
                'hamster': 0,  # 仓鼠
                'philanthropist': 0,  # 慈善家
                'popular': 0  # 群宠（接受的礼物数目）
            }
        }
        self.die_check = {  # 死亡结算
            'init': False,
            'state': 'return'
        }
        self.mining = {  # 挖矿结算
            'init': False,
            'state': 'success',
            'times': 0,
            'strength': 0,
            'gets': []
        }
        self.enchanting  = {  # 附魔
            'init': False,
            'state': 'success',
            'cost': [],
            'get': {
                'name': '',
                'number': 0,
                'enchanting': {
                    'sharp': 0,
                    'rapid': 0,
                    'strong': 0
                }
            }
        }
        self.cultivation = {  # 收获
            'init': False,
            'state': 'success',
            'name': '',
            'time': ''
        }
        self.harvest = {
            'init': False,
            'state': 'success',
            'harvest': [],
            'gets': []
        }

        self.decompose = {  # 分解物品
            'init': False,
            'state': 'success',
            'name': '',
            'number': 0,
            'gets': []
        }
        self.synthesis = {
            'init': False,
            'state': 'success',
            'name': '',
            'number': 0,
            'consume': []
        }

    # ======================================
    def show_goods(self, goods):
        reply = ''
        init = False
        for i in goods:
            if init:
                reply += '，'
            else:
                init = True
            if i['number'] > 1:
                reply += i['name'] + 'x' + str(i['number'])
            else:
                reply += i['name']
        return reply

    def show_type(self, number):
        if number == 0:
            return '物品'
        # 装备
        elif number == 1:
            return '装备'

        elif number == 10:
            return '饰品'
        elif number == 11:
            return '武器'
        elif number == 111:
            return '剑'
        elif number == 112:
            return '斧'
        elif number == 113:
            return '枪'
        elif number == 114:
            return '弓'
        elif number == 115:
            return '弩'
        elif number == 116:
            return '火统'

        elif number == 12:
            return '面具'
        elif number == 13:
            return '项链'
        elif number == 14:
            return '戒指'
        elif number == 15:
            return '头盔'
        elif number == 16:
            return '胸甲'
        elif number == 17:
            return '护腿'
        elif number == 18:
            return '靴子'
        elif number == 19:
            return '背包'

        # 消耗品
        elif number == 2:
            return '消耗品'
        elif number == 21:
            return '药剂'
        elif number == 22:
            return '食物'
            
        elif number == 24:
            return '礼包'
        elif number == 25:
            return '卷轴'
        elif number == 26:
            return '晶石'
        elif number == 27:
            return '树苗、种子、牲畜'

        # 材料
        elif number == 3:
            return '材料'
            
        elif number == 31:
            return '杂项材料'
        elif number == 32:
            return '矿石'

        elif number == 33:
            return '灵'
        elif number == 331:
            return '劣质灵'
        elif number == 332:
            return '普通灵'
        elif number == 333:
            return '精制灵'
        elif number == 334:
            return '史诗灵'
        elif number == 335:
            return '传说灵'
        elif number == 34:
            return '合成材料'

        # 纪念品
        elif number == 4:
            return '纪念品'
        elif number == 41:
            return '节日纪念品'
        elif number == 42:
            return '活动纪念品'

        return '【未知错误】'

    def show_attribute_number(self, number):
        if number >= 0:
            return '+' + str(number)
        else:
            return str(number)

    def show_items(self, items):
        reply = ''
        init = False
        for i in items:
            if not init:
                init = True
            else:
                reply += '，'
            reply += get_name_with_enchanting(i)
        return reply

    def show(self):
        reply = self.name

        # 指令结算
        if self.sign['init']:
            if self.sign['state'] == 'success':
                reply += '\n签到成功！当前积分：' + str(self.sign['gold']) + '（+' + str(self.sign['gold_sign']) + '）'
                reply += '\n连续签到：' + str(self.sign['consecutive']) + '天'
                reply += '\n总计签到：' + str(self.sign['sum']) + '天'
                if len(self.sign['gets']) != 0:
                    reply += '\n额外获得物品'
                    for activity, value in self.sign['gets'].items():
                        reply += '\n因为' + activity + '获得：' + self.show_goods(value)
            else:
                reply += '\n你今天已经签过到了哦~'
        elif self.change_occupation['init']:
            if self.change_occupation['state'] == 'success':
                if self.change_occupation['from'] == '':
                    reply += '\n你成功转职为：' + self.change_occupation['to']
                elif self.change_occupation['to'] == '':
                    reply += '\n你成功清除职业：' + self.change_occupation['from']
                else:
                    reply += '\n你成功从' + self.change_occupation['from'] + '转职为' + self.change_occupation['to']
                reply += '\n消耗：' + get_name_with_enchanting(self.change_occupation['need'])
            elif self.change_occupation['state'] == 'null':
                reply += '\n清空失败，你本来就没有职业'
            elif self.change_occupation['state'] == 'it was':
                if self.change_occupation['type'] == 0:
                    reply += '\n你本来就是' + self.change_occupation['from'] + '哦~试试输入“升级生活职业”来提升你的' + self.change_occupation['from'] + '等级'
                else:
                    reply += '\n你本来就是' + self.change_occupation['from'] + '哦~试试输入“升级战斗职业”来提升你的' + self.change_occupation['from'] + '等级'
            else:
                reply += '\n材料不足，转职失败。需要材料：' + get_name_with_enchanting(self.change_occupation['need'])
        elif self.level_up_occupation['init']:
            if self.level_up_occupation['state'] == 'success':
                reply += '\n你成功从「' + self.level_up_occupation['name'] + get_roman_numerals(self.level_up_occupation['from']) + '」升级为「' + self.level_up_occupation['name'] + get_roman_numerals(self.level_up_occupation['to']) + '」'
            elif self.level_up_occupation['state'] == 'max':
                if self.level_up_occupation['mode'] == 0:
                    reply += '\n你的生活职业已经达到最大等级'
                else:
                    reply += '\n你的战斗职业已经达到最大等级'
            elif self.level_up_occupation['state'] == 'null':
                if self.level_up_occupation['mode'] == 0:
                    reply += '\n你没有生活职业'
                else:
                    reply += '\n你没有战斗职业'
            else:
                reply += '\n材料不足，升级失败。需要材料：' + get_name_with_enchanting(self.level_up_occupation['need'])
        elif self.PVP['init']:
            if self.PVP['state'] == 'win':
                if self.PVP['is_fencing']:
                    maxLine = int(linecache.getline(r'data/RPG/system/fencing.txt', 1))
                    x = random.randrange(0, maxLine)
                    lineNumber = linecache.getline(r'data/RPG/system/fencing.txt', x * 2 + 3)
                    process = lineNumber.replace('*name1*', self.PVP['name1']).replace('*name2*', self.PVP['name2'])
                    reply = process
                    reply += '------------\n「' + self.PVP['name1'] + '」你击剑打败了「' + self.PVP['name2'] + '」，夺走了对方' + str(self.PVP['gold']) + '点节操（积分值）'
                else:
                    reply = '「' + self.PVP['name1'] + '」你决斗打败了「' + self.PVP['name2'] + '」，夺走了对方' + str(self.PVP['gold']) + '点积分'
            elif self.PVP['state'] == 'lose':
                if self.PVP['is_fencing']:
                    maxLine = int(linecache.getline(r'data/RPG/system/fencing.txt', 1))
                    x = random.randrange(0, maxLine)
                    lineNumber = linecache.getline(r'data/RPG/system/fencing.txt', x * 2 + 3)
                    process = lineNumber.replace('*name1*', self.PVP['name2']).replace('*name2*', self.PVP['name1'])
                    reply = process
                    reply += '------------\n「' + self.PVP['name1'] + '」你击剑输给了「' + self.PVP['name2'] + '」，被夺走了' + str(self.PVP['gold']) + '点节操（积分值）'
                else:
                    reply = '「' + self.PVP['name1'] + '」你决斗输给了「' + self.PVP['name2'] + '」，被夺走了' + str(self.PVP['gold']) + '点积分'
            elif self.PVP['state'] == 'fencing with yourself':
                reply += '\n好家伙，和自己击剑呢'
            elif self.PVP['state'] == 'no strength':
                reply += '\n你没有体力了呢~'
            elif self.PVP['state'] == 'active fencers have no points':
                reply += '\n你暂无积分哦~'
            elif self.PVP['state'] == 'passive fencers have no points':
                reply += '\n对方暂无积分哦~'
        elif self.introduction['init']:
            if self.introduction['state'] == 'success':
                reply = '名字：' + self.introduction['name'] + '（id：' + str(self.introduction['id']) + '）'
                reply += '\n类型：' + self.show_type(self.introduction['type'])

                init = False
                enchanting_introduction = ''
                if self.introduction['enchanting']['sharp'] != 0:
                    init = True
                    enchanting_introduction = '锋利' + get_roman_numerals(self.introduction['enchanting']['sharp'])
                if self.introduction['enchanting']['rapid'] != 0:
                    if not init:
                        init = True
                        enchanting_introduction = '迅捷' + get_roman_numerals(self.introduction['enchanting']['rapid'])
                    else:
                        enchanting_introduction += '，迅捷' + get_roman_numerals(self.introduction['enchanting']['rapid'])
                if self.introduction['enchanting']['strong'] != 0:
                    if not init:
                        init = True
                        enchanting_introduction = '坚固' + get_roman_numerals(self.introduction['enchanting']['strong'])
                    else:
                        enchanting_introduction += '，坚固' + get_roman_numerals(self.introduction['enchanting']['strong'])
                if init:
                    reply += '\n最大附魔：' + enchanting_introduction

                if self.introduction['cost'] != -1:
                    reply += '\n购买：' + str(self.introduction['cost'])
                else:
                    reply += '\n购买：无法购买'
                if self.introduction['sell'] != -1:
                    reply += '\n出售：' + str(self.introduction['sell'])
                else:
                    reply += '\n出售：无法出售'
                if self.introduction['limit'] != 0:
                    reply += '\n限购：' + str(self.introduction['limit'])
                reply += '\n介绍：' + self.introduction['comments']

                attribute = '\n效果：'
                init = False
                if self.introduction['attribute']['attack'] != 0:
                    init = True
                    attribute += '攻击力' + self.show_attribute_number(self.introduction['attribute']['attack'])
                if self.introduction['attribute']['armor'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    attribute += '护甲' + self.show_attribute_number(self.introduction['attribute']['armor'])
                if self.introduction['attribute']['speed'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    attribute += '速度' + self.show_attribute_number(self.introduction['attribute']['speed'])
                if self.introduction['attribute']['knapsack'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    attribute += '背包容量' + self.show_attribute_number(self.introduction['attribute']['knapsack'])
                
                if self.introduction['attribute']['hp']['number'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    if self.introduction['attribute']['hp']['number'] != -1:
                        attribute += '生命值' + self.show_attribute_number(self.introduction['attribute']['hp']['number'])
                    else:
                        attribute += '回满生命值'
                if self.introduction['attribute']['hp']['recovery'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    attribute += '每日生命值回复' + self.show_attribute_number(self.introduction['attribute']['hp']['recovery'])
                if self.introduction['attribute']['hp']['max'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    attribute += '最大生命值' + self.show_attribute_number(self.introduction['attribute']['hp']['max'])
                
                if self.introduction['attribute']['san']['number'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    if self.introduction['attribute']['san']['number'] != -1:
                        attribute += '精神值' + self.show_attribute_number(self.introduction['attribute']['san']['number'])
                    else:
                        attribute += '回满精神值'
                if self.introduction['attribute']['san']['recovery'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    attribute += '每日精神值回复' + self.show_attribute_number(self.introduction['attribute']['san']['recovery'])
                if self.introduction['attribute']['san']['max'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    attribute += '最大精神值' + self.show_attribute_number(self.introduction['attribute']['san']['max'])
                    
                if self.introduction['attribute']['strength']['number'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    if self.introduction['attribute']['strength']['number'] != -1:
                        attribute += '体力值' + self.show_attribute_number(self.introduction['attribute']['strength']['number'])
                    else:
                        attribute += '回满体力值'
                if self.introduction['attribute']['strength']['recovery'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    attribute += '每日体力值回复' + self.show_attribute_number(self.introduction['attribute']['strength']['recovery'])
                if self.introduction['attribute']['strength']['max'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    attribute += '最大体力值' + self.show_attribute_number(self.introduction['attribute']['strength']['max'])

                if self.introduction['attribute']['resurrection'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    attribute += '复活'
                if self.introduction['attribute']['gold'] != 0:
                    if init:
                        attribute += '，'
                    else:
                        init = True
                    attribute += '积分' + self.show_attribute_number(self.introduction['attribute']['gold'])
    
                if init:
                    reply += attribute

                if self.introduction['synthesis']['number'] != 0:
                    reply += '\n通用合成路线：' + self.introduction['name']
                    if self.introduction['synthesis']['number'] > 1:
                        reply += 'x' + str(self.introduction['synthesis']['number'])
                    reply += '<-' + self.show_goods(self.introduction['synthesis']['path'])

                if self.introduction['forger_synthesis']['number'] != 0:
                    reply += '\n锻造师' + get_roman_numerals(self.introduction['forger_synthesis']['level']) + '额外合成路线：' + self.introduction['name']
                    if self.introduction['forger_synthesis']['number'] > 1:
                        reply += 'x' + str(self.introduction['forger_synthesis']['number'])
                    reply += '<-' + self.show_goods(self.introduction['forger_synthesis']['path'])
                    
                if self.introduction['enchanter_synthesis']['number'] != 0:
                    reply += '\n附魔师' + get_roman_numerals(self.introduction['enchanter_synthesis']['level']) + '额外合成路线：' + self.introduction['name']
                    if self.introduction['enchanter_synthesis']['number'] > 1:
                        reply += 'x' + str(self.introduction['enchanter_synthesis']['number'])
                    reply += '<-' + self.show_goods(self.introduction['enchanter_synthesis']['path'])
                    
                if self.introduction['nurturer_synthesis']['number'] != 0:
                    if self.introduction['nurturer_synthesis']['time'] == 0:
                        reply += '\n培育师' + get_roman_numerals(self.introduction['nurturer_synthesis']['level']) + '可合成：' + self.introduction['name']
                        if self.introduction['nurturer_synthesis']['number'] > 1:
                            reply += 'x' + str(self.introduction['nurturer_synthesis']['number'])
                        reply += '<-' + self.show_goods(self.introduction['nurturer_synthesis']['path'])
                    else:
                        reply += '\n培育师' + get_roman_numerals(self.introduction['nurturer_synthesis']['level']) + '可花费' + str(self.introduction['nurturer_synthesis']['time']) + '分钟培育：'
                        reply += self.show_goods(self.introduction['nurturer_synthesis']['path']) + '->'
                        reply += self.show_goods(self.introduction['nurturer_synthesis']['additional'])


                if self.introduction['decompose']['number'] != 0:
                    reply += '\n分解路线：' + self.introduction['name']
                    if self.introduction['decompose']['number'] > 1:
                        reply += 'x' + str(self.introduction['decompose']['number'])
                    reply += '->' + self.show_goods(self.introduction['decompose']['path'])
                
            elif self.introduction['state'] == 'unknown':
                reply = '不存在该物品'
        elif self.purchase['init']:
            if self.purchase['state'] == 'success':
                if self.purchase['type'] == 0:
                    if self.purchase['number'] > 1:
                        reply += '\n购买成功！花费' + str(self.purchase['cost']) + '积分，获得' + self.purchase['name'] + 'x' + str(self.purchase['number'])
                    else:
                        reply += '\n购买成功！花费' + str(self.purchase['cost']) + '积分，获得' + self.purchase['name']
                else:
                    if self.purchase['number'] > 1:
                        reply += '\n购买成功！花费' + self.show_items(self.purchase['cost_soul']) + '，获得' + self.purchase['name'] + 'x' + str(self.purchase['number'])
                    else:
                        reply += '\n购买成功！花费' + self.show_items(self.purchase['cost_soul']) + '，获得' + self.purchase['name']
            elif self.purchase['state'] == 'no gold':
                reply += '\n购买失败！积分不足或者物品不足'
            elif self.purchase['state'] == 'limit':
                reply += '\n购买失败！达到限购上限'
            elif self.purchase['state'] == 'not for sale':
                reply += '\n购买失败！该物品不出售'
            elif self.purchase['state'] == 'non-existent':
                reply += '\n购买失败！不存在该物品'
            elif self.purchase['state'] == 'the backpack is full':
                reply += '\n背包已满'
        elif self.discard['init']:
            if self.discard['state'] == 'success':
                reply += '\n成功丢弃' + self.show_goods(self.discard['goods'])
            elif self.discard['state'] == 'all':
                reply += '\n成功丢弃所有物品'
            elif self.discard['state'] == 'all fail':
                reply += '\n丢弃失败！本来就没有物品'
            elif self.discard['state'] == 'not enough':
                reply += '\n丢弃失败！没有足够多的物品'
            elif self.discard['state'] == 'non-existent':
                reply += '\n丢弃失败！没有该物品'
        elif self.sell['init']:
            if self.sell['state'] == 'success':
                reply += '\n成功出售' + self.show_goods(self.discard['goods']) + '，获得' + str(self.sell['sell']) + '积分'
            elif self.sell['state'] == 'not enough':
                reply += '\n出售失败！没有足够多的物品'
            elif self.sell['state'] == 'non-existent':
                reply += '\n出售失败！没有该物品'
            elif self.sell['state'] == 'not for sale':
                reply += '\n出售失败！该物品不可以出售'
        elif self.give['init']:
            if self.give['state'] == 'success':
                reply += '\n成功赠送' + self.show_goods(self.give['goods']) + '给「' + self.give['name'] + '」'   
            elif self.give['state'] == 'not enough':
                reply += '\n赠送失败！没有足够多的物品'
            elif self.give['state'] == 'non-existent':
                reply += '\n赠送失败！没有该物品'
            elif self.give['state'] == 'full knapsack':
                reply += '\n赠送失败！对方背包已满'
        elif self.use['init']:
            if self.use['state'] == 'success':
                if self.use['mode'] == 0:
                    reply += '\n成功使用' + self.show_goods(self.use['goods'])
                else:
                    reply += '\n成功装备' + self.show_goods(self.use['goods'])
                if self.use['comments'] != '':
                    reply += '\n' + self.use['comments']
                elif self.use['mode'] == 0:
                    reply += '\n效果：'
                    init = False
                    if self.use['gold'] != 0:
                        init = True
                        reply += '积分' + self.show_attribute_number(self.use['gold'])
                    if self.use['hp'] != 0:
                        if not init:
                            init = True
                        else:
                            reply += '，'
                        if self.use['hp'] > 0:
                            reply += '生命值' + self.show_attribute_number(self.use['hp'])
                        else:
                            reply += '回满生命值'
                    if self.use['san'] != 0:
                        if not init:
                            init = True
                        else:
                            reply += '，'
                        if self.use['san'] > 0:
                            reply += '精神值' + self.show_attribute_number(self.use['san'])
                        else:
                            reply += '回满精神值'
                    if self.use['strength'] != 0:
                        if not init:
                            init = True
                        else:
                            reply += '，'
                        if self.use['strength'] > 0:
                            reply += '体力值' + self.show_attribute_number(self.use['strength'])
                        else:
                            reply += '回满体力值'
                    
                    if self.use['hp-recovery'] != 0:
                        if not init:
                            init = True
                        else:
                            reply += '，'
                        reply += '生命值回复' + self.show_attribute_number(self.use['hp-recovery']) + '/天'
                    if self.use['hp-max'] != 0:
                        if not init:
                            init = True
                        else:
                            reply += '，'
                        reply += '最大生命值' + self.show_attribute_number(self.use['hp-max'])
                        
                    if self.use['san-recovery'] != 0:
                        if not init:
                            init = True
                        else:
                            reply += '，'
                        reply += '精神值回复' + self.show_attribute_number(self.use['san-recovery']) + '/天'
                    if self.use['san-max'] != 0:
                        if not init:
                            init = True
                        else:
                            reply += '，'
                        reply += '最大精神值' + self.show_attribute_number(self.use['san-max'])
                        
                    if self.use['strength-recovery'] != 0:
                        if not init:
                            init = True
                        else:
                            reply += '，'
                        reply += '体力回复' + self.show_attribute_number(self.use['strength-recovery']) + '/天'
                    if self.use['strength-max'] != 0:
                        if not init:
                            init = True
                        else:
                            reply += '，'
                        reply += '最大体力值' + self.show_attribute_number(self.use['strength-max'])


                    if self.use['resurrection'] != 0:
                        if not init:
                            init = True
                        else:
                            reply += '，'
                        reply += '复活'


            elif self.use['state'] == 'die':
                reply += '\n使用失败！你目前处于死亡状态，不能直接回复生命值'
            elif self.use['state'] == 'too much':
                reply += '\n使用失败！啊嘞？使用这么多的武器？'
            elif self.use['state'] == 'not enough':
                reply += '\n使用失败！没有足够多的物品'
            elif self.use['state'] == 'non-existent':
                reply += '\n使用失败！没有该物品'
            elif self.use['state'] == 'material':
                reply += '\n使用失败！材料不可以使用'
            elif self.use['state'] == 'keepsake':
                reply += '\n使用失败！纪念品不可以使用，只可以出售'
            elif self.use['state'] == 'cultivation':
                reply += '\n使用失败！这个物品只可以在培育师手里培育不可以直接使用'
            elif self.use['state'] == 'unknown':
                reply += '\n使用失败！物品大全里没有记录该物品，请联系官方群（479504567）'
            elif self.use['state'] == 'unknown type':
                reply += '\n使用失败！罕见错误：无法识别物品分类，请联系官方群（479504567）'
            elif self.use['state'] == 'hp overflow':
                reply += '\n使用失败！如果使用，生命值将超过最大生命值'
            elif self.use['state'] == 'san overflow':
                reply += '\n使用失败！如果使用，精神值将超过最大精神值'
            elif self.use['state'] == 'strength overflow':
                reply += '\n使用失败！如果使用，体力值将超过最大体力值'
            elif self.use['state'] == 'the backpack is full':
                reply += '\n装备失败！背包已满'
        elif self.remove_equipment['init']:
            if self.remove_equipment['state'] == 'success':
                reply += '\n成功卸下装备：' + self.remove_equipment['name']
            elif self.remove_equipment['state'] == 'the backpack is full':
                reply += '\n卸下装备失败！背包已满'
            elif self.remove_equipment['state'] == 'non-existent':
                reply += '\n卸下装备失败！没有装备该物品'
        elif self.monster_introduction['init']:
            reply = '名字：' + self.monster_introduction['name']
            reply += '\n评级：' + str(self.monster_introduction['level'])
            if str(self.monster_introduction['element']) == '':
                reply += '\n元素：（暂无）'
            else:    
                reply += '\n元素：' + str(self.monster_introduction['element'])
            reply += '\n介绍：' + str(self.monster_introduction['comments'])
        elif self.PVE['init']:
            if self.PVE['state'] == 'win':
                reply += '\n成功击败「' + self.show_goods(self.PVE['monsters']) + '」，损失' + str(self.PVE['hp']) + '点生命值'
                if len(self.PVE['gets']) != 0:
                    reply += '\n战利品：' + self.show_goods(self.PVE['gets'])
                else:
                    reply += '\n战利品：无'
            elif self.PVE['state'] == 'die':
                reply += '\n你在与「' +  self.show_goods(self.PVE['monsters']) + '」的战斗中死亡'
                if len(self.PVE['gets']) != 0:
                    reply += '\n战利品：' + self.show_goods(self.PVE['gets'])
                else:
                    reply += '\n战利品：无'
            elif self.PVE['state'] == 'no monster':
                reply += '\n当前区域没有怪物'
            elif self.PVE['state'] == 'no hp':
                reply += '\n你目前没有生命值呢'
            elif self.PVE['state'] == 'no strength':
                reply += '\n体力不足~'
        elif self.mining['init']:
            if self.mining['times'] != 0:
                reply += '\n你成功挖矿' + str(self.mining['times']) + '次，消耗' + str(self.mining['strength']) + '点体力值，得到：' + self.show_goods(self.mining['gets'])
            else:
                reply += '\n体力不足'
        elif self.decompose['init']:
            if self.decompose['state'] == 'success':
                reply += '\n成功将「' + self.decompose['name']
                if self.decompose['number'] > 1:
                    reply += 'x' + str(self.decompose['number'])
                reply += '」分解为「' + self.show_goods(self.decompose['gets']) + '」'
            elif self.decompose['state'] == 'knapsack':
                reply += '\n分解失败！背包已满'
            elif self.decompose['state'] == 'null':
                reply += '\n分解失败！该物品不可以分解'
            elif self.decompose['state'] == 'not enough':
                reply += '\n分解失败！没有足够的物品'
            elif self.decompose['state'] == 'non-existent':
                reply += '\n分解失败！没有该物品'
        elif self.synthesis['init']:
            if self.synthesis['state'] == 'success':
                reply += '\n成功将「' + self.show_goods(self.synthesis['consume']) + '」合成为「' + self.synthesis['name']
                if self.synthesis['number'] > 1:
                    reply += 'x' + str(self.synthesis['number'])
                reply += '」'
            elif self.synthesis['state'] == 'knapsack':
                reply += '\n合成失败！背包已满'
            elif self.synthesis['state'] == 'null':
                reply += '\n合成失败！该物品不可以合成'
            else:
                reply += '\n合成失败！没有足够的物品'
        elif self.enchanting['init']:
            if self.enchanting['state'] == 'success':
                reply += '\n附魔成功！消耗「' + self.show_items(self.enchanting['cost']) + '」获得「'+ get_name_with_enchanting(self.enchanting['get']) + '」'
            elif self.enchanting['state'] == 'job mismatch':
                reply += '\n附魔失败！你不是附魔师~'
            elif self.enchanting['state'] == 'null':
                reply += '\n附魔失败！没有这个附魔'
            elif self.enchanting['state'] == 'max':
                reply += '\n附魔失败！这件物品不能够承受如此高的附魔或者不存在该附魔~'
            elif self.enchanting['state'] == 'was':
                reply += '\n附魔失败！这件物品已经拥有了该附魔'
            elif self.enchanting['state'] == 'knapsack':
                reply += '\n附魔失败！背包空间不足'
            else:
                reply += '\n附魔失败！需要材料「' + self.show_items(self.enchanting['cost']) + '」'
        elif self.cultivation['init']:
            if self.cultivation['state'] == 'success':
                reply += '\n成功培育「' + self.cultivation['name'] + '」将会在' + self.cultivation['time'] + '成熟'
            elif self.cultivation['state'] == 'job mismatch':
                reply += '\n培育失败！你不是培育师~'
            elif self.cultivation['state'] == 'level':
                reply += '\n培育失败！你的培育师等级不够'
            elif self.cultivation['state'] == 'null':
                reply += '\n培育失败！「' + self.cultivation['name'] + '」不可以培育'
            elif self.cultivation['state'] == 'max':
                reply += '\n培育失败！你的农场已经满了'
            else:
                reply += '\n培育失败！你没有「' + self.cultivation['name'] + '」'
        elif self.harvest['init']:
            if self.harvest['state'] == 'success':
                reply += '\n成功收获「'
                init = False
                for name in self.harvest['harvest']:
                    if init:
                        reply += '，'
                    else:
                        init = True
                    reply += name
                reply += '」获得「' + self.show_items(self.harvest['gets']) + '」'
            elif self.harvest['state'] == 'job mismatch':
                reply += '\n收获失败！你不是培育师~'
            elif self.harvest['state'] == 'nothing':
                reply += '\n收获失败！没有可以收获的或者背包已满'
        else:
            reply += '\n【操作指令内出现未预期的错误】'

        # BUFF结算
        if self.poisoning['init']:
            if self.poisoning['state'] == 'success':
                reply += '\n触发「中毒' + get_roman_numerals(self.poisoning['level']) + '」失去' + str(self.poisoning['hp']) + '点生命值'
            if self.poisoning['state'] == 'die':
                reply += '\n触发「中毒' + get_roman_numerals(self.poisoning['level']) + '」死亡'
        if self.paralysis['init']:
            if self.paralysis['state'] == 'success':
                reply += '\n触发「麻痹' + get_roman_numerals(self.paralysis['level']) + '」额外消耗' + str(self.paralysis['strength']) + '点体力值'
            elif self.paralysis['state'] == 'nothing':
                reply += '\n触发「麻痹' + get_roman_numerals(self.paralysis['level']) + '」好像什么也没有发生'
        if self.double_gold['init']:
            if self.double_gold['state'] == 'success':
                reply += '\n触发「双倍积分收益' + get_roman_numerals(self.double_gold['level']) + '」额外获得' + str(self.double_gold['gold']) + '点积分'
            elif self.double_gold['state'] == 'nothing':
                reply += '\n触发「双倍积分收益' + get_roman_numerals(self.double_gold['level']) + '」好像什么也没有发生'
        if self.half_gold['init']:
            if self.half_gold['state'] == 'success':
                reply += '\n触发「减半积分收益' + get_roman_numerals(self.half_gold['level']) + '」失去' + str(self.half_gold['gold']) + '点积分'
            elif self.half_gold['state'] == 'nothing':
                reply += '\n触发「减半积分收益' + get_roman_numerals(self.half_gold['level']) + '」好像什么也没有发生'

        # 死亡结算
        if self.die_check['init']:
            if self.die_check['state'] == 'return':
                reply += '\n死亡结算：因为死亡你已经回到了出生地'
            elif self.die_check['state'] == '不死图腾':
                reply += '\n死亡结算：「不死图腾」帮你免除了本次死亡'
        
        # 成就
        if self.achievement['init']:
            achievement = self.achievement['achievement']
            if achievement['synthesis'] != 0:
                reply += '\n解锁成就「这是什么' + get_roman_numerals(achievement['synthesis']) + '」'
            if achievement['decompose'] != 0:
                reply += '\n解锁成就「湮灭' + get_roman_numerals(achievement['decompose']) + '」'
            if achievement['fully_armed'] != 0:
                reply += '\n解锁成就「全副武装' + get_roman_numerals(achievement['fully_armed']) + '」'
            if achievement['human_sovereigns'] != 0:
                reply += '\n解锁成就「人皇' + get_roman_numerals(achievement['human_sovereigns']) + '」'
            if achievement['boss_killer'] != 0:
                reply += '\n解锁成就「BOSS杀手' + get_roman_numerals(achievement['boss_killer']) + '」'
            if achievement['monster_kill'] != 0:
                reply += '\n解锁成就「怪物猎人' + get_roman_numerals(achievement['monster_kill']) + '」'
            if achievement['almighty'] != 0:
                reply += '\n解锁成就「全能达人' + get_roman_numerals(achievement['almighty']) + '」'
            if achievement['hunting_moment'] != 0:
                reply += '\n解锁成就「猎杀时刻' + get_roman_numerals(achievement['hunting_moment']) + '」'
            if achievement['miner'] != 0:
                reply += '\n解锁成就「黄金矿工' + get_roman_numerals(achievement['miner']) + '」'
            if achievement['lumberjack'] != 0:
                reply += '\n解锁成就「伐木工' + get_roman_numerals(achievement['lumberjack']) + '」'
            if achievement['hamster'] != 0:
                reply += '\n解锁成就「仓鼠' + get_roman_numerals(achievement['hamster']) + '」'
            if achievement['philanthropist'] != 0:
                reply += '\n解锁成就「慈善家' + get_roman_numerals(achievement['philanthropist']) + '」'
            if achievement['popular'] != 0:
                reply += '\n解锁成就「群宠' + get_roman_numerals(achievement['popular']) + '」'

        return reply

    # ======================================
    def append_PVP(self, PVP):
        self.PVP = PVP
        self.init = True

    def append_PVE(self, PVE):
        self.PVE = PVE
        self.init = True

    def append_sign(self, sign):
        self.sign = sign
        self.init = True

    def append_change_occupation(self, change_occupation):
        self.change_occupation = change_occupation
        self.init = True
    
    def append_level_up_occupation(self, level_up_occupation):
        self.level_up_occupation = level_up_occupation
        self.init = True

    def append_introduction(self, introduction):
        self.introduction = introduction
        self.init = True

    def append_purchase(self, purchase):
        self.purchase = purchase
        self.init = True

    def append_discard(self, discard):
        self.discard = discard
        self.init = True

    def append_sell(self, sell):
        self.sell = sell
        self.init = True

    def append_give(self, give):
        self.give = give
        self.init = True

    def append_use(self, use):
        self.use = use
        self.init = True

    def append_remove_equipment(self, remove_equipment):
        self.remove_equipment = remove_equipment
        self.init = True

    def append_monster_introduction(self, monster_introduction):
        self.monster_introduction = monster_introduction
        self.init = True

    def append_poisoning(self, poisoning):
        self.poisoning = poisoning
        self.init = True

    def append_paralysis(self, paralysis):
        self.paralysis = paralysis
        self.init = True

    def append_achievement(self, achievement):
        self.achievement = achievement
        self.init = True
    
    def append_double_gold(self, double_gold):
        self.double_gold = double_gold
        self.init = True
    
    def append_half_gold(self, half_gold):
        self.half_gold = half_gold
        self.init = True

    def append_die_check(self, die_check):
        self.die_check = die_check
        self.init = True

    def append_mining(self, mining):
        self.mining = mining
        self.init = True

    def append_decompose(self, decompose):
        self.decompose = decompose
        self.init = True

    def append_synthesis(self, synthesis):
        self.synthesis = synthesis
        self.init = True

    def append_enchanting(self, enchanting):
        self.enchanting = enchanting
        self.init = True

    def append_cultivation(self, cultivation):
        self.cultivation = cultivation
        self.init = True

    def append_harvest(self, harvest):
        self.harvest = harvest
        self.init = True

    def set_name(self, name):
        self.name = name
        self.init = True

    def get_init(self):
        return self.init

class Core:
    def __init__(self):
        super().__init__()
        self.users = {}  # 用户

        self.system = {}  # 系统数据，主要为boss血量等
        self.rank = {}  # 排名数据

        self.init = True  # 是否有初始化

        self.goods = {}  # 物品数据
        self.shop = []  # 商店
        self.soul_shop = {}  # 灵商店

        self.map = {}  # 群系表
        self.monster = {}  # 怪物表
        self.boss = {}  # boss表

        # self.baseInformation = {}  # 基本介绍
        # self.buff = {}  # buff表

        self.decompose = {}  # 分解
        self.synthesis = {}  # 合成
        self.forger_synthesis = {}  # 锻造师合成表
        self.nurturer_synthesis = {}  # 培育师合成表
        self.enchanter_synthesis = {}  # 附魔师合成表

        self.luck = BaseFunction.luck()

        self.load()  # 加载数据

    def load(self):
        # 获取用户数据与排行榜
        self.users = dataManage.load_obj(user_path)
        self.rank = {
            'gold': {
                '1': 0,
                '2': 0,
                '3': 0
            },
            'rate': {
                'all': 0,
                'over100': 0
            },
            'fencing_master': 0,
            'ascents': 0,  # 登顶次数
            'be_fenced': 0,
            'monster': 0,
            'die': 0,  # 死亡数
            'travel': 0
        }
        rank = dataManage.load_obj(rank_path)
        if rank.__contains__('gold'):
            if rank['gold'].__contains__('1'):
                self.rank['gold']['1'] = rank['gold']['1']
            if rank['gold'].__contains__('2'):
                self.rank['gold']['2'] = rank['gold']['2']
            if rank['gold'].__contains__('3'):
                self.rank['gold']['3'] = rank['gold']['3']
        if rank.__contains__('fencing_master'):
            if rank['rate'].__contains__('all'):
                self.rank['rate']['all'] = rank['rate']['all']
            if rank['rate'].__contains__('over100'):
                self.rank['rate']['over100'] = rank['rate']['over100']
        if rank.__contains__('fencing_master'):
            self.rank['fencing_master'] = rank['fencing_master']
        if rank.__contains__('ascents'):
            self.rank['ascents'] = rank['ascents']
        if rank.__contains__('be_fenced'):
            self.rank['be_fenced'] = rank['be_fenced']
        if rank.__contains__('monster'):
            self.rank['monster'] = rank['monster']
        if rank.__contains__('die'):
            self.rank['die'] = rank['die']
        if rank.__contains__('travel'):
            self.rank['travel'] = rank['travel']

        # 获取物品
        index = 1
        with open(goods_path + '.txt', 'r+', encoding='utf-8') as f:
            text = f.readlines()
            for i in text:
                i = i.strip()
                if len(i) > 0 and i[0] != '#':
                    data = i.split(' ')
                    if len(data) > 3:  # 至少得有名字、简介、类型
                        if not self.goods.__contains__(data[0]):
                            goods = {
                                'id': index,  # 编号
                                'type': 0,

                                'limit': 0,
                                'cost': -1,
                                'sell': -1,
                                
                                'gold': 0,
                                'attack': 0,
                                'armor': 0,
                                'speed': 0,
                                'hp': 0,
                                'hp-recovery': 0,
                                'hp-max': 0,
                                'san': 0,
                                'san-recovery': 0,
                                'san-max': 0,
                                'strength': 0,
                                'strength-recovery': 0,
                                'strength-max': 0,
                                'knapsack': 0,

                                'resurrection': 0,
                                
                                'enchanting-sharp': 0,
                                'enchanting-rapid': 0,
                                'enchanting-strong': 0,

                                'comments': ''
                            }
                            for j in data:
                                j_list = j.split('=')
                                if len(j_list) == 2:
                                    if j_list[0] != 'comments':
                                        goods[j_list[0]] = get_number(j_list[1])
                                    else:
                                        goods[j_list[0]] = j_list[1]
                            if goods['type'] != 0 and goods['comments'] != '':
                                index += 1
                                self.goods[data[0]] = copy.deepcopy(goods)

        with open(shop_path + '.txt', 'r+', encoding='utf-8') as f:
            text = f.readlines()
            for line in text:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    if self.goods.__contains__(line) and line not in self.shop:
                        self.shop.append(line)
                        
        with open(soul_shop_path + '.txt', 'r+', encoding='utf-8') as f:
            text = f.readlines()
            for line in text:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    data = line.split(' ')
                    if len(data) == 2 and self.goods.__contains__(data[0]):
                        item = {
                            'cost': []
                        }
                        information = data[1].split('=')
                        cost_list = information[1].split('，')
                        for section in cost_list:
                            piece = section.split('x')
                            if len(piece) == 2 and piece[1].isdigit():
                                single = {
                                    'name': piece[0],
                                    'number': int(piece[1]),
                                    'enchanting': {
                                        'sharp': 0,
                                        'rapid': 0,
                                        'strong': 0
                                    }
                                }
                                item['cost'].append(single)
                        if not self.soul_shop.__contains__(data[0]) and len(item['cost']) != 0:
                            self.soul_shop[data[0]] = item
        
        # 分解表&合成表的获取
        # （分解表）
        with open(conversion_path + 'decompose.txt', 'r+', encoding='utf-8') as f:
            text = f.readlines()
            for line in text:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    data = line.split(' ')
                    if len(data) >= 2:
                        decomposition_route = {
                            'number': 0,
                            'path': []
                        }

                        name = ''
                        if 'x' in data[0]:
                            name_list = data[0].split('x')
                            name = name_list[0]
                            if name_list[1].isdigit():
                                decomposition_route['number'] = int(name_list[1])
                        else:
                            name = data[0]
                            decomposition_route['number'] = 1

                        for temp_item in data:
                            section = temp_item.split('=')
                            if len(section) == 2:
                                if section[0] == 'path':
                                    goods_list = section[1].split('，')
                                    for goods in goods_list:
                                        information = goods.split('x')
                                        item = {
                                            'name': '',
                                            'number': 0,
                                            'enchanting': {
                                                'sharp': 0,
                                                'rapid': 0,
                                                'strong': 0
                                            }
                                        }
                                        if len(information) == 1:
                                            item['name'] = information[0]
                                        elif len(information) == 2:
                                            item['name'] = information[0]
                                            if information[1].isdigit():
                                                item['number'] = int(information[1])

                                        if self.goods.__contains__(item['name']):
                                            decomposition_route['path'].append(item)

                        if self.goods.__contains__(name):
                            self.decompose[name] = decomposition_route

        # （合成表）
        with open(conversion_path + 'synthesis.txt', 'r+', encoding='utf-8') as f:
            text = f.readlines()
            for line in text:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    data = line.split(' ')
                    if len(data) >= 2:
                        synthesis_route = {
                            'number': 0,
                            'path': []
                        }

                        name = ''
                        if 'x' in data[0]:
                            name_list = data[0].split('x')
                            name = name_list[0]
                            if name_list[1].isdigit():
                                synthesis_route['number'] = int(name_list[1])
                        else:
                            name = data[0]
                            synthesis_route['number'] = 1

                        for temp_item in data:
                            section = temp_item.split('=')
                            if len(section) == 2:
                                if section[0] == 'path':
                                    goods_list = section[1].split('，')
                                    for goods in goods_list:
                                        information = goods.split('x')
                                        item = {
                                            'name': '',
                                            'number': 0,
                                            'enchanting': {
                                                'sharp': 0,
                                                'rapid': 0,
                                                'strong': 0
                                            }
                                        }
                                        if len(information) == 1:
                                            item['name'] = information[0]
                                        elif len(information) == 2:
                                            item['name'] = information[0]
                                            if information[1].isdigit():
                                                item['number'] = int(information[1])

                                        if self.goods.__contains__(item['name']):
                                            synthesis_route['path'].append(item)

                        if self.goods.__contains__(name):
                            self.synthesis[name] = synthesis_route
        
        # （锻造师合成表）
        with open(conversion_path + 'forger_synthesis.txt', 'r+', encoding='utf-8') as f:
            text = f.readlines()
            for line in text:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    data = line.split(' ')
                    if len(data) >= 2:
                        synthesis_route = {
                            'number': 0,
                            'level': 0,
                            'path': []
                        }

                        name = ''
                        if 'x' in data[0]:
                            name_list = data[0].split('x')
                            name = name_list[0]
                            if name_list[1].isdigit():
                                synthesis_route['number'] = int(name_list[1])
                        else:
                            name = data[0]
                            synthesis_route['number'] = 1

                        for temp_item in data:
                            section = temp_item.split('=')
                            if len(section) == 2:
                                if section[0] == 'path':
                                    goods_list = section[1].split('，')
                                    for goods in goods_list:
                                        information = goods.split('x')
                                        item = {
                                            'name': '',
                                            'number': 0,
                                            'enchanting': {
                                                'sharp': 0,
                                                'rapid': 0,
                                                'strong': 0
                                            }
                                        }
                                        if len(information) == 1:
                                            item['name'] = information[0]
                                        elif len(information) == 2:
                                            item['name'] = information[0]
                                            if information[1].isdigit():
                                                item['number'] = int(information[1])

                                        if self.goods.__contains__(item['name']):
                                            synthesis_route['path'].append(item)
                                elif section[0] == 'level':
                                    synthesis_route['level'] = get_number(section[1])
                        if self.goods.__contains__(name):
                            self.forger_synthesis[name] = synthesis_route

        # （附魔师合成表）
        with open(conversion_path + 'enchanter_synthesis.txt', 'r+', encoding='utf-8') as f:
            text = f.readlines()
            for line in text:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    data = line.split(' ')
                    if len(data) >= 2:
                        synthesis_route = {
                            'number': 0,
                            'level': 0,
                            'path': []
                        }

                        name = ''
                        if 'x' in data[0]:
                            name_list = data[0].split('x')
                            name = name_list[0]
                            if name_list[1].isdigit():
                                synthesis_route['number'] = int(name_list[1])
                        else:
                            name = data[0]
                            synthesis_route['number'] = 1

                        for temp_item in data:
                            section = temp_item.split('=')
                            if len(section) == 2:
                                if section[0] == 'path':
                                    goods_list = section[1].split('，')
                                    for goods in goods_list:
                                        information = goods.split('x')
                                        item = {
                                            'name': '',
                                            'number': 0,
                                            'enchanting': {
                                                'sharp': 0,
                                                'rapid': 0,
                                                'strong': 0
                                            }
                                        }
                                        if len(information) == 1:
                                            item['name'] = information[0]
                                        elif len(information) == 2:
                                            item['name'] = information[0]
                                            if information[1].isdigit():
                                                item['number'] = int(information[1])

                                        if self.goods.__contains__(item['name']):
                                            synthesis_route['path'].append(item)
                                elif section[0] == 'level':
                                    synthesis_route['level'] = get_number(section[1])
                        if self.goods.__contains__(name):
                            self.enchanter_synthesis[name] = synthesis_route

        # （培育师合成表）
        with open(conversion_path + 'nurturer_synthesis.txt', 'r+', encoding='utf-8') as f:
            text = f.readlines()
            for line in text:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    data = line.split(' ')
                    if len(data) >= 2:
                        synthesis_route = {
                            'number': 0,
                            'level': 0,
                            'additional': [],
                            'path': [],
                            'time': 0
                        }

                        name = ''
                        if 'x' in data[0]:
                            name_list = data[0].split('x')
                            name = name_list[0]
                            if name_list[1].isdigit():
                                synthesis_route['number'] = int(name_list[1])
                        else:
                            name = data[0]
                            synthesis_route['number'] = 1

                        for temp_item in data:
                            section = temp_item.split('=')
                            if len(section) == 2:
                                if section[0] == 'path' or section[0] == 'additional':
                                    goods_list = section[1].split('，')
                                    for goods in goods_list:
                                        information = goods.split('x')
                                        item = {
                                            'name': '',
                                            'number': 0,
                                            'enchanting': {
                                                'sharp': 0,
                                                'rapid': 0,
                                                'strong': 0
                                            }
                                        }
                                        if len(information) == 1:
                                            item['name'] = information[0]
                                        elif len(information) == 2:
                                            item['name'] = information[0]
                                            if information[1].isdigit():
                                                item['number'] = int(information[1])

                                        if self.goods.__contains__(item['name']):
                                            synthesis_route[section[0]].append(item)
                                elif section[0] == 'level':
                                    synthesis_route['level'] = get_number(section[1])
                                elif section[0] == 'time':
                                    synthesis_route['time'] = get_number(section[1])
                        if self.goods.__contains__(name):
                            self.nurturer_synthesis[name] = synthesis_route

        # 获取怪物表
        with open(monster_path + '.txt', 'r+', encoding='utf-8') as f:
            text = f.readlines()
            for line in text:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    data = line.split(' ')
                    if len(data) >= 6:
                        if not self.monster.__contains__(data[0]):
                            monster = {
                                'level': 0,
                                'attack': 0,
                                'armor': 0,
                                'speed': 0,
                                'hp': 0,
                                'element': '',  # 元素
                                'comments': '',
                                'spoils': []
                            }
                            for j in data:
                                j_list = j.split('=')
                                if len(j_list) == 2:
                                    if j_list[0] != 'comments' and j_list[0] != 'spoils' and j_list[0] != 'element':
                                        monster[j_list[0]] = get_number(j_list[1])
                                    elif j_list[0] == 'comments' or j_list[0] == 'element':
                                        monster[j_list[0]] = j_list[1]
                                    else:
                                        things = j_list[1].split('，')
                                        for section in things:
                                            section_list = section.split('x')
                                            if len(section_list) == 1:
                                                name, enchanting = analysis_name(section_list[0])
                                                if self.goods.__contains__(name):
                                                    item = {
                                                        'name': name,
                                                        'number': 1,
                                                        'enchanting': enchanting
                                                    }
                                                    monster['spoils'].append(item)
                                            elif len(section_list) == 2 and section_list[1].isdigit():
                                                name, enchanting = analysis_name(section_list[0])
                                                if self.goods.__contains__(name):
                                                    item = {
                                                        'name': name,
                                                        'number': int(section_list[1]),
                                                        'enchanting': enchanting
                                                    }
                                                    monster['spoils'].append(item)
                            if monster['level'] != 0 and monster['hp'] != 0 and monster['comments'] != '':
                                if 1 <= monster['level'] <= 3:
                                    name = '劣质灵'
                                elif 4 <= monster['level'] <= 6:
                                    name = '普通灵'
                                elif 7 <= monster['level'] <= 9:
                                    name = '稀有灵'
                                elif 7 <= monster['level'] <= 9:
                                    name = '史诗灵'
                                elif monster['level'] == 13:
                                    name = '传奇灵'
                                else:
                                    name = ''

                                if name != '':
                                    item = {
                                        'name': name,
                                        'number': 1,
                                        'enchanting': {
                                            'sharp': 0,
                                            'rapid': 0,
                                            'strong': 0
                                        }
                                    }
                                    monster['spoils'].append(item)
                                self.monster[data[0]] = copy.deepcopy(monster)
        # 加载群系表
        with open(map_path + 'map.txt', 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    data = line.split(' ')
                    if len(data) >= 2 and not self.map.__contains__(data[0]):
                        map = {
                            'level': -1,
                            'boss': '',
                            'monster': []
                        }

                        for information in data:
                            information_list = information.split('=')
                            if len(information_list) == 2:
                                if information_list[0] != 'monster':
                                    map[information_list[0]] = get_number(information_list[1])

                        if map['level'] != -1:
                            self.map[data[0]] = copy.deepcopy(map)

        # 加载群系怪物
        del_key_list = []
        for key, value in self.map.items():
            if not os.path.exists(map_path + key + '.txt'):
                del_key_list.append(key)
            else:
                with open(map_path + key + '.txt', 'r+', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        if len(line) > 0 and line[0] != '#':
                            data = line.split(' ')
                            if len(data) == 2 and data[0].isdigit():
                                monster = {
                                    'proportion': int(data[0]),
                                    'monster': []
                                }
                                information = data[1].split('，')
                                for temp in information:
                                    section = temp.split('x')
                                    if len(section) == 2 and section[1].isdigit():
                                        single = {
                                            'name': section[0],
                                            'number': int(section[1])
                                        }
                                        if self.monster.__contains__(section[0]):
                                            monster['monster'].append(single)
                                if monster['proportion'] != 0 and len(monster['monster']) != 0:
                                    self.map[key]['monster'].append(monster)
        for key in del_key_list:
            del self.map[key]
        
        # 重新计算属性
        for key, value in self.users.items():
            temp_value = self.recalculate_equipment_attribute(value)
            self.users[key] = self.recharge_occupation_attribute(temp_value)

    def save_user_information(self):
        dataManage.save_obj(self.users, user_path)
        dataManage.save_obj(self.rank, rank_path)

    # ==========================================
    # 配置信息获取
    def get_user(self, qq):
        today = str(datetime.date.today())
        if self.users.__contains__(qq) and qq != 0:
            if self.users[qq]['config']['last_handle'] != today:
                self.users[qq]['config']['last_handle'] = today
                self.users[qq]['config']['limit'] = {}  # 清除限购
                
                # 回复生命值
                if self.users[qq]['attribute']['own']['hp']['number'] < self.get_max_hp(self.users[qq]):
                    self.users[qq]['attribute']['own']['hp']['number'] += self.get_recovery_hp(self.users[qq])
                    if self.users[qq]['attribute']['own']['hp']['number'] > self.get_max_hp(self.users[qq]):
                        self.users[qq]['attribute']['own']['hp']['number'] = self.get_max_hp(self.users[qq])
                
                # 回复精神值
                if self.users[qq]['attribute']['own']['san']['number'] < self.get_max_san(self.users[qq]):
                    self.users[qq]['attribute']['own']['san']['number'] += self.get_recovery_san(self.users[qq])
                    if self.users[qq]['attribute']['own']['san']['number'] > self.get_max_san(self.users[qq]):
                        self.users[qq]['attribute']['own']['san']['number'] = self.get_max_san(self.users[qq])
                
                # 回复体力值
                if self.users[qq]['attribute']['own']['strength']['number'] < self.get_max_strength(self.users[qq]):
                    self.users[qq]['attribute']['own']['strength']['number'] += self.get_recovery_strength(self.users[qq])
                    if self.users[qq]['attribute']['own']['strength']['number'] > self.get_max_strength(self.users[qq]):
                        self.users[qq]['attribute']['own']['strength']['number'] = self.get_max_strength(self.users[qq])

            # 群系判断
            if not self.map.__contains__(self.users[qq]['config']['place']):
                init_map = []
                for key, value in self.map:
                    if self.map[key]['level'] == 0:
                        init_map.append(key)
                self.users[qq]['config']['place'] = random.choice(init_map)

            # buff判断
            del_buff_list = []
            for buff in self.users[qq]['buff']:
                if buff['type'] == 0 and buff['times'] <= 0:
                    del_buff_list.append(buff)
                if buff['type'] == 1 and is_beyond_deadline(buff['date']):
                    del_buff_list.append(buff)
            for buff in del_buff_list:
                self.users[qq]['buff'].remove(buff)

            self.save_user_information()
            return copy.deepcopy(self.users[qq])
        user = {
            'config': {
                'version': 0,  # 版本号
                'report': '',  # 迁移报告
                'qq': 0,  # qq号
                'name': '【未初始化】',  # 昵称
                'init_name': False,  # 是否有初始化昵称
                'date': getNow.toString(),  # 注册日期
                'sign': {
                    'last_date': '2021-8-1',  # 上一次签到的日期
                    'consecutive': 0,  # 连续签到的天数
                    'sum': 0  # 累计签到的天星术
                },
                'die_check': False,  # 死亡检验
                'place': '内测新手村',  # 当前所在的位置
                'born_place': '内测新手村',  # 出生地
                'last_handle': today,  # 上一次获取的时候
                'limit': {}  # 限购
            },
            'attribute': {
                'strengthen': {  # 强化
                    'attack': 0,
                    'armor': 0,
                    'speed': 0,
                    'hp': {
                        'recovery': 0,
                        'max': 0
                    },
                    'san': {
                        'recovery': 0,
                        'max': 0
                    },
                    'strength': {
                        'recovery': 0,
                        'max': 0
                    },
                    'times': 0
                },
                'own': {  # 玩家自己的属性
                    'gold': 0,
                    'attack': 1,
                    'armor': 1,
                    'speed': 100,
                    'hp': {
                        'number': 100,
                        'recovery': 100,
                        'max': 100
                    },
                    'san': {
                        'number': 100,
                        'recovery': 100,
                        'max': 100
                    },
                    'strength': {
                        'number': 20,
                        'recovery': 20,
                        'max': 300
                    },
                    'knapsack': 15
                },
                'equipment': {  # 装备带来的属性
                    'attack': 0,
                    'armor': 0,
                    'speed': 0,
                    'hp': {
                        'recovery': 0,
                        'max': 0
                    },
                    'san': {
                        'recovery': 0,
                        'max': 0
                    },
                    'strength': {
                        'recovery': 0,
                        'max': 0
                    },
                    'knapsack': 0
                },
                'skill': {  # 技能带来的属性
                    'attack': 0,
                    'armor': 0,
                    'speed': 0,
                    'hp': {
                        'recovery': 0,
                        'max': 0
                    },
                    'san': {
                        'recovery': 0,
                        'max': 0
                    },
                    'strength': {
                        'recovery': 0,
                        'max': 0
                    },
                    'knapsack': 0
                },
                'occupation': {  # 职业带来的属性
                    'attack': 0,
                    'armor': 0,
                    'speed': 0,
                    'hp': {
                        'recovery': 0,
                        'max': 0
                    },
                    'san': {
                        'recovery': 0,
                        'max': 0
                    },
                    'strength': {
                        'recovery': 0,
                        'max': 0
                    },
                    'knapsack': 0
                },
                'buff': {  # buff带来的属性
                    'attack': 0,
                    'armor': 0,
                    'speed': 0,
                    'hp': {
                        'recovery': 0,
                        'max': 0
                    },
                    'san': {
                        'recovery': 0,
                        'max': 0
                    },
                    'strength': {
                        'recovery': 0,
                        'max': 0
                    }
                }
            },
            'buff': [],  # 增减益效果
            'occupation': {  # 职业
                'work': '',
                'work_level': 1,  # 等级
                'farm': {
                    'max': 5,  # 农场的格子
                    'crop': []  # 作物
                },
                'fight': '',
                'fight_level': 1
            },
            'skill': {  # 技能
                'skill-1': None,
                'skill-2': None,
                'skill-3': None,
                'skill-4': None
            },
            'equipment': {  # 装备
                'arms': {},  # 武器
                'mask': {},  # 面具
                'hat': {},  # 头部
                'jacket': {},  # 身体
                'trousers': {},  # 裤子
                'shoes': {},  # 鞋子
                'ring': {},  # 戒指
                'necklace': {},  # 项链
                'knapsack': {},  # 背包
                'ornaments': {}  # 饰品
            },
            'warehouse': [],  # 背包
            'combat_data': {  # 战斗数据
                'PVP_victory': 0,
                'PVP_defeat': 0,
                'PVP_active': 0,
                'PVP_passive': 0,
                'PVE_victory': 0,
                'PVE_defeat': 0,
                'die': 0,
                'monster_kill': 0,
                'boss_kill': 0,
                'top_times': 0  # 登顶次数
            },
            'survival_data': {  # 生存数据
                'synthesis': 0,  # 合成物品数
                'decompose': 0,  # 分解物品数
                'change_occupation': 0,  # 转职次数
                'mining': 0,  # 挖矿次数
                'lumbering': 0,  # 伐木次数
                'hoarding': 0,  # 仓库内囤积的物品数
                'gift_give': 0,  # 赠送物品次数
                'gift_received': 0,  # 接受礼物的次数（群宠）
                'travel': 1  # 旅行次数
            },
            'achievement': {
                'synthesis': 0,  # 这是什么（合成物品数）
                'decompose': 0,  # 湮灭（分解物品数）
                'fully_armed': 0,  # 全副武装
                'human_sovereigns': 0,  # 人皇
                'boss_killer': 0,  # BOSS杀手
                'monster_kill': 0,  # 怪物杀手（击杀怪物数量）
                'almighty': 0,  # 全能达人
                'hunting_moment': 0,  # 猎杀时刻
                'miner': 0,  # 黄金矿工
                'lumberjack': 0,  # 伐木工
                'hamster': 0,  # 仓鼠
                'philanthropist': 0,  # 慈善家
                'popular': 0  # 群宠（接受的礼物数目）
            }
        }

        # 新手大礼包
        item = {
            'name': '复活药水',
            'number': 3,
            'enchanting': {
                'sharp': 0,
                'rapid': 0,
                'strong': 0
            }
        }
        user['warehouse'].append(copy.deepcopy(item))
        item = {
            'name': '甘霖',
            'number': 3,
            'enchanting': {
                'sharp': 0,
                'rapid': 0,
                'strong': 0
            }
        }
        user['warehouse'].append(copy.deepcopy(item))
        item = {
            'name': '晨露',
            'number': 3,
            'enchanting': {
                'sharp': 0,
                'rapid': 0,
                'strong': 0
            }
        }
        user['warehouse'].append(copy.deepcopy(item))


        init_map = []
        for key, value in self.map.items():
            if self.map[key]['level'] == 0:
                init_map.append(key)
        user['config']['place'] = random.choice(init_map)
        user['config']['born_place'] = user['config']['place']

        self.users[qq] = user
        self.save_user_information()
        return user

    def get_boss(self, name):
        boss = {
            'name': '',
            'attack': 0,
            'armor': 0,
            'speed': 0,
            'hp': 0
        }
        return boss

    def get_rank(self):
        return copy.deepcopy(self.rank)

    def get_monster(self, name):
        if self.monster.__contains__(name):
            return copy.deepcopy(self.monster[name])
        return None

    def get_goods_introduction(self, name):
        result = Result()
        introduction = {
            'init': False,
            'state': 'success',
            'name': '',
            'id': 0,
            'type': 0,
            'limit': 0,
            'cost': -1,
            'sell': -1,
            'enchanting': {
                'sharp': 0,
                'rapid': 0,
                'strong': 0
            },
            'attribute': {  # 装备带来的属性
                'attack': 0,
                'armor': 0,
                'speed': 0,
                'hp': {
                    'number': 0,
                    'recovery': 0,
                    'max': 0
                },
                'san': {
                    'number': 0,
                    'recovery': 0,
                    'max': 0
                },
                'strength': {
                    'number': 0,
                    'recovery': 0,
                    'max': 0
                },
                'knapsack': 0,
                'resurrection': 0,
                'gold': 0
            },
            'comments': '',
            'decompose': {
                'number': 0,
                'path': []
            },
            'synthesis': {
                'number': 0,
                'path': []
            },
            'forger_synthesis': {
                'number': 0,
                'level': 0,
                'path': []
            },
            'enchanter_synthesis': {  # 附魔师合成路线
                'number': 0,
                'level': 0,
                'path': []
            },
            'nurturer_synthesis': {  # 培育师合成路线
                'number': 0,
                'level': 0,
                'time': 0,
                'additional': [],
                'path': []
            }
        }

        check_id = -1
        if name.isdigit():
            check_id = int(name)
        elif name[:3] == 'id：' and name[3:].isdigit():
            check_id = int(name[3:])

        if check_id != -1:
            max = len(self.goods)
            if 0 < check_id <= max:
                for key, value in self.goods.items():
                    if value['id'] == check_id:
                        name = key
                        break

        if self.goods.__contains__(name):
            goods = self.get_goods(name)
            introduction['init'] = True
            introduction['name'] = name
            introduction['id'] = goods['id']
            introduction['type'] = goods['type']
            introduction['limit'] = goods['limit']
            introduction['cost'] = goods['cost']
            introduction['sell'] = goods['sell']
            introduction['comments'] = goods['comments']

            introduction['enchanting']['sharp'] = goods['enchanting-sharp']
            introduction['enchanting']['rapid'] = goods['enchanting-rapid']
            introduction['enchanting']['strong'] = goods['enchanting-strong']

            introduction['attribute']['resurrection'] = goods['resurrection']
            introduction['attribute']['gold'] = goods['gold']

            introduction['attribute']['attack'] = goods['attack']
            introduction['attribute']['armor'] = goods['armor']
            introduction['attribute']['speed'] = goods['speed']
            introduction['attribute']['knapsack'] = goods['knapsack']

            introduction['attribute']['hp']['number'] = goods['hp']
            introduction['attribute']['hp']['recovery'] = goods['hp-recovery']
            introduction['attribute']['hp']['max'] = goods['hp-max']

            introduction['attribute']['san']['number'] = goods['san']
            introduction['attribute']['san']['recovery'] = goods['san-recovery']
            introduction['attribute']['san']['max'] = goods['san-max']

            introduction['attribute']['strength']['number'] = goods['strength']
            introduction['attribute']['strength']['recovery'] = goods['strength-recovery']
            introduction['attribute']['strength']['max'] = goods['strength-max']

            if self.forger_synthesis.__contains__(name):
                introduction['forger_synthesis'] = self.forger_synthesis[name]
            if self.enchanter_synthesis.__contains__(name):
                introduction['enchanter_synthesis'] = self.enchanter_synthesis[name]
            if self.nurturer_synthesis.__contains__(name):
                introduction['nurturer_synthesis'] = self.nurturer_synthesis[name]

            if self.synthesis.__contains__(name):
                introduction['synthesis'] = self.synthesis[name]
            if self.decompose.__contains__(name):
                introduction['decompose'] = self.decompose[name]

            result.append_introduction(introduction)
        elif self.monster.__contains__(name):
                monster_introduction = {
                    'init': True,
                    'name': '',
                    'level': 0,
                    'attack': 0,
                    'armor': 0,
                    'speed': 0,
                    'hp': 0,
                    'element': '',  # 元素
                    'comments': '',
                    'spoils': []
                }
                monster_introduction['name'] = name
                monster_introduction['level'] = self.monster[name]['level']
                monster_introduction['attack'] = self.monster[name]['attack']
                monster_introduction['armor'] = self.monster[name]['armor']
                monster_introduction['speed'] = self.monster[name]['speed']
                monster_introduction['hp'] = self.monster[name]['hp']
                monster_introduction['element'] = self.monster[name]['element']
                monster_introduction['comments'] = self.monster[name]['comments']
                monster_introduction['spoils'] = self.monster[name]['spoils']
                result.append_monster_introduction(monster_introduction)
        else:
            if '，' not in name and '。' not in name and '/' not in name and '？' not in name and '！' not in name and '呗' not in name:
                introduction['init'] = True
                introduction['state'] = 'unknown'
                result.append_introduction(introduction)

        return result

    def get_goods(self, name):
        if self.goods.__contains__(name):
            return copy.deepcopy(self.goods[name])
        return None

    def get_shop(self):
        return copy.deepcopy(self.shop)

    def get_soul_shop(self):
        return copy.deepcopy(self.soul_shop)

    def get_synthesis(self):
        return copy.deepcopy(self.synthesis)
        
    def get_decompose(self):
        return copy.deepcopy(self.decompose)
        
    def get_forger_synthesis(self):
        return copy.deepcopy(self.forger_synthesis)
        
    def get_nurturer_synthesis(self):
        return copy.deepcopy(self.nurturer_synthesis)
        
    def get_enchanter_synthesis(self):
        return copy.deepcopy(self.enchanter_synthesis)

    # ==========================================
    # 数据获取
    def get_attack(self, user):
        return user['attribute']['strengthen']['attack'] + user['attribute']['own']['attack'] + \
               user['attribute']['equipment']['attack'] + user['attribute']['skill']['attack'] + \
               user['attribute']['occupation']['attack'] + user['attribute']['buff']['attack']

    def get_armor(self, user):
        return user['attribute']['strengthen']['armor'] + user['attribute']['own']['armor'] + \
               user['attribute']['equipment']['armor'] + user['attribute']['skill']['armor'] + \
               user['attribute']['occupation']['armor'] + user['attribute']['buff']['armor']

    def get_speed(self, user):
        return user['attribute']['strengthen']['speed'] + user['attribute']['own']['speed'] + \
               user['attribute']['equipment']['speed'] + user['attribute']['skill']['speed'] + \
               user['attribute']['occupation']['speed'] + user['attribute']['buff']['speed']

    def get_max_strength(self, user):
        return user['attribute']['strengthen']['strength']['max'] + user['attribute']['own']['strength']['max'] + \
               user['attribute']['equipment']['strength']['max'] + user['attribute']['skill']['strength']['max'] + \
               user['attribute']['occupation']['strength']['max'] + user['attribute']['buff']['strength']['max']

    def get_recovery_strength(self, user):
        return user['attribute']['strengthen']['strength']['recovery'] + user['attribute']['own']['strength'][
            'recovery'] + user['attribute']['equipment']['strength']['recovery'] + \
               user['attribute']['skill']['strength']['recovery'] + user['attribute']['occupation']['strength'][
                   'recovery'] + user['attribute']['buff']['strength']['recovery']

    def get_max_hp(self, user):
        return user['attribute']['strengthen']['hp']['max'] + user['attribute']['own']['hp']['max'] + \
               user['attribute']['equipment']['hp']['max'] + user['attribute']['skill']['hp']['max'] + \
               user['attribute']['occupation']['hp']['max'] + user['attribute']['buff']['hp']['max']

    def get_recovery_hp(self, user):
        return user['attribute']['strengthen']['hp']['recovery'] + user['attribute']['own']['hp']['recovery'] + \
               user['attribute']['equipment']['hp']['recovery'] + user['attribute']['skill']['hp']['recovery'] + \
               user['attribute']['occupation']['hp']['recovery'] + user['attribute']['buff']['hp']['recovery']

    def get_max_san(self, user):
        return user['attribute']['strengthen']['san']['max'] + user['attribute']['own']['san']['max'] + \
               user['attribute']['equipment']['san']['max'] + user['attribute']['skill']['san']['max'] + \
               user['attribute']['occupation']['san']['max'] + user['attribute']['buff']['san']['max']

    def get_recovery_san(self, user):
        return user['attribute']['strengthen']['san']['recovery'] + user['attribute']['own']['san']['recovery'] + \
               user['attribute']['equipment']['san']['recovery'] + user['attribute']['skill']['san']['recovery'] + \
               user['attribute']['occupation']['san']['recovery'] + user['attribute']['buff']['san']['recovery']

    def get_max_knapsack(self, user):
        return user['attribute']['own']['knapsack'] + user['attribute']['equipment']['knapsack'] + \
               user['attribute']['skill']['knapsack'] + user['attribute']['occupation']['knapsack']

    def get_knapsack(self, user):
        return user['warehouse']

    def get_PVP_times(self, user):
        return user['combat_data']['PVP_victory'] + user['combat_data']['PVP_defeat']

    def get_PVP_rate(self, user):
        sum = self.get_PVP_times(user)
        if sum != 0:
            return int(float(user['combat_data']['PVP_victory']) / float(sum) * 100)
        else:
            return 0

    def get_PVE_times(self, user):
        return user['combat_data']['PVE_victory'] + user['combat_data']['PVE_defeat']

    def get_PVE_rate(self, user):
        sum = self.get_PVE_times(user)
        if sum != 0:
            return int(float(user['combat_data']['PVE_victory']) / float(sum) * 100)
        else:
            return 0

    def get_achievement_number(self, user):
        number = 0
        if user['achievement']['synthesis'] != 0:
            number += 1
        if user['achievement']['decompose'] != 0:
            number += 1
        if user['achievement']['fully_armed'] != 0:
            number += 1
        if user['achievement']['human_sovereigns'] != 0:
            number += 1
        if user['achievement']['boss_killer'] != 0:
            number += 1
        if user['achievement']['monster_kill'] != 0:
            number += 1
        if user['achievement']['almighty'] != 0:
            number += 1
        if user['achievement']['hunting_moment'] != 0:
            number += 1
        if user['achievement']['miner'] != 0:
            number += 1
        if user['achievement']['lumberjack'] != 0:
            number += 1
        if user['achievement']['hamster'] != 0:
            number += 1
        if user['achievement']['philanthropist'] != 0:
            number += 1
        if user['achievement']['popular'] != 0:
            number += 1
        return number

    # ==========================================
    # 基本操作

    # 数据更新
    def update(self, qq, new_user, result):
        # 一系列判定
        new_user = self.recalculate_equipment_attribute(new_user)
        user = self.get_user(qq)
        gold_gap = new_user['attribute']['own']['gold'] - user['attribute']['own']['gold']

        # 有收益行为
        if gold_gap > 0:
            reply, level, new_user = self.remove_buff('双倍积分收益', new_user)
            if reply:
                double_gold = {  # 双倍积分收益
                    'init': True,
                    'state': 'success',
                    'level': level,
                    'gold': 0
                }
                rand = random.randint(0, 99)
                if rand < level * 10:
                    double_gold['gold'] = gold_gap
                    new_user['attribute']['own']['gold'] += gold_gap
                    gold_gap *= 2
                else:
                    double_gold['state'] = 'nothing'
                result.append_double_gold(double_gold)

            reply, level, new_user = self.remove_buff('减半积分收益', new_user)
            if reply:
                half_gold = {  # 减半积分收益
                    'init': True,
                    'state': 'success',
                    'level': level,
                    'gold': 0
                }
                rand = random.randint(0, 99)
                if rand < level * 10:
                    temp = int(gold_gap / 2)
                    half_gold['gold'] = temp
                    new_user['attribute']['own']['gold'] -= temp
                    gold_gap -= temp
                else:
                    half_gold['state'] = 'nothing'
                result.append_half_gold(half_gold)


        # 有消耗体力的行为
        if new_user['attribute']['own']['strength']['number'] < user['attribute']['own']['strength']['number']:
            reply, level, new_user = self.remove_buff('中毒', new_user)
            if reply:
                poisoning = {  # 中毒
                    'init': True,
                    'state': 'success',
                    'level': level,
                    'hp': level
                }
                new_user['attribute']['own']['hp']['number'] -= level
                if new_user['attribute']['own']['hp']['number'] < 0:
                    user['config']['die_check'] = True
                    poisoning['state'] = 'die'
                    poisoning['hp'] -= new_user['attribute']['own']['hp']['number']
                    new_user['attribute']['own']['hp']['number'] = 0
                    new_user['combat_data']['die'] += 1
                result.append_poisoning(poisoning)
                
            reply, level, new_user = self.remove_buff('麻痹', new_user)
            if reply:
                paralysis = {  # 麻痹
                    'init': True,
                    'state': 'success',
                    'level': level,
                    'strength': level
                }
                rand = random.randint(0, 99)
                if rand < level * 10:
                    new_user['attribute']['own']['strength']['number'] -= level
                    if new_user['attribute']['own']['strength']['number'] < 0:
                        paralysis['strength'] -= new_user['attribute']['own']['strength']['number']
                        new_user['attribute']['own']['strength']['number'] = 0
                else:
                    paralysis['state'] = 'nothing'
                result.append_paralysis(paralysis)

        # 有改变地点的行为
        if new_user['config']['place'] != user['config']['place']:
            new_user['survival_data']['travel'] += 1
        
        # 死亡结算
        if new_user['config']['die_check']:
            new_user['config']['die_check'] = False
            die_check = {  # 死亡结算
                'init': True,
                'state': 'return'
            }
            if new_user['equipment']['ornaments'] != {} and new_user['equipment']['ornaments']['name'] == '不死图腾':
                new_user['equipment']['ornaments'] = {}
                new_user = self.recalculate_equipment_attribute(new_user)

                new_user['attribute']['own']['hp']['number'] = self.get_max_hp(new_user)
                die_check['state'] = '不死图腾'
            else:
                new_user['config']['place'] = new_user['config']['born_place']
            result.append_die_check(die_check)

        # ==========================
        # 排行榜计算
        # 旅行之地判断
        if qq != self.rank['travel']:
            temp_user = self.get_user(self.rank['travel'])
            if new_user['survival_data']['travel'] > temp_user['survival_data']['travel']:
                self.rank['travel'] = qq
            elif self.rank['travel'] == 0:
                self.rank['travel'] = qq
        
        # 击剑数目判断
        if qq != self.rank['fencing_master']:
            temp_user = self.get_user(self.rank['fencing_master'])
            if self.get_PVP_times(new_user) > self.get_PVP_times(temp_user):
                self.rank['fencing_master'] = qq
        
        # 被击剑数目判断
        if qq != self.rank['be_fenced']:
            temp_user = self.get_user(self.rank['be_fenced'])
            if new_user['combat_data']['PVP_passive'] > temp_user['combat_data']['PVP_passive']:
                self.rank['be_fenced'] = qq

        # 登顶次数判断
        if qq != self.rank['ascents']:
            temp_user = self.get_user(self.rank['ascents'])
            if new_user['combat_data']['top_times'] > temp_user['combat_data']['top_times']:
                self.rank['ascents'] = qq

        # 杀怪数量判断
        if qq != self.rank['monster']:
            temp_user = self.get_user(self.rank['monster'])
            if new_user['combat_data']['monster_kill'] > temp_user['combat_data']['monster_kill']:
                self.rank['monster'] = qq
                
        # 杀怪数量判断
        if qq != self.rank['die']:
            temp_user = self.get_user(self.rank['die'])
            if new_user['combat_data']['die'] > temp_user['combat_data']['die']:
                self.rank['die'] = qq
        
        if self.get_PVP_times(new_user) > 100:
            # 胜率判断
            if qq != self.rank['rate']['over100']:
                temp_user = self.get_user(self.rank['rate']['over100'])
                if self.get_PVP_rate(new_user) > self.get_PVP_rate(temp_user):
                    self.rank['rate']['over100'] = qq
        # 胜率判断
        if qq != self.rank['rate']['all']:
            temp_user = self.get_user(self.rank['rate']['all'])
            if self.get_PVP_rate(new_user) > self.get_PVP_rate(temp_user):
                self.rank['rate']['all'] = qq

        # 积分判断
        if gold_gap > 0:
            if qq == self.rank['gold']['1']:  # 如果本来是第一那么往上升就无所谓
                pass
            elif qq == self.rank['gold']['2']:
                temp_user = self.get_user(self.rank['gold']['1'])
                if temp_user['attribute']['own']['gold'] < new_user['attribute']['own']['gold']:
                    self.rank['gold']['2'] = self.rank['gold']['1']
                    self.rank['gold']['1'] = qq

                    new_user['combat_data']['top_times'] += 1
            elif qq == self.rank['gold']['3']:  # 如果本来是第三往上升
                temp_user = self.get_user(self.rank['gold']['1'])
                temp_user2 = self.get_user(self.rank['gold']['2'])
                if temp_user['attribute']['own']['gold'] < new_user['attribute']['own']['gold']:
                    self.rank['gold']['3'] = self.rank['gold']['2']
                    self.rank['gold']['2'] = self.rank['gold']['1']
                    self.rank['gold']['1'] = qq
                elif temp_user2['attribute']['own']['gold'] < new_user['attribute']['own']['gold']:
                    self.rank['gold']['3'] = self.rank['gold']['2']
                    self.rank['gold']['2'] = qq
            else:
                temp_user = self.get_user(self.rank['gold']['1'])
                temp_user2 = self.get_user(self.rank['gold']['2'])
                temp_user3 = self.get_user(self.rank['gold']['3'])
                if temp_user['attribute']['own']['gold'] < new_user['attribute']['own']['gold']:
                    self.rank['gold']['3'] = self.rank['gold']['2']
                    self.rank['gold']['2'] = self.rank['gold']['1']
                    self.rank['gold']['1'] = qq
                elif temp_user2['attribute']['own']['gold'] < new_user['attribute']['own']['gold']:
                    self.rank['gold']['3'] = self.rank['gold']['2']
                    self.rank['gold']['2'] = qq
                elif temp_user3['attribute']['own']['gold'] < new_user['attribute']['own']['gold']:
                    self.rank['gold']['3'] = qq
        elif gold_gap < 0:
            if qq == self.rank['gold']['1'] or qq == self.rank['gold']['2'] or qq == self.rank['gold']['3']: # 如果不是榜上的人掉积分无所谓
                gold_qq = [0, 0, 0]
                gold_number = [0, 0, 0]
                for key, value in self.users.items():
                    if value['attribute']['own']['gold'] > gold_number[0]:
                        gold_qq[2] = gold_qq[1]
                        gold_number[2] = gold_number[1]

                        gold_qq[1] = gold_qq[0]
                        gold_number[1] = gold_number[0]

                        gold_qq[0] = key
                        gold_number[0] = value['attribute']['own']['gold']
                    elif value['attribute']['own']['gold'] > gold_number[1]:
                        gold_qq[2] = gold_qq[1]
                        gold_number[2] = gold_number[1]

                        gold_qq[1] = key
                        gold_number[1] = value['attribute']['own']['gold']
                    elif value['attribute']['own']['gold'] > gold_number[2]:
                        gold_qq[2] = key
                        gold_number[2] = value['attribute']['own']['gold']
                if self.rank['gold']['1'] != gold_qq[0]:
                    self.users[gold_qq[0]]['combat_data']['top_times'] += 1
                self.rank['gold']['1'] = gold_qq[0]
                self.rank['gold']['2'] = gold_qq[1]
                self.rank['gold']['3'] = gold_qq[2]

        new_user, result = self.achievement_check(new_user, result)
        self.users[qq] = new_user
        self.save_user_information()
        return result

    # 成就检查
    def achievement_check(self, user, result):
        achievement = {  # 达成成就
            'init': True,
            'state': 'success',
            'achievement': {
                'synthesis': 0,  # 这是什么（合成物品数）
                'decompose': 0,  # 湮灭（分解物品数）
                'fully_armed': 0,  # 全副武装
                'human_sovereigns': 0,  # 人皇
                'boss_killer': 0,  # BOSS杀手
                'monster_kill': 0,  # 怪物杀手（击杀怪物数量）
                'almighty': 0,  # 全能达人
                'hunting_moment': 0,  # 猎杀时刻
                'miner': 0,  # 黄金矿工
                'lumberjack': 0,  # 伐木工
                'hamster': 0,  # 仓鼠
                'philanthropist': 0,  # 慈善家
                'popular': 0  # 群宠（接受的礼物数目）
            }
        }

        # 这是什么
        if user['survival_data']['synthesis'] >= 1000:
            if user['achievement']['synthesis'] < 5:
                user['achievement']['synthesis'] = 5
                achievement['achievement']['synthesis'] = 5
        elif user['survival_data']['synthesis'] >= 500:
            if user['achievement']['synthesis'] < 4:
                user['achievement']['synthesis'] = 4
                achievement['achievement']['synthesis'] = 4
        elif user['survival_data']['synthesis'] >= 100:
            if user['achievement']['synthesis'] < 3:
                user['achievement']['synthesis'] = 3
                achievement['achievement']['synthesis'] = 3
        elif user['survival_data']['synthesis'] >= 10:
            if user['achievement']['synthesis'] < 2:
                user['achievement']['synthesis'] = 2
                achievement['achievement']['synthesis'] = 2
        elif user['survival_data']['synthesis'] >= 1:
            if user['achievement']['synthesis'] < 1:
                user['achievement']['synthesis'] = 1
                achievement['achievement']['synthesis'] = 1

        # 湮灭
        if user['survival_data']['decompose'] >= 1000:
            if user['achievement']['decompose'] < 5:
                user['achievement']['decompose'] = 5
                achievement['achievement']['decompose'] = 5
        elif user['survival_data']['decompose'] >= 500:
            if user['achievement']['decompose'] < 4:
                user['achievement']['decompose'] = 4
                achievement['achievement']['decompose'] = 4
        elif user['survival_data']['decompose'] >= 100:
            if user['achievement']['decompose'] < 3:
                user['achievement']['decompose'] = 3
                achievement['achievement']['decompose'] = 3
        elif user['survival_data']['decompose'] >= 10:
            if user['achievement']['decompose'] < 2:
                user['achievement']['decompose'] = 2
                achievement['achievement']['decompose'] = 2
        elif user['survival_data']['decompose'] >= 1:
            if user['achievement']['decompose'] < 1:
                user['achievement']['decompose'] = 1
                achievement['achievement']['decompose'] = 1

        # BOSS杀手
        if user['combat_data']['boss_kill'] >= 100:
            if user['achievement']['boss_killer'] < 3:
                user['achievement']['boss_killer'] = 3
                achievement['achievement']['boss_killer'] = 3
        elif user['combat_data']['boss_kill'] >= 10:
            if user['achievement']['boss_killer'] < 2:
                user['achievement']['boss_killer'] = 2
                achievement['achievement']['boss_killer'] = 2
        elif user['combat_data']['boss_kill'] >= 1:
            if user['achievement']['boss_killer'] < 1:
                user['achievement']['boss_killer'] = 1
                achievement['achievement']['boss_killer'] = 1
                
        # 怪物杀手
        if user['combat_data']['monster_kill'] >= 10000:
            if user['achievement']['monster_kill'] < 5:
                user['achievement']['monster_kill'] = 5
                achievement['achievement']['monster_kill'] = 5
        elif user['combat_data']['monster_kill'] >= 1000:
            if user['achievement']['monster_kill'] < 4:
                user['achievement']['monster_kill'] = 4
                achievement['achievement']['monster_kill'] = 4
        elif user['combat_data']['monster_kill'] >= 500:
            if user['achievement']['monster_kill'] < 3:
                user['achievement']['monster_kill'] = 3
                achievement['achievement']['monster_kill'] = 3
        elif user['combat_data']['monster_kill'] >= 100:
            if user['achievement']['monster_kill'] < 2:
                user['achievement']['monster_kill'] = 2
                achievement['achievement']['monster_kill'] = 2
        elif user['combat_data']['monster_kill'] >= 10:
            if user['achievement']['monster_kill'] < 1:
                user['achievement']['monster_kill'] = 1
                achievement['achievement']['monster_kill'] = 1

        # 全能达人
        if user['survival_data']['change_occupation'] >= 10:
            if user['achievement']['almighty'] < 3:
                user['achievement']['almighty'] = 3
                achievement['achievement']['almighty'] = 3
        elif user['survival_data']['change_occupation'] >= 5:
            if user['achievement']['almighty'] < 2:
                user['achievement']['almighty'] = 2
                achievement['achievement']['almighty'] = 2
        elif user['survival_data']['change_occupation'] >= 1:
            if user['achievement']['almighty'] < 1:
                user['achievement']['almighty'] = 1
                achievement['achievement']['almighty'] = 1

        # 猎杀时刻
        if self.get_PVP_times(user) >= 10000:
            if user['achievement']['hunting_moment'] < 5:
                user['achievement']['hunting_moment'] = 5
                achievement['achievement']['hunting_moment'] = 5
        elif self.get_PVP_times(user) >= 1000:
            if user['achievement']['hunting_moment'] < 4:
                user['achievement']['hunting_moment'] = 4
                achievement['achievement']['hunting_moment'] = 4
        elif self.get_PVP_times(user) >= 500:
            if user['achievement']['hunting_moment'] < 3:
                user['achievement']['hunting_moment'] = 3
                achievement['achievement']['hunting_moment'] = 3
        elif self.get_PVP_times(user) >= 100:
            if user['achievement']['hunting_moment'] < 2:
                user['achievement']['hunting_moment'] = 2
                achievement['achievement']['hunting_moment'] = 2
        elif self.get_PVP_times(user) >= 10:
            if user['achievement']['hunting_moment'] < 1:
                user['achievement']['hunting_moment'] = 1
                achievement['achievement']['hunting_moment'] = 1

        # 伐木工
        if user['survival_data']['lumbering'] >= 10000:
            if user['achievement']['lumberjack'] < 4:
                user['achievement']['lumberjack'] = 4
                achievement['achievement']['lumberjack'] = 4
        elif user['survival_data']['lumbering'] >= 1000:
            if user['achievement']['lumberjack'] < 3:
                user['achievement']['lumberjack'] = 3
                achievement['achievement']['lumberjack'] = 3
        elif user['survival_data']['lumbering'] >= 100:
            if user['achievement']['lumberjack'] < 2:
                user['achievement']['lumberjack'] = 2
                achievement['achievement']['lumberjack'] = 2
        elif user['survival_data']['lumbering'] >= 10:
            if user['achievement']['lumberjack'] < 1:
                user['achievement']['lumberjack'] = 1
                achievement['achievement']['lumberjack'] = 1
 
        # 黄金矿工
        if user['survival_data']['mining'] >= 10000:
            if user['achievement']['miner'] < 4:
                user['achievement']['miner'] = 4
                achievement['achievement']['miner'] = 4
        elif user['survival_data']['mining'] >= 1000:
            if user['achievement']['miner'] < 3:
                user['achievement']['miner'] = 3
                achievement['achievement']['miner'] = 3
        elif user['survival_data']['mining'] >= 100:
            if user['achievement']['miner'] < 2:
                user['achievement']['miner'] = 2
                achievement['achievement']['miner'] = 2
        elif user['survival_data']['mining'] >= 10:
            if user['achievement']['miner'] < 1:
                user['achievement']['miner'] = 1
                achievement['achievement']['miner'] = 1

        # 慈善家
        if user['survival_data']['gift_give'] >= 100:
            if user['achievement']['philanthropist'] < 3:
                user['achievement']['philanthropist'] = 3
                achievement['achievement']['philanthropist'] = 3
        elif user['survival_data']['gift_give'] >= 10:
            if user['achievement']['philanthropist'] < 2:
                user['achievement']['philanthropist'] = 2
                achievement['achievement']['philanthropist'] = 2
        elif user['survival_data']['gift_give'] >= 1:
            if user['achievement']['philanthropist'] < 1:
                user['achievement']['philanthropist'] = 1
                achievement['achievement']['philanthropist'] = 1

        # 群宠
        if user['survival_data']['gift_received'] >= 100:
            if user['achievement']['popular'] < 3:
                user['achievement']['popular'] = 3
                achievement['achievement']['popular'] = 3
        elif user['survival_data']['gift_received'] >= 10:
            if user['achievement']['popular'] < 2:
                user['achievement']['popular'] = 2
                achievement['achievement']['popular'] = 2
        elif user['survival_data']['gift_received'] >= 1:
            if user['achievement']['popular'] < 1:
                user['achievement']['popular'] = 1
                achievement['achievement']['popular'] = 1

        # 全副武装
        flag = True
        for key, value in user['equipment'].items():
            if value == {}:
                flag = False
                break
        if flag:
            if user['achievement']['fully_armed'] < 1:
                user['achievement']['fully_armed'] = 1
                achievement['achievement']['fully_armed'] = 1

        # 仓鼠
        number = 0
        for value in user['warehouse']:
            number += value['number']
        if number >= 10000:
            if user['achievement']['hamster'] < 5:
                user['achievement']['hamster'] = 5
                achievement['achievement']['hamster'] = 5
        elif number >= 5000:
            if user['achievement']['hamster'] < 4:
                user['achievement']['hamster'] = 4
                achievement['achievement']['hamster'] = 4
        elif number >= 1000:
            if user['achievement']['hamster'] < 3:
                user['achievement']['hamster'] = 3
                achievement['achievement']['hamster'] = 3
        elif number >= 500:
            if user['achievement']['hamster'] < 2:
                user['achievement']['hamster'] = 2
                achievement['achievement']['hamster'] = 2
        elif number >= 100:
            if user['achievement']['hamster'] < 1:
                user['achievement']['hamster'] = 1
                achievement['achievement']['hamster'] = 1

        result.append_achievement(achievement)
        return user, result

    # 获得物品
    def get_items(self, user, items):
        reply = False

        if not self.goods.__contains__(items['name']):
            return False, user

        # 物品堆叠判断
        for index in range(len(user['warehouse'])):
            value = user['warehouse'][index]
            if value['name'] == items['name']:
                if value['enchanting']['sharp'] != items['enchanting']['sharp']:
                    continue
                if value['enchanting']['rapid'] != items['enchanting']['rapid']:
                    continue
                if value['enchanting']['strong'] != items['enchanting']['strong']:
                    continue
                
                reply = True
                user['warehouse'][index]['number'] += items['number']
        
        # 看能否新增物品
        if not reply:
            if len(user['warehouse']) < self.get_max_knapsack(user):
                reply = True
                user['warehouse'].append(items)
        
        return reply, user

    # 删除物品
    def remove_items(self, user, items):
        reply = 2

        for index in range(len(user['warehouse'])):
            value = user['warehouse'][index]
            if value['name'] == items['name']:
                if value['enchanting']['sharp'] != items['enchanting']['sharp']:
                    continue
                if value['enchanting']['rapid'] != items['enchanting']['rapid']:
                    continue
                if value['enchanting']['strong'] != items['enchanting']['strong']:
                    continue
                
                if user['warehouse'][index]['number'] >= items['number']:
                    reply = 0
                    user['warehouse'][index]['number'] -= items['number']
                    if user['warehouse'][index]['number'] == 0:
                        del user['warehouse'][index]
                    break
                else:
                    reply = 1

        return reply, user

    # 获得buff
    def get_buff(self, user, buff):
        valid_name = ['无敌', '进攻', '防御', '双倍积分收益', '减半积分收益', '中毒', '麻痹', '英勇', '圣光祝福']
        reply = False

        if buff['name'] in valid_name:
            for index in range(len(user['buff'])):
                if user['buff'][index]['name'] == buff['name'] and buff['type'] == user['buff'][index]['type'] and buff['level'] == user['buff'][index]['level']:
                    reply = True
                    if buff['type'] == 0:
                        user['buff'][index]['times'] += buff['times']
                    else:
                        if is_greater_date(buff['date'], user['buff'][index]['date']):
                            user['buff'][index]['date'] = buff['date']
            if not reply:
                reply = True
                user['buff'].append(buff)
        return reply, user

    # 名字重复性检验
    def name_check(self, name):
        for key, value in self.users.items():
            if name == value['config']['name']:
                return True
        return False

    # 重新计算装备属性
    def recalculate_equipment_attribute(self, user):
        equipment = {  # 装备
            'attack': 0,
            'armor': 0,
            'speed': 0,
            'hp': {
                'recovery': 0,
                'max': 0
            },
            'san': {
                'recovery': 0,
                'max': 0
            },
            'strength': {
                'recovery': 0,
                'max': 0
            },
            'knapsack': 0
        }

        enchanting = {
            'sharp': 0,
            'rapid': 0,
            'strong': 0
        }

        if user['equipment']['arms'] != {} and self.goods.__contains__(user['equipment']['arms']['name']):
            name = user['equipment']['arms']['name']
            equipment['attack'] += self.goods[name]['attack']
            equipment['armor'] += self.goods[name]['armor']
            equipment['speed'] += self.goods[name]['speed']
            equipment['knapsack'] += self.goods[name]['knapsack']

            equipment['hp']['recovery'] += self.goods[name]['hp-recovery']
            equipment['hp']['max'] += self.goods[name]['hp-max']

            equipment['san']['recovery'] += self.goods[name]['san-recovery']
            equipment['san']['max'] += self.goods[name]['san-max']

            equipment['strength']['recovery'] += self.goods[name]['strength-recovery']
            equipment['strength']['max'] += self.goods[name]['strength-max']

            enchanting['sharp'] += user['equipment']['arms']['enchanting']['sharp']
            enchanting['rapid'] += user['equipment']['arms']['enchanting']['rapid']
            enchanting['strong'] += user['equipment']['arms']['enchanting']['strong']

        if user['equipment']['mask'] != {} and self.goods.__contains__(user['equipment']['mask']['name']):
            name = user['equipment']['mask']['name']
            equipment['attack'] += self.goods[name]['attack']
            equipment['armor'] += self.goods[name]['armor']
            equipment['speed'] += self.goods[name]['speed']
            equipment['knapsack'] += self.goods[name]['knapsack']

            equipment['hp']['recovery'] += self.goods[name]['hp-recovery']
            equipment['hp']['max'] += self.goods[name]['hp-max']

            equipment['san']['recovery'] += self.goods[name]['san-recovery']
            equipment['san']['max'] += self.goods[name]['san-max']

            equipment['strength']['recovery'] += self.goods[name]['strength-recovery']
            equipment['strength']['max'] += self.goods[name]['strength-max']
            name = user['equipment']['arms']['name']
            equipment['attack'] += self.goods[name]['attack']
            equipment['armor'] += self.goods[name]['armor']
            equipment['speed'] += self.goods[name]['speed']
            equipment['knapsack'] += self.goods[name]['knapsack']

            equipment['hp']['recovery'] += self.goods[name]['hp-recovery']
            equipment['hp']['max'] += self.goods[name]['hp-max']

            equipment['san']['recovery'] += self.goods[name]['san-recovery']
            equipment['san']['max'] += self.goods[name]['san-max']

            equipment['strength']['recovery'] += self.goods[name]['strength-recovery']
            equipment['strength']['max'] += self.goods[name]['strength-max']

            enchanting['sharp'] += user['equipment']['mask']['enchanting']['sharp']
            enchanting['rapid'] += user['equipment']['mask']['enchanting']['rapid']
            enchanting['strong'] += user['equipment']['mask']['enchanting']['strong']

        if user['equipment']['hat'] != {} and self.goods.__contains__(user['equipment']['hat']['name']):
            name = user['equipment']['hat']['name']
            equipment['attack'] += self.goods[name]['attack']
            equipment['armor'] += self.goods[name]['armor']
            equipment['speed'] += self.goods[name]['speed']
            equipment['knapsack'] += self.goods[name]['knapsack']

            equipment['hp']['recovery'] += self.goods[name]['hp-recovery']
            equipment['hp']['max'] += self.goods[name]['hp-max']

            equipment['san']['recovery'] += self.goods[name]['san-recovery']
            equipment['san']['max'] += self.goods[name]['san-max']

            equipment['strength']['recovery'] += self.goods[name]['strength-recovery']
            equipment['strength']['max'] += self.goods[name]['strength-max']

            enchanting['sharp'] += user['equipment']['hat']['enchanting']['sharp']
            enchanting['rapid'] += user['equipment']['hat']['enchanting']['rapid']
            enchanting['strong'] += user['equipment']['hat']['enchanting']['strong']

        if user['equipment']['jacket'] != {} and self.goods.__contains__(user['equipment']['jacket']['name']):
            name = user['equipment']['jacket']['name']
            equipment['attack'] += self.goods[name]['attack']
            equipment['armor'] += self.goods[name]['armor']
            equipment['speed'] += self.goods[name]['speed']
            equipment['knapsack'] += self.goods[name]['knapsack']

            equipment['hp']['recovery'] += self.goods[name]['hp-recovery']
            equipment['hp']['max'] += self.goods[name]['hp-max']

            equipment['san']['recovery'] += self.goods[name]['san-recovery']
            equipment['san']['max'] += self.goods[name]['san-max']

            equipment['strength']['recovery'] += self.goods[name]['strength-recovery']
            equipment['strength']['max'] += self.goods[name]['strength-max']

            enchanting['sharp'] += user['equipment']['jacket']['enchanting']['sharp']
            enchanting['rapid'] += user['equipment']['jacket']['enchanting']['rapid']
            enchanting['strong'] += user['equipment']['jacket']['enchanting']['strong']
            
        if user['equipment']['trousers'] != {} and self.goods.__contains__(user['equipment']['trousers']['name']):
            name = user['equipment']['trousers']['name']
            equipment['attack'] += self.goods[name]['attack']
            equipment['armor'] += self.goods[name]['armor']
            equipment['speed'] += self.goods[name]['speed']
            equipment['knapsack'] += self.goods[name]['knapsack']

            equipment['hp']['recovery'] += self.goods[name]['hp-recovery']
            equipment['hp']['max'] += self.goods[name]['hp-max']

            equipment['san']['recovery'] += self.goods[name]['san-recovery']
            equipment['san']['max'] += self.goods[name]['san-max']

            equipment['strength']['recovery'] += self.goods[name]['strength-recovery']
            equipment['strength']['max'] += self.goods[name]['strength-max']

            enchanting['sharp'] += user['equipment']['trousers']['enchanting']['sharp']
            enchanting['rapid'] += user['equipment']['trousers']['enchanting']['rapid']
            enchanting['strong'] += user['equipment']['trousers']['enchanting']['strong']
            
        if user['equipment']['shoes'] != {} and self.goods.__contains__(user['equipment']['shoes']['name']):
            name = user['equipment']['shoes']['name']
            equipment['attack'] += self.goods[name]['attack']
            equipment['armor'] += self.goods[name]['armor']
            equipment['speed'] += self.goods[name]['speed']
            equipment['knapsack'] += self.goods[name]['knapsack']

            equipment['hp']['recovery'] += self.goods[name]['hp-recovery']
            equipment['hp']['max'] += self.goods[name]['hp-max']

            equipment['san']['recovery'] += self.goods[name]['san-recovery']
            equipment['san']['max'] += self.goods[name]['san-max']

            equipment['strength']['recovery'] += self.goods[name]['strength-recovery']
            equipment['strength']['max'] += self.goods[name]['strength-max']

            enchanting['sharp'] += user['equipment']['shoes']['enchanting']['sharp']
            enchanting['rapid'] += user['equipment']['shoes']['enchanting']['rapid']
            enchanting['strong'] += user['equipment']['shoes']['enchanting']['strong']

        if user['equipment']['ring'] != {} and self.goods.__contains__(user['equipment']['ring']['name']):
            name = user['equipment']['ring']['name']
            equipment['attack'] += self.goods[name]['attack']
            equipment['armor'] += self.goods[name]['armor']
            equipment['speed'] += self.goods[name]['speed']
            equipment['knapsack'] += self.goods[name]['knapsack']

            equipment['hp']['recovery'] += self.goods[name]['hp-recovery']
            equipment['hp']['max'] += self.goods[name]['hp-max']

            equipment['san']['recovery'] += self.goods[name]['san-recovery']
            equipment['san']['max'] += self.goods[name]['san-max']

            equipment['strength']['recovery'] += self.goods[name]['strength-recovery']
            equipment['strength']['max'] += self.goods[name]['strength-max']

            enchanting['sharp'] += user['equipment']['ring']['enchanting']['sharp']
            enchanting['rapid'] += user['equipment']['ring']['enchanting']['rapid']
            enchanting['strong'] += user['equipment']['ring']['enchanting']['strong']
            
        if user['equipment']['necklace'] != {} and self.goods.__contains__(user['equipment']['necklace']['name']):
            name = user['equipment']['necklace']['name']
            equipment['attack'] += self.goods[name]['attack']
            equipment['armor'] += self.goods[name]['armor']
            equipment['speed'] += self.goods[name]['speed']
            equipment['knapsack'] += self.goods[name]['knapsack']

            equipment['hp']['recovery'] += self.goods[name]['hp-recovery']
            equipment['hp']['max'] += self.goods[name]['hp-max']

            equipment['san']['recovery'] += self.goods[name]['san-recovery']
            equipment['san']['max'] += self.goods[name]['san-max']

            equipment['strength']['recovery'] += self.goods[name]['strength-recovery']
            equipment['strength']['max'] += self.goods[name]['strength-max']

            enchanting['sharp'] += user['equipment']['necklace']['enchanting']['sharp']
            enchanting['rapid'] += user['equipment']['necklace']['enchanting']['rapid']
            enchanting['strong'] += user['equipment']['necklace']['enchanting']['strong']
            
        if user['equipment']['knapsack'] != {} and self.goods.__contains__(user['equipment']['knapsack']['name']):
            name = user['equipment']['knapsack']['name']
            equipment['attack'] += self.goods[name]['attack']
            equipment['armor'] += self.goods[name]['armor']
            equipment['speed'] += self.goods[name]['speed']
            equipment['knapsack'] += self.goods[name]['knapsack']

            equipment['hp']['recovery'] += self.goods[name]['hp-recovery']
            equipment['hp']['max'] += self.goods[name]['hp-max']

            equipment['san']['recovery'] += self.goods[name]['san-recovery']
            equipment['san']['max'] += self.goods[name]['san-max']

            equipment['strength']['recovery'] += self.goods[name]['strength-recovery']
            equipment['strength']['max'] += self.goods[name]['strength-max']

            enchanting['sharp'] += user['equipment']['knapsack']['enchanting']['sharp']
            enchanting['rapid'] += user['equipment']['knapsack']['enchanting']['rapid']
            enchanting['strong'] += user['equipment']['knapsack']['enchanting']['strong']
            
        if user['equipment']['ornaments'] != {} and self.goods.__contains__(user['equipment']['ornaments']['name']):
            name = user['equipment']['ornaments']['name']
            equipment['attack'] += self.goods[name]['attack']
            equipment['armor'] += self.goods[name]['armor']
            equipment['speed'] += self.goods[name]['speed']
            equipment['knapsack'] += self.goods[name]['knapsack']

            equipment['hp']['recovery'] += self.goods[name]['hp-recovery']
            equipment['hp']['max'] += self.goods[name]['hp-max']

            equipment['san']['recovery'] += self.goods[name]['san-recovery']
            equipment['san']['max'] += self.goods[name]['san-max']

            equipment['strength']['recovery'] += self.goods[name]['strength-recovery']
            equipment['strength']['max'] += self.goods[name]['strength-max']

            enchanting['sharp'] += user['equipment']['ornaments']['enchanting']['sharp']
            enchanting['rapid'] += user['equipment']['ornaments']['enchanting']['rapid']
            enchanting['strong'] += user['equipment']['ornaments']['enchanting']['strong']

        equipment['attack'] += enchanting['sharp']
        equipment['armor'] += enchanting['strong']
        equipment['speed'] += enchanting['rapid'] * 5

        user['attribute']['equipment'] = equipment
        return user

    # 判断是否有怪物
    def is_map_monster(self, user):
        if not self.map.__contains__(user['config']['place']):
            return False
        else:
            map = self.map[user['config']['place']]
            if len(map['monster']) == 0:
                return False
        return True

    # ==========================================
    # buff判断
    def remove_buff(self, name, user):
        reply = False
        level = 0
        apply_index = -1

        for index in range(len(user['buff'])):
            if user['buff'][index]['name'] == name:
                if (user['buff'][index]['level'] > level and user['buff'][apply_index]['type'] == user['buff'][index]['type']) or (user['buff'][apply_index]['type'] == 0 and user['buff'][index]['type'] != 0):
                    reply = True
                    level = user['buff'][index]['level']
                    apply_index = index

        if reply:
            if user['buff'][apply_index]['type'] == 0:  # 如果是次数buff则需要减少
                user['buff'][apply_index]['times'] -= 1
                
        return reply, level, user

    # ==========================================
    # 转职
    def recharge_occupation_attribute(self, user):
        user['attribute']['occupation'] = {  # 职业带来的属性
            'attack': 0,
            'armor': 0,
            'speed': 0,
            'hp': {
                'recovery': 0,
                'max': 0
            },
            'san': {
                'recovery': 0,
                'max': 0
            },
            'strength': {
                'recovery': 0,
                'max': 0
            },
            'knapsack': 0
        }

        if user['occupation']['work'] == '矿工':
            user['attribute']['occupation']['strength']['max'] += 120
        elif user['occupation']['work'] == '培育师':
            user['attribute']['occupation']['strength']['max'] += 80
        elif user['occupation']['work'] == '锻造师':
            user['attribute']['occupation']['strength']['max'] += 100
        elif user['occupation']['work'] == '附魔师':
            user['attribute']['occupation']['strength']['max'] += 100

        if user['occupation']['fight'] == '战士':
            if user['occupation']['fight_level'] == 1:
                user['attribute']['occupation']['attack'] += 2
                user['attribute']['occupation']['armor'] += 2
            elif user['occupation']['fight_level'] == 2:
                user['attribute']['occupation']['attack'] += 4
                user['attribute']['occupation']['armor'] += 4
            elif user['occupation']['fight_level'] == 3:
                user['attribute']['occupation']['attack'] += 6
                user['attribute']['occupation']['armor'] += 6
            user['attribute']['occupation']['speed'] += 10
        elif user['occupation']['fight'] == '盾战士':
            if user['occupation']['fight_level'] == 1:
                user['attribute']['occupation']['armor'] += 4
            elif user['occupation']['fight_level'] == 2:
                user['attribute']['occupation']['armor'] += 8
            elif user['occupation']['fight_level'] == 3:
                user['attribute']['occupation']['armor'] += 12
            user['attribute']['occupation']['speed'] -= 10
            user['attribute']['occupation']['hp']['max'] += 10
            user['attribute']['occupation']['strength']['max'] += 50
        elif user['occupation']['fight'] == '弓箭手':
            if user['occupation']['fight_level'] == 1:
                user['attribute']['occupation']['attack'] += 3
                user['attribute']['occupation']['speed'] += 20
            elif user['occupation']['fight_level'] == 2:
                user['attribute']['occupation']['attack'] += 6
                user['attribute']['occupation']['speed'] += 25
            elif user['occupation']['fight_level'] == 3:
                user['attribute']['occupation']['attack'] += 9
                user['attribute']['occupation']['speed'] += 30

            user['attribute']['occupation']['hp']['max'] -= 10
        elif user['occupation']['fight'] == '魔法师':
            if user['occupation']['fight_level'] == 1:
                user['attribute']['occupation']['attack'] += 3
            elif user['occupation']['fight_level'] == 2:
                user['attribute']['occupation']['attack'] += 6
            elif user['occupation']['fight_level'] == 3:
                user['attribute']['occupation']['attack'] += 9
                
            user['attribute']['occupation']['strength']['max'] -= 50
            user['attribute']['occupation']['hp']['max'] -= 20

        return user

    def change_occupation_miner(self, qq):
        user = self.get_user(qq)
        result = Result()
        change_occupation = {
            'init': True,
            'state': 'success',  # 转职状态
            'type': 0,
            'from': user['occupation']['work'],
            'to': '矿工',
            'need': {}
        }
        result.set_name(user['config']['name'])

        if user['occupation']['work'] == '矿工':
            change_occupation['state'] = 'it was'
            change_occupation['type'] = 0
        else:
            if user['occupation']['work'] == '':
                item = {
                    'name': '劣质灵',
                    'number': 10,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            else:
                item = {
                    'name': '钻石',
                    'number': 5,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            change_occupation['need'] = item

            reply, user = self.remove_items(user, item)
            if reply == 0:
                user['survival_data']['change_occupation'] += 1
                user['occupation']['work'] = '矿工'
                user['occupation']['work_level'] = 1
            elif reply == 1:
                change_occupation['state'] = 'not enough'
            elif reply == 2:
                change_occupation['state'] = 'non-existent'

        user = self.recharge_occupation_attribute(user)
        result.append_change_occupation(change_occupation)
        result = self.update(qq, user, result)
        return result

    def change_occupation_nurturer(self, qq):
        result = Result()
        user = self.get_user(qq)
        change_occupation = {
            'init': True,
            'state': 'success',  # 转职状态
            'type': 0,
            'from': user['occupation']['work'],
            'to': '培育师',
            'need': {}
        }
        result.set_name(user['config']['name'])

        if user['occupation']['work'] == '培育师':
            change_occupation['state'] = 'it was'
            change_occupation['type'] = 0
        else:
            if user['occupation']['work'] == '':
                item = {
                    'name': '劣质灵',
                    'number': 10,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            else:
                item = {
                    'name': '钻石',
                    'number': 5,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            change_occupation['need'] = item

            reply, user = self.remove_items(user, item)
            if reply == 0:
                user['survival_data']['change_occupation'] += 1
                user['occupation']['work'] = '培育师'
                user['occupation']['work_level'] = 1
            elif reply == 1:
                change_occupation['state'] = 'not enough'
            elif reply == 2:
                change_occupation['state'] = 'non-existent'
        user = self.recharge_occupation_attribute(user)
        result.append_change_occupation(change_occupation)
        result = self.update(qq, user, result)
        return result

    def change_occupation_forger(self, qq):
        result = Result()
        user = self.get_user(qq)
        change_occupation = {
            'init': True,
            'state': 'success',  # 转职状态
            'type': 0,
            'from': user['occupation']['work'],
            'to': '锻造师',
            'need': {}
        }
        result.set_name(user['config']['name'])

        if user['occupation']['work'] == '锻造师':
            change_occupation['state'] = 'it was'
            change_occupation['type'] = 0
        else:
            if user['occupation']['work'] == '':
                item = {
                    'name': '劣质灵',
                    'number': 10,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            else:
                item = {
                    'name': '钻石',
                    'number': 5,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            change_occupation['need'] = item

            reply, user = self.remove_items(user, item)
            if reply == 0:
                user['survival_data']['change_occupation'] += 1
                user['occupation']['work'] = '锻造师'
                user['occupation']['work_level'] = 1
            elif reply == 1:
                change_occupation['state'] = 'not enough'
            elif reply == 2:
                change_occupation['state'] = 'non-existent'
        user = self.recharge_occupation_attribute(user)
        result.append_change_occupation(change_occupation)
        result = self.update(qq, user, result)
        return result

    def change_occupation_enchanter(self, qq):
        result = Result()
        user = self.get_user(qq)
        change_occupation = {
            'init': True,
            'state': 'success',  # 转职状态
            'type': 0,
            'from': user['occupation']['work'],
            'to': '附魔师',
            'need': {}
        }
        result.set_name(user['config']['name'])

        if user['occupation']['work'] == '附魔师':
            change_occupation['state'] = 'it was'
            change_occupation['type'] = 0
        else:
            if user['occupation']['work'] == '':
                item = {
                    'name': '劣质灵',
                    'number': 10,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            else:
                item = {
                    'name': '钻石',
                    'number': 5,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            change_occupation['need'] = item

            reply, user = self.remove_items(user, item)
            if reply == 0:
                user['survival_data']['change_occupation'] += 1
                user['occupation']['work'] = '附魔师'
                user['occupation']['work_level'] = 1
            elif reply == 1:
                change_occupation['state'] = 'not enough'
            elif reply == 2:
                change_occupation['state'] = 'non-existent'
        user = self.recharge_occupation_attribute(user)
        result.append_change_occupation(change_occupation)
        result = self.update(qq, user, result)
        return result

    def change_occupation_work_null(self, qq):
        result = Result()
        user = self.get_user(qq)
        change_occupation = {
            'init': True,
            'state': 'success',  # 转职状态
            'type': 0,
            'from': user['occupation']['work'],
            'to': '',
            'need': {}
        }
        result.set_name(user['config']['name'])

        if user['occupation']['work'] == '':
            change_occupation['state'] = 'null'
        else:
            item = {
                'name': '钻石',
                'number': 5,
                'enchanting': {
                    'sharp': 0,
                    'rapid': 0,
                    'strong': 0
                }
            }
            change_occupation['need'] = item

            reply, user = self.remove_items(user, item)
            if reply == 0:
                user['survival_data']['change_occupation'] += 1
                user['occupation']['work'] = ''
                user['occupation']['work_level'] = 1
            elif reply == 1:
                change_occupation['state'] = 'not enough'
            elif reply == 2:
                change_occupation['state'] = 'non-existent'
        user = self.recharge_occupation_attribute(user)
        result.append_change_occupation(change_occupation)
        result = self.update(qq, user, result)
        return result

    def change_occupation_work_level(self, qq):
        result = Result()
        user = self.get_user(qq)
        level_up_occupation = {
            'init': True,
            'state': 'success',  # 转职状态
            'mode': 0,  # 0生活职业，1：战斗职业
            'name': user['occupation']['work'],
            'from': user['occupation']['work_level'],
            'to': user['occupation']['work_level'] + 1,
            'need': {}
        }
        result.set_name(user['config']['name'])

        if user['occupation']['work'] == '':
            level_up_occupation['state'] = 'null'
        else:
            item = {
                'name': '钻石',
                'number': 1,
                'enchanting': {
                    'sharp': 0,
                    'rapid': 0,
                    'strong': 0
                }
            }
            if user['occupation']['work'] == '矿工':
                if user['occupation']['work_level'] == 1:
                    item = {
                        'name': '钛合金',
                        'number': 5,
                        'enchanting': {
                            'sharp': 0,
                            'rapid': 0,
                            'strong': 0
                        }
                    }
                elif user['occupation']['work_level'] == 2:
                    item = {
                        'name': '下界合金靴',
                        'number': 1,
                        'enchanting': {
                            'sharp': 0,
                            'rapid': 2,
                            'strong': 2
                        }
                    }
            elif user['occupation']['work'] == '锻造师':
                if user['occupation']['work_level'] == 1:
                    item = {
                        'name': '钛矿石',
                        'number': 6,
                        'enchanting': {
                            'sharp': 0,
                            'rapid': 0,
                            'strong': 0
                        }
                    }
                elif user['occupation']['work_level'] == 2:
                    item = {
                        'name': '下界石英',
                        'number': 5,
                        'enchanting': {
                            'sharp': 0,
                            'rapid': 0,
                            'strong': 0
                        }
                    }
            elif user['occupation']['work'] == '附魔师':
                if user['occupation']['work_level'] == 1:
                    item = {
                        'name': '苹果',
                        'number': 80,
                        'enchanting': {
                            'sharp': 0,
                            'rapid': 0,
                            'strong': 0
                        }
                    }
                elif user['occupation']['work_level'] == 2:
                    item = {
                        'name': '熟肉',
                        'number': 40,
                        'enchanting': {
                            'sharp': 0,
                            'rapid': 0,
                            'strong': 0
                        }
                    }
            elif user['occupation']['work'] == '培育师':
                if user['occupation']['work_level'] == 1:
                    item = {
                        'name': '钛合金剑',
                        'number': 1,
                        'enchanting': {
                            'sharp': 1,
                            'rapid': 1,
                            'strong': 0
                        }
                    }
                elif user['occupation']['work_level'] == 2:
                    item = {
                        'name': '灵石',
                        'number': 5,
                        'enchanting': {
                            'sharp': 0,
                            'rapid': 0,
                            'strong': 0
                        }
                    }
            level_up_occupation['need'] = item

            reply, user = self.remove_items(user, item)
            if reply == 0:
                if user['occupation']['work_level'] < 3:
                    user['occupation']['work_level'] += 1
                else:
                    level_up_occupation['state'] = 'max'
            elif reply == 1:
                level_up_occupation['state'] = 'not enough'
            elif reply == 2:
                level_up_occupation['state'] = 'non-existent'
        user = self.recharge_occupation_attribute(user)
        result.append_level_up_occupation(level_up_occupation)
        result = self.update(qq, user, result)
        return result

    def change_occupation_warrior(self, qq):
        result = Result()
        user = self.get_user(qq)
        change_occupation = {
            'init': True,
            'state': 'success',  # 转职状态
            'type': 0,
            'from': user['occupation']['fight'],
            'to': '战士',
            'need': {}
        }
        result.set_name(user['config']['name'])

        if user['occupation']['fight'] == '战士':
            change_occupation['state'] = 'it was'
            change_occupation['type'] = 1
        else:
            if user['occupation']['fight'] == '':
                item = {
                    'name': '劣质灵',
                    'number': 10,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            else:
                item = {
                    'name': '稀有灵',
                    'number': 30,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            change_occupation['need'] = item

            reply, user = self.remove_items(user, item)
            if reply == 0:
                user['survival_data']['change_occupation'] += 1
                user['occupation']['fight'] = '战士'
                user['occupation']['fight_level'] = 1
            elif reply == 1:
                change_occupation['state'] = 'not enough'
            elif reply == 2:
                change_occupation['state'] = 'non-existent'
        user = self.recharge_occupation_attribute(user)
        result.append_change_occupation(change_occupation)
        result = self.update(qq, user, result)
        return result

    def change_occupation_shield(self, qq):
        result = Result()
        user = self.get_user(qq)
        change_occupation = {
            'init': True,
            'state': 'success',  # 转职状态
            'type': 0,
            'from': user['occupation']['fight'],
            'to': '盾战士',
            'need': {}
        }
        result.set_name(user['config']['name'])

        if user['occupation']['fight'] == '盾战士':
            change_occupation['state'] = 'it was'
            change_occupation['type'] = 1
        else:
            if user['occupation']['fight'] == '':
                item = {
                    'name': '劣质灵',
                    'number': 10,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            else:
                item = {
                    'name': '稀有灵',
                    'number': 30,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            change_occupation['need'] = item

            reply, user = self.remove_items(user, item)
            if reply == 0:
                user['survival_data']['change_occupation'] += 1
                user['occupation']['fight'] = '盾战士'
                user['occupation']['fight_level'] = 1
            elif reply == 1:
                change_occupation['state'] = 'not enough'
            elif reply == 2:
                change_occupation['state'] = 'non-existent'
        user = self.recharge_occupation_attribute(user)
        result.append_change_occupation(change_occupation)
        result = self.update(qq, user, result)
        return result

    def change_occupation_archer(self, qq):
        result = Result()
        user = self.get_user(qq)
        change_occupation = {
            'init': True,
            'state': 'success',  # 转职状态
            'type': 0,
            'from': user['occupation']['fight'],
            'to': '弓箭手',
            'need': {}
        }
        result.set_name(user['config']['name'])

        if user['occupation']['fight'] == '弓箭手':
            change_occupation['state'] = 'it was'
            change_occupation['type'] = 1
        else:
            if user['occupation']['fight'] == '':
                item = {
                    'name': '劣质灵',
                    'number': 10,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            else:
                item = {
                    'name': '稀有灵',
                    'number': 30,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            change_occupation['need'] = item

            reply, user = self.remove_items(user, item)
            if reply == 0:
                user['survival_data']['change_occupation'] += 1
                user['occupation']['fight'] = '弓箭手'
                user['occupation']['fight_level'] = 1
            elif reply == 1:
                change_occupation['state'] = 'not enough'
            elif reply == 2:
                change_occupation['state'] = 'non-existent'
        user = self.recharge_occupation_attribute(user)
        result.append_change_occupation(change_occupation)
        result = self.update(qq, user, result)
        return result

    def change_occupation_magician(self, qq):
        result = Result()
        user = self.get_user(qq)
        change_occupation = {
            'init': True,
            'state': 'success',  # 转职状态
            'type': 0,
            'from': user['occupation']['fight'],
            'to': '魔法师',
            'need': {}
        }
        result.set_name(user['config']['name'])

        if user['occupation']['fight'] == '魔法师':
            change_occupation['state'] = 'it was'
            change_occupation['type'] = 1
        else:
            if user['occupation']['fight'] == '':
                item = {
                    'name': '劣质灵',
                    'number': 10,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            else:
                item = {
                    'name': '稀有灵',
                    'number': 30,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
            change_occupation['need'] = item

            reply, user = self.remove_items(user, item)
            if reply == 0:
                user['survival_data']['change_occupation'] += 1
                user['occupation']['fight'] = '魔法师'
                user['occupation']['fight_level'] = 1
            elif reply == 1:
                change_occupation['state'] = 'not enough'
            elif reply == 2:
                change_occupation['state'] = 'non-existent'
        user = self.recharge_occupation_attribute(user)
        result.append_change_occupation(change_occupation)
        result = self.update(qq, user, result)
        return result

    def change_occupation_fight_null(self, qq):
        result = Result()
        user = self.get_user(qq)
        change_occupation = {
            'init': True,
            'state': 'success',  # 转职状态
            'type': 0,
            'from': user['occupation']['fight'],
            'to': '',
            'need': {}
        }
        result.set_name(user['config']['name'])

        if user['occupation']['fight'] == '':
            change_occupation['state'] = 'null'
        else:
            item = {
                'name': '稀有灵',
                'number': 30,
                'enchanting': {
                    'sharp': 0,
                    'rapid': 0,
                    'strong': 0
                }
            }
            change_occupation['need'] = item

            reply, user = self.remove_items(user, item)
            if reply == 0:
                user['survival_data']['change_occupation'] += 1
                user['occupation']['fight'] = ''
                user['occupation']['fight_level'] = 1
            elif reply == 1:
                change_occupation['state'] = 'not enough'
            elif reply == 2:
                change_occupation['state'] = 'non-existent'
        user = self.recharge_occupation_attribute(user)
        result.append_change_occupation(change_occupation)
        result = self.update(qq, user, result)
        return result

    def change_occupation_fight_level(self, qq):
        result = Result()
        user = self.get_user(qq)
        level_up_occupation = {
            'init': True,
            'state': 'success',  # 转职状态
            'mode': 1,  # 0生活职业，1：战斗职业
            'name': user['occupation']['fight'],
            'from': user['occupation']['fight_level'],
            'to': user['occupation']['fight_level'] + 1,
            'need': {}
        }
        result.set_name(user['config']['name'])

        if user['occupation']['fight'] == '':
            level_up_occupation['state'] = 'null'
        else:
            item = {
                'name': '稀有灵',
                'number': 10,
                'enchanting': {
                    'sharp': 0,
                    'rapid': 0,
                    'strong': 0
                }
            }
            if user['occupation']['fight_level'] == 2:
                item = {
                    'name': '史诗灵',
                    'number': 10,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 1,
                        'strong': 1
                    }
                }
            level_up_occupation['need'] = item

            reply, user = self.remove_items(user, item)
            if reply == 0:
                if user['occupation']['fight_level'] < 3:
                    user['occupation']['fight_level'] += 1
                else:
                    level_up_occupation['state'] = 'max'
            elif reply == 1:
                level_up_occupation['state'] = 'not enough'
            elif reply == 2:
                level_up_occupation['state'] = 'non-existent'
        user = self.recharge_occupation_attribute(user)
        result.append_level_up_occupation(level_up_occupation)
        result = self.update(qq, user, result)
        return result

    # ==========================================
    # 操作
    def sign(self, qq):
        today = str(datetime.date.today())
        user = self.get_user(qq)
        message_sign = {
            'init': True,
            'state': 'success',  # 签到成功
            'gold': 0,  # 现在的积分
            'gold_sign': 0,  # 签到所获得的积分
            'gets': {},  # 签到所获得的物品
            'consecutive': 0,
            'sum': 0
        }
        result = Result()

        if today != user['config']['sign']['last_date']:
            if is_yesterday(user['config']['sign']['last_date']):
                user['config']['sign']['consecutive'] += 1
            else:
                user['config']['sign']['consecutive'] = 1
            user['config']['sign']['last_date'] = today
            user['config']['sign']['sum'] += 1

            luck = self.luck.get_luck_number(qq)
            gold = random.randint(5, 20) + int(luck / 20)

            user['attribute']['own']['gold'] += gold

            message_sign['gold'] = user['attribute']['own']['gold']
            message_sign['gold_sign'] = gold
            message_sign['consecutive'] = user['config']['sign']['consecutive']
            message_sign['sum'] = user['config']['sign']['sum']
        else:
            message_sign['state'] = 'fail'
        result.set_name(user['config']['name'])
        result.append_sign(message_sign)
        result = self.update(qq, user, result)
        return result

    def PVP(self, active, passive, is_fencing):
        user_active = self.get_user(active)
        user_passive = self.get_user(passive)
        result = Result()
        PVP = {
            'init': True,
            'state': 'win',
            'is_fencing': is_fencing,  # 是否是击剑
            'name1': '',  # 主动名字
            'name2': '',  # 被动名字
            'gold': 0
        }
        result.set_name(user_active['config']['name'])
        PVP['name1'] = user_active['config']['name']
        PVP['name2'] = user_passive['config']['name']

        if active == passive:  # 和自己击剑
            PVP['state'] = 'fencing with yourself'
        elif user_active['attribute']['own']['strength']['number'] < 1:  # 没有体力值
            PVP['state'] = 'no strength'
        elif user_active['attribute']['own']['gold'] < 1:  # 主动击剑的人没有积分
            PVP['state'] = 'active fencers have no points'
        elif user_passive['attribute']['own']['gold'] <= 1:  # 被动击剑的人没有积分
            PVP['state'] = 'passive fencers have no points'
        else:
            user_active['attribute']['own']['strength']['number'] -= 1
            user_active['combat_data']['PVP_active'] += 1
            user_passive['combat_data']['PVP_passive'] += 1
            user_passive['attribute']['own']['san']['number'] -= 1
            if user_passive['attribute']['own']['san']['number'] < 0:
                user_passive['attribute']['own']['san']['number'] = 0

            ran = random.randrange(0, 100)
            if user_passive['attribute']['own']['san']['number'] != 0:
                line = 50 + 2 * (self.get_attack(user_active) - self.get_armor(user_passive)) * \
                       user_active['attribute']['own']['san']['number'] / user_passive['attribute']['own']['san'][
                           'number']
            else:
                line = 100

            reply, level1, user_active = self.remove_buff('进攻', user_active)
            reply, level2, user_passive = self.remove_buff('防御', user_passive)

            line += level1 * 10 - level2 * 10
            
            reply1, level1, user_active = self.remove_buff('无敌', user_active)
            reply2, level2, user_active = self.remove_buff('无敌', user_active)

            if reply1:
                line = 100
            elif reply2:
                line = 0

            gold = random.randrange(0, 8) + 1
            if user_passive['attribute']['own']['san']['number'] == 0 or user_active['attribute']['own']['san'][
                'number'] / user_passive['attribute']['own']['san']['number'] > 3:
                gold = 1
            elif self.get_attack(user_active) - self.get_armor(user_passive) > 25:
                gold = 1

            if line > ran:
                PVP['state'] = 'win'

                user_active['combat_data']['PVP_victory'] += 1
                user_passive['combat_data']['PVP_defeat'] += 1

                if gold > user_passive['attribute']['own']['gold']:  # 扣除积分
                    gold = user_passive['attribute']['own']['gold']
                    user_passive['attribute']['own']['gold'] = 0
                    user_active['attribute']['own']['gold'] += gold
                else:
                    user_passive['attribute']['own']['gold'] -= gold
                    user_active['attribute']['own']['gold'] += gold
            else:
                PVP['state'] = 'lose'

                user_passive['combat_data']['PVP_victory'] += 1
                user_active['combat_data']['PVP_defeat'] += 1
                
                if gold > user_active['attribute']['own']['gold']:  # 扣除积分
                    gold = user_active['attribute']['own']['gold']
                    user_active['attribute']['own']['gold'] = 0
                    user_passive['attribute']['own']['gold'] += gold
                else:
                    user_active['attribute']['own']['gold'] -= gold
                    user_passive['attribute']['own']['gold'] += gold

            PVP['gold'] = gold
            self.update(active, user_active, result)
            self.update(passive, user_passive, Result())
        result.append_PVP(PVP)
        return result

    def PVE(self, qq, user, monsters, result_PVE):
        for monster in monsters:
            target = self.get_monster(monster['name'])
            if target is not None:
                for index in range(monster['number']):
                    part1 = self.get_attack(user) - target['armor']
                    if part1 <= 0:
                        part1 = 1
                    
                    part2 = target['attack'] - self.get_armor(user)
                    if self.get_speed(user) != 0:
                        part3 = target['speed'] / self.get_speed(user)
                    else:
                        part3 = 1.0
                
                    hurt = float(float(target['hp']) / part1 * part2) * part3

                    luck = float(self.luck.get_luck_number(qq))
                    if luck >= 50:
                        part_luck = 1.0 + (luck - 50.0) / 50.0
                    else:
                        part_luck = 1.0 / (1.0 + (50.0 - luck) / 50.0)
                    hurt /= part_luck
                    part_rand = random.randint(0, 10)
                    hurt += part_rand

                    hurt = int(hurt)
                    if hurt <= 0:
                        hurt = 1
                    result_PVE['hp'] += hurt

                    if user['attribute']['own']['hp']['number'] < hurt:
                        result_PVE['state'] = 'die'
                        user['config']['die_check'] = True
                        user['attribute']['own']['hp']['number'] = 0
                        break
                    else:
                        user['combat_data']['monster_kill'] += 1
                        user['attribute']['own']['hp']['number'] -= hurt
                        spoils = copy.deepcopy(target['spoils'])
                        for goods in spoils:
                            reply, user = self.get_items(user, goods)
                            if reply:
                                is_stack = False

                                for index in range(len(result_PVE['gets'])):
                                    if result_PVE['gets'][index]['name'] == goods['name'] and result_PVE['gets'][index]['enchanting'] == goods['enchanting']:
                                        result_PVE['gets'][index]['number'] += goods['number']
                                        is_stack = True
                                        break

                                if not is_stack:
                                    result_PVE['gets'].append(copy.deepcopy(goods))

            if result_PVE['state'] == 'die':
                break
        return user, result_PVE

    def PVB(self, qq, boss):
        pass

    def purchase(self, qq, name, number):
        user = self.get_user(qq)
        result = Result()
        result.set_name(user['config']['name'])
        purchase = {
            'init': True,
            'state': 'success',
            'type': 0,  # 0表示正常商店购买，1表示灵商店购买
            'cost_soul': [],
            'cost': 0,
            'name': name,
            'number': number
        }

        if not self.goods.__contains__(name):
            purchase['state'] = 'non-existent'  # 不存在
        elif name not in self.shop:
            if self.soul_shop.__contains__(name):
                purchase['type'] = 1
                cost = copy.deepcopy(self.soul_shop[name]['cost'])
                
                operated = []

                for i in cost:
                    i['number'] *= number
                    reply, user = self.remove_items(user, i)
                    if reply == 0:
                        operated.append(i)
                    else:
                        purchase['state'] = 'no gold'
                        break
                purchase['cost_soul'] = operated
                    
                # 限购
                if purchase['state'] == 'success':
                    if self.goods[name]['limit'] != 0:
                        if user['config']['limit'].__contains__(name):
                            if user['config']['limit'][name] + number > self.goods[name]['limit']:
                                purchase['state'] = 'limit'
                            else:
                                user['config']['limit'][name] += number
                        else:
                            if number > self.goods[name]['limit']:
                                purchase['state'] = 'limit'
                            else:
                                user['config']['limit'][name] = number
                
                # 获取物品
                if purchase['state'] == 'success':
                    item = {
                        'name': name,
                        'number': number,
                        'enchanting': {
                            'sharp': 0,
                            'rapid': 0,
                            'strong': 0
                        }
                    }
                    reply, user = self.get_items(user, item)
                    if not reply:
                        purchase['state'] = 'the backpack is full'


                # 判断是否成功
                if purchase['state'] != 'success':
                    for i in operated:
                        reply, user = self.get_items(user, i)
            else:
                purchase['state'] = 'not for sale'  # 不可购买
        elif self.goods[name]['cost'] < 0:
            purchase['state'] = 'not for sale'  # 不可购买
        else:
            if user['attribute']['own']['gold'] < self.goods[name]['cost'] * number:
                purchase['state'] = 'no gold'  # 积分不足
                result.append_purchase(purchase)
                return result
            
            # 限购
            if self.goods[name]['limit'] != 0:
                if user['config']['limit'].__contains__(name):
                    if user['config']['limit'][name] + number > self.goods[name]['limit']:
                        purchase['state'] = 'limit'
                        result.append_purchase(purchase)
                        return result
                    else:
                        user['config']['limit'][name] += number
                else:
                    if number > self.goods[name]['limit']:
                        purchase['state'] = 'limit'
                        result.append_purchase(purchase)
                        return result
                    else:
                        user['config']['limit'][name] = number

            items = {
                'name': name,
                'number': number,
                'enchanting': {
                    'sharp': 0,
                    'rapid': 0,
                    'strong': 0
                }
            }
            reply, user = self.get_items(user, items)
            if not reply:
                purchase['state'] = 'the backpack is full'
            else:
                user['attribute']['own']['gold'] -= self.goods[name]['cost'] * number
                purchase['cost'] = self.goods[name]['cost'] * number

        result.append_purchase(purchase)
        result = self.update(qq, user, result)
        return result

    def discard(self, qq, name, number):
        result = Result()
        user = self.get_user(qq)
        result.set_name(user['config']['name'])
        discard = {
            'init': True,
            'state': 'success',
            'goods': []
        }

        name, enchanting = analysis_name(name)
        item = {
            'name': name,
            'number': number,
            'enchanting': enchanting
        }
        reply, user = self.remove_items(user, item)
        if reply == 0:
            discard['goods'].append(item)
        elif reply == 1:
            discard['state'] = 'not enough'
        elif reply == 2:
            discard['state'] = 'non-existent'

        result.append_discard(discard)
        result = self.update(qq, user, result)
        return result

    def discard_all(self, qq):
        result = Result()
        user = self.get_user(qq)
        result.set_name(user['config']['name'])
        discard = {
            'init': True,
            'state': 'all',
            'goods': []
        }

        if len(user['warehouse']) == 0:
            discard['state'] = 'all fail'
        else:
            discard['goods'] = user['warehouse']
            user['warehouse'] = []

        result.append_discard(discard)
        result = self.update(qq, user, result)
        return result

    def sell(self, qq, name, number):
        result = Result()
        user = self.get_user(qq)
        result.set_name(user['config']['name'])
        sell = {
            'init': True,
            'state': 'success',
            'sell': 0,
            'goods': []
        }

        name, enchanting = analysis_name(name)
        item = {
            'name': name,
            'number': number,
            'enchanting': enchanting
        }
        goods = self.get_goods(name)
        if goods['sell'] == -1:
            sell['state'] = 'not for sale'
        else:
            gold = goods['sell'] * number
            reply, user = self.remove_items(user, item)
            if reply == 0:
                sell['goods'].append(item)
                sell['sell'] = gold
                user['attribute']['own']['gold'] += gold
            elif reply == 1:
                sell['state'] = 'not enough'
            elif reply == 2:
                sell['state'] = 'non-existent'

        result.append_sell(sell)
        result = self.update(qq, user, result)
        return result

    def give(self, qq, qq2, name, number):
        result = Result()
        user = self.get_user(qq)
        user_received = self.get_user(qq2)
        result.set_name(user['config']['name'])
        give = {
            'init': True,
            'state': 'success',
            'name': user_received['config']['name'],
            'goods': []
        }

        name, enchanting = analysis_name(name)
        item = {
            'name': name,
            'number': number,
            'enchanting': enchanting
        }
        reply, user = self.remove_items(user, item)
        if reply == 0:
            give['goods'].append(item)
            reply2, user_received = self.get_items(user_received, item)
            if not reply2:
                reply2, user = self.get_items(user, item)
                give['state'] = 'full knapsack'
            else:
                user['survival_data']['gift_give'] += 1
                user_received['survival_data']['gift_received'] += 1
        elif reply == 1:
            give['state'] = 'not enough'
        elif reply == 2:
            give['state'] = 'non-existent'
        
        result.append_give(give)
        result = self.update(qq, user, result)
        self.update(qq2, user_received, Result())
        return result

    def use(self, qq, name, number):
        result = Result()
        user = self.get_user(qq)
        result.set_name(user['config']['name'])
        use = {
            'init': True,
            'state': 'success',
            'goods': [],
            'mode': 0,  # 0：使用，1：装备
            'gold': 0,
            'hp': 0,
            'hp-recovery': 0,
            'hp-max': 0,
            'san': 0,
            'san-recovery': 0,
            'san-max': 0,
            'strength': 0,
            'strength-recovery': 0,
            'strength-max': 0,
            'resurrection': 0,
            'comments': '',
        }

        name, enchanting = analysis_name(name)
        item = {
            'name': name,
            'number': number,
            'enchanting': enchanting
        }
        reply, user = self.remove_items(user, item)
        if reply == 0:
            use['goods'].append(item)
            
            if self.goods.__contains__(name):
                # 材料
                goods = self.get_goods(name)

                if goods['type'] == 3 or (31 <= goods['type'] <= 34) or (331 <= goods['type'] <= 335):
                    use['state'] = 'material'
                elif goods['type'] == 4 or (41 <= goods['type'] <= 42):
                    use['state'] = 'keepsake'
                elif goods['type'] == 1 or (10 <= goods['type'] <= 19) or (111 <= goods['type'] <=116):
                    if number == 1:
                        use['mode'] = 1
                        if goods['type'] == 1:
                            use['state'] = 'unknown type'
                        elif goods['type'] == 10: # 饰品
                            if user['equipment']['ornaments'] != {}:
                                reply, user = self.get_items(user, user['equipment']['ornaments'])
                                if reply:
                                    user['equipment']['ornaments'] = item
                                else:
                                    use['state'] = 'the backpack is full'
                            else:
                                user['equipment']['ornaments'] = item
                        elif goods['type'] == 11 or (111 <= goods['type'] <=116): # 武器
                            if user['equipment']['arms'] != {}:
                                reply, user = self.get_items(user, user['equipment']['arms'])
                                if reply:
                                    user['equipment']['arms'] = item
                                else:
                                    use['state'] = 'the backpack is full'
                            else:
                                user['equipment']['arms'] = item
                        elif goods['type'] == 12: # 面具
                            if user['equipment']['mask'] != {}:
                                reply, user = self.get_items(user, user['equipment']['mask'])
                                if reply:
                                    user['equipment']['mask'] = item
                                else:
                                    use['state'] = 'the backpack is full'
                            else:
                                user['equipment']['mask'] = item
                        elif goods['type'] == 13: # 项链
                            if user['equipment']['necklace'] != {}:
                                reply, user = self.get_items(user, user['equipment']['necklace'])
                                if reply:
                                    user['equipment']['necklace'] = item
                                else:
                                    use['state'] = 'the backpack is full'
                            else:
                                user['equipment']['necklace'] = item
                        elif goods['type'] == 14: # 戒指
                            if user['equipment']['ring'] != {}:
                                reply, user = self.get_items(user, user['equipment']['ring'])
                                if reply:
                                    user['equipment']['ring'] = item
                                else:
                                    use['state'] = 'the backpack is full'
                            else:
                                user['equipment']['ring'] = item
                        elif goods['type'] == 15: # 头盔
                            if user['equipment']['hat'] != {}:
                                reply, user = self.get_items(user, user['equipment']['hat'])
                                if reply:
                                    user['equipment']['hat'] = item
                                else:
                                    use['state'] = 'the backpack is full'
                            else:
                                user['equipment']['hat'] = item
                        elif goods['type'] == 16: # 胸甲
                            if user['equipment']['jacket'] != {}:
                                reply, user = self.get_items(user, user['equipment']['jacket'])
                                if reply:
                                    user['equipment']['jacket'] = item
                                else:
                                    use['state'] = 'the backpack is full'
                            else:
                                user['equipment']['jacket'] = item
                        elif goods['type'] == 17: # 护腿
                            if user['equipment']['trousers'] != {}:
                                reply, user = self.get_items(user, user['equipment']['trousers'])
                                if reply:
                                    user['equipment']['trousers'] = item
                                else:
                                    use['state'] = 'the backpack is full'
                            else:
                                user['equipment']['trousers'] = item
                        elif goods['type'] == 18: # 靴子
                            if user['equipment']['shoes'] != {}:
                                reply, user = self.get_items(user, user['equipment']['shoes'])
                                if reply:
                                    user['equipment']['shoes'] = item
                                else:
                                    use['state'] = 'the backpack is full'
                            else:
                                user['equipment']['shoes'] = item
                        elif goods['type'] == 19: # 背包
                            if user['equipment']['knapsack'] != {}:
                                reply, user = self.get_items(user, user['equipment']['knapsack'])
                                if reply:
                                    user['equipment']['knapsack'] = item
                                else:
                                    use['state'] = 'the backpack is full'
                            else:
                                user['equipment']['knapsack'] = item
                    else:
                        use['state'] = 'too much'
                elif goods['type'] == 2 or (21 <= goods['type'] <= 27 and goods['type'] != 23):
                    if goods['type'] == 27:  # 树苗、种子、牲畜
                        use['state'] = 'cultivation'
                    elif goods['type'] == 26:  # 晶石
                        if name == '低级传送石':
                            init_map = []
                            for key, value in self.map.items():
                                if self.map[key]['level'] == 0:
                                    init_map.append(key)
                            if len(init_map) != 0:
                                user['config']['place'] = random.choice(init_map)
                            use['comments'] = '再一次天转地旋之后你被传送到了' + user['config']['place']
                            user['survival_data']['travel'] += 1
                        elif name == '中级传送石':
                            init_map = []
                            for key, value in self.map.items():
                                if self.map[key]['level'] == 1:
                                    init_map.append(key)
                            if len(init_map) != 0:
                                user['config']['place'] = random.choice(init_map)
                            use['comments'] = '再一次天转地旋之后你被传送到了' + user['config']['place']
                            user['survival_data']['travel'] += 1
                        elif name == '高级传送石':
                            init_map = []
                            for key, value in self.map.items():
                                if self.map[key]['level'] == 2:
                                    init_map.append(key)
                            if len(init_map) != 0:
                                user['config']['place'] = random.choice(init_map)
                            use['comments'] = '再一次天转地旋之后你被传送到了' + user['config']['place']
                            user['survival_data']['travel'] += 1

                    elif goods['type'] == 25:  # 卷轴
                        buff = {
                            'name': '',  # buff名字
                            'type': 0,  # 0表示次数，1表示时间
                            'level': 1,  # 级别
                            'date': '',  # 时间
                            'times': 0  # 次数
                        }
                        if name == '5级进攻卷轴':
                            buff['name'] = '进攻'
                            buff['level'] = 5
                            buff['type'] = 1
                            buff['times'] = addition_minute(getNow.toString(), 5)
                            use['comments'] = '你获得了5分钟的5级进攻buff'
                            reply, user = self.get_buff(user, buff)
                        elif name == '4级进攻卷轴':
                            buff['name'] = '进攻'
                            buff['level'] = 4
                            buff['type'] = 1
                            buff['times'] = addition_minute(getNow.toString(), 5)
                            use['comments'] = '你获得了5分钟的4级进攻buff'
                            reply, user = self.get_buff(user, buff)
                        elif name == '3级进攻卷轴':
                            buff['name'] = '进攻'
                            buff['level'] = 3
                            buff['type'] = 1
                            buff['times'] = addition_minute(getNow.toString(), 5)
                            use['comments'] = '你获得了5分钟的3级进攻buff'
                            reply, user = self.get_buff(user, buff)
                        elif name == '2级进攻卷轴':
                            buff['name'] = '进攻'
                            buff['level'] = 2
                            buff['type'] = 1
                            buff['times'] = addition_minute(getNow.toString(), 5)
                            use['comments'] = '你获得了5分钟的2级进攻buff'
                            reply, user = self.get_buff(user, buff)
                        elif name == '1级进攻卷轴':
                            buff['name'] = '进攻'
                            buff['level'] = 1
                            buff['type'] = 1
                            buff['times'] = addition_minute(getNow.toString(), 5)
                            use['comments'] = '你获得了5分钟的1级进攻buff'
                            reply, user = self.get_buff(user, buff)

                        elif name == '5级防御卷轴':
                            buff['name'] = '防御'
                            buff['level'] = 5
                            buff['type'] = 1
                            buff['times'] = addition_minute(getNow.toString(), 5)
                            use['comments'] = '你获得了5分钟的5级防御buff'
                            reply, user = self.get_buff(user, buff)
                        elif name == '4级防御卷轴':
                            buff['name'] = '防御'
                            buff['level'] = 4
                            buff['type'] = 1
                            buff['times'] = addition_minute(getNow.toString(), 5)
                            use['comments'] = '你获得了5分钟的4级防御buff'
                            reply, user = self.get_buff(user, buff)
                        elif name == '3级防御卷轴':
                            buff['name'] = '防御'
                            buff['level'] = 3
                            buff['type'] = 1
                            buff['times'] = addition_minute(getNow.toString(), 5)
                            use['comments'] = '你获得了5分钟的3级防御buff'
                            reply, user = self.get_buff(user, buff)
                        elif name == '2级防御卷轴':
                            buff['name'] = '防御'
                            buff['level'] = 2
                            buff['type'] = 1
                            buff['times'] = addition_minute(getNow.toString(), 5)
                            use['comments'] = '你获得了5分钟的2级防御buff'
                            reply, user = self.get_buff(user, buff)
                        elif name == '1级防御卷轴':
                            buff['name'] = '防御'
                            buff['level'] = 1
                            buff['type'] = 1
                            buff['times'] = addition_minute(getNow.toString(), 5)
                            use['comments'] = '你获得了5分钟的1级防御buff'
                            reply, user = self.get_buff(user, buff)

                    else:
                        check = True
                        hp = goods['hp'] * number
                        hp_recovery = goods['hp-recovery'] * number
                        hp_max = goods['hp-max'] * number
                        san = goods['san'] * number
                        san_recovery = goods['san-recovery'] * number
                        san_max = goods['san-max'] * number
                        strength = goods['strength'] * number
                        strength_recovery = goods['strength-recovery'] * number
                        strength_max = goods['strength-max'] * number
                        gold = goods['gold'] * number
                        resurrection = goods['resurrection']

                        if hp != 0 and hp + user['attribute']['own']['hp']['number'] > self.get_max_hp(user) + hp_max:
                            check = False
                            use['state'] = 'hp overflow'
                        elif san != 0 and san + user['attribute']['own']['san']['number'] > self.get_max_san(user) + san_max:
                            check = False
                            use['state'] = 'san overflow'
                        elif strength != 0 and strength + user['attribute']['own']['strength']['number'] > self.get_max_strength(user) + strength_max:
                            check = False
                            use['state'] = 'strength overflow'
                        
                        if user['attribute']['own']['hp']['number'] == 0 and hp != 0:
                            if resurrection == 0:
                                check = False
                                use['state'] = 'die'

                        if check:
                            user['attribute']['own']['gold'] += gold
                            if hp <= -1:
                                user['attribute']['own']['hp']['number'] = hp_max + self.get_max_hp(user)
                            elif user['attribute']['own']['hp']['number'] != 0:
                                user['attribute']['own']['hp']['number'] += hp
                            else:
                                user['attribute']['own']['hp']['number'] = hp_max + self.get_max_hp(user)
                            user['attribute']['own']['hp']['recovery'] += hp_recovery
                            user['attribute']['own']['hp']['max'] += hp_max
                            if san <= -1:
                                user['attribute']['own']['san']['number'] = san_max + self.get_max_san(user)
                            else:
                                user['attribute']['own']['san']['number'] += san 
                            user['attribute']['own']['san']['recovery'] += san_recovery
                            user['attribute']['own']['san']['max'] += san_max
                            if strength <= -1:
                                user['attribute']['own']['strength']['number'] = strength_max + self.get_max_strength(user)
                            else:
                                user['attribute']['own']['strength']['number'] += strength
                            user['attribute']['own']['strength']['recovery'] += strength_recovery
                            user['attribute']['own']['strength']['max'] += strength_max

                            use['gold'] = gold
                            use['hp'] = hp
                            use['hp-recovery'] = hp_recovery
                            use['hp-max'] = hp_max
                            use['san'] = san
                            use['san-recovery'] = san_recovery
                            use['san-max'] = san_max
                            use['strength'] = strength
                            use['strength-recovery'] = strength_recovery
                            use['strength-max'] = strength_max
                            use['resurrection'] = resurrection
                else:
                    use['state'] = 'unknown type'
            else:
                use['state'] = 'unknown'

            if use['state'] != 'success':  # 如果没有使用成功返还物品
                reply, user = self.get_items(user, item)
        elif reply == 1:
            use['state'] = 'not enough'
        elif reply == 2:
            use['state'] = 'non-existent'

        result.append_use(use)
        result = self.update(qq, user, result)
        return result

    def remove_equipment(self, qq, name):
        result = Result()
        user = self.get_user(qq)
        result.set_name(user['config']['name'])
        remove_equipment = {
            'init': True,
            'state': 'non-existent',
            'name': name
        }
        
        name, enchanting = analysis_name(name)
        item = {
            'name': name,
            'number': 1,
            'enchanting': enchanting
        }

        if item == user['equipment']['arms']:
            reply, user = self.get_items(user, item)
            if reply:
                user['equipment']['arms'] = {}
                remove_equipment['state'] = 'success'
            else:
                remove_equipment['state'] = 'the backpack is full'
        elif item == user['equipment']['mask']:
            reply, user = self.get_items(user, item)
            if reply:
                user['equipment']['mask'] = {}
                remove_equipment['state'] = 'success'
            else:
                remove_equipment['state'] = 'the backpack is full'
        elif item == user['equipment']['necklace']:
            reply, user = self.get_items(user, item)
            if reply:
                user['equipment']['necklace'] = {}
                remove_equipment['state'] = 'success'
            else:
                remove_equipment['state'] = 'the backpack is full'
        elif item == user['equipment']['ring']:
            reply, user = self.get_items(user, item)
            if reply:
                user['equipment']['ring'] = {}
                remove_equipment['state'] = 'success'
            else:
                remove_equipment['state'] = 'the backpack is full'
        elif item == user['equipment']['hat']:
            reply, user = self.get_items(user, item)
            if reply:
                user['equipment']['hat'] = {}
                remove_equipment['state'] = 'success'
            else:
                remove_equipment['state'] = 'the backpack is full'
        elif item == user['equipment']['jacket']:
            reply, user = self.get_items(user, item)
            if reply:
                user['equipment']['jacket'] = {}
                remove_equipment['state'] = 'success'
            else:
                remove_equipment['state'] = 'the backpack is full'
        elif item == user['equipment']['trousers']:
            reply, user = self.get_items(user, item)
            if reply:
                user['equipment']['trousers'] = {}
                remove_equipment['state'] = 'success'
            else:
                remove_equipment['state'] = 'the backpack is full'
        elif item == user['equipment']['shoes']:
            reply, user = self.get_items(user, item)
            if reply:
                user['equipment']['shoes'] = {}
                remove_equipment['state'] = 'success'
            else:
                remove_equipment['state'] = 'the backpack is full'
        elif item == user['equipment']['knapsack']:
            reply, user = self.get_items(user, item)
            if reply:
                user['equipment']['knapsack'] = {}
                remove_equipment['state'] = 'success'
            else:
                remove_equipment['state'] = 'the backpack is full'
        elif item == user['equipment']['ornaments']:
            reply, user = self.get_items(user, item)
            if reply:
                user['equipment']['ornaments'] = {}
                remove_equipment['state'] = 'success'
            else:
                remove_equipment['state'] = 'the backpack is full'
        
        result.append_remove_equipment(remove_equipment)
        result = self.update(qq, user, result)
        return result

    def hunt(self, qq):
        result = Result()
        user = self.get_user(qq)
        result.set_name(user['config']['name'])
        result_PVE = {
            'init': True,
            'state': 'win',
            'hp': 0,  # 损失生命值
            'monsters': [],  # 怪物
            'gets': []  # 掉落物
        }

        if self.is_map_monster(user):
            if user['attribute']['own']['strength']['number'] < 2:
                result_PVE['state'] = 'no strength'
            else:
                user['attribute']['own']['strength']['number'] -= 2

                map = self.map[user['config']['place']]
                now = 0
                total = 0
                for monster in map['monster']:
                    total += monster['proportion']
                rand = random.randint(0, total - 1)
                for monster in map['monster']:
                    now += monster['proportion']
                    if now >= rand:
                        if user['attribute']['own']['hp']['number'] <= 0:
                            result_PVE['state'] = 'no hp'
                        else:
                            result_PVE['monsters'] = monster['monster']
                            user, result_PVE = self.PVE(qq, user, monster['monster'], result_PVE)

                            if result_PVE['state'] != 'die':
                                user['combat_data']['PVE_victory'] += 1
                            else:
                                user['combat_data']['PVE_defeat'] += 1
                                user['combat_data']['die'] += 1
                        break
        else:
            result_PVE['state'] = 'no monster'
        
        result.append_PVE(result_PVE)
        result = self.update(qq, user, result)
        return result

    def mining(self, qq, times):
        result = Result()
        user = self.get_user(qq)
        result.set_name(user['config']['name'])
        mining = {  # 挖矿结算
            'init': True,
            'state': 'success',
            'times': 0,
            'strength': 0,
            'gets': []
        }

        level = 0
        if user['occupation']['work'] == '矿工':
            level = user['occupation']['work_level']
        
        if times > 10:  # 最高挖二十次
            times = 10
        for index in range(times):
            if user['attribute']['own']['strength']['number'] < 2:
                break

            user['survival_data']['mining'] += 1
            user['attribute']['own']['strength']['number'] -= 2
            mining['strength'] += 2
            mining['times'] += 1

            if level >= 3:
                ran = random.randint(0, 100000)
                items = {
                    'name': '',
                    'number': 1,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
                if ran < 72000:
                    items['name'] = '碎石'
                    reply, user = self.get_items(user, items)
                elif ran < 85000:
                    items['name'] = '石头'
                    reply, user = self.get_items(user, items)
                elif ran < 90070:
                    items['name'] = '铁锭'
                    reply, user = self.get_items(user, items)
                elif ran < 91270:
                    items['name'] = '铝锭'
                    reply, user = self.get_items(user, items)
                elif ran < 92270:
                    items['name'] = '钛矿石'
                    reply, user = self.get_items(user, items)
                elif ran < 92570:
                    items['name'] = '下界石英'
                    reply, user = self.get_items(user, items)
                elif ran < 92820:
                    items['name'] = '灵石'
                    reply, user = self.get_items(user, items)
                elif ran < 92920:
                    items['name'] = '魔法石'
                    reply, user = self.get_items(user, items)
                elif ran < 93000:
                    items['name'] = '末地水晶'
                    reply, user = self.get_items(user, items)
                elif ran < 93500:
                    items['name'] = '钻石'
                    reply, user = self.get_items(user, items)
                elif ran < 95000:
                    items['name'] = '金锭'
                    reply, user = self.get_items(user, items)
                elif ran < 96000:
                    items['name'] = '燧石'
                    reply, user = self.get_items(user, items)
                else:
                    items['name'] = '皮革'
                    reply, user = self.get_items(user, items)
                if reply:
                    mining['gets'].append(items)
            if level >= 2:
                ran = random.randint(0, 100000)
                items = {
                    'name': '',
                    'number': 1,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
                if ran < 78720:
                    items['name'] = '碎石'
                    reply, user = self.get_items(user, items)
                elif ran < 91720:
                    items['name'] = '石头'
                    reply, user = self.get_items(user, items)
                elif ran < 94720:
                    items['name'] = '铁锭'
                    reply, user = self.get_items(user, items)
                elif ran < 95320:
                    items['name'] = '铝锭'
                    reply, user = self.get_items(user, items)
                elif ran < 95820:
                    items['name'] = '钛矿石'
                    reply, user = self.get_items(user, items)
                elif ran < 95920:
                    items['name'] = '下界石英'
                    reply, user = self.get_items(user, items)
                elif ran < 96000:
                    items['name'] = '灵石'
                    reply, user = self.get_items(user, items)
                elif ran < 96500:
                    items['name'] = '钻石'
                    reply, user = self.get_items(user, items)
                elif ran < 97500:
                    items['name'] = '金锭'
                    reply, user = self.get_items(user, items)
                elif ran < 98000:
                    items['name'] = '燧石'
                    reply, user = self.get_items(user, items)
                else:
                    items['name'] = '皮革'
                    reply, user = self.get_items(user, items)
                if reply:
                    mining['gets'].append(items)
            elif level >= 1:
                ran = random.randint(0, 100000)
                items = {
                    'name': '',
                    'number': 1,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
                if ran < 90000:
                    items['name'] = '碎石'
                    reply, user = self.get_items(user, items)
                elif ran < 95000:
                    items['name'] = '石头'
                    reply, user = self.get_items(user, items)
                elif ran < 97110:
                    items['name'] = '铁锭'
                    reply, user = self.get_items(user, items)
                elif ran < 97260:
                    items['name'] = '铝锭'
                    reply, user = self.get_items(user, items)
                elif ran < 97360:
                    items['name'] = '钛矿石'
                    reply, user = self.get_items(user, items)
                elif ran < 97380:
                    items['name'] = '下界石英'
                    reply, user = self.get_items(user, items)
                elif ran < 97400:
                    items['name'] = '灵石'
                    reply, user = self.get_items(user, items)
                elif ran < 97500:
                    items['name'] = '钻石'
                    reply, user = self.get_items(user, items)
                elif ran < 98500:
                    items['name'] = '金锭'
                    reply, user = self.get_items(user, items)
                elif ran < 99000:
                    items['name'] = '燧石'
                    reply, user = self.get_items(user, items)
                else:
                    items['name'] = '皮革'
                    reply, user = self.get_items(user, items)
                if reply:
                    mining['gets'].append(items)
            else:
                ran = random.randint(0, 100000)
                items = {
                    'name': '',
                    'number': 1,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
                if ran < 96000:
                    items['name'] = '碎石'
                    reply, user = self.get_items(user, items)
                elif ran < 98000:
                    items['name'] = '石头'
                    reply, user = self.get_items(user, items)
                elif ran < 99290:
                    items['name'] = '铁锭'
                    reply, user = self.get_items(user, items)
                elif ran < 99390:
                    items['name'] = '铝锭'
                    reply, user = self.get_items(user, items)
                elif ran < 99490:
                    items['name'] = '钛矿石'
                    reply, user = self.get_items(user, items)
                elif ran < 99500:
                    items['name'] = '钻石'
                    reply, user = self.get_items(user, items)
                else:
                    items['name'] = '金锭'
                    reply, user = self.get_items(user, items)
                if reply:
                    mining['gets'].append(items)

        stack_gets = []
        copy_gets = copy.deepcopy(mining['gets'])
        for item in copy_gets:
            is_stack = False
            for temp in range(len(stack_gets)):
                if item['name'] == stack_gets[temp]['name']:
                    stack_gets[temp]['number'] += item['number']
                    is_stack = True
            if not is_stack:
                stack_gets.append(item)
        mining['gets'] = copy.deepcopy(stack_gets)

        result.append_mining(mining)
        result = self.update(qq, user, result)
        return result

    def decompose_item(self, qq, name, number):
        result = Result()
        user = self.get_user(qq)
        result.set_name(user['config']['name'])
        decompose = {  # 分解物品
            'init': True,
            'state': 'success',
            'name': name,
            'number': number,
            'gets': []
        }

        if self.decompose.__contains__(name):
            item = {
                'name': name,
                'number': self.decompose[name]['number'] * number,
                'enchanting': {
                    'sharp': 0,
                    'rapid': 0,
                    'strong': 0
                }
            }
            decompose['number'] = item['number']

            reply, user = self.remove_items(user, item)
            if reply == 0:
                operated = []
                reply2 = True
                for i in self.decompose[name]['path']:
                    temp = copy.deepcopy(i)
                    temp['number'] *= number
                    reply2, user = self.get_items(user, temp)
                    if not reply2:
                        break
                    else:
                        operated.append(temp)
                        decompose['gets'].append(temp)
                
                if not reply2:  # 如果不能分解撤销操作
                    decompose['state'] = 'knapsack'
                    for i in operated:
                        reply3, user = self.remove_items(user, i)  # 退回已经加入的物品
                    reply3, user = self.get_items(user, item)  # 退回分解的物品
                else:
                    user['survival_data']['decompose'] += decompose['number']
            elif reply == 1:
                decompose['state'] = 'not enough'
            elif reply == 2:
                decompose['state'] = 'non-existent'
        else:
            decompose['state'] = 'null'
        
        result.append_decompose(decompose)
        result = self.update(qq, user, result)
        return result

    def synthesis_item(self, qq, name, number):
        result = Result()
        user = self.get_user(qq)
        result.set_name(user['config']['name'])
        synthesis = {
            'init': True,
            'state': 'success',
            'name': name,
            'number': number,
            'consume': []
        }

        level = 0
        if user['occupation']['work'] == '锻造师':
            level = user['occupation']['work_level']

        is_check = False
        path = []
        operated = []

        if self.forger_synthesis.__contains__(name) and level > 0:
            forger_synthesis_copy = copy.deepcopy(self.forger_synthesis[name])
            if level >= forger_synthesis_copy['level']:
                is_check = True
                path = copy.deepcopy(forger_synthesis_copy['path'])
                get_number = self.forger_synthesis[name]['number'] * number
        
        level = 0
        if user['occupation']['work'] == '附魔师':
            level = user['occupation']['work_level']

        if not is_check and self.enchanter_synthesis.__contains__(name) and level > 0:
            enchanter_synthesis_copy = copy.deepcopy(self.enchanter_synthesis[name])
            if level >= enchanter_synthesis_copy['level']:
                is_check = True
                path = copy.deepcopy(enchanter_synthesis_copy['path'])
                get_number = self.enchanter_synthesis[name]['number'] * number
        
        level = 0
        if user['occupation']['work'] == '培育师':
            level = user['occupation']['work_level']

        if not is_check and self.nurturer_synthesis.__contains__(name) and level > 0:
            nurturer_synthesis_copy = copy.deepcopy(self.nurturer_synthesis[name])
            if level >= nurturer_synthesis_copy['level'] and nurturer_synthesis_copy['time'] == 0:
                is_check = True
                path = copy.deepcopy(nurturer_synthesis_copy['path'])
                get_number = self.nurturer_synthesis[name]['number'] * number

        if not is_check and self.synthesis.__contains__(name):
            is_check = True
            path = copy.deepcopy(self.synthesis[name]['path'])
            get_number = self.synthesis[name]['number'] * number


        if is_check:
            for item in path:
                item['number'] *= number
                reply, user = self.remove_items(user, item)
                if reply == 0:
                    operated.append(item)
                    synthesis['consume'].append(item)
                elif reply == 1:
                    synthesis['state'] = 'not enough'
                    break
                elif reply == 2:
                    synthesis['state'] = 'non-existent'
                    break
            
            if synthesis['state'] != 'success':
                for item in operated:
                    reply, user = self.get_items(user, item)
            else:
                item = {
                    'name': name,
                    'number': get_number,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
                synthesis['number'] = get_number
                reply, user = self.get_items(user, item)
                if reply:
                    is_check = True
                    user['survival_data']['synthesis'] += get_number
                else:
                    synthesis['state'] = 'knapsack'
                    for item in operated:
                        reply, user = self.get_items(user, item)
        else:
            synthesis['state'] = 'null'

        result.append_synthesis(synthesis)
        result = self.update(qq, user, result)
        return result

    def enchanting_item(self, qq, item, enchanting_name, level):
        result = Result()
        user = self.get_user(qq)
        result.set_name(user['config']['name'])
        enchanting  = {  # 附魔
            'init': True,
            'state': 'success',
            'cost': [],
            'get': {
                'name': '',
                'number': 0,
                'enchanting': {
                    'sharp': 0,
                    'rapid': 0,
                    'strong': 0
                }
            }
        }

        if user['occupation']['work'] != '附魔师':
            enchanting['state'] = 'job mismatch'

        # 检验是否已经是该附魔，并且检验是否超过最大附魔限制
        if enchanting['state'] == 'success':
            goods = self.get_goods(item['name'])
            if enchanting_name == '锋利':
                if level > goods['enchanting-sharp']:
                    enchanting['state'] = 'max'
                elif level == item['enchanting']['sharp']:
                    enchanting['state'] = 'was'
            elif enchanting_name == '迅捷':
                if level > goods['enchanting-rapid']:
                    enchanting['state'] = 'max'
                elif level == item['enchanting']['rapid']:
                    enchanting['state'] = 'was'
            elif enchanting_name == '坚固':
                if level > goods['enchanting-strong']:
                    enchanting['state'] = 'max'
                elif level == item['enchanting']['strong']:
                    enchanting['state'] = 'was'

        if enchanting['state'] == 'success':
            enchanting['cost'].append(item)
            reply, user = self.remove_items(user, item)
            if reply == 0:

                cost_item = {
                    'name': '',
                    'number': 1,
                    'enchanting': {
                        'sharp': 0,
                        'rapid': 0,
                        'strong': 0
                    }
                }
                if enchanting_name == '锋利':
                    if level == 1:
                        cost_item['name'] = '玛瑙'
                    elif level == 2:
                        cost_item['name'] = '天蓝石'
                    elif level == 3:
                        cost_item['name'] = '青金石'
                elif enchanting_name == '迅捷':
                    if level == 1:
                        cost_item['name'] = '猫眼'
                    elif level == 2:
                        cost_item['name'] = '碧玺'
                    elif level == 3:
                        cost_item['name'] = '翡翠'
                elif enchanting_name == '坚固':
                    if level == 1:
                        cost_item['name'] = '红水晶'
                    elif level == 2:
                        cost_item['name'] = '蓝水晶'
                    elif level == 3:
                        cost_item['name'] = '紫水晶'
                
                if cost_item['name'] == '':
                    enchanting['state'] = 'max'
                    temp, user = self.get_items(user, item)
                else:
                    enchanting['cost'].append(cost_item)
                    reply2, user = self.remove_items(user, cost_item)
                    if reply2 == 0:
                        item_get = copy.deepcopy(item)
                        if enchanting_name == '锋利':
                            item_get['enchanting']['sharp'] = level
                        elif enchanting_name == '迅捷':
                            item_get['enchanting']['rapid'] = level
                        elif enchanting_name == '坚固':
                            item_get['enchanting']['strong'] = level

                        reply3, user = self.get_items(user, item_get)
                        if reply3:
                            enchanting['get'] = item_get
                        else:
                            enchanting['state'] = 'knapsack'
                            temp, user = self.get_items(user, cost_item)
                            temp, user = self.get_items(user, item)
                    elif reply2 == 1:
                        enchanting['state'] = 'not enough'
                        temp, user = self.get_items(user, item)
                    elif reply2 == 2:
                        enchanting['state'] = 'non-existent'
                        temp, user = self.get_items(user, item)
            elif reply == 1:
                enchanting['state'] = 'not enough'
            elif reply == 2:
                enchanting['state'] = 'non-existent'

        result.append_enchanting(enchanting)
        result = self.update(qq, user, result)
        return result

    # 培育
    def cultivation_item(self, qq, name):
        result = Result()
        user = self.get_user(qq)
        result.set_name(user['config']['name'])

        cultivation = {
            'init': True,
            'state': 'success',
            'name': name,
            'time': ''
        }

        if user['occupation']['work'] == '培育师':
            items = {
                'name': name,
                'number': 1,
                'enchanting': {
                    'sharp': 0,
                    'rapid': 0,
                    'strong': 0
                }
            }
            reply, user  = self.remove_items(user, items)
            if reply == 0:
                if len(user['occupation']['farm']['crop']) < user['occupation']['farm']['max']:
                    if self.nurturer_synthesis.__contains__(name):
                        if self.nurturer_synthesis[name]['level'] <= user['occupation']['work_level']:
                            new_crop = {
                                'name': name,
                                'time': addition_minute(getNow.toString(), self.nurturer_synthesis[name]['time'])
                            }
                            user['occupation']['farm']['crop'].append(new_crop)
                            cultivation['time'] = new_crop['time']
                        else:
                            cultivation['state'] = 'level'
                    else:
                        cultivation['state'] = 'null'
                else:
                    cultivation['state'] = 'max'
            else:
                cultivation['state'] = 'non-existent'
        else:
            cultivation['state'] = 'job mismatch'
        
        result.append_cultivation(cultivation)
        result = self.update(qq, user, result)
        return result

    # 收获
    def harvest_item(self, qq):
        result = Result()
        user = self.get_user(qq)
        result.set_name(user['config']['name'])
        harvest = {
            'init': True,
            'state': 'success',
            'harvest': [],
            'gets': []
        }

        
        if user['occupation']['work'] != '培育师':
            harvest['state'] = 'job mismatch'
            result.append_harvest(harvest)
            return result

        is_get = False
        new_crop = []
        for index in range(len(user['occupation']['farm']['crop'])):
            name = user['occupation']['farm']['crop'][index]['name']
            if is_beyond_deadline(user['occupation']['farm']['crop'][index]['time']):
                items = copy.deepcopy(self.nurturer_synthesis[name]['additional'])
                operated = []
                is_back = False
                for i in items:
                    reply, user = self.get_items(user, i)
                    if reply:
                        operated.append(i)
                        harvest['gets'].append(i)
                    else:
                        is_back = True
                        break

                if is_back:
                    for i in operated:
                        reply, user = self.remove_items(user, i)
                    new_crop.append(copy.deepcopy(user['occupation']['farm']['crop'][index]))
                else:
                    is_get = True
                    harvest['harvest'].append(name)
            else:
                new_crop.append(copy.deepcopy(user['occupation']['farm']['crop'][index]))

        if not is_get:
            harvest['state'] = 'nothing'
        else:
            user['occupation']['farm']['crop'] = new_crop

        result.append_harvest(harvest)
        result = self.update(qq, user, result)
        return result

class RPG:
    def __init__(self):
        super().__init__()
        self.core = Core()

    def get_data(self, user):
        reply = '昵称：' + user['config']['name']
        if not user['config']['init_name']:
            reply += '（自动获取）'
        reply += '\n积分：' + str(user['attribute']['own']['gold'])
        reply += '\n体力：' + str(user['attribute']['own']['strength']['number']) + '/' + str(
            self.core.get_max_strength(user)) + '（+' + str(self.core.get_recovery_strength(user)) + '/天）'
        reply += '\n生命值：' + str(user['attribute']['own']['hp']['number']) + '/' + str(
            self.core.get_max_hp(user)) + '（+' + str(self.core.get_recovery_hp(user)) + '/天）'
        reply += '\n精神值：' + str(user['attribute']['own']['san']['number']) + '/' + str(
            self.core.get_max_san(user)) + '（+' + str(self.core.get_recovery_san(user)) + '/天）'
        reply += '\n攻击力：' + str(self.core.get_attack(user))
        reply += '\n护甲：' + str(self.core.get_armor(user))
        reply += '\n速度：' + str(self.core.get_speed(user))

        reply += '\n职业：'
        if user['occupation']['work'] == '' and user['occupation']['fight'] == '':
            reply += '暂无'
        elif user['occupation']['work'] == '':
            reply += user['occupation']['fight'] + get_roman_numerals(user['occupation']['fight_level']) + '（战斗职业）'
        elif user['occupation']['fight'] == '':
            reply += user['occupation']['work'] + get_roman_numerals(user['occupation']['work_level']) + '（生活职业）'
        else:
            reply += user['occupation']['work'] + get_roman_numerals(user['occupation']['work_level']) + '（生活职业）、' + user['occupation']['fight'] + get_roman_numerals(user['occupation']['fight_level']) + '（战斗职业）'
        reply += '\n当前所在群系：' + str(user['config']['place'])
        reply += '\n出生地：' + str(user['config']['born_place'])

        reply += '\nPVP：' + str(self.core.get_PVP_times(user)) + '（' + str(self.core.get_PVP_rate(user)) + '%）'
        
        reply += '\n成就：' + str(self.core.get_achievement_number(user)) + '个'

        reply += '\n背包物品数：' + str(len(self.core.get_knapsack(user))) + '/' + str(self.core.get_max_knapsack(user))

        return reply

    def as_demonstrable(self, string):
        if string == {}:
            return '(暂无)'
        else:
            return get_name_with_enchanting(string)

    def get_equipment(self, user):
        reply = user['config']['name'] + '你的装备如下：'
        reply += '\n武器：' + self.as_demonstrable(user['equipment']['arms'])
        reply += '\n面具：' + self.as_demonstrable(user['equipment']['mask'])
        reply += '\n项链：' + self.as_demonstrable(user['equipment']['necklace'])
        reply += '\n戒指：' + self.as_demonstrable(user['equipment']['ring'])
        reply += '\n头盔：' + self.as_demonstrable(user['equipment']['hat'])
        reply += '\n胸甲：' + self.as_demonstrable(user['equipment']['jacket'])
        reply += '\n护腿：' + self.as_demonstrable(user['equipment']['trousers'])
        reply += '\n靴子：' + self.as_demonstrable(user['equipment']['shoes'])
        reply += '\n背包：' + self.as_demonstrable(user['equipment']['knapsack'])
        reply += '\n饰品：' + self.as_demonstrable(user['equipment']['ornaments'])
        return reply

    def get_rate(self, user):
        reply = user['config']['name'] + '你的数据如下：'
        reply += '\n签到：' + str(user['config']['sign']['sum']) + '天'

        reply += '\nPVP场次：' + str(self.core.get_PVP_times(user)) + '场（胜利：' + str(
            user['combat_data']['PVP_victory']) + '场）'
        reply += '\nPVP胜率：' + str(self.core.get_PVP_rate(user)) + '%'
        reply += '\nPVE场次：' + str(self.core.get_PVE_times(user)) + '场（胜利：' + str(
            user['combat_data']['PVE_victory']) + '场）'
        reply += '\nPVE胜率：' + str(self.core.get_PVE_rate(user)) + '%'
        reply += '\n死亡次数：' + str(user['combat_data']['die'])
        reply += '\n击杀怪物：' + str(user['combat_data']['monster_kill'])
        reply += '\nBOSS击杀数：' + str(user['combat_data']['boss_kill'])

        reply += '\n合成物品：' + str(user['survival_data']['synthesis']) + '个'
        reply += '\n分解物品：' + str(user['survival_data']['decompose']) + '个'
        reply += '\n转换职业：' + str(user['survival_data']['change_occupation']) + '次'
        reply += '\n挖矿：' + str(user['survival_data']['mining']) + '次'
        reply += '\n赠送物品：' + str(user['survival_data']['gift_give']) + '次'
        reply += '\n收到礼物：' + str(user['survival_data']['gift_received']) + '次'
        reply += '\n转换群系：' + str(user['survival_data']['travel']) + '次'
        return reply

    def get_knapsack(self, user):
        knapsack = self.core.get_knapsack(user)
        reply = user['config']['name'] + '你的背包如下：' + str(len(self.core.get_knapsack(user))) + '/' + str(self.core.get_max_knapsack(user))
        
        for item in knapsack:
            reply += '\n' + get_name_with_enchanting(item)
        return reply

    def get_buff(self, user):
        reply = user['config']['name'] + '你的buff如下：'
        if len(user['buff']) == 0:
            reply += '（暂无）'
        else:
            for buff in user['buff']:
                reply += '\n' + buff['name'] + get_roman_numerals(buff['level'])
                if buff['type'] == 0:
                    reply += '（剩余' + str(buff['times']) + '次）'
                else:
                    reply += '（' + buff['date'] + '到期）'
        return reply

    def get_achievement(self, user):
        reply = user['config']['name'] + '你的成就如下：'
        init = False

        if user['achievement']['synthesis'] != 0:
            init = True
            reply += '\n这是什么' + get_roman_numerals(user['achievement']['synthesis']) + '（合成一定数量的物品获得）'
        if user['achievement']['decompose'] != 0:
            init = True
            reply += '\n湮灭' + get_roman_numerals(user['achievement']['decompose']) + '（分解一定数量的物品获得）'
        if user['achievement']['fully_armed'] != 0:
            init = True
            reply += '\n全副武装' + get_roman_numerals(user['achievement']['fully_armed']) + '（穿戴全套装备）'
        if user['achievement']['human_sovereigns'] != 0:
            init = True
            reply += '\n人皇' + get_roman_numerals(user['achievement']['human_sovereigns']) + '（击杀第一个boss）'
        if user['achievement']['boss_killer'] != 0:
            init = True
            reply += '\nBOSS杀手' + get_roman_numerals(user['achievement']['boss_killer']) + '（击杀一定数量的BOSS）'
        if user['achievement']['monster_kill'] != 0:
            init = True
            reply += '\n怪物猎人' + get_roman_numerals(user['achievement']['monster_kill']) + '（击杀一定数量的怪物）'
        if user['achievement']['almighty'] != 0:
            init = True
            reply += '\n全能达人' + get_roman_numerals(user['achievement']['almighty']) + '（转职次数有关）'
        if user['achievement']['hunting_moment'] != 0:
            init = True
            reply += '\n猎杀时刻' + get_roman_numerals(user['achievement']['hunting_moment']) + '（PVP次数有关）'
        if user['achievement']['miner'] != 0:
            init = True
            reply += '\n黄金矿工' + get_roman_numerals(user['achievement']['miner']) + '（挖矿次数有关）'
        if user['achievement']['lumberjack'] != 0:
            init = True
            reply += '\n伐木工' + get_roman_numerals(user['achievement']['lumberjack']) + '（砍树次数有关）'
        if user['achievement']['hamster'] != 0:
            init = True
            reply += '\n仓鼠' + get_roman_numerals(user['achievement']['hamster']) + '（囤积一定数量的物品）'
        if user['achievement']['philanthropist'] != 0:
            init = True
            reply += '\n慈善家' + get_roman_numerals(user['achievement']['philanthropist']) + '（赠送一定数量的物品）'
        if user['achievement']['popular'] != 0:
            init = True
            reply += '\n群宠' + get_roman_numerals(user['achievement']['popular']) + '（被赠送一定数量的物品）'

        if not init:
            reply += '（暂无）'
        return reply

    def get_rank(self):
        rank = self.core.get_rank()
        reply = '排行榜'
        reply += '\n----------------'
        if rank['gold']['1'] != 0:
            temp_user = self.core.get_user(rank['gold']['1'])
            reply += '\n积分第一：' + temp_user['config']['name'] + '（' + str(temp_user['attribute']['own']['gold']) + '）'
        if rank['gold']['2'] != 0:
            temp_user = self.core.get_user(rank['gold']['2'])
            reply += '\n积分第二：' + temp_user['config']['name'] + '（' + str(temp_user['attribute']['own']['gold']) + '）'
        if rank['gold']['3'] != 0:
            temp_user = self.core.get_user(rank['gold']['3'])
            reply += '\n积分第三：' + temp_user['config']['name'] + '（' + str(temp_user['attribute']['own']['gold']) + '）'
        if rank['rate']['all'] != 0:
            temp_user = self.core.get_user(rank['rate']['all'])
            reply += '\n胜率第一：' + temp_user['config']['name'] + '（' + str(self.core.get_PVP_rate(temp_user)) + '%）'
        if rank['rate']['over100'] != 0:
            temp_user = self.core.get_user(rank['rate']['over100'])
            reply += '\n胜率第一（超过100场）：' + temp_user['config']['name'] + '（' + str(self.core.get_PVP_rate(temp_user)) + '%）'
        if rank['fencing_master'] != 0:
            temp_user = self.core.get_user(rank['fencing_master'])
            reply += '\n击剑达人：' + temp_user['config']['name'] + '（' + str(self.core.get_PVP_times(temp_user)) + '场）'
        if rank['ascents'] != 0:
            temp_user = self.core.get_user(rank['ascents'])
            reply += '\n登顶次数最多：' + temp_user['config']['name'] + '（' + str(temp_user['combat_data']['top_times']) + '次）'
        if rank['be_fenced'] != 0:
            temp_user = self.core.get_user(rank['be_fenced'])
            reply += '\n被击剑次数最多：' + temp_user['config']['name'] + '（' + str(temp_user['combat_data']['PVP_passive']) + '次）'
        if rank['monster'] != 0:
            temp_user = self.core.get_user(rank['monster'])
            reply += '\n怪物猎人：' + temp_user['config']['name'] + '（' + str(temp_user['combat_data']['monster_kill']) + '只）'
        if rank['die'] != 0:
            temp_user = self.core.get_user(rank['die'])
            reply += '\n反复作死：' + temp_user['config']['name'] + '（死亡' + str(temp_user['combat_data']['die']) + '次）'
        if rank['travel'] != 0:
            temp_user = self.core.get_user(rank['travel'])
            reply += '\n流浪者：' + temp_user['config']['name'] + '（转换群系' + str(temp_user['survival_data']['travel']) + '次）'
        return reply

    def get_farm(self, user):
        reply = user['config']['name'] + '你的农场如下：'

        if user['occupation']['work'] == '培育师':
            reply += str(len(user['occupation']['farm']['crop'])) + '/' + str(user['occupation']['farm']['max'])

            for crop in user['occupation']['farm']['crop']:
                if is_beyond_deadline(crop['time']):
                    reply += '\n' + crop['name'] + '（已经成熟）'
                else:
                    reply += '\n' + crop['name'] + '（' + crop['time'] + '成熟）'
        else:
            reply = user['config']['name'] + '你不是培育师没有农场'
        return reply

    def get_synthesis(self, name):
        result = Result()
        decompose = self.core.get_decompose()  # 分解
        synthesis = self.core.get_synthesis()  # 合成
        forger_synthesis = self.core.get_forger_synthesis()  # 锻造师合成表
        nurturer_synthesis = self.core.get_nurturer_synthesis()  # 培育师合成表
        enchanter_synthesis = self.core.get_enchanter_synthesis()  # 附魔师合成表

        print(name)
        goods = self.core.get_goods(name)
        if goods is None:
            return '不存在该物品'

        reply = '名字：' + name
        reply += '\n合成路线：'
        if synthesis.__contains__(name):
            reply += name
            if synthesis[name]['number'] != 0:
                reply += 'x' + str(synthesis[name]['number'])
            reply += '<-' + result.show_items(synthesis[name]['path'])
        else:
            reply += '（暂无）'
        reply += '\n分解路线：'
        if decompose.__contains__(name):
            reply += name
            if decompose[name]['number'] != 0:
                reply += 'x' + str(decompose[name]['number'])
            reply += '<-' + result.show_items(decompose[name]['path'])
        else:
            reply += '（暂无）'

        if forger_synthesis.__contains__(name):
            reply += '\n锻造师' + get_roman_numerals(forger_synthesis[name]['level']) + '合成路线：'
            reply += name
            if forger_synthesis[name]['number'] != 0:
                reply += 'x' + str(forger_synthesis[name]['number'])
            reply += '<-' + result.show_items(forger_synthesis[name]['path'])
            
        if enchanter_synthesis.__contains__(name):
            reply += '\n附魔师' + get_roman_numerals(enchanter_synthesis[name]['level']) + '合成路线：'
            reply += name
            if enchanter_synthesis[name]['number'] != 0:
                reply += 'x' + str(enchanter_synthesis[name]['number'])
            reply += '<-' + result.show_items(enchanter_synthesis[name]['path'])

        if nurturer_synthesis.__contains__(name):
            if nurturer_synthesis[name]['time'] == 0:
                reply += '\n培育师' + get_roman_numerals(nurturer_synthesis[name]['level']) + '合成路线：'
                reply += name
                if nurturer_synthesis[name]['number'] != 0:
                    reply += 'x' + str(nurturer_synthesis[name]['number'])
                reply += '<-' + result.show_items(nurturer_synthesis[name]['path'])
            else:
                reply += '\n培育师' + get_roman_numerals(nurturer_synthesis[name]['level']) + '可以培育' + str(nurturer_synthesis[name]['time']) + '分钟获得：' + result.show_items(nurturer_synthesis[name]['additional'])

        reply += '\n参与合成路线：'
        for key, value in synthesis.items():
            for i in value['path']:
                if i['name'] == name:
                    reply += '\n' + key
                    if value['number'] > 1:
                        reply += 'x' + str(value['number'])
                    reply += '<-' + result.show_items(value['path'])
                    break
        
        for key, value in forger_synthesis.items():
            for i in value['path']:
                if i['name'] == name:
                    reply += '\n' + key
                    if value['number'] > 1:
                        reply += 'x' + str(value['number'])
                    reply += '<-' + result.show_items(value['path'])
                    reply += '（锻造师' + get_roman_numerals(value['level']) + '）'
                    break
        
        for key, value in enchanter_synthesis.items():
            for i in value['path']:
                if i['name'] == name:
                    reply += '\n' + key
                    if value['number'] > 1:
                        reply += 'x' + str(value['number'])
                    reply += '<-' + result.show_items(value['path'])
                    reply += '（附魔师' + get_roman_numerals(value['level']) + '）'
                    break
                
        for key, value in nurturer_synthesis.items():
            if value['time'] == 0:
                for i in value['path']:
                    if i['name'] == name:
                        reply += '\n' + key
                        if value['number'] > 1:
                            reply += 'x' + str(value['number'])
                        reply += '<-' + result.show_items(value['path'])
                        reply += '（培育师' + get_roman_numerals(value['level']) + '）'
                        break
            else:
                for i in value['additional']:
                    if i['name'] == name:
                        reply += '\n' + result.show_items(value['additional'])
                        reply += '<-' + result.show_items(value['path'])
                        reply += '（培育师' + get_roman_numerals(value['level']) + '培育）'
                        break
        
        return reply
    
    # 入口函数
    def handle(self, message, qq, name, config, bot_config, be_at, limit):
        bot_qq = bot_config['qq']
        bot_name = bot_config['name']
        message = message.replace('(', '（').replace(')', '）').replace(',', '，')
        message = message.lower()
        message_length = len(message)

        need_reply = False
        reply_text = ''
        reply_image = ''

        if message == '模拟抽卡' or message == '模拟单抽':
            reply_text = MRFZ_card()
            need_reply = True
        elif message == '模拟十连':
            reply_text = MRFZ_card10()
            need_reply = True

        # 先初始化人物
        user = self.core.get_user(qq)
        if not user['config']['init_name']:
            user['config']['name'] = name
            self.core.update(qq, user, Result())
        if user['attribute']['strengthen']['times'] != 0:
            user['attribute']['strengthen']['times'] = 0
            user['attribute']['strengthen']['attack'] = 0
            user['attribute']['strengthen']['armor'] = 0
            self.core.update(qq, user, Result())

        # 数据查看
        if not need_reply:
            if (message == '积分' or message == '我的积分') and not limit:
                reply_text = user['config']['name'] + '\n你的积分为：' + str(user['attribute']['own']['gold'])
                need_reply = True
            elif (message == '体力' or message == '我的体力') and not limit:
                reply_text = user['config']['name'] + '\n你的体力为：' + str(
                    user['attribute']['own']['strength']['number']) + '/' + str(
                    self.core.get_max_strength(user)) + '（+' + str(self.core.get_recovery_strength(user)) + '/天）'
                need_reply = True
            elif (message == '数据' or message == '我的数据') and not limit:
                reply_text = self.get_data(user)
                need_reply = True
            elif (message == '战斗数据' or message == '统计数据') and not limit:
                reply_text = self.get_rate(user)
                need_reply = True
            elif (message == 'buff' or message == '我的buff') and not limit:
                reply_text = self.get_buff(user)
                need_reply = True
            elif (message == '装备' or message == '我的装备') and not limit:
                reply_text = self.get_equipment(user)
                need_reply = True
            elif (message == '背包' or message == '我的背包') and not limit:
                reply_text = self.get_knapsack(user)
                need_reply = True
            elif (message == '成就' or message == '我的成就') and not limit:
                reply_text = self.get_achievement(user)
                need_reply = True
            elif message == '排行榜' and not limit:
                reply_text = self.get_rank()
                need_reply = True

            elif message == '农场' and not limit:
                reply_text = self.get_farm(user)
                need_reply = True

            elif message == '商店':
                shop = self.core.get_shop()
                reply_text = '商品如下：'
                for name in shop:
                    goods = self.core.get_goods(name)
                    if goods is not None:
                        reply_text += '\n' + name + '：' + str(goods['cost']) + '积分'
                        if goods['limit'] != 0:
                            reply_text += '（限购：' + str(goods['limit']) + '）'
                need_reply = True
            elif message == '灵商店':
                soul_shop = self.core.get_soul_shop()
                reply_text = '灵商店商品如下：'
                for name, value in soul_shop.items():
                    goods = self.core.get_goods(name)
                    if goods is not None:
                        reply_text += '\n' + name + '：'
                        init = False
                        for item in value['cost']:
                            if not init:
                                init = True
                            else:
                                reply_text += '，'
                            reply_text += get_name_with_enchanting(item)
                        if goods['limit'] != 0:
                            reply_text += '（限购：' + str(goods['limit']) + '）'
                need_reply = True
            
            elif (message[:4] == '查询合成' or message[:4] == '介绍合成') and not limit:
                temp = message[4:].strip()
                reply_text = self.get_synthesis(temp)
                need_reply = True
            elif (message[:2] == '介绍' or message[:2] == '查询') and not limit:
                name = message[2:].strip()
                if len(name) > 0:
                    result = self.core.get_goods_introduction(name)
                    reply_text = result.show()
                    need_reply = True
            
        # 复杂交互操作
        if not need_reply:
            replylist = [
                '一把把你按在了地上',
                '敲了敲你的脑袋',
                '摸了摸你的头说：“乖，一边去~”',
                '白了你一眼',
                '并不想理你',
                '对你感到了无语',
                '宠溺地说到：“别闹”',
                '的白眼已经要超越天际了',
                '一下子就躲开了'
            ]
            give_replylist = [
                '谢谢啦，不过*bot*不需要哦~',
                '啊嘞？这是要给我的吗？',
                '呜呜~*bot*小柒好感动，不过你还是自己留着吧~'
            ]

            if message == '签到':
                result = self.core.sign(qq)
                reply_text = result.show()
                need_reply = True
            elif '击剑' in message:
                if be_at:
                    reply_text = bot_name + random.choice(replylist)
                    need_reply = True
                elif '@' in message:
                    temp_message = message.replace('击剑', '')
                    temp_message = temp_message.strip()
                    if temp_message[0] == '@' and temp_message[1:].isdigit():
                        result = self.core.PVP(qq, int(temp_message[1:]), True)
                        reply_text = result.show()
                        need_reply = True
            elif '决斗' in message:
                if be_at:
                    reply_text = bot_name + random.choice(replylist)
                    need_reply = True
                elif '@' in message:
                    temp_message = message.replace('决斗', '')
                    temp_message = temp_message.strip()
                    if temp_message[0] == '@' and temp_message[1:].isdigit():
                        result = self.core.PVP(qq, int(temp_message[1:]), False)
                        reply_text = result.show()
                        need_reply = True
            elif '赠送' in message:
                if be_at:
                    reply_text = random.choice(give_replylist).replace('*bot*', bot_name)
                    need_reply = True
                elif '@' in message:
                    temp_message = message.replace('赠送', '')
                    temp_message = temp_message.strip()
                    if temp_message[0] == '@':
                        right = 1
                        for i in range(1, len(temp_message)):
                            if temp_message[right].isdigit():
                                right = i + 1
                            else:
                                break
                        
                        if right < len(temp_message):
                            data = temp_message[right:].strip().split(' ')
                            if len(data) == 1:
                                result = self.core.give(qq, int(temp_message[1:right]), data[0], 1)
                                reply_text = result.show()
                                need_reply = True
                            elif len(data) == 2 and data[1].isdigit():
                                result = self.core.give(qq, int(temp_message[1:right]), data[0], int(data[1]))
                                reply_text = result.show()
                                need_reply = True

            elif message == '挑战榜首' and not limit:
                rank = self.core.get_rank()
                result = self.core.PVP(qq, rank['gold']['1'], True)
                reply_text = result.show()
                need_reply = True
            elif message == '围攻榜首' and not limit:
                rank = self.core.get_rank()
                result = self.core.PVP(qq, rank['gold']['1'], False)
                reply_text = result.show()
                need_reply = True

            elif message == '挖矿' and not limit:
                result = self.core.mining(qq, 1)
                reply_text = result.show()
                need_reply = True
            elif message[:2] == '挖矿' and not limit:
                temp = message[2:].strip()
                if temp[-1] == '次':
                    temp = temp[:-1]
                if temp.isdigit():
                    result = self.core.mining(qq, int(temp))
                    reply_text = result.show()
                    need_reply = True
            elif message == '探险' and not limit:
                reply_text = '探险功能暂时离开了哦~不妨输入“游戏帮助”看看新功能'
                need_reply = True
            elif message == '闲逛' and not limit:
                reply_text = '闲逛功能暂时离开了哦~不妨输入“游戏帮助”看看新功能'
                need_reply = True
            elif message == '打boss' and not limit:
                pass
            elif message == '打怪' and not limit:
                result = self.core.hunt(qq)
                reply_text = result.show()
                need_reply = True

            elif message[:2] == '培育' and not limit:
                temp = message[2:].strip()
                result = self.core.cultivation_item(qq, temp)
                reply_text = result.show()
                need_reply = True
            elif message == '收获' and not limit:
                result = self.core.harvest_item(qq)
                reply_text = result.show()
                need_reply = True
                
        # 简单交互操作
        if not need_reply:
            if message[:2] == '转职' and not limit:
                occupation = message[2:].strip()
                if occupation == '矿工':
                    result = self.core.change_occupation_miner(qq)
                    reply_text = result.show()
                elif occupation == '培育师':
                    result = self.core.change_occupation_nurturer(qq)
                    reply_text = result.show()
                elif occupation == '锻造师':
                    result = self.core.change_occupation_forger(qq)
                    reply_text = result.show()
                elif occupation == '附魔师':
                    result = self.core.change_occupation_enchanter(qq)
                    reply_text = result.show()

                elif occupation == '战士':
                    result = self.core.change_occupation_warrior(qq)
                    reply_text = result.show()
                elif occupation == '盾战士':
                    result = self.core.change_occupation_shield(qq)
                    reply_text = result.show()
                elif occupation == '弓箭手':
                    result = self.core.change_occupation_archer(qq)
                    reply_text = result.show()
                elif occupation == '魔法师':
                    result = self.core.change_occupation_magician(qq)
                    reply_text = result.show()
                else:
                    reply_text = '可选职业如下：'
                    reply_text += '\n生活职业：矿工、培育师、锻造师、附魔师'
                    reply_text += '\n战斗职业：战士、盾战士、弓箭手、魔法师'
                    reply_text += '\n如果需要升级输入“升级生活职业”或者“升级战斗职业”'
                need_reply = True
            elif message == '升级生活职业' and not limit:
                need_reply = True
                result = self.core.change_occupation_work_level(qq)
                reply_text = result.show()
            elif message == '升级战斗职业' and not limit:
                need_reply = True
                result = self.core.change_occupation_fight_level(qq)
                reply_text = result.show()
            elif (message == '清空生活职业' or message == '清除生活职业') and not limit:
                result = self.core.change_occupation_work_null(qq)
                reply_text = result.show()
                need_reply = True
            elif (message == '清空战斗职业' or message == '清除生活职业') and not limit:
                result = self.core.change_occupation_fight_null(qq)
                reply_text = result.show()
                need_reply = True

            elif message[:2] == '购买' and not limit:
                information = message[2:].strip()
                if 'x' in information:
                    data = information.split('x')
                else:
                    data = information.split(' ')

                if len(data) == 2 and data[1].isdigit():
                    result = self.core.purchase(qq, data[0], int(data[1]))
                    reply_text = result.show()
                elif len(data) == 1:
                    result = self.core.purchase(qq, data[0], 1)
                    reply_text = result.show()
                else:
                    reply_text = '购买格式错误！'
                need_reply = True
            
            elif message == '丢弃所有物品' and not limit:
                result = self.core.discard_all(qq)
                reply_text = result.show()
                need_reply = True
            elif message[:2] == '丢弃' and not limit:
                information = message[2:].strip()
                if 'x' in information:
                    data = information.split('x')
                else:
                    data = information.split(' ')

                if len(data) == 2 and data[1].isdigit():
                    result = self.core.discard(qq, data[0], int(data[1]))
                    reply_text = result.show()
                elif len(data) == 1:
                    result = self.core.discard(qq, data[0], 1)
                    reply_text = result.show()
                else:
                    reply_text = '丢弃格式错误！'
                need_reply = True

            elif message[:2] == '卖出' or message[:2] == '出售' and not limit:
                information = message[2:].strip()
                if 'x' in information:
                    data = information.split('x')
                else:
                    data = information.split(' ')

                if len(data) == 2 and data[1].isdigit():
                    result = self.core.sell(qq, data[0], int(data[1]))
                    reply_text = result.show()
                elif len(data) == 1:
                    result = self.core.sell(qq, data[0], 1)
                    reply_text = result.show()
                else:
                    reply_text = '出售格式错误！'
                need_reply = True
            
            elif (message == '清除名字' or message == '清除昵称') and not limit:
                if user['config']['init_name']:
                    user = self.core.get_user(qq)
                    user['config']['name'] = name
                    user['config']['init_name'] = False
                    self.core.update(qq, user, Result())
                    reply_text = '清除成功~'
                else:
                    reply_text = '你没有设置昵称哦~'
                need_reply = True
            elif (message[:4] == '修改名字' or message[:4] == '修改昵称') and not limit:
                nickname = message[4:].strip()
                flag = True
                screens = ['小柒', '操', '傻逼', '母dog', '母狗', 'mugou', '鸡鸡', '群主', '群管理', '窝嫩叠', '尼玛']
                for screen in screens:
                    if screen in nickname:
                        flag = False
                
                if flag:
                    if not self.core.name_check(nickname):
                        user = self.core.get_user(qq)
                        user['config']['name'] = nickname
                        user['config']['init_name'] = True
                        self.core.update(qq, user, Result())
                        reply_text = '修改成功~'
                    else:
                        reply_text = '改名字已被使用'
                else:
                    reply_text = '改名字包含敏感词汇，不可使用'
                need_reply = True

            elif (message[:2] == '装备' or message[:2] == '使用') and not limit:
                temp = message[2:].strip()
                if 'x' in temp:
                    temp_list = temp.split('x')
                else:
                    temp_list = temp.split(' ')
                reply_text = '格式错误！'
                need_reply = True

                if len(temp_list) == 1:
                    result = self.core.use(qq, temp_list[0], 1)
                    reply_text = result.show()
                elif len(temp_list) == 2 and temp_list[1].isdigit():
                    result = self.core.use(qq, temp_list[0], int(temp_list[1]))
                    reply_text = result.show()
            elif (message[:2] == '取下' or message[:2] == '卸下') and not limit:
                temp = message[2:].strip()
                result = self.core.remove_equipment(qq, temp)
                reply_text = result.show()
                need_reply = True

            elif message[:2] == '合成' and not limit:
                temp = message[2:].strip()
                if 'x' in temp:
                    temp_list = temp.split('x')
                else:
                    temp_list = temp.split(' ')

                if len(temp_list) == 1:
                    result = self.core.synthesis_item(qq, temp_list[0], 1)
                    reply_text = result.show()
                    need_reply = True
                elif len(temp_list) == 2 and temp_list[1].isdigit():
                    result = self.core.synthesis_item(qq, temp_list[0], int(temp_list[1]))
                    reply_text = result.show()
                    need_reply = True

            elif message[:2] == '分解' and not limit:
                temp = message[2:].strip()
                if 'x' in temp:
                    temp_list = temp.split('x')
                else:
                    temp_list = temp.split(' ')

                if len(temp_list) == 1:
                    result = self.core.decompose_item(qq, temp_list[0], 1)
                    reply_text = result.show()
                    need_reply = True
                elif len(temp_list) == 2 and temp_list[1].isdigit():
                    result = self.core.decompose_item(qq, temp_list[0], int(temp_list[1]))
                    reply_text = result.show()
                    need_reply = True

            elif message[:2] == '附魔' and not limit:
                temp = message[2:].strip()
                information = temp.split(' ')
                if len(information) == 2:
                    need_reply = True
                    reply_text = '格式错误'
                    name, enchanting = analysis_name(information[0])
                    items = {
                        'name': name,
                        'number': 1,
                        'enchanting': enchanting
                    }
                    if information[1][-1].isdigit():
                        level = int(information[1][-1])
                        enchanting_name = information[1][:-1]
                        result = self.core.enchanting_item(qq, items, enchanting_name, level)
                        reply_text = result.show()

        # 管理员操作
        if not need_reply:
            if qq == bot_config['master'] or qq in bot_config['RPG_administrator']:
                need_reply, reply_text, reply_image = self.operate(message, qq, config, bot_config)

        if need_reply:
            if user['config']['version'] == -1:
                user['config']['version'] = 0
                reply_text = user['config']['report']
                user['config']['report'] = ''
                self.core.update(qq, user, Result())

        return need_reply, reply_text, reply_image

    def operate(self, message, qq, config, bot_config):
        need_reply = False
        reply_text = ''
        reply_image = ''
        
        if message[:4] == '修改积分':
            number = message[4:].strip().split(' ')
            if len(number) == 1 and number[0].isdigit():
                user = self.core.get_user(qq)
                user['attribute']['own']['gold'] = int(number[0])
                self.core.update(qq, user, Result())
                reply_text = '修改成功~'
            elif len(number) == 2 and number[0].isdigit() and number[1].isdigit():
                user = self.core.get_user(int(number[0]))
                user['attribute']['own']['gold'] = int(number[1])
                self.core.update(int(number[0]), user, Result())
                reply_text = '修改成功~'
            else:
                reply_text = '格式错误~'
            need_reply = True
        elif message[:4] == '修改体力':
            number = message[4:].strip().split(' ')
            if len(number) == 1 and number[0].isdigit():
                user = self.core.get_user(qq)
                user['attribute']['own']['strength']['number'] = int(number[0])
                self.core.update(qq, user, Result())
                reply_text = '修改成功~'
            elif len(number) == 2 and number[0].isdigit() and number[1].isdigit():
                user = self.core.get_user(int(number[0]))
                user['attribute']['own']['strength']['number'] = int(number[1])
                self.core.update(int(number[0]), user, Result())
                reply_text = '修改成功~'
            else:
                reply_text = '格式错误~'
            need_reply = True
        elif message[:4] == '给予物品':
            reply_text = '格式错误'
            need_reply = True
            information = message[4:].strip().split(' ')
            if len(information) == 1:
                name, enchanting = analysis_name(information[0])
                user = self.core.get_user(qq)

                goods = self.core.get_goods(name)
                if goods is None:
                    reply_text = '物品不存在！'
                else:
                    items = {
                        'name': name,
                        'number': 1,
                        'enchanting': enchanting
                    }
                    reply, user = self.core.get_items(user, items)

                    if reply:
                        self.core.update(qq, user, Result())
                        reply_text = '给予成功~'
                    else:
                        reply_text = '对方背包已满'
            elif len(information) == 2:
                if information[0].isdigit():
                    name, enchanting = analysis_name(information[1])
                    user = self.core.get_user(int(information[0]))

                    goods = self.core.get_goods(name)
                    if goods is None:
                        reply_text = '物品不存在！'
                    else:
                        items = {
                            'name': name,
                            'number': 1,
                            'enchanting': enchanting
                        }
                        reply, user = self.core.get_items(user, items)

                        if reply:
                            self.core.update(int(information[0]), user, Result())
                            reply_text = '给予成功~'
                        else:
                            reply_text = '对方背包已满'
                elif information[1].isdigit():
                    name, enchanting = analysis_name(information[0])
                    user = self.core.get_user(qq)

                    goods = self.core.get_goods(name)
                    if goods is None:
                        reply_text = '物品不存在！'
                    else:
                        items = {
                            'name': name,
                            'number': int(information[1]),
                            'enchanting': enchanting
                        }
                        reply, user = self.core.get_items(user, items)

                        if reply:
                            self.core.update(qq, user, Result())
                            reply_text = '给予成功~'
                        else:
                            reply_text = '对方背包已满'
                elif information[0] == '*':
                    reply_text = '给予全部人物品' + information[1] + '，但是还未实现'
            elif len(information) == 3:
                if information[0].isdigit() and information[2].isdigit():
                    name, enchanting = analysis_name(information[1])
                    user = self.core.get_user(int(information[0]))

                    goods = self.core.get_goods(name)
                    if goods is None:
                        reply_text = '物品不存在！'
                    else:
                        items = {
                            'name': name,
                            'number': int(information[2]),
                            'enchanting': enchanting
                        }
                        reply, user = self.core.get_items(user, items)

                        if reply:
                            self.core.update(int(information[0]), user, Result())
                            reply_text = '给予成功~'
                        else:
                            reply_text = '对方背包已满'
        elif message[:6] == '给予buff':
            reply_text = '格式错误'
            need_reply = True
            information = message[6:].strip().split(' ')
            buff = {
                'name': '',  # buff名字
                'type': 0,  # 0表示次数，1表示时间
                'level': 1,  # 级别
                'date': '',  # 时间
                'times': 0  # 次数
            }
            target_qq = qq

            if len(information) == 3 and information[0].isdigit():
                target_qq = int(information[0])
                if information[1][-1] == '级' and information[1][-2].isdigit():
                    buff['name'] = information[1][:-2]
                    buff['level'] = int(information[1][-2])
                else:
                    buff['name'] = information[1]
                    
                if information[2][-1] == '次' and information[2][:-1].isdigit():
                    buff['times'] = int(information[2][:-1])
                elif information[2][-2:] == '分钟' and information[2][:-2].isdigit():
                    buff['type'] = 1
                    buff['date'] = addition_minute(getNow.toString(), int(information[2][:-2]))

                user = self.core.get_user(target_qq)
                reply, user = self.core.get_buff(user, buff)
                self.core.update(target_qq, user, Result())
                if reply:
                    reply_text = '给予成功！'
                else:
                    reply_text = '不存在该buff'

        elif message[:4] == '查看数据':
            temp_message = message[4:].strip()
            if temp_message.isdigit():
                user = self.core.get_user(int(temp_message))
                reply_text = self.get_data(user)
                need_reply = True
        elif message[:6] == '查看buff':
            temp_message = message[6:].strip()
            if temp_message.isdigit():
                user = self.core.get_user(int(temp_message))
                reply_text = self.get_buff(user)
                need_reply = True
        elif message[:6] == '查看统计数据':
            temp_message = message[6:].strip()
            if temp_message.isdigit():
                user = self.core.get_user(int(temp_message))
                reply_text = self.get_rate(user)
                need_reply = True
        elif message[:4] == '查看装备':
            temp_message = message[4:].strip()
            if temp_message.isdigit():
                user = self.core.get_user(int(temp_message))
                reply_text = self.get_equipment(user)
                need_reply = True
        elif message[:4] == '查看背包':
            temp_message = message[4:].strip()
            if temp_message.isdigit():
                user = self.core.get_user(int(temp_message))
                reply_text = self.get_knapsack(user)
                need_reply = True
        elif message[:4] == '查看成就':
            temp_message = message[4:].strip()
            if temp_message.isdigit():
                user = self.core.get_user(int(temp_message))
                reply_text = self.get_achievement(user)
                need_reply = True
        
        return need_reply, reply_text, reply_image
