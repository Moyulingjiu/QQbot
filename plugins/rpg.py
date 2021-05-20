# 一个rpg游戏，附带在小柒上
import asyncio # 异步
from graia.application.entry import (
    GraiaMiraiApplication, Session,
    MessageChain, Group, Friend, Member, MemberInfo,
    Plain, Image, AtAll, At, Face, Source
)
from graia.application.entry import (
    BotMuteEvent, BotGroupPermissionChangeEvent
)
from graia.broadcast import Broadcast


import random
import datetime
import linecache

from plugins import dataManage

async def menu(strMessage, groupId, member, app, botBaseInformation, messageChain):
    Bot_QQ = botBaseInformation['baseInformation']['Bot_QQ']
    Bot_Name = botBaseInformation['baseInformation']['Bot_Name']

    needReply = False
    needAt = False
    reply = ''
    isImage = ''

    memberName = ''
    if groupId != 0:
        memberName = member.name
    else:
        memberName = member.nickname

    newUser(member.id, memberName)

    if strMessage.strip() == '签到':
        id = member.id
        reply = memberName + sign(id)
        needReply = True
    elif '击剑' in strMessage and groupId != 0:
        tmp = strMessage.replace('击剑', '').strip()
        if tmp[0] == '@' and tmp[1:].isdigit():
            target = int(tmp[1:])
            if target != Bot_QQ:
                await fencing(member, target, app)
            else:
                replylist = ['一把把你按在了地上', '敲了敲你的脑袋', '摸了摸你的头说：“乖，一边去~”']
                reply = Bot_Name + random.choice(replylist)
        needReply = True
    elif strMessage == '我的积分' or strMessage == '积分':
        id = member.id
        reply = memberName + getGold(id)
        needReply = True
    elif strMessage == '我的体力' or strMessage == '体力':
        id = member.id
        reply = memberName + getStrength(id)
        needReply = True
    elif strMessage == '我的胜率' or strMessage == '胜率':
        id = member.id
        reply = memberName + getRate(id)
        needReply = True
    elif strMessage == '排行榜':
        reply = getRank()
        needReply = True
    elif strMessage == '兑换体力':
        reply = memberName + rechargeStrength(member.id)
        needReply = True
    elif strMessage == '模拟抽卡' or strMessage == '模拟单抽':
        reply = MRFZ_card()
        needReply = True
    elif strMessage == '模拟十连':
        reply = MRFZ_card10()
        needReply = True
    elif strMessage == '围攻榜首' and groupId != 0:
        await fencingTop(member, app)
        needReply = True
    elif strMessage == '探险':
        reply = fishing(member.id, memberName)
        needReply = True
    elif strMessage == '闲逛':
        reply = memberName + hangOut(member.id)
        needReply = True
    elif '摸摸' in strMessage and groupId != 0:
        tmp = strMessage.replace('摸摸', '').strip()
        if tmp[0] == '@' and tmp[1:].isdigit():
            target = int(tmp[1:])
            print(target)
            print(Bot_QQ)
            print(str(target) == str(Bot_QQ))
            if str(target) == str(Bot_QQ):
                reply = Bot_Name + touch(member.id, memberName)
                print(reply)
        needReply = True
    
    return (needReply, needAt, reply, isImage)

def sign(id):
    today = str(datetime.date.today())
    user = dataManage.load_obj('user/information')
    if today != user[id]['sign-date']:
        user[id]['sign-date'] = today
        user[id]['gold'] += random.randint(3, 10)
        dataManage.save_obj(user, 'user/information')
        return '签到成功！当前积分：' + str(user[id]['gold'])
    else:
        return '你今天已经签到过了哦~'

def getGold(id):
    user = dataManage.load_obj('user/information')
    return '你的积分为：' + str(user[id]['gold'])
  
def getStrength(id):
    user = dataManage.load_obj('user/information')
    return '你的体力为：' + str(user[id]['attribute']['strength'])

def getRate(id):
    user = dataManage.load_obj('user/information')
    if user[id]['match']['win'] + user[id]['match']['lose'] == 0:
        return  '你还暂未进行任何对决'
    rate = float(user[id]['match']['win']) / float(user[id]['match']['win'] + user[id]['match']['lose'])
    rate = round(rate, 2) * 100
    result = '\n总计场次：' + str(user[id]['match']['win'] + user[id]['match']['lose'])
    result += '\n获胜次数：' + str(user[id]['match']['win'])
    result += '\n你的胜率为：' + str(int(rate)) + '%'
    return result

def newUser(id, name):
    user = dataManage.load_obj('user/information')
    today = str(datetime.date.today())
    
    if not user.__contains__(id):
        user[id] = {
            'name': name,
            'gold': 0,
            'sign-date': '',
            'warehouse': [],
            'match': {
                'win': 0,
                'lose': 0,
                'monster': 0,
                'legend': 0
            },
            'equipment': {
                'hat': '',
                'jacket': '',
                'trousers': '',
                'shoes': '',
                'ring-left': '',
                'ring-right': '',
                'knapsack': ''
            },
            'attribute': {
                'attack': 5,
                'hp': 100,
                'defense': 0,
                'san': 100,
                'strength': 20
            },
            'last-operate-date': today
        }
        dataManage.save_obj(user, 'user/information')
    else:
        if user[id]['last-operate-date'] != today:
            user[id]['attribute']['strength'] += 20
            user[id]['last-operate-date'] = today
            user[id]['name'] = name
            dataManage.save_obj(user, 'user/information')

def rechargeStrength(id):
    user = dataManage.load_obj('user/information')
    if user[id]['gold'] < 2:
        return '你的积分小于2不能兑换体力'
    user[id]['gold'] -= 2
    user[id]['attribute']['strength'] += 5
    dataManage.save_obj(user, 'user/information')
    return '你获得了5点体力'

async def fencing(member, id2, app):
    if member.id == id2:
        await app.sendGroupMessage(member.group, MessageChain.create([
            Plain('好家伙，和自己击剑呢？')
        ]))
        return

    other = await app.getMember(member.group.id, id2)

    if other != None:
        newUser(other.id, other.name)
        user = dataManage.load_obj('user/information')
        if user[other.id]['gold'] <= 1:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain(other.name + '的积分值小于等于1，不能进行击剑')
            ]))
            return
        if user[member.id]['gold'] <= 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('你暂无积分值不可以击剑')
            ]))
            return
        if user[member.id]['attribute']['strength'] <= 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('你今日的体力值已经为0了，不能再击剑啦~')
            ]))
            return
        user[member.id]['attribute']['strength'] -= 1
 
        ran = random.randint(1, 100)
        winner = ''
        loser = ''
        result = ''
        if ran < 60:
            winner = member.name
            loser = other.name
            maxGetGold = 3
            if user[other.id]['gold'] < 3:
                maxGetGold = user[other.id]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['gold'] += getGold
            user[other.id]['gold'] -= getGold
            user[member.id]['match']['win'] += 1
            user[other.id]['match']['lose'] += 1
            result = member.name + '你击剑打败了'+ loser + '，夺走了对方' + str(getGold) + '点节操（积分值）'
        else:
            winner = other.name
            loser = member.name
            maxGetGold = 3
            if user[member.id]['gold'] < 3:
                maxGetGold = user[member.id]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['gold'] -= getGold
            user[other.id]['gold'] += getGold
            user[member.id]['match']['lose'] += 1
            user[other.id]['match']['win'] += 1
            result = member.name + '你击剑输给了' + winner + '，被夺走了' + str(getGold) + '点节操（积分值）'
        
        maxLine = int(linecache.getline(r'data/user/fencing.txt', 1))
        x = random.randrange(0, maxLine)
        lineNumber = linecache.getline(r'data/user/fencing.txt', x * 2 + 3)
        process = lineNumber.replace('*name1*', winner).replace('*name2*', loser)

        await app.sendGroupMessage(member.group, MessageChain.create([
            Plain(process),
            Plain('------------\n'),
            Plain(result)
        ]))
        dataManage.save_obj(user, 'user/information')

async def fencingTop(member, app):
    user = dataManage.load_obj('user/information')
    goldId = 0

    for key, value in user.items():
        if goldId == 0:
            goldId = key
        else:
            if value['gold'] > user[goldId]['gold']:
                goldId = key
    
    if goldId == member.id:
        await app.sendGroupMessage(member.group, MessageChain.create([
            Plain('自己也要围攻自己吗？')
        ]))
        return
    else:
        user = dataManage.load_obj('user/information')
        if user[goldId]['gold'] <= 1:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain(user[goldId]['name'] + '的积分值小于等于1，不能进行击剑')
            ]))
            return
        if user[member.id]['gold'] <= 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('你暂无积分值不可以击剑')
            ]))
            return
        if user[member.id]['attribute']['strength'] <= 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('你今日的体力值已经为0了，不能再击剑啦~')
            ]))
            return
        user[member.id]['attribute']['strength'] -= 1
 
        ran = random.randint(1, 100)
        winner = ''
        loser = ''
        result = ''
        if ran < 60:
            winner = member.name
            loser = user[goldId]['name']
            maxGetGold = 3
            if user[goldId]['gold'] < 3:
                maxGetGold = user[goldId]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['gold'] += getGold
            user[goldId]['gold'] -= getGold
            user[member.id]['match']['win'] += 1
            user[goldId]['match']['lose'] += 1
            result = member.name + '你击剑打败了'+ loser + '，夺走了对方' + str(getGold) + '点节操（积分值）'
        else:
            winner = user[goldId]['name']
            loser = member.name
            maxGetGold = 3
            if user[member.id]['gold'] < 3:
                maxGetGold = user[member.id]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['gold'] -= getGold
            user[goldId]['gold'] += getGold
            user[member.id]['match']['lose'] += 1
            user[goldId]['match']['win'] += 1
            result = member.name + '你击剑输给了' + winner + '，被夺走了' + str(getGold) + '点节操（积分值）'
        
        maxLine = int(linecache.getline(r'data/user/fencing.txt', 1))
        x = random.randrange(0, maxLine)
        lineNumber = linecache.getline(r'data/user/fencing.txt', x * 2 + 3)
        process = lineNumber.replace('*name1*', winner).replace('*name2*', loser)

        await app.sendGroupMessage(member.group, MessageChain.create([
            Plain(process),
            Plain('------------\n'),
            Plain(result)
        ]))
        dataManage.save_obj(user, 'user/information')
        
def getRank():
    user = dataManage.load_obj('user/information')

    goldId = 0
    goldId2 = 0
    goldId3 = 0

    rateId = 0
    rate = 0.0
    rateValueId = 0
    rateValue = 0

    timesId = 0

    if len(user) == 0:
        return '暂无排行榜'

    for key, value in user.items():
        if goldId == 0:
            goldId = key
            rateId = key
            timesId = key
            if user[rateId]['match']['win'] + user[rateId]['match']['lose'] != 0:
                rate = float(user[rateId]['match']['win']) / float(user[rateId]['match']['win'] + user[rateId]['match']['lose'])
            else:
                rate = 0.0
        else:
            if value['gold'] > user[goldId]['gold']:
                goldId3 = goldId2
                goldId2 = goldId
                goldId = key
            elif goldId2 == 0 or value['gold'] > user[goldId2]['gold']:
                goldId3 = goldId2
                goldId2 = key 
            elif goldId3 == 0 or value['gold'] > user[goldId3]['gold']:
                goldId3 = key

            if user[key]['match']['win'] + user[key]['match']['lose'] > user[timesId]['match']['win'] + user[timesId]['match']['lose']:
                timesId = key

            if user[key]['match']['win'] + user[key]['match']['lose'] != 0:
                rate2 = float(user[key]['match']['win']) / float(user[key]['match']['win'] + user[key]['match']['lose'])
                if rate2 > rate:
                    rate = rate2
                    rateId = key
                if user[key]['match']['win'] + user[key]['match']['lose'] > 50:
                    if rateValueId == 0:
                        rateValue = rate2
                        rateValueId = key
                    elif rate2 > rateValue:
                        rateValue = rate2
                        rateValueId = key

        
    userRank = dataManage.load_obj('user/rank')
    result = '排行榜\n'
    result += '----------------\n'
    result += '积分第一：' + user[goldId]['name'] + '（' + str(user[goldId]['gold']) + '）\n'
    if goldId2 != 0:
        result += '积分第二：' + user[goldId2]['name'] + '（' + str(user[goldId2]['gold']) + '）\n'
    if goldId3 != 0:
        result += '积分第三：' + user[goldId3]['name'] + '（' + str(user[goldId3]['gold']) + '）\n'
    
    rate = round(rate, 2) * 100
    result += '胜率第一：' + user[rateId]['name'] + '（' + str(int(rate)) + '%）\n'
    rateValue = round(rateValue, 2) * 100
    if rateValueId != 0:
        result += '胜率第一（大于50场）：' + user[rateValueId]['name'] + '（' + str(int(rateValue)) + '%）\n'
    result += '击剑达人：' + user[timesId]['name'] + '（' + str(int(user[timesId]['match']['win'] + user[timesId]['match']['lose'])) + '场）'
    return result

# ============================================

def MRFZ_card():
    botBaseInformation = dataManage.load_obj('baseInformation')
    if not botBaseInformation['reply'].__contains__('cards'):
        botBaseInformation['reply']['cards'] = 0
    botBaseInformation['reply']['cards'] += 1
    if botBaseInformation['reply']['cards'] > 5:
        return '你抽卡太快了，每分钟最多只能抽5次哦~'
    dataManage.save_obj(botBaseInformation, 'baseInformation')

    card1 = []
    card2 = []
    card3 = []
    card4 = []
    card5 = []
    card6 = []
    information = []
    with open('data/明日方舟/PersonaCard.txt', 'r+', encoding = 'utf-8') as f:
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
    botBaseInformation = dataManage.load_obj('baseInformation')
    if not botBaseInformation['reply'].__contains__('cards'):
        botBaseInformation['reply']['cards'] = 0
    botBaseInformation['reply']['cards'] += 1
    if botBaseInformation['reply']['cards'] > 5:
        return '你抽卡太快了，每分钟最多只能抽5次哦~'
    dataManage.save_obj(botBaseInformation, 'baseInformation')

    card1 = []
    card2 = []
    card3 = []
    card4 = []
    card5 = []
    card6 = []
    information = []
    with open('data/明日方舟/PersonaCard.txt', 'r+', encoding = 'utf-8') as f:
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
def touch(id, name):
    user = dataManage.load_obj('user/information')
    if user[id]['attribute']['strength'] < 1 or user[id]['gold'] > 1:
        return '对' + name + '不屑一顾'
    user[id]['attribute']['strength'] -= 1
    user[id]['gold'] += random.randint(1, 5)
    dataManage.save_obj(user, 'user/information')
    return '看' + name + '太可怜，于是给了你一些积分'

'''
消耗体力：1

50% 啥也没有
20% 1点体力 | 1点积分
20% 2点体力 | 2点积分
9% 3点体力 | 3点积分
0.9% 4点体力 | 4点积分
0.1% 10点体力 | 10点积分

E = 0.916
'''
def fishing(id, name):
    user = dataManage.load_obj('user/information')
    if user[id]['attribute']['strength'] < 1:
        return name + '体力值不足不能探险'
    user[id]['attribute']['strength'] -= 1
    ran = random.randrange(0, 1000)
    ran2 = random.randrange(0, 2)

    describe_dict = ['你来到了一个黑漆漆的山洞，四周十分安静，一番探索之后', '你来到一个遗迹，一番探索之后', '你发现了一个宝箱', '在亚马逊的原始森林里，你被讨厌的虫子烦的要死']

    describe = random.choice(describe_dict)
    result = ''

    if ran < 500:
        result = '什么也没有获得'
    elif ran < 700:
        if ran2 == 0:
            user[id]['attribute']['strength'] += 1
            result = '获得了1点体力'
        else:
            user[id]['gold'] += 1
            result = '获得了1点积分值'
    elif ran < 900:
        if ran2 == 0:
            user[id]['attribute']['strength'] += 2
            result = '获得了2点体力'
        else:
            user[id]['gold'] += 2
            result = '获得了2点积分值'
    elif ran < 990:
        if ran2 == 0:
            user[id]['attribute']['strength'] += 3
            result = '获得了3点体力'
        else:
            user[id]['gold'] += 3
            result = '获得了3点积分值'
    elif ran < 999:
        if ran2 == 0:
            user[id]['attribute']['strength'] += 4
            result = '获得了4点体力'
        else:
            user[id]['gold'] += 4
            result = '获得了4点积分值'
    else:
        if ran2 == 0:
            user[id]['attribute']['strength'] += 10
            result = '获得了10点体力'
        else:
            user[id]['gold'] += 10
            result = '获得了10点积分值'

    
    dataManage.save_obj(user, 'user/information')
    return name + describe + '，' + result


def hangOut(id):
    user = dataManage.load_obj('user/information')
    if user[id]['gold'] <= 0:
        return '你的积分为0，不能闲逛了'
    result = ''

    ran = random.randrange(0, 19)
    if ran == 0:
        result = '你在闲逛的时候被舞女拉进了小树林，积分-2，体力+2'
        user[id]['gold'] -= 2
        user[id]['attribute']['strength'] += 2
    elif ran == 1:
        result = '你在闲逛的时候遇见了阿拉灯神丁，他说实现你三个愿望然后摸了你的钱包转身就走，积分+3'
        user[id]['gold'] += 3
    elif ran == 2:
        result = '你在闲逛的时候邂逅了笑猫，他送给你了一个大大的笑容，体力+3'
        user[id]['attribute']['strength'] += 3
    elif ran == 3:
        result = '你在闲逛的时候被网红火锅店吸引没忍住冲了进去，积分-1，体力+2'
        user[id]['gold'] -= 1
        user[id]['attribute']['strength'] += 2
    elif ran == 4:
        result = '你在闲逛的时候逛回去了，啥也没获得,体力-1'
        if user[id]['attribute']['strength'] > 1:
            user[id]['attribute']['strength'] -= 1
    elif ran == 5:
        result = '你在闲逛的时候踩了一坨便便并且坚信明天会走狗屎运'
    elif ran == 6:
        result = '你在闲逛的时候遇见了一个可怜的乞丐，给了他一些钱，积分-5'
        user[id]['gold'] -= 5
    elif ran == 7:
        result = '你在闲逛的时候玩手机没看路，撞上了电线杆，体力值-10'
        if user[id]['attribute']['strength'] > 10:
            user[id]['attribute']['strength'] -= 10
        else:
            user[id]['attribute']['strength'] = 0
    elif ran == 8:
        result = '你在路上看美女被小柒发现，惨遭暴打，体力-2，积分-2'
        user[id]['gold'] -= 2
        if user[id]['attribute']['strength'] > 2:
            user[id]['attribute']['strength'] -= 2
        else:
            user[id]['attribute']['strength'] = 0
    elif ran == 9:
        result = '你出门之后天下起了倾盆大雨，狂奔回家之后发现钥匙丢在了咖啡厅，于是去咖啡厅拿了钥匙后折返，体力-1'
        if user[id]['attribute']['strength'] > 1:
            user[id]['attribute']['strength'] -= 1
        else:
            user[id]['attribute']['strength'] = 0
    elif ran == 10:
        result = '你闲逛的时候碰见富豪在路上撒钱，积分+2'
        user[id]['gold'] += 2
    elif ran == 11:
        result = '你在闲逛的时候，不小心掉进了下水道，积分-5，体力-5'
        user[id]['gold'] -= 5
        if user[id]['attribute']['strength'] > 5:
            user[id]['attribute']['strength'] -= 5
        else:
            user[id]['attribute']['strength'] = 0
    elif ran == 12:
        result = '你在闲逛的时候，遇见了一个卖苹果的老婆婆，你买了一些苹果，积分-1，体力+5'
        user[id]['gold'] -= 1
        user[id]['attribute']['strength'] += 5
    elif ran == 13:
        result = '你在闲逛的时候，遇见了一个卖苹果的老婆婆，你买了一些苹果，发现是毒苹果，积分-1，体力-5'
        user[id]['gold'] -= 1
        if user[id]['attribute']['strength'] > 5:
            user[id]['attribute']['strength'] -= 5
        else:
            user[id]['attribute']['strength'] = 0
    elif ran == 14:
        result = '你在闲逛的时候，决定尝试一下彩票，但是没有中奖，积分-2'
        user[id]['gold'] -= 2
    elif ran == 15:
        result = '你在闲逛的时候，决定尝试一下彩票，中奖了，积分+2'
        user[id]['gold'] += 2
    elif ran == 16:
        result = '你在闲逛的时候，决定尝试一下彩票，中奖了，积分+3'
        user[id]['gold'] += 3
    elif ran == 17:
        result = '你在闲逛的时候，决定尝试一下彩票，中奖了，积分+1'
        user[id]['gold'] += 1
    elif ran == 18:
        result = '你在闲逛的时候，决定尝试一下刮刮乐，但是没有中奖，积分-2'
        user[id]['gold'] -= 2
    elif ran == 19:
        result = '你在闲逛的时候，决定尝试一下刮刮乐，中奖了，积分+1'
        user[id]['gold'] += 1
    elif ran == 20:
        result = '你在闲逛的时候，嘴馋买了个 冰淇淋，积分-2'
        user[id]['gold'] -= 2
    elif ran == 21:
        result = '你在闲逛的时候，嘴馋买了个 冰淇淋，积分-2，体力+2'
        user[id]['gold'] -= 2
        user[id]['attribute']['strength'] += 2

    else:
        result = '你闲逛了一圈，啥也没有发生'

    
    dataManage.save_obj(user, 'user/information')
    return result