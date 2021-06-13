# 一个rpg游戏，附带在小柒上
import asyncio  # 异步
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
from plugins import logManage
from plugins import getNow

user = {}  # 用户数据
systemData = {}
init = True

baseInformation = {}  # 基本介绍

buff = {}  # buff表

goods = {}  # 物品表

goodsAvailable = []  # 商店

decompose = {}  # 分解

synthesis = {}  # 合成


async def menu(message, group_id, member, app, bot_information, right, be_at):
    global user
    global systemData
    Bot_QQ = bot_information['baseInformation']['Bot_QQ']
    Bot_Name = bot_information['baseInformation']['Bot_Name']

    needReply = False
    needAt = False
    reply = ''
    isImage = ''
    at_qq = 0

    if group_id in bot_information['gameOff']:  # 本群关闭了游戏
        return needReply, reply, isImage, at_qq, needAt

    memberName = ''
    if group_id != 0:
        memberName = member.name
    else:
        memberName = member.nickname

    newUser(member.id, memberName)

    if message.strip() == '签到':
        id = member.id
        reply = memberName + sign(id)
        needReply = True
    elif message[:4] == '查询合成' or message[:4] == '介绍合成' or message[:4] == '查看合成' or message[:4] == '解释合成' or message[:4] == '合成路线':
        reply = getSynthesis(message[4:].strip())
        needReply = True
    elif message[:4] == '查询分解' or message[:4] == '介绍分解' or message[:4] == '查看分解' or message[:4] == '解释分解':
        reply = getDecompose(message[4:].strip())
        needReply = True
    elif message[:2] == '介绍' or message[:2] == '查询' or message[:2] == '查看' or message[:2] == '解释':
        reply = getComments(message[2:].strip())
        needReply = True
    elif '击剑' in message and group_id != 0:
        tmp = message.replace('击剑', '').strip()
        print(tmp)
        tmp_length = len(tmp)
        if be_at and tmp_length == 0:
            replylist = [
                '一把把你按在了地上',
                '敲了敲你的脑袋',
                '摸了摸你的头说：“乖，一边去~”',
                '白了你一眼',
                '并不想理你',
                '对你感到了无语'
            ]
            reply = Bot_Name + random.choice(replylist)
            needReply = True
        elif tmp_length > 2 and tmp[0] == '@' and tmp[1:].isdigit():
            target = int(tmp[1:])
            await fencing(member, target, app)
            needReply = True
    elif message == '我的积分' or message == '积分':
        id = member.id
        reply = memberName + getGold(id)
        needReply = True
    elif message == '我的体力' or message == '体力':
        id = member.id
        reply = memberName + getStrength(id)
        needReply = True
    elif message == '我的胜率' or message == '胜率':
        id = member.id
        reply = memberName + getRate(id)
        needReply = True
    elif message == '排行榜':
        reply = getRank()
        needReply = True
    elif message == '兑换体力':
        reply = memberName + rechargeStrength(member.id)
        needReply = True

    elif message == '模拟抽卡' or message == '模拟单抽':
        reply = MRFZ_card()
        needReply = True
    elif message == '模拟十连':
        reply = MRFZ_card10()
        needReply = True

    elif message == '围攻榜首':
        await fencingTop(member, app, group_id)
        needReply = True
    elif message == '探险':
        reply = fishing(member.id, memberName)
        needReply = True
    elif message == '闲逛':
        reply = memberName + hangOut(member.id)
        needReply = True
    elif message == '挖矿':
        reply = memberName + dig(member.id)
        needReply = True
    elif '摸摸' in message and group_id != 0:
        tmp = message.replace('摸摸', '').strip()
        if tmp[0] == '@' and tmp[1:].isdigit():
            target = int(tmp[1:])
            print(target)
            print(Bot_QQ)
            print(str(target) == str(Bot_QQ))
            if str(target) == str(Bot_QQ):
                reply = Bot_Name + touch(member.id, memberName)
                print(reply)
        needReply = True
    elif message == '强化进攻' or message == '强化攻击' or message == '强化攻击力':
        reply = memberName + strengthenAttack(member.id)
        needReply = True
    elif message == '强化防守' or message == '强化防御' or message == '强化防御力':
        reply = memberName + strengthenDefense(member.id)
        needReply = True
    elif message == '数据' or message == '我的数据' or message == '属性' or message == '我的属性':
        reply = getMyData(member.id)
        needReply = True
    elif message == '背包' or message == '我的背包':
        reply = memberName + getWarehouse(member.id)
        needReply = True
    elif message == '装备' or message == '我的装备':
        reply = memberName + getEquipment(member.id)
        needReply = True
    elif message == 'BUFF' or message == 'buff' or message == 'Buff' or message == '我的BUFF' or message == '我的buff' or message == '我的Buff':
        reply = memberName + getBuff(member.id)
        needReply = True
    elif message[:2] == '装备' or message[:2] == '使用':
        strList = message[2:].strip().split(' ')
        if len(strList) == 1:
            reply = memberName + useGoods(member.id, strList[0], 1)
            needReply = True
        elif len(strList) == 2:
            if strList[1].isdigit():
                number = int(strList[1])
                if number > 0:
                    reply = memberName + useGoods(member.id, strList[0], number)
                    needReply = True
    elif message[:2] == '取下' or message[:2] == '卸下':
        strList = message[2:].strip().split(' ')
        if len(strList) == 1:
            reply = memberName + getOffGoods(member.id, strList[0])
            needReply = True
    elif message == '商店':
        reply = getShop()
        needReply = True
    elif message[:2] == '购买':
        strList = message[2:].strip().split(' ')
        if len(strList) == 1:
            reply = memberName + purchase(member.id, strList[0], 1)
            needReply = True
        elif len(strList) == 2:
            if strList[1].isdigit():
                number = int(strList[1])
                if number > 0:
                    reply = memberName + purchase(member.id, strList[0], number)
                    needReply = True
    elif message[:2] == '出售' or message[:2] == '卖出' or message[:2] == '卖掉' or message[:2] == '售出':
        strList = message[2:].strip().split(' ')
        if len(strList) == 1:
            reply = memberName + sellGoods(member.id, strList[0], 1)
            needReply = True
        elif len(strList) == 2:
            if strList[1].isdigit():
                number = int(strList[1])
                if number > 0:
                    reply = memberName + sellGoods(member.id, strList[0], number)
                    needReply = True
    elif message[:2] == '丢弃' or message[:2] == '丢掉':
        strList = message[2:].strip().split(' ')
        if len(strList) == 1:
            reply = memberName + discard(member.id, strList[0], 1)
            needReply = True
        elif len(strList) == 2:
            if strList[1].isdigit():
                number = int(strList[1])
                if number > 0:
                    reply = memberName + discard(member.id, strList[0], number)
                    needReply = True
    elif '决斗' in message and group_id != 0:
        tmp = message.replace('决斗', '').strip()
        tmp_length = len(tmp)
        if be_at and tmp_length == 0:
            replylist = [
                '一把把你按在了地上',
                '敲了敲你的脑袋',
                '摸了摸你的头说：“乖，一边去~”',
                '白了你一眼',
                '并不想理你',
                '对你感到了无语'
            ]
            reply = Bot_Name + random.choice(replylist)
            needReply = True
        elif tmp_length > 2 and tmp[0] == '@' and tmp[1:].isdigit():
            target = int(tmp[1:])
            await duel(member, target, app)
            needReply = True
    elif message == '挑战榜首':
        await duelTop(member, app, group_id)
        needReply = True
    elif message[:4] == '修改昵称' or message[:4] == '修改名字' or message[:4] == '修改姓名':
        tmpName = message[4:].strip()
        reply = changeName(member.id, tmpName)
        needReply = True

    elif ('赠送' in message or '送' in message) and '@' in message:
        message = message.replace('赠送', '').replace('送', '')
        i = message.find('@')
        last = i + 1
        length = len(message)
        while message[last].isdigit() and last < length:
            last += 1
        if last != i + 1:
            id2 = int(message[i + 1: last])
            tmp = message.replace('@' + message[i + 1: last], '')
            if len(tmp) > 0:
                tmplist = tmp.strip().split(' ')
                if len(tmplist) == 1:
                    reply = giveOtherGoods(member.id, id2, tmplist[0], 1)
                    needReply = True
                elif len(tmplist) == 2 and tmplist[1].isdigit():
                    reply = giveOtherGoods(member.id, id2, tmplist[0], int(tmplist[1]))
                    needReply = True

    elif message[:2] == '合成':
        strList = message[2:].strip().split(' ')
        if len(strList) == 1:
            reply = memberName + '，' + synthesisGoods(member.id, strList[0], 1)
            needReply = True
        elif len(strList) == 2:
            if strList[1].isdigit():
                number = int(strList[1])
                if number > 0:
                    reply = memberName + synthesisGoods(member.id, strList[0], number)
                    needReply = True
    elif message[:2] == '分解':
        strList = message[2:].strip().split(' ')
        if len(strList) == 1:
            reply = memberName + '，' + decomposeGoods(member.id, strList[0], 1)
            needReply = True
        elif len(strList) == 2:
            if strList[1].isdigit():
                number = int(strList[1])
                if number > 0:
                    reply = memberName + decomposeGoods(member.id, strList[0], number)
                    needReply = True

    # 主人权限
    if right == 0:
        if message == '重新加载游戏数据':
            reload()
            reply = '重新加载完成'
            needReply = True
        elif message[:5] == '修改体力 ':
            strList = message.split(' ')

            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = editStrength(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = editStrength(int(strList[1]), int(strList[2]))
                    needReply = True
                elif strList[1] == '*' and strList[2].isdigit():
                    reply = giveAllStrength(int(strList[2]))
                    needReply = True
        elif message[:5] == '修改积分 ':
            strList = message.split(' ')

            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = editGold(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = editGold(int(strList[1]), int(strList[2]))
                    needReply = True
                elif strList[1] == '*' and strList[2].isdigit():
                    reply = giveAllGold(int(strList[2]))
                    needReply = True
        elif message[:5] == '查看数据 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = viewUser(int(strList[1]))
                    needReply = True
        elif message[:5] == '查看胜率 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = viewRate(int(strList[1]))
                    needReply = True
        elif message[:5] == '查看背包 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = viewWarehouse(int(strList[1]))
                    needReply = True
        elif message[:5] == '查看装备 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = viewEquipment(int(strList[1]))
                    needReply = True
        elif message[:7] == '查看BUFF ' or message[:7] == '查看buff ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = viewBuff(int(strList[1]))
                    needReply = True

        elif message[:5] == '给予物品 ' or message[:5] == '给予装备 ':
            strList = message.split(' ')
            if len(strList) == 2:
                reply = giveGoods(member.id, strList[1], 1)
                needReply = True
            elif len(strList) == 3:
                if strList[2].isdigit():
                    reply = giveGoods(member.id, strList[1], int(strList[2]))
                    needReply = True
                elif strList[1].isdigit():
                    reply = giveGoods(int(strList[1]), strList[2], 1)
                    needReply = True
                elif strList[1] == '*':
                    reply = giveAllGoods(strList[2], 1)
                    needReply = True
            elif len(strList) == 4:
                if strList[1].isdigit() and strList[3].isdigit():  # 给指定人物品
                    reply = giveGoods(int(strList[1]), strList[2], int(strList[3]))
                    needReply = True
                elif strList[1] == '*' and strList[3].isdigit():  # 给所有人物品
                    reply = giveAllGoods(strList[2], int(strList[3]))
                    needReply = True

        elif message == '开启无敌':
            reply = changeToGod(member.id)
            needReply = True
        elif message[:5] == '开启无敌 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToGod(int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToTmpGod(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:7] == '开启临时无敌 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToTmpGod(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToTmpGod(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message == '关闭无敌':
            reply = closeGod(member.id)
            needReply = True
        elif message[:5] == '关闭无敌 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = closeGod(int(strList[1]))
                    needReply = True
            needReply = True
        elif message == '查看无敌的人':
            reply = viewGod()
            needReply = True

        elif message[:7] == '开启1级防御 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToDefense1(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToDefense1(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:7] == '开启2级防御 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToDefense2(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToDefense2(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:7] == '开启3级防御 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToDefense3(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToDefense3(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:7] == '开启4级防御 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToDefense4(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToDefense4(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:7] == '开启5级防御 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToDefense5(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToDefense5(int(strList[1]), int(strList[2]))
                    needReply = True

        elif message[:7] == '开启1级进攻 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToRampage1(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToRampage1(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:7] == '开启2级进攻 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToRampage2(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToRampage2(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:7] == '开启3级进攻 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToRampage3(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToRampage3(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:7] == '开启4级进攻 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToRampage4(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToRampage4(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:7] == '开启5级进攻 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToRampage5(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToRampage5(int(strList[1]), int(strList[2]))
                    needReply = True

        elif message[:9] == '开启积分收益减半 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToHalveGold(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToHalveGold(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:9] == '开启击剑不掉积分 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToNoLoss(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToNoLoss(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:9] == '开启双倍积分收益 ' or message[:9] == '开启两倍积分收益 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToDoubleGold(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToDoubleGold(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:9] == '开启三倍积分收益 ':
            strList = message.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToTripleGold(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToTripleGold(int(strList[1]), int(strList[2]))
                    needReply = True
        elif message[:11] == '开启固定增减积分收益 ':
            strList = message.split(' ')
            if len(strList) == 3:
                if strList[1].isdigit():
                    if strList[2].isdigit():
                        reply = changeToFixedGold(member.id, int(strList[1]), int(strList[2]))
                        needReply = True
                    elif strList[2][:1] == '-' and strList[2][1:].isdigit():
                        reply = changeToFixedGold(member.id, int(strList[1]), -int(strList[2][1:]))
                        needReply = True
            elif len(strList) == 4:
                if strList[1].isdigit() and strList[2].isdigit():
                    if strList[3].isdigit():
                        reply = changeToFixedGold(int(strList[1]), int(strList[2]), int(strList[3]))
                        needReply = True
                    elif strList[3][:1] == '-' and strList[3][1:].isdigit():
                        reply = changeToFixedGold(int(strList[1]), int(strList[2]), -int(strList[3][1:]))
                        needReply = True

        # 记录操作
        if needReply:
            logManage.log(getNow.toString(), member.id, message + "; 执行结果：" + reply)

    if needReply:
        dataManage.save_obj(user, 'user/information')
        dataManage.save_obj(systemData, 'user/system')
    return needReply, reply, isImage, at_qq, needAt


# ============================================
# 基础操作

def getNumber(string):
    if string[0] == '-' and string[1:].isdigit():
        return -1 * int(string[1:])
    elif string.isdigit():
        return int(string)
    else:
        return 0


def giveOtherGoods(from_id, to_id, name, number):
    global user
    global goods
    if not goods.__contains__(name):
        return '你没有该物品'
    if not user[from_id]['warehouse'].__contains__(name):
        return '你没有该物品'
    if user[from_id]['warehouse'][name]['number'] < number:
        return '你没有足够的物品'
    newUser(to_id, '(无名)')
    if from_id == to_id:
        return '自己送自己礼物干什么嘞？'

    if getGooods(to_id, 2, name, number):
        discard(from_id, name, number)
        return '赠送成功！'
    else:
        return '对方背包已满！'


# 重新加载文件
def reload():
    global systemData
    global user
    global goods
    global goodsAvailable
    global buff
    global baseInformation
    global decompose
    global synthesis

    systemData = {}
    user = {}
    goods = {}
    goodsAvailable = []
    buff = {}
    baseInformation = {}
    index = 1
    # 获取物品
    with open('data/user/goods.txt', 'r+', encoding='utf-8') as f:
        text = f.readlines()
        for i in text:
            i = i.strip()
            if len(i) > 0 and i[0] != '#':
                datas = i.split(' ')
                if len(datas) > 3:  # 至少得有名字、简介、类型
                    if not goods.__contains__(datas[0]):
                        goods[datas[0]] = {
                            'id': index  # 编号
                        }
                        index += 1
                        for j in datas:
                            j_list = j.split('=')
                            if len(j_list) == 2:
                                if j_list[0] != 'comments':
                                    goods[datas[0]][j_list[0]] = getNumber(j_list[1])
                                else:
                                    goods[datas[0]][j_list[0]] = j_list[1]

    # 获取商店物品
    with open('data/user/shop.txt', 'r+', encoding='utf-8') as f:
        text = f.readlines()
        for i in text:
            i = i.strip()
            if len(i) > 0 and i[0] != '#':
                if goods.__contains__(i) and not i in goodsAvailable:
                    goodsAvailable.append(i)

    # 获取buff数据
    with open('data/user/buff.txt', 'r+', encoding='utf-8') as f:
        text = f.readlines()
        for i in text:
            i = i.strip()
            if len(i) > 0 and i[0] != '#':
                datas = i.split('=')
                if len(datas) == 2:
                    buff[datas[0]] = datas[1]

    # 获取基本数据
    with open('data/user/baseInformation.txt', 'r+', encoding='utf-8') as f:
        text = f.readlines()
        for i in text:
            i = i.strip()
            if len(i) > 0 and i[0] != '#':
                datas = i.split('=')
                if len(datas) == 2:
                    baseInformation[datas[0]] = datas[1]

    # 获取合成数据
    with open('data/user/synthesis.txt', 'r+', encoding='utf-8') as f:
        text = f.readlines()
        for i in text:
            i = i.strip()
            if len(i) > 0 and i[0] != '#':
                datas = i.split(' ')
                if len(datas) > 1:  # 至少得有名字、合成物品
                    if goods.__contains__(datas[0]):
                        synthesis[datas[0]] = {}  # 如果拥有该物品才可以合成
                        for j in datas:
                            j_list = j.split('=')
                            if len(j_list) == 2 and j_list[1].isdigit() and goods.__contains__(j_list[0]):
                                synthesis[datas[0]][j_list[0]] = int(j_list[1])
                        if len(synthesis[datas[0]]) == 0:
                            del synthesis[datas[0]]

    # 获取分解数据
    with open('data/user/decompose.txt', 'r+', encoding='utf-8') as f:
        text = f.readlines()
        for i in text:
            i = i.strip()
            if len(i) > 0 and i[0] != '#':
                datas = i.split(' ')
                if len(datas) > 1:  # 至少得有名字、分解物品
                    if goods.__contains__(datas[0]):
                        decompose[datas[0]] = {}  # 如果拥有该物品才可以合成
                        for j in datas:
                            j_list = j.split('=')
                            if len(j_list) == 2 and j_list[1].isdigit() and goods.__contains__(j_list[0]):
                                decompose[datas[0]][j_list[0]] = int(j_list[1])
                        if len(decompose[datas[0]]) == 0:
                            del decompose[datas[0]]

    user = dataManage.load_obj('user/information')
    systemData = dataManage.load_obj('user/system')

    for key, value in user.items():
        recalculateAttribute(key)

    return True


# 积分、体力值修改
def update(id, mode, gold, strength):  # mode值表示了该击剑由什么模式产生的（-2：交易操作、-1：管理员权限、0：击剑、1：探险、2：闲逛）
    global user
    global systemData
    if user.__contains__(id):
        if mode >= 0:
            if gold > 0:  # 增益buff
                if systemData['halveGold'].__contains__(id):  # 积分收益减半
                    systemData['halveGold'][id]['number'] -= 1
                    if systemData['halveGold'][id]['number'] <= 0:
                        del systemData['halveGold'][id]
                    gold *= 0.5
                    gold = int(gold)
                elif systemData['doubleGold'].__contains__(id):  # 双倍积分收益
                    systemData['doubleGold'][id]['number'] -= 1
                    if systemData['doubleGold'][id]['number'] <= 0:
                        del systemData['doubleGold'][id]
                    gold *= 2
                elif systemData['tripleGold'].__contains__(id):  # 三倍积分收益
                    systemData['tripleGold'][id]['number'] -= 1
                    if systemData['tripleGold'][id]['number'] <= 0:
                        del systemData['tripleGold'][id]
                    gold *= 3
                elif systemData['fixedGold'].__contains__(id):  # 固定增减积分收益
                    systemData['fixedGold'][id]['number'] -= 1
                    gold += systemData['fixedGold'][id]['gold']
                    if gold < 0:  # 收益不能减少为负数
                        gold = 0
                    if systemData['fixedGold'][id]['number'] <= 0:
                        del systemData['fixedGold'][id]
            elif gold < 0:  # 负收益buff
                if systemData['noLoss'].__contains__(id):  # 击剑不掉积分
                    if mode == 0:
                        systemData['noLoss'][id]['number'] -= 1
                        if systemData['noLoss'][id]['number'] <= 0:
                            del systemData['noLoss'][id]
                        gold = 0

        # 数值修改
        user[id]['attribute']['strength'] += strength
        if user[id]['attribute']['strength'] < 0:
            user[id]['attribute']['strength'] = 0
        if mode != -1:
            user[id]['gold'] += gold
        else:
            tmp = gold  # 修改积分也要进行排序检验
            if user[id]['gold'] > gold:
                gold = 1
            elif user[id]['gold'] < gold:
                gold = -1
            else:
                gold = 0
            user[id]['gold'] = tmp

        # ===============================
        # 排行榜更新
        times = user[id]['match']['win'] + user[id]['match']['lose']
        rate = float(user[id]['match']['win']) / float(user[id]['match']['win'] + user[id]['match']['lose']) if (
                user[id]['match']['win'] + user[id]['match']['lose'] > 0) else 0.0

        if times > systemData['rank']['field']['number']:  # 场次第一
            systemData['rank']['field']['number'] = times
            systemData['rank']['field']['id'] = id

        if rate > systemData['rank']['rate']['rate']:  # 胜率第一
            systemData['rank']['rate']['rate'] = rate
            systemData['rank']['rate']['id'] = id
        elif id == systemData['rank']['rate']['id']:  # 如果本身就是胜率第一，更新胜率
            systemData['rank']['rate']['rate'] = rate

        if times > 50:
            if rate > systemData['rank']['rate50']['rate']:  # 胜率第一（大于50场）
                systemData['rank']['rate50']['rate'] = rate
                systemData['rank']['rate50']['id'] = id
            elif systemData['rank']['rate50']['id'] == id:
                systemData['rank']['rate50']['rate'] = rate

        if user[id]['match']['lostTopTimes'] > systemData['rank']['loser']['number']:  # 被击剑的次数
            systemData['rank']['loser']['number'] = user[id]['match']['lostTopTimes']
            systemData['rank']['loser']['id'] = id

        if gold > 0:  # 增加收入
            if user[id]['gold'] > systemData['rank']['gold-1']['gold']:  # 登顶
                if id == systemData['rank']['gold-1']['id']:  # 本来就是榜首，那么就更新数据
                    systemData['rank']['gold-1']['gold'] = user[id]['gold']
                else:
                    user[id]['match']['topTimes'] += 1  # 登顶次数+1
                    if user[id]['match']['topTimes'] > systemData['rank']['challenger']['number']:
                        systemData['rank']['challenger']['number'] = user[id]['match']['topTimes']
                        systemData['rank']['challenger']['id'] = id

                    if id == systemData['rank']['gold-2']['id']:  # 如果登顶之前是第二名
                        systemData['rank']['gold-2']['gold'] = systemData['rank']['gold-1']['gold']
                        systemData['rank']['gold-2']['id'] = systemData['rank']['gold-1']['id']

                        systemData['rank']['gold-1']['gold'] = user[id]['gold']
                        systemData['rank']['gold-1']['id'] = id
                    else:  # 如果不是第二名，那么就是一样的操作逻辑
                        systemData['rank']['gold-3']['gold'] = systemData['rank']['gold-2']['gold']
                        systemData['rank']['gold-3']['id'] = systemData['rank']['gold-2']['id']

                        systemData['rank']['gold-2']['gold'] = systemData['rank']['gold-1']['gold']
                        systemData['rank']['gold-2']['id'] = systemData['rank']['gold-1']['id']

                        systemData['rank']['gold-1']['gold'] = user[id]['gold']
                        systemData['rank']['gold-1']['id'] = id
            elif user[id]['gold'] > systemData['rank']['gold-2']['gold'] and id != systemData['rank']['gold-1'][
                'id']:  # 大于第二，并且不是榜首
                if id == systemData['rank']['gold-2']['id']:  # 本来就是第二，那么就更新数据
                    systemData['rank']['gold-2']['gold'] = user[id]['gold']
                else:
                    systemData['rank']['gold-3']['gold'] = systemData['rank']['gold-2']['gold']
                    systemData['rank']['gold-3']['id'] = systemData['rank']['gold-2']['id']

                    systemData['rank']['gold-2']['gold'] = user[id]['gold']
                    systemData['rank']['gold-2']['id'] = id
            elif user[id]['gold'] > systemData['rank']['gold-3']['gold'] and id != systemData['rank']['gold-1'][
                'id'] and id != systemData['rank']['gold-2']['id']:  # 大于第三，并且不是榜首和第二
                systemData['rank']['gold-3']['gold'] = user[id]['gold']
                systemData['rank']['gold-3']['id'] = id  # 这里就算它本来是第三仍旧没有影响

        elif gold < 0:  # 收入减少
            if id == systemData['rank']['gold-1']['id'] or id == systemData['rank']['gold-2']['id'] or id == \
                    systemData['rank']['gold-3']['id']:  # 榜上有名（如果榜上无名，那么他的积分减少对排行榜就没有任何影响）
                goldId = 0
                goldId2 = 0
                goldId3 = 0
                for key, value in user.items():
                    if goldId == 0:
                        goldId = key
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
                if goldId != systemData['rank']['gold-1']['id']:
                    user[goldId]['match']['topTimes'] += 1  # 登顶次数+1
                    if user[goldId]['match']['topTimes'] > systemData['rank']['challenger']['number']:
                        systemData['rank']['challenger']['number'] = user[goldId]['match']['topTimes']
                        systemData['rank']['challenger']['id'] = goldId

                systemData['rank']['gold-1']['id'] = goldId
                systemData['rank']['gold-1']['gold'] = user[goldId]['gold']

                systemData['rank']['gold-2']['id'] = goldId2
                systemData['rank']['gold-2']['gold'] = user[goldId2]['gold'] if goldId2 != 0 else 0

                systemData['rank']['gold-3']['id'] = goldId3
                systemData['rank']['gold-3']['gold'] = user[goldId3]['gold'] if goldId3 != 0 else 0


# 获得商品
def getGooods(id, mode, name, number):  # （-1：系统补偿,0：购买所得，1：探险、闲逛获得,2：赠送所得）
    global user

    b = type(number)
    if str(b) != '<class \'int\'>':
        return False

    if user[id]['warehouse'].__contains__(name):
        user[id]['warehouse'][name]['number'] += number
        return True
    elif len(user[id]['warehouse']) < user[id]['attribute']['knapsack-max'] + user[id]['attribute']['knapsack-up']:
        user[id]['warehouse'][name] = {
            'number': number
        }
        return True
    else:
        return False


# 重新计算装备的属性值
def recalculateAttribute(id):
    user[id]['attribute']['attack-up'] = 0
    user[id]['attribute']['defense-up'] = 0
    user[id]['attribute']['hp-up'] = 0
    user[id]['attribute']['san-up'] = 0
    user[id]['attribute']['strength-up'] = 0
    user[id]['attribute']['strength-sign-up'] = 0
    user[id]['attribute']['knapsack-up'] = 0

    if user[id]['equipment']['arms'] != '':
        apllyAttribute(id, user[id]['equipment']['arms'])
    if user[id]['equipment']['jacket'] != '':
        apllyAttribute(id, user[id]['equipment']['hat'])
    if user[id]['equipment']['jacket'] != '':
        apllyAttribute(id, user[id]['equipment']['jacket'])
    if user[id]['equipment']['trousers'] != '':
        apllyAttribute(id, user[id]['equipment']['trousers'])
    if user[id]['equipment']['shoes'] != '':
        apllyAttribute(id, user[id]['equipment']['shoes'])

    if user[id]['equipment']['ring-left'] != '':
        apllyAttribute(id, user[id]['equipment']['ring-left'])
    if user[id]['equipment']['ring-right'] != '':
        apllyAttribute(id, user[id]['equipment']['ring-right'])
    if user[id]['equipment']['knapsack'] != '':
        apllyAttribute(id, user[id]['equipment']['knapsack'])


# 脱下物品
def getOffGoods(id, name):
    global goods
    global user

    flag = -1
    if user[id]['equipment']['arms'] == name:
        flag = 1
        user[id]['equipment']['arms'] = ''
    elif user[id]['equipment']['hat'] == name:
        flag = 2
        user[id]['equipment']['hat'] = ''
    elif user[id]['equipment']['jacket'] == name:
        flag = 3
        user[id]['equipment']['jacket'] = ''
    elif user[id]['equipment']['trousers'] == name:
        flag = 4
        user[id]['equipment']['trousers'] = ''
    elif user[id]['equipment']['shoes'] == name:
        flag = 5
        user[id]['equipment']['shoes'] = ''
    elif user[id]['equipment']['ring-left'] == name:
        flag = 6
        user[id]['equipment']['ring-left'] = ''
    elif user[id]['equipment']['ring-right'] == name:
        flag = 7
        user[id]['equipment']['ring-right'] = ''
    elif user[id]['equipment']['knapsack'] == name:
        flag = 8
        user[id]['equipment']['knapsack'] = ''

    if flag > 0:
        if getGooods(id, 0, name, 1):
            cancelAttribute(id, name)
            return '已将' + name + '放入背包'
        else:
            if flag == 1:
                user[id]['equipment']['arms'] = name
            elif flag == 2:
                user[id]['equipment']['hat'] = name
            elif flag == 3:
                user[id]['equipment']['jacket'] = name
            elif flag == 4:
                user[id]['equipment']['trousers'] = name
            elif flag == 5:
                user[id]['equipment']['shoes'] = name
            elif flag == 6:
                user[id]['equipment']['ring-left'] = name
            elif flag == 7:
                user[id]['equipment']['ring-right'] = name
            elif flag == 8:
                user[id]['equipment']['knapsack'] = name
            return '背包已满'
    else:
        return '你的装备不存在该物品'


# 应用属性值
def apllyAttribute(id, name):
    global goods
    global user
    if not goods.__contains__(name):
        return

    if goods[name].__contains__('attack'):
        user[id]['attribute']['attack-up'] += goods[name]['attack']
    if goods[name].__contains__('defense'):
        user[id]['attribute']['defense-up'] += goods[name]['defense']
    if goods[name].__contains__('hp'):
        user[id]['attribute']['hp-up'] += goods[name]['hp']
    if goods[name].__contains__('san'):
        user[id]['attribute']['san-up'] += goods[name]['san']
    if goods[name].__contains__('strength'):
        user[id]['attribute']['strength-up'] += goods[name]['strength']
    if goods[name].__contains__('strength-sign'):
        user[id]['attribute']['strength-sign-up'] += goods[name]['strength-sign']
    if goods[name].__contains__('knapsack'):
        user[id]['attribute']['knapsack-up'] += goods[name]['knapsack']


# 取消应用属性值
def cancelAttribute(id, name):
    global goods
    global user

    if goods[name].__contains__('attack'):
        user[id]['attribute']['attack-up'] -= goods[name]['attack']
    if goods[name].__contains__('defense'):
        user[id]['attribute']['defense-up'] -= goods[name]['defense']
    if goods[name].__contains__('hp'):
        user[id]['attribute']['hp-up'] -= goods[name]['hp']
    if goods[name].__contains__('san'):
        user[id]['attribute']['san-up'] -= goods[name]['san']
    if goods[name].__contains__('strength'):
        user[id]['attribute']['strength-up'] -= goods[name]['strength']
    if goods[name].__contains__('strength-sign'):
        user[id]['attribute']['strength-sign-up'] -= goods[name]['strength-sign']
    if goods[name].__contains__('knapsack'):
        user[id]['attribute']['knapsack-up'] -= goods[name]['knapsack']


# 使用商品
def useGoods(id, name, number):
    global user
    global goods
    maxStrength = user[id]['attribute']['strength-max'] + user[id]['attribute']['strength-up']

    if user[id]['warehouse'].__contains__(name):
        # 武器装备
        if (0 < goods[name]['type'] < 9) or goods[name]['type'] == 14:
            if goods[name]['type'] == 1:
                if user[id]['equipment']['arms'] != '':
                    discard(id, name, 1)
                    if '放入背包' in getOffGoods(id, user[id]['equipment']['arms']):
                        user[id]['equipment']['arms'] = name
                        apllyAttribute(id, name)
                        return '装备成功！'
                    else:
                        getGooods(id, -1, name, 1)
                        return '背包无法给其腾出空间'
                else:
                    discard(id, name, 1)
                    user[id]['equipment']['arms'] = name
                    apllyAttribute(id, name)
                    return '装备成功！'
            elif goods[name]['type'] == 2:
                if user[id]['equipment']['hat'] != '':
                    discard(id, name, 1)
                    if '放入背包' in getOffGoods(id, user[id]['equipment']['hat']):
                        user[id]['equipment']['hat'] = name
                        apllyAttribute(id, name)
                        return '装备成功！'
                    else:
                        getGooods(id, -1, name, 1)
                        return '背包无法给其腾出空间'
                else:
                    discard(id, name, 1)
                    user[id]['equipment']['hat'] = name
                    apllyAttribute(id, name)
                    return '装备成功！'
            elif goods[name]['type'] == 3:
                if user[id]['equipment']['jacket'] != '':
                    discard(id, name, 1)
                    if '放入背包' in getOffGoods(id, user[id]['equipment']['jacket']):
                        user[id]['equipment']['jacket'] = name
                        apllyAttribute(id, name)
                        return '装备成功！'
                    else:
                        getGooods(id, -1, name, 1)
                        return '背包无法给其腾出空间'
                else:
                    discard(id, name, 1)
                    user[id]['equipment']['jacket'] = name
                    apllyAttribute(id, name)
                    return '装备成功！'
            elif goods[name]['type'] == 4:
                if user[id]['equipment']['trousers'] != '':
                    discard(id, name, 1)
                    if '放入背包' in getOffGoods(id, user[id]['equipment']['trousers']):
                        user[id]['equipment']['trousers'] = name
                        apllyAttribute(id, name)
                        return '装备成功！'
                    else:
                        getGooods(id, -1, name, 1)
                        return '背包无法给其腾出空间'
                else:
                    discard(id, name, 1)
                    user[id]['equipment']['trousers'] = name
                    apllyAttribute(id, name)
                    return '装备成功！'
            elif goods[name]['type'] == 5:
                if user[id]['equipment']['shoes'] != '':
                    discard(id, name, 1)
                    if '放入背包' in getOffGoods(id, user[id]['equipment']['shoes']):
                        user[id]['equipment']['shoes'] = name
                        apllyAttribute(id, name)
                        return '装备成功！'
                    else:
                        getGooods(id, -1, name, 1)
                        return '背包无法给其腾出空间'
                else:
                    discard(id, name, 1)
                    user[id]['equipment']['shoes'] = name
                    apllyAttribute(id, name)
                    return '装备成功！'
            elif goods[name]['type'] == 6:
                if user[id]['equipment']['ring-left'] != '':
                    discard(id, name, 1)
                    if '放入背包' in getOffGoods(id, user[id]['equipment']['ring-left']):
                        user[id]['equipment']['ring-left'] = name
                        apllyAttribute(id, name)
                        return '装备成功！'
                    else:
                        getGooods(id, -1, name, 1)
                        return '背包无法给其腾出空间'
                else:
                    discard(id, name, 1)
                    user[id]['equipment']['ring-left'] = name
                    apllyAttribute(id, name)
                    return '装备成功！'
            elif goods[name]['type'] == 7:
                if user[id]['equipment']['ring-right'] != '':
                    discard(id, name, 1)
                    if '放入背包' in getOffGoods(id, user[id]['equipment']['ring-right']):
                        user[id]['equipment']['ring-right'] = name
                        apllyAttribute(id, name)
                        return '装备成功！'
                    else:
                        getGooods(id, -1, name, 1)
                        return '背包无法给其腾出空间'
                else:
                    discard(id, name, 1)
                    user[id]['equipment']['ring-right'] = name
                    apllyAttribute(id, name)
                    return '装备成功！'
            elif goods[name]['type'] == 8:
                if user[id]['equipment']['knapsack'] != '':
                    discard(id, name, 1)
                    if '放入背包' in getOffGoods(id, user[id]['equipment']['knapsack']):
                        user[id]['equipment']['knapsack'] = name
                        apllyAttribute(id, name)
                        return '装备成功！'
                    else:
                        getGooods(id, -1, name, 1)
                        return '背包无法给其腾出空间'
                else:
                    discard(id, name, 1)
                    user[id]['equipment']['knapsack'] = name
                    apllyAttribute(id, name)
                    return '装备成功！'
        # 消耗品
        else:
            if goods[name]['type'] == 12:
                return '纪念品不可以使用，只可以出售和丢弃'
            elif goods[name]['type'] == 13:
                return '材料不可以使用，只可以出售、丢弃、修补强化装备'
            elif goods[name]['type'] > 15:
                return '未知物品暂时不可以使用哦~'

            if number > user[id]['warehouse'][name]['number']:
                number = user[id]['warehouse'][name]['number']
            countWord = ''
            if goods[name]['type'] == 0:  # 药水
                countWord = '瓶'
            elif goods[name]['type'] == 9:  # 卷轴
                countWord = '张'
            elif goods[name]['type'] == 10:  # 宝箱、礼包
                countWord = '个'
            elif goods[name]['type'] == 11:  # 矿石
                countWord = '个'
            elif goods[name]['type'] == 15:  # 食物
                countWord = '个'

            # 积分、体力
            gold = 0
            strength = 0
            if goods[name].__contains__('gold'):
                gold = goods[name]['gold'] * number
            if goods[name].__contains__('strength'):

                if user[id]['attribute']['strength'] + goods[name]['strength'] * number > maxStrength:
                    return '体力值已满，无法使用'
                strength = goods[name]['strength'] * number
            update(id, -2, gold, strength)

            # 血量、san值
            if goods[name].__contains__('san'):
                user[id]['attribute']['san'] += goods[name]['san'] * number

            if goods[name].__contains__('hp'):
                maxHp = user[id]['attribute']['hp-max'] + user[id]['attribute']['hp-up']
                user[id]['attribute']['hp'] += goods[name]['hp'] * number
                if user[id]['attribute']['hp'] > maxHp:
                    user[id]['attribute']['hp'] = maxHp

            if name == '5级防御卷轴':
                changeToDefense5(id, number)
            elif name == '4级防御卷轴':
                changeToDefense4(id, number)
            elif name == '5级进攻卷轴':
                changeToRampage5(id, number)
            elif name == '4级进攻卷轴':
                changeToRampage4(id, number)

            discard(id, name, number)
            return '你成功使用' + str(number) + countWord + name
    else:
        return '你没有该物品'


def typeToString(number):
    if number == 0:
        return '药水'
    elif number == 1:
        return '武器'
    elif number == 2:
        return '头盔'
    elif number == 3:
        return '胸甲'
    elif number == 4:
        return '护腿'
    elif number == 5:
        return '靴子'
    elif number == 6:
        return '戒指（左）'
    elif number == 7:
        return '戒指（右）'
    elif number == 8:
        return '背包'
    elif number == 9:
        return '卷轴'
    elif number == 10:
        return '宝箱'
    elif number == 11:
        return '矿石'
    elif number == 12:
        return '纪念品'
    elif number == 13:
        return '材料'
    elif number == 14:
        return '附加戒指'
    elif number == 15:
        return '食物'
    elif number == 16:
        return '道具'
    return '（未知）'


# 分解与合成
def decomposeGoods(id, name, number):
    if not goods.__contains__(name):
        return '不存在该物品！'
    if not decompose.__contains__(name):
        return '该物品不可以分解！'
    if not user[id]['warehouse'].__contains__(name):
        return '你的背包不存在该物品！'

    if number > user[id]['warehouse'][name]['number']:
        number = user[id]['warehouse'][name]['number']

    discard(id, name, number)  # 丢弃物品
    operate = {}  # 记录每一步的操作，以便于恢复操作
    flag = True  # 分解是否成功
    for key, value in decompose[name].items():
        if not getGooods(id, -1, key, value * number):
            flag = False
            break

        if operate.__contains__(key):  # 记录操作
            operate[key] += value * number
        else:
            operate[key] = value * number

    if flag:
        return '成功分解' + str(number) + '个物品！'
    else:
        for key, value in operate.items():
            discard(id, key, value)
        getGooods(id, -1, name, number)
        return '背包已满！'


def synthesisGoods(id, name, number):
    if not goods.__contains__(name):
        return '不存在该物品！'
    if not synthesis.__contains__(name):
        return '该物品无法合成！'

    operate = {}  # 记录每一步的操作，以便于恢复操作
    flag = True  # 合成是否成功
    for key, value in synthesis[name].items():
        if user[id]['warehouse'].__contains__(key) and user[id]['warehouse'][key]['number'] >= value * number:
            discard(id, key, value * number)
            if operate.__contains__(key):  # 记录操作
                operate[key] += value * number
            else:
                operate[key] = value * number
        else:
            flag = False
            break

    if flag and not getGooods(id, -1, name, number):  # 获取合成后的物品
        flag = False

    if flag:
        return '成功合成' + str(number) + '个物品！'
    else:
        for key, value in operate.items():
            getGooods(id, -1, key, value)
        return '背包已满或材料不足，合成失败！'


# ============================================
# 操作

# 签到
def sign(id):
    global user
    today = str(datetime.date.today())

    if today != user[id]['sign-date']:
        user[id]['sign-date'] = today
        update(id, -2, random.randint(5, 30), 0)
        return '签到成功！当前积分：' + str(user[id]['gold'])
    else:
        return '你今天已经签到过了哦~'


# 获取积分
def getGold(id):
    global user

    return '你的积分为：' + str(user[id]['gold'])


# 获取体力
def getStrength(id):
    global user
    maxStrength = user[id]['attribute']['strength-max'] + user[id]['attribute']['strength-up']
    return '你的体力为：' + str(user[id]['attribute']['strength']) + '/' + str(maxStrength)


# 获取胜率
def getRate(id):
    global user
    if user[id]['match']['win'] + user[id]['match']['lose'] == 0:
        return '你还暂未进行任何对决'
    rate = float(user[id]['match']['win']) / float(user[id]['match']['win'] + user[id]['match']['lose'])
    rate = round(rate, 2) * 100
    result = '\n总计场次：' + str(user[id]['match']['win'] + user[id]['match']['lose'])
    result += '\n获胜次数：' + str(user[id]['match']['win'])
    result += '\n你的胜率为：' + str(int(rate)) + '%'
    result += '\n登顶次数：' + str(user[id]['match']['topTimes'])
    return result


# 获取数据
def getMyData(id):
    global user
    result = '昵称：' + user[id]['name']
    if not user[id]['initName']:
        result += '（自动获取）'
    result += '\n'
    result += '积分：' + str(user[id]['gold']) + '\n'

    maxStrength = user[id]['attribute']['strength-max'] + user[id]['attribute']['strength-up']
    result += '体力：' + str(user[id]['attribute']['strength']) + '/' + str(maxStrength) + '\n'

    maxHp = user[id]['attribute']['hp-max'] + user[id]['attribute']['hp-up']
    result += '生命值：' + str(user[id]['attribute']['hp']) + '/' + str(maxHp) + '\n'

    attack = user[id]['attribute']['attack'] + user[id]['attribute']['attack-up']
    result += '攻击力：' + str(attack) + '（' + str(user[id]['attribute']['attack-up']) + '）\n'

    defense = user[id]['attribute']['defense'] + user[id]['attribute']['defense-up']
    result += '护甲：' + str(defense) + '（' + str(user[id]['attribute']['defense-up']) + '）\n'

    maxSan = user[id]['attribute']['san-max'] + user[id]['attribute']['san-up']
    result += 'San值：' + str(user[id]['attribute']['san']) + '/' + str(maxSan) + '\n'

    result += '总计场次：' + str(user[id]['match']['win'] + user[id]['match']['lose'])
    if user[id]['match']['win'] + user[id]['match']['lose'] != 0:
        rate = float(user[id]['match']['win']) / float(user[id]['match']['win'] + user[id]['match']['lose'])
        rate = round(rate, 2) * 100
        result += '（' + str(int(rate)) + '%）'

    maxKnapsack = user[id]['attribute']['knapsack-max'] + user[id]['attribute']['knapsack-up']
    result += '\n背包物品数：' + str(len(user[id]['warehouse'])) + '/' + str(maxKnapsack)

    result += '\n强化次数：' + str(user[id]['attribute']['strengthen']) + '次'
    return result


# 获取仓库
def getWarehouse(id):
    global user
    maxKnapsack = user[id]['attribute']['knapsack-max'] + user[id]['attribute']['knapsack-up']
    result = '你的背包：' + str(len(user[id]['warehouse'])) + '/' + str(maxKnapsack)
    if len(user[id]['warehouse']) == 0:
        result += '无'
    else:
        for i, value in user[id]['warehouse'].items():
            result += '\n'
            result += i
            if value['number'] > 1:
                result += 'X' + str(value['number'])
    return result


# 获取装备
def getEquipment(id):
    global user
    result = '你的装备：\n'
    result += '武器：' + (user[id]['equipment']['arms'] if len(user[id]['equipment']['arms']) > 0 else '（暂无）') + '\n'
    result += '头盔：' + (user[id]['equipment']['hat'] if len(user[id]['equipment']['hat']) > 0 else '（暂无）') + '\n'
    result += '胸甲：' + (user[id]['equipment']['jacket'] if len(user[id]['equipment']['jacket']) > 0 else '（暂无）') + '\n'
    result += '护腿：' + (
        user[id]['equipment']['trousers'] if len(user[id]['equipment']['trousers']) > 0 else '（暂无）') + '\n'
    result += '鞋子：' + (user[id]['equipment']['shoes'] if len(user[id]['equipment']['shoes']) > 0 else '（暂无）') + '\n'
    result += '戒指（左）：' + (
        user[id]['equipment']['ring-left'] if len(user[id]['equipment']['ring-left']) > 0 else '（暂无）') + '\n'
    result += '戒指（右）：' + (
        user[id]['equipment']['ring-right'] if len(user[id]['equipment']['ring-right']) > 0 else '（暂无）') + '\n'
    result += '背包：' + (user[id]['equipment']['knapsack'] if len(user[id]['equipment']['knapsack']) > 0 else '（暂无）')
    return result


# 获取buff
def getBuff(id):
    global systemData

    result = '你的BUFF如下：'
    if id in systemData['god']:  # 用户是无敌模式
        result += '\n永久无敌模式'
    if systemData['tmpGod'].__contains__(id):  # 用户是无敌模式
        result += '\n临时无敌模式：' + str(systemData['tmpGod'][id]['number']) + '次'

    if systemData['defense-5'].__contains__(id):  # 5级防御
        result += '\n5级防御：' + str(systemData['defense-5'][id]['number']) + '次'
    if systemData['defense-4'].__contains__(id):  # 4级防御
        result += '\n4级防御：' + str(systemData['defense-4'][id]['number']) + '次'
    if systemData['defense-3'].__contains__(id):  # 3级防御
        result += '\n3级防御：' + str(systemData['defense-3'][id]['number']) + '次'
    if systemData['defense-2'].__contains__(id):  # 2级防御
        result += '\n2级防御：' + str(systemData['defense-2'][id]['number']) + '次'
    if systemData['defense-1'].__contains__(id):  # 1级防御
        result += '\n1级防御：' + str(systemData['defense-1'][id]['number']) + '次'

    if systemData['rampage-5'].__contains__(id):  # 5级暴走
        result += '\n5级进攻：' + str(systemData['rampage-5'][id]['number']) + '次'
    if systemData['rampage-4'].__contains__(id):  # 4级暴走
        result += '\n4级进攻：' + str(systemData['rampage-4'][id]['number']) + '次'
    if systemData['rampage-3'].__contains__(id):  # 3级暴走
        result += '\n3级进攻：' + str(systemData['rampage-3'][id]['number']) + '次'
    if systemData['rampage-2'].__contains__(id):  # 2级暴走
        result += '\n2级进攻：' + str(systemData['rampage-2'][id]['number']) + '次'
    if systemData['rampage-1'].__contains__(id):  # 1级暴走
        result += '\n1级进攻：' + str(systemData['rampage-1'][id]['number']) + '次'

    if systemData['halveGold'].__contains__(id):  # 积分收益减半
        result += '\n积分收益减半：' + str(systemData['halveGold'][id]['number']) + '次'
    if systemData['doubleGold'].__contains__(id):  # 双倍积分收益
        result += '\n积分收益双倍：' + str(systemData['doubleGold'][id]['number']) + '次'
    if systemData['tripleGold'].__contains__(id):  # 三倍积分收益
        result += '\n积分收益三倍：' + str(systemData['tripleGold'][id]['number']) + '次'
    if systemData['fixedGold'].__contains__(id):  # 固定增减积分收益
        if systemData['fixedGold'][id]['gold'] > 0:
            result += '\n收益增减固定积分：' + str(systemData['fixedGold'][id]['number']) + '次（积分+' + str(
                systemData['fixedGold'][id]['gold']) + '）'
        else:
            result += '\n收益增减固定积分：' + str(systemData['fixedGold'][id]['number']) + '次（积分' + str(
                systemData['fixedGold'][id]['gold']) + '）'
    if systemData['noLoss'].__contains__(id):  # 击剑不掉积分
        result += '\n击剑免掉积分：' + str(systemData['noLoss'][id]['number']) + '次'

    if result == '你的BUFF如下：':
        result = '你的BUFF如下：暂无'
    return result


# 获取商店
def getShop():
    global goodsAvailable
    global goods
    result = '商品目录如下：'
    for i in goodsAvailable:
        result += '\n' + i + '：' + str(goods[i]['cost']) + '积分'
    return result


# 介绍物品
def getComments(name):
    global goods
    global buff
    if goods.__contains__(name):
        result = '名字：' + name + '（id:' + str(goods[name]['id']) + '）'
        result += '\n类型：' + typeToString(goods[name]['type'])
        if goods[name]['cost'] >= 0:
            result += '\n购买：' + str(goods[name]['cost']) + '积分'
        else:
            result += '\n购买：无法购买'
        if goods[name]['sell'] >= 0:
            result += '\n出售：' + str(goods[name]['sell']) + '积分'
        else:
            result += '\n出售：无法出售'
        if synthesis.__contains__(name):
            result += '\n合成路径：'
            flag = True
            for key, value in synthesis[name].items():
                if not flag:
                    result += '，'
                else:
                    flag = False
                result += key + 'X' + str(value)
        if decompose.__contains__(name):
            result += '\n可分解为：'
            flag = True
            for key, value in decompose[name].items():
                if not flag:
                    result += '，'
                else:
                    flag = False
                result += key + 'X' + str(value)
        result += '\n介绍：' + str(goods[name]['comments'])
        return result
    elif buff.__contains__(name):
        result = '名字：' + name
        result += '\n类型：buff'
        result += '\n介绍：' + str(buff[name]['comments'])
        return result
    elif baseInformation.__contains__(name):
        result = '名字：' + name
        result += '\n介绍：' + str(baseInformation[name]['comments'])
        return result
    elif name.isdigit() or (name[3:].isdigit() and (name[:3] == 'id:' or name[:3] == 'id：')):
        if not name.isdigit():
            name = name[3:]
        goodsId = int(name)
        for key, value in goods.items():
            if value['id'] == goodsId:
                result = '名字：' + key + '（id:' + str(goods[key]['id']) + '）'
                result += '\n类型：' + typeToString(goods[key]['type'])
                if goods[key]['cost'] >= 0:
                    result += '\n购买：' + str(goods[key]['cost']) + '积分'
                else:
                    result += '\n购买：无法购买'
                if goods[key]['sell'] >= 0:
                    result += '\n出售：' + str(goods[key]['sell']) + '积分'
                else:
                    result += '\n出售：无法出售'
                if synthesis.__contains__(key):
                    result += '\n合成路径：'
                    flag = True
                    for key2, value2 in synthesis[key].items():
                        if not flag:
                            result += '，'
                        else:
                            flag = False
                        result += key2 + 'X' + str(value2)
                if decompose.__contains__(key):
                    result += '\n可分解为：'
                    flag = True
                    for key2, value2 in decompose[key].items():
                        if not flag:
                            result += '，'
                        else:
                            flag = False
                        result += key2 + 'X' + str(value2)
                result += '\n介绍：' + str(goods[key]['comments'])
                return result
        return '不存在该物品'
    else:
        return '不存在该物品'


# 查询合成路线
def getSynthesis(name):
    if goods.__contains__(name):
        result = '物品：' + name
        result += '\n合成路径：'
        if synthesis.__contains__(name):
            flag = True
            for key, value in synthesis[name].items():
                if not flag:
                    result += '，'
                else:
                    flag = False
                result += key + 'X' + str(value)
        else:
            result += '无'

        result += '\n可分解为：'
        if decompose.__contains__(name):
            flag = True
            for key, value in decompose[name].items():
                if not flag:
                    result += '，'
                else:
                    flag = False
                result += key + 'X' + str(value)
        else:
            result += '无'

        result += '\n参与合成路径：'
        synthesis_list = []

        for key, value in synthesis.items():
            for key2, value2 in value.items():
                if key2 == name:
                    synthesis_list.append(key)
                    break

        if len(synthesis_list) == 0:
            result += '无'
        else:
            for i in synthesis_list:
                result += '\n' + i + '<-'
                flag = True
                for key, value in synthesis[i].items():
                    if not flag:
                        result += '，'
                    else:
                        flag = False
                    result += key + 'X' + str(value)

        return result

    else:
        return '不存在该物品'


# 查询分解路线
def getDecompose(name):
    if goods.__contains__(name):
        result = '物品：' + name
        if decompose.__contains__(name):
            result += '\n可分解为：'
            flag = True
            for key, value in decompose[name].items():
                if not flag:
                    result += '，'
                else:
                    flag = False
                result += key + 'X' + str(value)
            return result
        return '该物品不可分解'
    else:
        return '不存在该物品'


# 改变名字
def changeName(id, name):
    global user
    flag = True
    for key, value in user.items():
        if value['name'] == name:
            return '这个名字已经被其他人占用了哦！'

    user[id]['name'] = name
    user[id]['initName'] = True
    return name + '修改成功~'


# 新用戶
def newUser(id, name):
    global user
    global init
    global systemData

    if init:
        reload()
        init = False
    today = str(datetime.date.today())

    if not user.__contains__(id):
        user[id] = {
            'name': name,
            'initName': False,
            'gold': 0,
            'sign-date': '',
            'warehouse': {},  # 背包
            'match': {  # 比赛场次
                'win': 0,  # 胜利
                'lose': 0,  # 失败
                'monster': 0,  # 怪物击杀数
                'legend': 0,  # boss击杀数
                'topTimes': 0,  # 登顶次数
                'lostTopTimes': 0  # 被击剑次数
            },
            'equipment': {  # 装备
                'arms': '',  # 武器
                'hat': '',  # 头部
                'jacket': '',  # 身体
                'trousers': '',  # 裤子
                'shoes': '',  # 鞋子
                'ring-left': '',  # 左戒指
                'ring-right': '',  # 右戒指
                'ring': [],  # 附加戒指（只有一半收益，但是可以弄8个）
                'knapsack': ''  # 背包
            },
            'attribute': {
                'strengthen': 0,  # 强化次数

                'attack': 5,  # 攻击力
                "attack-up": 0,  # 装备的攻击力附加

                'hp': 100,  # 生命值
                'hp-max': 100,  # 最大生命值
                'hp-up': 0,  # 装备的最大生命值附加

                'defense': 0,  # 防御值
                'defense-up': 0,  # 装备的防御力附加

                'san': 100,  # 精神力
                'san-max': 100,  # 最大精神力
                'san-up': 0,  # 装备的最大精神力附加

                'strength': 20,  # 体力
                'strength-max': 120,  # 最大体力值
                'strength-sign': 20,  # 每天的体力恢复量
                'strength-up': 0,  # 装备的最大体力附加
                'strength-sign-up': 0,  # 装备的签到体力恢复

                'knapsack-max': 10,  # 最大背包容量
                'knapsack-up': 0,  # 装备提升的最大背包容量

                'gold-income': 0,  # 每次积分收益的增加积分
                'gold-expenditure': 0,  # 每次积分支出减少
                'gold-income-shop': 0,  # 每次商店积分收益的增加积分
                'gold-expenditure-shop': 0,  # 每次商店积分支出减少
            },
            'last-operate-date': today
        }
    else:
        if user[id]['last-operate-date'] != today:
            # 体力值修改
            maxStrength = user[id]['attribute']['strength-max'] + user[id]['attribute']['strength-up']
            signStrength = user[id]['attribute']['strength-sign'] + user[id]['attribute']['strength-sign-up']

            if user[id]['attribute']['strength'] < maxStrength - signStrength:
                user[id]['attribute']['strength'] += signStrength
            elif user[id]['attribute']['strength'] < maxStrength:
                user[id]['attribute']['strength'] = maxStrength

            # san值
            maxSan = user[id]['attribute']['san-max'] + user[id]['attribute']['san-up']
            user[id]['attribute']['san'] += 100
            if user[id]['attribute']['san'] > maxSan:
                user[id]['attribute']['san'] = maxSan

            # hp值
            maxHp = user[id]['attribute']['hp-max'] + user[id]['attribute']['hp-up']
            user[id]['attribute']['hp'] += 100
            if user[id]['attribute']['hp'] > maxHp:
                user[id]['attribute']['hp'] = maxHp

            user[id]['last-operate-date'] = today
            if not user[id]['initName']:
                user[id]['name'] = name


def rechargeStrength(id):
    global user
    maxStrength = user[id]['attribute']['strength-max'] + user[id]['attribute']['strength-up']
    cost = 5
    gain = 5
    if user[id]['gold'] < cost:
        return '你的积分小于' + str(cost) + '不能兑换体力'

    if user[id]['attribute']['strength'] >= maxStrength:
        return '你的体力值已满不能兑换体力'
    elif user[id]['attribute']['strength'] >= maxStrength - gain:
        update(id, -2, -cost, 0)
        user[id]['attribute']['strength'] = maxStrength
        return '你消耗了' + str(cost) + '积分，获得了' + str(gain) + '点体力'
    else:
        update(id, -2, -cost, 0)
        user[id]['attribute']['strength'] += gain
        return '你消耗了' + str(cost) + '积分，获得了' + str(gain) + '点体力'


# 击剑
async def fencing(member, id2, app):
    if member.id == id2:
        await app.sendGroupMessage(member.group, MessageChain.create([
            Plain('好家伙，和自己击剑呢？')
        ]))
        return

    other = await app.getMember(member.group.id, id2)

    if other != None:
        newUser(other.id, other.name)
        global user
        global systemData

        # 体力值与积分判断
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
        user[other.id]['attribute']['san'] -= 1
        user[other.id]['match']['lostTopTimes'] += 1

        ran = random.randrange(0, 1000)
        # 获胜概率为 你的攻击 - 对方防御力 + 你的san值 - 对方san值
        attack = user[member.id]['attribute']['attack'] + user[member.id]['attribute']['attack-up']
        defense = user[other.id]['attribute']['defense'] + user[member.id]['attribute']['defense-up']
        winPoint = 500 + (
                    (attack - defense) * 10 + user[member.id]['attribute']['san'] - user[other.id]['attribute']['san'])

        # BUFF启用
        if member.id in systemData['god']:  # 用户是无敌模式
            winPoint = 1000
        elif other.id in systemData['god']:  # 被击剑对象是无敌模式
            winPoint = 0
        elif systemData['tmpGod'].__contains__(member.id):  # 用户是无敌模式
            winPoint = 1000
            systemData['tmpGod'][member.id]['number'] -= 1
            if systemData['tmpGod'][member.id]['number'] <= 0:
                del systemData['tmpGod'][member.id]
        elif systemData['tmpGod'].__contains__(other.id):  # 被击剑对象是无敌模式
            winPoint = 0
            systemData['tmpGod'][other.id]['number'] -= 1
            if systemData['tmpGod'][other.id]['number'] <= 0:
                del systemData['tmpGod'][other.id]
        else:
            if systemData['defense-5'].__contains__(other.id):  # 5级防御
                winPoint -= 500
                systemData['defense-5'][other.id]['number'] -= 1
                if systemData['defense-5'][other.id]['number'] <= 0:
                    del systemData['defense-5'][other.id]
            elif systemData['defense-4'].__contains__(other.id):  # 4级防御
                winPoint -= 400
                systemData['defense-4'][other.id]['number'] -= 1
                if systemData['defense-4'][other.id]['number'] <= 0:
                    del systemData['defense-4'][other.id]
            elif systemData['defense-3'].__contains__(other.id):  # 3级防御
                winPoint -= 300
                systemData['defense-3'][other.id]['number'] -= 1
                if systemData['defense-3'][other.id]['number'] <= 0:
                    del systemData['defense-3'][other.id]
            elif systemData['defense-2'].__contains__(other.id):  # 2级防御
                winPoint -= 200
                systemData['defense-2'][other.id]['number'] -= 1
                if systemData['defense-2'][other.id]['number'] <= 0:
                    del systemData['defense-2'][other.id]
            elif systemData['defense-1'].__contains__(other.id):  # 1级防御
                winPoint -= 100
                systemData['defense-1'][other.id]['number'] -= 1
                if systemData['defense-1'][other.id]['number'] <= 0:
                    del systemData['defense-1'][other.id]

            if systemData['rampage-5'].__contains__(member.id):  # 5级暴走
                winPoint += 500
                systemData['rampage-5'][member.id]['number'] -= 1
                if systemData['rampage-5'][member.id]['number'] <= 0:
                    del systemData['rampage-5'][member.id]
            elif systemData['rampage-4'].__contains__(member.id):  # 4级暴走
                winPoint += 400
                systemData['rampage-4'][member.id]['number'] -= 1
                if systemData['rampage-4'][member.id]['number'] <= 0:
                    del systemData['rampage-4'][member.id]
            elif systemData['rampage-3'].__contains__(member.id):  # 3级暴走
                winPoint += 300
                systemData['rampage-3'][member.id]['number'] -= 1
                if systemData['rampage-3'][member.id]['number'] <= 0:
                    del systemData['rampage-3'][member.id]
            elif systemData['rampage-2'].__contains__(member.id):  # 2级暴走
                winPoint += 200
                systemData['rampage-2'][member.id]['number'] -= 1
                if systemData['rampage-2'][member.id]['number'] <= 0:
                    del systemData['rampage-2'][member.id]
            elif systemData['rampage-1'].__contains__(member.id):  # 1级暴走
                winPoint += 100
                systemData['rampage-1'][member.id]['number'] -= 1
                if systemData['rampage-1'][member.id]['number'] <= 0:
                    del systemData['rampage-1'][member.id]

        winner = ''
        loser = ''
        result = ''
        maxGetGold = 8
        if ran < winPoint:
            winner = member.name
            loser = other.name
            if user[other.id]['gold'] < maxGetGold:
                maxGetGold = user[other.id]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['match']['win'] += 1
            user[other.id]['match']['lose'] += 1
            result = member.name + '你击剑打败了' + loser + '，夺走了对方' + str(getGold) + '点节操（积分值）'
            update(member.id, 0, getGold, 0)
            update(other.id, 0, -getGold, 0)
        else:
            winner = other.name
            loser = member.name
            if user[member.id]['gold'] < maxGetGold:
                maxGetGold = user[member.id]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['match']['lose'] += 1
            user[other.id]['match']['win'] += 1
            result = member.name + '你击剑输给了' + winner + '，被夺走了' + str(getGold) + '点节操（积分值）'
            update(member.id, 0, -getGold, 0)
            update(other.id, 0, getGold, 0)

        maxLine = int(linecache.getline(r'data/user/fencing.txt', 1))
        x = random.randrange(0, maxLine)
        lineNumber = linecache.getline(r'data/user/fencing.txt', x * 2 + 3)
        process = lineNumber.replace('*name1*', winner).replace('*name2*', loser)

        await app.sendGroupMessage(member.group, MessageChain.create([
            Plain(process),
            Plain('------------\n'),
            Plain(result)
        ]))


# 挑战榜首
async def fencingTop(member, app, group_id):
    global user
    global systemData

    goldId = systemData['rank']['gold-1']['id']

    if goldId == member.id:
        if group_id != 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('自己也要围攻自己吗？')
            ]))
            return
        else:
            await app.sendFriendMessage(member, MessageChain.create([
                Plain('自己也要围攻自己吗？~')
            ]))
            return
    else:
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
        user[goldId]['attribute']['san'] -= 1
        user[goldId]['match']['lostTopTimes'] += 1

        ran = random.randrange(0, 1000)
        # 获胜概率为 你的攻击 - 对方防御力 + 你的san值 - 对方san值
        attack = user[member.id]['attribute']['attack'] + user[member.id]['attribute']['attack-up']
        defense = user[goldId]['attribute']['defense'] + user[member.id]['attribute']['defense-up']
        winPoint = 500 + (
                    (attack - defense) * 10 + user[member.id]['attribute']['san'] - user[goldId]['attribute']['san'])

        # BUFF启用
        if member.id in systemData['god']:  # 用户是无敌模式
            winPoint = 1000
        elif goldId in systemData['god']:  # 被击剑对象是无敌模式
            winPoint = 0
        elif systemData['tmpGod'].__contains__(member.id):  # 用户是无敌模式
            winPoint = 1000
            systemData['tmpGod'][member.id]['number'] -= 1
            if systemData['tmpGod'][member.id]['number'] <= 0:
                del systemData['tmpGod'][member.id]
        elif systemData['tmpGod'].__contains__(goldId):  # 被击剑对象是无敌模式
            winPoint = 0
            systemData['tmpGod'][goldId]['number'] -= 1
            if systemData['tmpGod'][goldId]['number'] <= 0:
                del systemData['tmpGod'][goldId]
        else:
            if systemData['defense-5'].__contains__(goldId):  # 5级防御
                winPoint -= 500
                systemData['defense-5'][goldId]['number'] -= 1
                if systemData['defense-5'][goldId]['number'] <= 0:
                    del systemData['defense-5'][goldId]
            elif systemData['defense-4'].__contains__(goldId):  # 4级防御
                winPoint -= 400
                systemData['defense-4'][goldId]['number'] -= 1
                if systemData['defense-4'][goldId]['number'] <= 0:
                    del systemData['defense-4'][goldId]
            elif systemData['defense-3'].__contains__(goldId):  # 3级防御
                winPoint -= 300
                systemData['defense-3'][goldId]['number'] -= 1
                if systemData['defense-3'][goldId]['number'] <= 0:
                    del systemData['defense-3'][goldId]
            elif systemData['defense-2'].__contains__(goldId):  # 2级防御
                winPoint -= 200
                systemData['defense-2'][goldId]['number'] -= 1
                if systemData['defense-2'][goldId]['number'] <= 0:
                    del systemData['defense-2'][goldId]
            elif systemData['defense-1'].__contains__(goldId):  # 1级防御
                winPoint -= 100
                systemData['defense-1'][goldId]['number'] -= 1
                if systemData['defense-1'][goldId]['number'] <= 0:
                    del systemData['defense-1'][goldId]

            if systemData['rampage-5'].__contains__(member.id):  # 5级暴走
                winPoint += 500
                systemData['rampage-5'][member.id]['number'] -= 1
                if systemData['rampage-5'][member.id]['number'] <= 0:
                    del systemData['rampage-5'][member.id]
            elif systemData['rampage-4'].__contains__(member.id):  # 4级暴走
                winPoint += 400
                systemData['rampage-4'][member.id]['number'] -= 1
                if systemData['rampage-4'][member.id]['number'] <= 0:
                    del systemData['rampage-4'][member.id]
            elif systemData['rampage-3'].__contains__(member.id):  # 3级暴走
                winPoint += 300
                systemData['rampage-3'][member.id]['number'] -= 1
                if systemData['rampage-3'][member.id]['number'] <= 0:
                    del systemData['rampage-3'][member.id]
            elif systemData['rampage-2'].__contains__(member.id):  # 2级暴走
                winPoint += 200
                systemData['rampage-2'][member.id]['number'] -= 1
                if systemData['rampage-2'][member.id]['number'] <= 0:
                    del systemData['rampage-2'][member.id]
            elif systemData['rampage-1'].__contains__(member.id):  # 1级暴走
                winPoint += 100
                systemData['rampage-1'][member.id]['number'] -= 1
                if systemData['rampage-1'][member.id]['number'] <= 0:
                    del systemData['rampage-1'][member.id]

        winner = ''
        loser = ''
        result = ''
        memberName = ''
        if group_id == 0:
            memberName = member.nickname
        else:
            memberName = member.name
        maxGetGold = 8
        if ran < winPoint:
            winner = memberName
            loser = user[goldId]['name']
            if user[goldId]['gold'] < maxGetGold:
                maxGetGold = user[goldId]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['match']['win'] += 1
            user[goldId]['match']['lose'] += 1
            result = memberName + '你击剑打败了' + loser + '，夺走了对方' + str(getGold) + '点节操（积分值）'
            update(member.id, 0, getGold, 0)
            update(goldId, 0, -getGold, 0)
        else:
            winner = user[goldId]['name']
            loser = memberName
            if user[member.id]['gold'] < maxGetGold:
                maxGetGold = user[member.id]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['match']['lose'] += 1
            user[goldId]['match']['win'] += 1
            result = memberName + '你击剑输给了' + winner + '，被夺走了' + str(getGold) + '点节操（积分值）'
            update(member.id, 0, -getGold, 0)
            update(goldId, 0, getGold, 0)

        maxLine = int(linecache.getline(r'data/user/fencing.txt', 1))
        x = random.randrange(0, maxLine)
        lineNumber = linecache.getline(r'data/user/fencing.txt', x * 2 + 3)
        process = lineNumber.replace('*name1*', winner).replace('*name2*', loser)

        if group_id != 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain(process),
                Plain('------------\n'),
                Plain(result)
            ]))
        else:
            await app.sendFriendMessage(member, MessageChain.create([
                Plain(process),
                Plain('------------\n'),
                Plain(result)
            ]))


# 决斗

async def duel(member, id2, app):
    if member.id == id2:
        await app.sendGroupMessage(member.group, MessageChain.create([
            Plain('好家伙，和自己决斗呢？')
        ]))
        return

    other = await app.getMember(member.group.id, id2)

    if other != None:
        newUser(other.id, other.name)
        global user
        global systemData

        # 体力值与积分判断
        if user[other.id]['gold'] <= 1:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain(other.name + '的积分值小于等于1，不能进行决斗')
            ]))
            return
        if user[member.id]['gold'] <= 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('你暂无积分值不可以决斗')
            ]))
            return
        if user[member.id]['attribute']['strength'] <= 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('你今日的体力值已经为0了，不能再决斗啦~')
            ]))
            return
        user[member.id]['attribute']['strength'] -= 1
        user[other.id]['attribute']['san'] -= 1
        user[other.id]['match']['lostTopTimes'] += 1

        ran = random.randrange(0, 1000)
        # 获胜概率为 你的攻击 - 对方防御力 + 你的san值 - 对方san值
        attack = user[member.id]['attribute']['attack'] + user[member.id]['attribute']['attack-up']
        defense = user[other.id]['attribute']['defense'] + user[member.id]['attribute']['defense-up']
        winPoint = 500 + (
                    attack - defense + user[member.id]['attribute']['san'] - user[other.id]['attribute']['san']) * 10

        # BUFF启用
        if member.id in systemData['god']:  # 用户是无敌模式
            winPoint = 1000
        elif other.id in systemData['god']:  # 被决斗对象是无敌模式
            winPoint = 0
        elif systemData['tmpGod'].__contains__(member.id):  # 用户是无敌模式
            winPoint = 1000
            systemData['tmpGod'][member.id]['number'] -= 1
            if systemData['tmpGod'][member.id]['number'] <= 0:
                del systemData['tmpGod'][member.id]
        elif systemData['tmpGod'].__contains__(other.id):  # 被决斗对象是无敌模式
            winPoint = 0
            systemData['tmpGod'][other.id]['number'] -= 1
            if systemData['tmpGod'][other.id]['number'] <= 0:
                del systemData['tmpGod'][other.id]
        else:
            if systemData['defense-5'].__contains__(other.id):  # 5级防御
                winPoint -= 500
                systemData['defense-5'][other.id]['number'] -= 1
                if systemData['defense-5'][other.id]['number'] <= 0:
                    del systemData['defense-5'][other.id]
            elif systemData['defense-4'].__contains__(other.id):  # 4级防御
                winPoint -= 400
                systemData['defense-4'][other.id]['number'] -= 1
                if systemData['defense-4'][other.id]['number'] <= 0:
                    del systemData['defense-4'][other.id]
            elif systemData['defense-3'].__contains__(other.id):  # 3级防御
                winPoint -= 300
                systemData['defense-3'][other.id]['number'] -= 1
                if systemData['defense-3'][other.id]['number'] <= 0:
                    del systemData['defense-3'][other.id]
            elif systemData['defense-2'].__contains__(other.id):  # 2级防御
                winPoint -= 200
                systemData['defense-2'][other.id]['number'] -= 1
                if systemData['defense-2'][other.id]['number'] <= 0:
                    del systemData['defense-2'][other.id]
            elif systemData['defense-1'].__contains__(other.id):  # 1级防御
                winPoint -= 100
                systemData['defense-1'][other.id]['number'] -= 1
                if systemData['defense-1'][other.id]['number'] <= 0:
                    del systemData['defense-1'][other.id]

            if systemData['rampage-5'].__contains__(member.id):  # 5级暴走
                winPoint += 500
                systemData['rampage-5'][member.id]['number'] -= 1
                if systemData['rampage-5'][member.id]['number'] <= 0:
                    del systemData['rampage-5'][member.id]
            elif systemData['rampage-4'].__contains__(member.id):  # 4级暴走
                winPoint += 400
                systemData['rampage-4'][member.id]['number'] -= 1
                if systemData['rampage-4'][member.id]['number'] <= 0:
                    del systemData['rampage-4'][member.id]
            elif systemData['rampage-3'].__contains__(member.id):  # 3级暴走
                winPoint += 300
                systemData['rampage-3'][member.id]['number'] -= 1
                if systemData['rampage-3'][member.id]['number'] <= 0:
                    del systemData['rampage-3'][member.id]
            elif systemData['rampage-2'].__contains__(member.id):  # 2级暴走
                winPoint += 200
                systemData['rampage-2'][member.id]['number'] -= 1
                if systemData['rampage-2'][member.id]['number'] <= 0:
                    del systemData['rampage-2'][member.id]
            elif systemData['rampage-1'].__contains__(member.id):  # 1级暴走
                winPoint += 100
                systemData['rampage-1'][member.id]['number'] -= 1
                if systemData['rampage-1'][member.id]['number'] <= 0:
                    del systemData['rampage-1'][member.id]

        winner = ''
        loser = ''
        result = ''
        maxGetGold = 8
        if ran < winPoint:
            winner = member.name
            loser = other.name
            if user[other.id]['gold'] < maxGetGold:
                maxGetGold = user[other.id]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['match']['win'] += 1
            user[other.id]['match']['lose'] += 1
            result = member.name + '你决斗打败了' + loser + '，夺走了对方' + str(getGold) + '点积分值'
            update(member.id, 0, getGold, 0)
            update(other.id, 0, -getGold, 0)
        else:
            winner = other.name
            loser = member.name
            if user[member.id]['gold'] < maxGetGold:
                maxGetGold = user[member.id]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['match']['lose'] += 1
            user[other.id]['match']['win'] += 1
            result = member.name + '你决斗输给了' + winner + '，被夺走了' + str(getGold) + '点积分值'
            update(member.id, 0, -getGold, 0)
            update(other.id, 0, getGold, 0)

        await app.sendGroupMessage(member.group, MessageChain.create([
            Plain(result)
        ]))


# 决斗榜首
async def duelTop(member, app, group_id):
    global user
    global systemData

    goldId = systemData['rank']['gold-1']['id']

    if goldId == member.id:
        if group_id != 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('自己也要打自己吗？')
            ]))
            return
        else:
            await app.sendFriendMessage(member, MessageChain.create([
                Plain('自己也要打自己吗？~')
            ]))
            return
    else:
        if user[goldId]['gold'] <= 1:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain(user[goldId]['name'] + '的积分值小于等于1，不能进行决斗')
            ]))
            return
        if user[member.id]['gold'] <= 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('你暂无积分值不可以决斗')
            ]))
            return
        if user[member.id]['attribute']['strength'] <= 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('你今日的体力值已经为0了，不能再决斗啦~')
            ]))
            return
        user[member.id]['attribute']['strength'] -= 1
        user[goldId]['attribute']['san'] -= 1
        user[goldId]['match']['lostTopTimes'] += 1

        ran = random.randrange(0, 1000)
        # 获胜概率为 你的攻击 - 对方防御力 + 你的san值 - 对方san值
        attack = user[member.id]['attribute']['attack'] + user[member.id]['attribute']['attack-up']
        defense = user[goldId]['attribute']['defense'] + user[member.id]['attribute']['defense-up']
        winPoint = 500 + (
                    (attack - defense) * 10 + user[member.id]['attribute']['san'] - user[goldId]['attribute']['san'])

        # BUFF启用
        if member.id in systemData['god']:  # 用户是无敌模式
            winPoint = 1000
        elif goldId in systemData['god']:  # 被决斗对象是无敌模式
            winPoint = 0
        elif systemData['tmpGod'].__contains__(member.id):  # 用户是无敌模式
            winPoint = 1000
            systemData['tmpGod'][member.id]['number'] -= 1
            if systemData['tmpGod'][member.id]['number'] <= 0:
                del systemData['tmpGod'][member.id]
        elif systemData['tmpGod'].__contains__(goldId):  # 被决斗对象是无敌模式
            winPoint = 0
            systemData['tmpGod'][goldId]['number'] -= 1
            if systemData['tmpGod'][goldId]['number'] <= 0:
                del systemData['tmpGod'][goldId]
        else:
            if systemData['defense-5'].__contains__(goldId):  # 5级防御
                winPoint -= 500
                systemData['defense-5'][goldId]['number'] -= 1
                if systemData['defense-5'][goldId]['number'] <= 0:
                    del systemData['defense-5'][goldId]
            elif systemData['defense-4'].__contains__(goldId):  # 4级防御
                winPoint -= 400
                systemData['defense-4'][goldId]['number'] -= 1
                if systemData['defense-4'][goldId]['number'] <= 0:
                    del systemData['defense-4'][goldId]
            elif systemData['defense-3'].__contains__(goldId):  # 3级防御
                winPoint -= 300
                systemData['defense-3'][goldId]['number'] -= 1
                if systemData['defense-3'][goldId]['number'] <= 0:
                    del systemData['defense-3'][goldId]
            elif systemData['defense-2'].__contains__(goldId):  # 2级防御
                winPoint -= 200
                systemData['defense-2'][goldId]['number'] -= 1
                if systemData['defense-2'][goldId]['number'] <= 0:
                    del systemData['defense-2'][goldId]
            elif systemData['defense-1'].__contains__(goldId):  # 1级防御
                winPoint -= 100
                systemData['defense-1'][goldId]['number'] -= 1
                if systemData['defense-1'][goldId]['number'] <= 0:
                    del systemData['defense-1'][goldId]

            if systemData['rampage-5'].__contains__(member.id):  # 5级暴走
                winPoint += 500
                systemData['rampage-5'][member.id]['number'] -= 1
                if systemData['rampage-5'][member.id]['number'] <= 0:
                    del systemData['rampage-5'][member.id]
            elif systemData['rampage-4'].__contains__(member.id):  # 4级暴走
                winPoint += 400
                systemData['rampage-4'][member.id]['number'] -= 1
                if systemData['rampage-4'][member.id]['number'] <= 0:
                    del systemData['rampage-4'][member.id]
            elif systemData['rampage-3'].__contains__(member.id):  # 3级暴走
                winPoint += 300
                systemData['rampage-3'][member.id]['number'] -= 1
                if systemData['rampage-3'][member.id]['number'] <= 0:
                    del systemData['rampage-3'][member.id]
            elif systemData['rampage-2'].__contains__(member.id):  # 2级暴走
                winPoint += 200
                systemData['rampage-2'][member.id]['number'] -= 1
                if systemData['rampage-2'][member.id]['number'] <= 0:
                    del systemData['rampage-2'][member.id]
            elif systemData['rampage-1'].__contains__(member.id):  # 1级暴走
                winPoint += 100
                systemData['rampage-1'][member.id]['number'] -= 1
                if systemData['rampage-1'][member.id]['number'] <= 0:
                    del systemData['rampage-1'][member.id]

        winner = ''
        loser = ''
        result = ''
        memberName = ''
        if group_id == 0:
            memberName = member.nickname
        else:
            memberName = member.name
        maxGetGold = 8
        if ran < winPoint:
            winner = memberName
            loser = user[goldId]['name']
            if user[goldId]['gold'] < maxGetGold:
                maxGetGold = user[goldId]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['match']['win'] += 1
            user[goldId]['match']['lose'] += 1
            result = memberName + '你决斗打败了' + loser + '，夺走了对方' + str(getGold) + '点积分值'
            update(member.id, 0, getGold, 0)
            update(goldId, 0, -getGold, 0)
        else:
            winner = user[goldId]['name']
            loser = memberName
            if user[member.id]['gold'] < maxGetGold:
                maxGetGold = user[member.id]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['match']['lose'] += 1
            user[goldId]['match']['win'] += 1
            result = memberName + '你决斗输给了' + winner + '，被夺走了' + str(getGold) + '点积分值'
            update(member.id, 0, -getGold, 0)
            update(goldId, 0, getGold, 0)

        if group_id != 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain(result)
            ]))
        else:
            await app.sendFriendMessage(member, MessageChain.create([
                Plain(result)
            ]))


# 获取排行榜
def getRank():
    global user
    global systemData

    if len(user) == 0:
        return '暂无排行榜'

    result = '排行榜\n'
    result += '----------------\n'
    result += '积分第一：' + user[systemData['rank']['gold-1']['id']]['name'] + '（' + str(
        user[systemData['rank']['gold-1']['id']]['gold']) + '）\n'
    if systemData['rank']['gold-2']['id'] != 0:
        result += '积分第二：' + user[systemData['rank']['gold-2']['id']]['name'] + '（' + str(
            user[systemData['rank']['gold-2']['id']]['gold']) + '）\n'
    if systemData['rank']['gold-3']['id'] != 0:
        result += '积分第三：' + user[systemData['rank']['gold-3']['id']]['name'] + '（' + str(
            user[systemData['rank']['gold-3']['id']]['gold']) + '）\n'

    rate = round(systemData['rank']['rate']['rate'], 2) * 100
    result += '胜率第一：' + user[systemData['rank']['rate']['id']]['name'] + '（' + str(int(rate)) + '%）'
    rateValue = round(systemData['rank']['rate50']['rate'], 2) * 100
    if systemData['rank']['rate50']['id'] != 0:
        result += '\n胜率第一（大于50场）：' + user[systemData['rank']['rate50']['id']]['name'] + '（' + str(int(rateValue)) + '%）'

    if systemData['rank']['field']['id'] != 0:
        result += '\n击剑达人：' + user[systemData['rank']['field']['id']]['name'] + '（' + str(
            systemData['rank']['field']['number']) + '场）'
    if systemData['rank']['challenger']['id'] != 0:
        result += '\n登顶次数最多：' + user[systemData['rank']['challenger']['id']]['name'] + '（' + str(
            systemData['rank']['challenger']['number']) + '次）'
    if systemData['rank']['loser']['id'] != 0:
        result += '\n被击剑次数最多：' + user[systemData['rank']['loser']['id']]['name'] + '（' + str(
            systemData['rank']['loser']['number']) + '次）'

    return result


# 购买商品
def purchase(id, name, number):
    global goodsAvailable
    global goods
    global user
    if name in goodsAvailable:
        if user[id]['gold'] >= goods[name]['cost'] * number:
            if getGooods(id, 0, name, number):
                update(id, -2, -goods[name]['cost'] * number, 0)
                return '购买成功！'
            else:
                return '背包已满'
        else:
            return '积分不足~'
    else:
        return '不存在该物品或者不可购买'


# 丢弃商品
def discard(id, name, number):
    global user
    if user[id]['warehouse'].__contains__(name):
        user[id]['warehouse'][name]['number'] -= number
        if user[id]['warehouse'][name]['number'] <= 0:
            del user[id]['warehouse'][name]
        return '丢弃成功！'
    else:
        return '你没有该物品~'


# 出售商品
def sellGoods(id, name, number):
    global user
    global goods
    if user[id]['warehouse'].__contains__(name):
        if number > user[id]['warehouse'][name]['number']:
            number = user[id]['warehouse'][name]['number']
        gold = goods[name]['sell'] * number
        update(id, -2, gold, 0)
        user[id]['warehouse'][name]['number'] -= number
        if user[id]['warehouse'][name]['number'] <= 0:
            del user[id]['warehouse'][name]
        return '你成功出售' + str(number) + '件物品，获得' + str(gold) + '积分'
    else:
        return '你没有该物品~'


# ============================================
# 明日方舟抽卡模拟器

def MRFZ_card():
    bot_information = dataManage.load_obj('baseInformation')
    if not bot_information['reply'].__contains__('cards'):
        bot_information['reply']['cards'] = 0
    bot_information['reply']['cards'] += 1
    if bot_information['reply']['cards'] > 5:
        return '你抽卡太快了，每分钟最多只能抽5次哦~'
    dataManage.save_obj(bot_information, 'baseInformation')

    card1 = []
    card2 = []
    card3 = []
    card4 = []
    card5 = []
    card6 = []
    information = []
    with open('data/明日方舟/PersonaCard.txt', 'r+', encoding='utf-8') as f:
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
    bot_information = dataManage.load_obj('baseInformation')
    if not bot_information['reply'].__contains__('cards'):
        bot_information['reply']['cards'] = 0
    bot_information['reply']['cards'] += 1
    if bot_information['reply']['cards'] > 5:
        return '你抽卡太快了，每分钟最多只能抽5次哦~'
    dataManage.save_obj(bot_information, 'baseInformation')

    card1 = []
    card2 = []
    card3 = []
    card4 = []
    card5 = []
    card6 = []
    information = []
    with open('data/明日方舟/PersonaCard.txt', 'r+', encoding='utf-8') as f:
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
    global user
    if user[id]['attribute']['strength'] < 1 or user[id]['gold'] > 1:
        return '对' + name + '不屑一顾'
    gold = random.randint(1, 3)
    if user[id]['gold'] + gold < 0:
        gold = -user[id]['gold'] + 1
    update(id, -2, gold, 0)
    return '看' + name + '太可怜，于是给了你一些积分'


'''
消耗体力 2

90% 木板
10% 苹果
'''


def cutDown(id):
    global user
    if user[id]['attribute']['strength'] < 1:
        return '你的体力值不足不能砍树'
    user[id]['attribute']['strength'] -= 1

    p = random.randrange(1000)


'''
消耗体力：2

10% 一无所获
0.5% 燧石
64.5% 碎石
12% 石头
7% 皮革
1% 破旧的装备
    0.10% 其余装备
    0.50% 一期装备
    0.30% 二期装备
    0.10% 三期装备
    
1% 铁
0.9% 黄金
0.09% 钻石
0.009% 合金
0.001% 下界合金
'''


def dig(id):
    global user
    if user[id]['attribute']['strength'] < 2:
        return '你的体力值不足不能挖矿'
    user[id]['attribute']['strength'] -= 2

    result = '你一番挖掘之后，'
    p = random.randrange(0, 10000)
    if p < 2000:
        result += '一无所获'
    elif p < 2050:
        ran = random.randrange(0, 4) + 1
        result += '获得了' + str(ran) + '块燧石'
        getGooods(id, 1, '燧石', ran)
    elif p < 8500:
        ran = random.randrange(0, 4) + 1
        result += '获得了' + str(ran) + '块碎石'
        getGooods(id, 1, '碎石', ran)
    elif p < 9000:
        ran = random.randrange(0, 3) + 1
        result += '获得了' + str(ran) + '块石头'
        getGooods(id, 1, '石头', ran)
    elif p < 9700:
        result += '获得了1个沙子'
        getGooods(id, 1, '沙子', 1)
    elif p < 9710:
        result += '获得了1块下品灵石'
        getGooods(id, 1, '下品灵石', 1)
    elif p < 9750:
        result += '获得了1块皮革'
        getGooods(id, 1, '皮革', 1)
    elif p < 9800:  # 装备
        p2 = random.randrange(0, 100)

        if p2 < 50:
            ran = random.randrange(0, 6)
            if ran == 0:
                result += '获得了破旧的木剑X1'
                getGooods(id, 1, '破旧的木剑', 1)
            elif ran == 1:
                result += '获得了破旧的木斧X1'
                getGooods(id, 1, '破旧的木斧', 1)
            elif ran == 2:
                result += '获得了破旧的布头盔X1'
                getGooods(id, 1, '破旧的布头盔', 1)
            elif ran == 3:
                result += '获得了破旧的布甲X1'
                getGooods(id, 1, '破旧的布甲', 1)
            elif ran == 4:
                result += '获得了破旧的布护腿X1'
                getGooods(id, 1, '破旧的布护腿', 1)
            elif ran == 5:
                result += '获得了破旧的布靴X1'
                getGooods(id, 1, '破旧的布靴', 1)
        elif p2 < 80:
            ran = random.randrange(0, 6)
            if ran == 0:
                result += '获得了破旧的石剑X1'
                getGooods(id, 1, '破旧的石剑', 1)
            elif ran == 1:
                result += '获得了破旧的石斧X1'
                getGooods(id, 1, '破旧的石斧', 1)
            elif ran == 2:
                result += '获得了破旧的皮革头盔X1'
                getGooods(id, 1, '破旧的皮革头盔', 1)
            elif ran == 3:
                result += '获得了破旧的皮革甲X1'
                getGooods(id, 1, '破旧的皮革甲', 1)
            elif ran == 4:
                result += '获得了破旧的皮革护腿X1'
                getGooods(id, 1, '破旧的皮革护腿', 1)
            elif ran == 5:
                result += '获得了破旧的皮革靴X1'
                getGooods(id, 1, '破旧的皮革靴', 1)
        elif p2 < 90:
            ran = random.randrange(0, 6)
            if ran == 0:
                result += '获得了破旧的铁剑X1'
                getGooods(id, 1, '破旧的铁剑', 1)
            elif ran == 1:
                result += '获得了破旧的铁斧X1'
                getGooods(id, 1, '破旧的铁斧', 1)
            elif ran == 2:
                result += '获得了破旧的铁头盔X1'
                getGooods(id, 1, '破旧的铁头盔', 1)
            elif ran == 3:
                result += '获得了破旧的铁甲X1'
                getGooods(id, 1, '破旧的铁甲', 1)
            elif ran == 4:
                result += '获得了破旧的铁护腿X1'
                getGooods(id, 1, '破旧的铁护腿', 1)
            elif ran == 5:
                result += '获得了破旧的铁靴X1'
                getGooods(id, 1, '破旧的铁靴', 1)
        else:
            ran = random.randrange(0, 6)
            if ran == 0:
                result += '获得了攻击戒指X1'
                getGooods(id, 1, '攻击戒指', 1)
            elif ran == 1:
                result += '获得了守护戒指X1'
                getGooods(id, 1, '守护戒指', 1)
            elif ran == 2:
                result += '获得了制式长枪X1'
                getGooods(id, 1, '制式长枪', 1)
            elif ran == 3:
                result += '获得了铁制长枪X1'
                getGooods(id, 1, '铁制长枪', 1)
            elif ran == 4:
                result += '获得了大鸡腿X1'
                getGooods(id, 1, '大鸡腿', 1)
            elif ran == 5:
                result += '获得了布背包X1'
                getGooods(id, 1, '布背包', 1)

    elif p < 9970:
        result += '获得了1块铁锭'
        getGooods(id, 1, '铁锭', 1)
    elif p < 9990:
        result += '获得了1块金锭'
        getGooods(id, 1, '金锭', 1)
    else:
        p2 = random.randrange(0, 1000)
        if p2 < 900:
            result += '获得了1颗钻石'
            getGooods(id, 1, '钻石', 1)
        elif p2 < 990:
            result += '获得了1块合金'
            getGooods(id, 1, '合金', 1)
        else:
            result += '获得了1块下界合金'
            getGooods(id, 1, '下界合金', 1)

    return result


'''
消耗体力：1

40% 啥也没有
10% BUFF
20% 1点体力 | 1点积分
15% 2点体力 | 2点积分
4.5% 3点积分
0.4% 4点积分
0.1% 10点体力 | 10点积分

E = 0.711
'''


def fishing(id, name):
    global user
    if user[id]['attribute']['strength'] < 1:
        return name + '体力值不足不能探险'
    user[id]['attribute']['strength'] -= 1
    ran = random.randrange(0, 1000)
    ran2 = random.randrange(0, 2)

    describe_dict = [
        '你来到了一个黑漆漆的山洞，四周十分安静，一番探索之后',
        '你来到一个遗迹，一番探索之后',
        '你发现了一个宝箱',
        '在亚马逊的原始森林里，你被讨厌的虫子烦的要死',
        '你在古玩市场一番搜索之后',
        '你在一个古代陵墓里，一番探索之后',
        '你来到了南极，冰天雪地之中，一番探索之后',
        '你在狂风骤雨的大海上航行，遇见了一个廖无人烟的小岛，一番探索之后',
        '你在沙哈拉沙漠中，孤独的一个人前行',
        '你在古埃及的金字塔里，一番探索之后',
        '你在亚特兰蒂斯的遗迹里，一番探索之后',
        '你好像梦见了你在做梦梦你在做梦，等你清醒之后脑袋晕乎乎的，但不知道为什么',
        '你在大荒漠上行走，遇见了黑风暴，因祸得福发现了一个宝箱',
        '你在高山之上探索无人之地',
        '你决定在后院探险，发现了祖辈留下来的宝箱',
        '你走在大路上发现了一个人手里拿着宝箱，于是你来骗、来偷袭，获得了这个宝箱',
        '你乘坐飞船抵达了月球，探索一番后',
        '你来到了九龙城，这里乌烟瘴气，一番探索之后',
        '你乘坐宇宙飞船抵达了火星，一番探索之后',
        '你在寒冷的北极圈与北极熊作伴，一番探索之后',
        '你在大街上，在别人奇怪的目光里，一番搜寻之后'
    ]

    describe = random.choice(describe_dict)
    result = ''
    gold = 0
    strength = 0

    if ran < 400:
        result = '什么也没有获得'
    elif ran < 450:
        ran = random.randrange(0, 100)
        if ran < 40:  # 进攻模式
            ran2 = random.randrange(0, 100)
            if ran2 < 60:
                tmp = random.randrange(0, 10) + 1
                changeToRampage1(id, tmp)
                result += '获得了一个' + str(tmp) + '次的1级进攻BUFF'
            elif ran2 < 90:
                tmp = random.randrange(0, 5) + 1
                changeToRampage2(id, tmp)
                result += '获得了一个' + str(tmp) + '次的2级进攻BUFF'
            elif ran2 < 100:
                tmp = random.randrange(0, 3) + 1
                changeToRampage3(id, tmp)
                result += '获得了一个' + str(tmp) + '次的3级进攻BUFF'
        elif ran < 80:  # 防御模式
            ran2 = random.randrange(0, 100)
            if ran2 < 60:
                tmp = random.randrange(0, 10) + 1
                changeToDefense1(id, tmp)
                result += '获得了一个' + str(tmp) + '次的1级防御BUFF'
            elif ran2 < 90:
                tmp = random.randrange(0, 5) + 1
                changeToDefense2(id, tmp)
                result += '获得了一个' + str(tmp) + '次的2级防御BUFF'
            elif ran2 < 100:
                tmp = random.randrange(0, 3) + 1
                changeToDefense3(id, tmp)
                result += '获得了一个' + str(tmp) + '次的3级防御BUFF'
        elif ran < 88:  # 减半积分收益
            tmp = random.randrange(0, 10) + 1
            changeToHalveGold(id, tmp)
            result += '获得了一个' + str(tmp) + '次的收益减半BUFF'
        elif ran < 96:  # 双倍积分收益
            tmp = random.randrange(0, 10) + 1
            changeToDoubleGold(id, tmp)
            result += '获得了一个' + str(tmp) + '次的双倍积分收益BUFF'
        else:  # 固定增减积分收益
            tmp = random.randrange(0, 3) + 1
            tmp2 = random.randrange(0, 11) - 5
            changeToFixedGold(id, tmp, tmp2)
            if tmp2 > 0:
                result += '获得了一个' + str(tmp) + '次的收益积分+' + str(tmp2) + 'BUFF'
            else:
                result += '获得了一个' + str(tmp) + '次的收益积分' + str(tmp2) + 'BUFF'

    elif ran < 700:
        if ran2 == 0:
            strength = 1
            result = '获得了1点体力'
        else:
            gold = 1
            result = '获得了1点积分值'
    elif ran < 800:
        if ran2 == 0:
            strength = 2
            result = '获得了2点体力'
        else:
            gold = 2
            result = '获得了2点积分值'
    elif ran < 990:
        gold = 3
        result = '获得了3点积分值'
    elif ran < 999:
        gold = 4
        result = '获得了4点积分值'
    else:
        if ran2 == 0:
            strength = 10
            result = '获得了10点体力'
        else:
            gold = 10
            result = '获得了10点积分值'

    update(id, 1, gold, strength)  # 更新数据
    return name + describe + '，' + result


'''
20% 一无所获
15% BUFF & 装备
    2% 无敌模式
    10% 装备
        20% 守护戒指
        ```(10% 贪婪戒指)
        10% 大鸡腿
        10% 制式长枪
        20% 金条
        40% 金粒
    35% 进攻模式
    35% 防御模式
    5% 双倍积分收益
    3% 三倍积分收益
    5% 固定增减积分收益
    5% 减半积分收益
5% 不好不坏
20% 一般好
20% 一般坏
8%  比较好
8%  比较坏
2%   超级好
2%   超级坏
'''


def hangOut(id):
    global user
    if user[id]['gold'] < 1:
        return '你的积分小于1，不能闲逛了'
    if user[id]['attribute']['strength'] < 1:
        return '你的体力值小于1，不能闲逛了'

    probability = random.randrange(0, 1000)
    result = ''
    gold = 0
    strength = 0

    if probability < 200:  # 一无所获
        describe_dict = [
            '你闲逛了一圈，啥也没有发生',
            '你在闲逛的时候逛回去了，啥也没获得',
            '你在闲逛的时候踩了一坨便便并且坚信明天会走狗屎运',
            '你在闲逛的时候遇见了好朋友，他叫你回家开黑，于是你又回去了',
            '你在闲逛的时候想起了还有原神没有肝于是返回了',
            '你在闲逛的时候想起方舟的活动还没有打，于是回家了'
        ]
        result = random.choice(describe_dict)

    elif probability < 300:  # BUFF & 装备
        ran = random.randrange(0, 100)
        if ran < 20:  # 装备
            ran2 = random.randrange(0, 1000)
            if ran2 < 550:
                if getGooods(id, 1, '金粒', 1):
                    result = '你闲逛时获得了金粒'
                else:
                    result = '你闲逛时获得了金粒，但是背包满了'
            elif ran2 < 650:
                if getGooods(id, 1, '金条', 1):
                    result = '你闲逛时获得了金条'
                else:
                    result = '你闲逛时获得了金条，但是背包满了'
            elif ran2 < 700:
                if getGooods(id, 1, '金块', 1):
                    result = '你闲逛时获得了金块'
                else:
                    result = '你闲逛时获得了金块，但是背包满了'
            elif ran2 < 800:
                if getGooods(id, 1, '石头', 1):
                    result = '你闲逛时获得了石头'
                else:
                    result = '你闲逛时获得了石头，但是背包满了'
            elif ran2 < 900:
                if getGooods(id, 1, '木板', 1):
                    result = '你闲逛时获得了木板'
                else:
                    result = '你闲逛时获得了木板，但是背包满了'

            elif ran2 < 910:
                if getGooods(id, 1, '破旧的木剑', 1):
                    result = '你闲逛时获得了破旧的木剑'
                else:
                    result = '你闲逛时获得了破旧的木剑，但是背包满了'
            elif ran2 < 920:
                if getGooods(id, 1, '破旧的木斧', 1):
                    result = '你闲逛时获得了破旧的木斧'
                else:
                    result = '你闲逛时获得了破旧的木斧，但是背包满了'
            elif ran2 < 930:
                if getGooods(id, 1, '破旧的布头盔', 1):
                    result = '你闲逛时获得了破旧的布头盔'
                else:
                    result = '你闲逛时获得了破旧的布头盔，但是背包满了'
            elif ran2 < 940:
                if getGooods(id, 1, '破旧的布甲', 1):
                    result = '你闲逛时获得了破旧的布甲'
                else:
                    result = '你闲逛时获得了破旧的布头盔，但是背包满了'
            elif ran2 < 950:
                if getGooods(id, 1, '破旧的布护腿', 1):
                    result = '你闲逛时获得了破旧的布护腿'
                else:
                    result = '你闲逛时获得了破旧的布护腿，但是背包满了'
            elif ran2 < 960:
                if getGooods(id, 1, '破旧的布靴', 1):
                    result = '你闲逛时获得了破旧的布靴'
                else:
                    result = '你闲逛时获得了破旧的布靴，但是背包满了'

            elif ran2 < 965:
                if getGooods(id, 1, '守护戒指', 1):
                    result = '你闲逛时获得了守护戒指'
                else:
                    result = '你闲逛时获得了守护戒指，但是背包满了'
            elif ran2 < 970:
                if getGooods(id, 1, '攻击戒指', 1):
                    result = '你闲逛时获得了攻击戒指'
                else:
                    result = '你闲逛时获得了攻击戒指，但是背包满了'
            elif ran2 < 975:
                if getGooods(id, 1, '体力戒指', 1):
                    result = '你闲逛时获得了体力戒指'
                else:
                    result = '你闲逛时获得了体力戒指，但是背包满了'
            elif ran2 < 980:
                if getGooods(id, 1, '大鸡腿', 1):
                    result = '你闲逛时获得了大鸡腿'
                else:
                    result = '你闲逛时获得了大鸡腿，但是背包满了'
            elif ran2 < 985:
                if getGooods(id, 1, '铁制长枪', 1):
                    result = '你闲逛时获得了铁制长枪'
                else:
                    result = '你闲逛时获得了铁制长枪，但是背包满了'
            elif ran2 < 990:
                if getGooods(id, 1, '制式长枪', 1):
                    result = '你闲逛时获得了制式长枪'
                else:
                    result = '你闲逛时获得了制式长枪，但是背包满了'
            elif ran2 < 995:
                if getGooods(id, 1, '木剑', 1):
                    result = '你闲逛时获得了木剑'
                else:
                    result = '你闲逛时获得了木剑，但是背包满了'
            elif ran2 < 1000:
                if getGooods(id, 1, '布甲', 1):
                    result = '你闲逛时获得了布甲'
                else:
                    result = '你闲逛时获得了布甲，但是背包满了'
        elif ran < 45:  # 进攻模式
            ran2 = random.randrange(0, 100)
            if ran2 < 50:
                tmp = random.randrange(0, 5) + 1
                changeToRampage1(id, tmp)
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的1级进攻BUFF'
            elif ran2 < 80:
                tmp = random.randrange(0, 3) + 1
                changeToRampage2(id, tmp)
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的2级进攻BUFF'
            elif ran2 < 100:
                tmp = random.randrange(0, 2) + 1
                changeToRampage3(id, tmp)
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的3级进攻BUFF'
        elif ran < 80:  # 防御模式
            ran2 = random.randrange(0, 100)
            if ran2 < 50:
                tmp = random.randrange(0, 5) + 1
                changeToDefense1(id, tmp)
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的1级防御BUFF'
            elif ran2 < 80:
                tmp = random.randrange(0, 3) + 1
                changeToDefense2(id, tmp)
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的2级防御BUFF'
            elif ran2 < 100:
                tmp = random.randrange(0, 2) + 1
                changeToDefense3(id, tmp)
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的3级防御BUFF'
        elif ran < 85:  # 减半积分收益
            tmp = random.randrange(0, 10) + 1
            changeToHalveGold(id, tmp)
            result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的收益减半BUFF'
        elif ran < 87:  # 固定增减积分收益
            tmp = random.randrange(0, 5) + 1
            tmp2 = random.randrange(0, 11) - 5
            changeToFixedGold(id, tmp, tmp2)
            if tmp2 > 0:
                result = '你在闲逛的时候，获得了一个' + str(tmp) + '次的收益积分+' + str(tmp2) + '的BUFF'
            else:
                result = '你在闲逛的时候，获得了一个' + str(tmp) + '次的收益积分' + str(tmp2) + '的BUFF'
        elif ran < 90:  # 击剑不损失积分
            tmp = random.randrange(0, 5) + 1
            changeToNoLoss(id, tmp)
            result = '你在闲逛的时候，获得了一个' + str(tmp) + '次的击剑不损失积分BUFF'
        elif ran < 95:  # 双倍积分收益
            tmp = random.randrange(0, 10) + 1
            changeToDoubleGold(id, tmp)
            result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的双倍积分收益BUFF'
        elif ran < 98:  # 三倍积分收益
            tmp = random.randrange(0, 5) + 1
            changeToTripleGold(id, tmp)
            result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的双倍积分收益BUFF'
        else:  # 无敌模式
            tmp = random.randrange(0, 3) + 1
            changeToTmpGod(id, tmp)
            result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的临时击剑无敌BUFF'


    elif probability < 400:  # 不好不坏
        ran = random.randrange(0, 3)

        if ran == 0:
            result = '你在闲逛的时候被网红火锅店吸引没忍住冲了进去，积分-1，体力+2'
            gold = -1
            strength = 2
        elif ran == 1:
            result = '你在闲逛的时候，嘴馋买了个冰淇淋，积分-2，体力+2'
            gold = -2
            strength = 2
        if ran == 2:
            result = '你在闲逛的时候被舞女拉进了小树林，积分-2，体力+2'
            gold = -2
            strength = 2

    elif probability < 550:  # 一般好
        ran = random.randrange(0, 10)

        if ran == 0:
            result = '你在闲逛的时候遇见了阿拉灯神丁，他说实现你三个愿望然后摸了你的钱包转身就走，积分+3'
            gold = 3
        elif ran == 1:
            result = '你在闲逛的时候邂逅了笑猫，他送给你了一个大大的笑容，体力+3'
            strength = 3
        elif ran == 2:
            result = '你闲逛的时候碰见富豪在路上撒钱，积分+2'
            gold = 2
        elif ran == 3:
            result = '你在闲逛的时候，决定尝试一下彩票，中奖了，积分+1'
            gold = 1
        elif ran == 4:
            result = '你在闲逛的时候，决定尝试一下彩票，中奖了，积分+2'
            gold = 2
        elif ran == 5:
            result = '你在闲逛的时候，决定尝试一下彩票，中奖了，积分+3'
            gold = 3
        elif ran == 6:
            result = '你在闲逛的时候，决定尝试一下刮刮乐，中奖了，积分+1'
            gold = 1
        elif ran == 7:
            result = '你出去闲逛的时候邂逅了霸道总裁，总裁他妈为了拆散你们拿钱羞辱你，积分+2'
            gold = 2
        elif ran == 8:
            result = '你出去闲逛的时候邂逅了富婆，富婆他妈为了拆散你们拿钱羞辱你，积分+2'
            gold = 2
        elif ran == 9:
            result = '你闲逛的时候采到了采女孩的小蘑菇回去当晚饭，积分+1'
            gold = 1
        elif ran == 10:
            result = '你在闲逛的时候遇见了一个要自杀的女孩，将其救下后，她的家人奖励了你一些钱，积分+1'
            gold = 1

    elif probability < 800:  # 一般坏
        ran = random.randrange(0, 8)

        if ran == 0:
            result = '你在路上看美女被小柒发现，惨遭暴打，体力-2，积分-2'
            gold = -2
            strength = -2
        elif ran == 1:
            result = '你出门之后天下起了倾盆大雨，狂奔回家之后发现钥匙丢在了咖啡厅，于是去咖啡厅拿了钥匙后折返，体力-1'
            strength = -1
        elif ran == 2:
            result = '你在闲逛的时候逛回去了，啥也没获得,体力-1'
            strength = -1
        elif ran == 3:
            result = '你在闲逛的时候，决定尝试一下彩票，但是没有中奖，积分-2'
            gold = -2
        elif ran == 4:
            result = '你在闲逛的时候，决定尝试一下刮刮乐，但是没有中奖，积分-2'
            gold = -2
        elif ran == 5:
            result = '你在闲逛的时候，嘴馋买了个冰淇淋，积分-2'
            gold = -2
        elif ran == 6:
            result = '你闲逛的时候被牛顿的果子砸了并冒出了一圈星星，体力-2'
            strength = -2
        elif ran == 7:
            result = '你闲逛的时候被狗追，于是选择在树上卡了一天，体力-3'
            strength = -3

    elif probability < 880:  # 比较好
        ran = random.randrange(0, 4)

        if ran == 0:
            result = '你在闲逛的时候，遇见了一个卖苹果的老婆婆，你买了一些苹果，积分-1，体力+5'
            gold = -1
            strength = 5
        elif ran == 1:
            result = '你出去闲逛的时候碰见npy妈妈，原来Ta是隐藏的富二代，Ta妈妈甩给你五十万让你走，伤害性不大，侮辱性极强，积分+5'
            gold = 5
        elif ran == 2:
            result = '你买彩票中了二等奖，积分+5'
            gold = 5
        elif ran == 3:
            result = '你参加了一场马拉松并且获得了第一名，体力-1，积分+5'
            gold = 5
            strength = -1

    elif probability < 960:  # 比较坏
        ran = random.randrange(0, 4)

        if ran == 0:
            result = '你在闲逛的时候遇见了一个可怜的乞丐，给了他一些钱，积分-5'
            gold = -5
        elif ran == 1:
            result = '你在闲逛的时候，不小心掉进了下水道，积分-5，体力-5'
            gold = -5
            strength = -5
        elif ran == 2:
            result = '你在闲逛的时候，遇见了一个卖苹果的老婆婆，你买了一些苹果，发现是毒苹果，积分-1，体力-5'
            gold = -1
            strength = -5
        elif ran == 3:
            result = '你在闲逛的时候，遇见了一个歹徒正在欺负一个女孩，你立马飞奔而去打走歹徒，却发现原来他们是在拍戏，只好赔偿医疗费，积分-5'
            gold = -5

    elif probability < 980:  # 超级好
        ran = random.randrange(0, 2)

        if ran == 0:
            result = '你在收拾家里的东西的时候发现了祖先留下来的宝贝，积分+10'
            gold = 10
        elif ran == 1:
            result = '你的好朋友成了首富，请你大吃了一顿，体力+10'
            strength = 10

    elif probability < 1000:  # 超级坏
        ran = random.randrange(0, 2)

        if ran == 0:
            result = '你在闲逛的时候玩手机没看路，撞上了电线杆，体力值-10'
            strength = -10
        elif ran == 1:
            result = '你在闲逛的时候遇见了阿拉灯神丁，他说实现你三个愿望然后趁你不注意摸偷了你的钱包转身就跑，积分-10'
            gold = -10

    update(id, 2, gold, strength)  # 更新数据
    return result


# ============================================
# 管理操作

def editGold(id, gold):
    global user
    if user.__contains__(id):
        update(id, -1, gold, 0)
        return '积分修改成功'
    else:
        return '不存在该用户'


def editStrength(id, strength):
    global user
    if user.__contains__(id):
        user[id]['attribute']['strength'] = strength
        return '体力修改成功'
    else:
        return '不存在该用户'


def viewUser(id):
    global user
    if user.__contains__(id):
        return getMyData(id)
    else:
        return '不存在该用户'


def viewRate(id):
    global user
    if user.__contains__(id):
        return user[id]['name'] + getRate(id)
    else:
        return '不存在该用户'


def viewWarehouse(id):
    global user
    if user.__contains__(id):
        return user[id]['name'] + getWarehouse(id)[1:]
    else:
        return '不存在该用户'


def viewEquipment(id):
    global user
    if user.__contains__(id):
        return user[id]['name'] + getEquipment(id)[1:]
    else:
        return '不存在该用户'


def viewBuff(id):
    global user
    if user.__contains__(id):
        return user[id]['name'] + getBuff(id)[1:]
    else:
        return '不存在该用户'


def giveGoods(id, name, number):
    global user
    global goods
    if user.__contains__(id):
        if goods.__contains__(name):
            if getGooods(id, -1, name, number):
                return '给予成功！'
            else:
                return '给予失败！'
        else:
            return '不存在该物品'
    else:
        return '不存在该用户'


def giveAllGoods(name, number):
    global user
    global goods

    for key, value in user.items():
        getGooods(key, -1, name, number)
    return '已将该物品发放给每个人'


def giveAllGold(number):
    global user

    for key, value in user.items():
        update(key, -2, number, 0)
    return '已将积分发放给每个人'


def giveAllStrength(number):
    global user
    global goods

    for key, value in user.items():
        update(key, -2, 0, number)
    return '已将体力发放给每个人'


# BUFF启用
def viewGod():
    global systemData
    global user
    result = '无敌的人：' + str(systemData['god'])
    result += '\n临时无敌模式：'
    for key, value in systemData['tmpGod'].items():
        if user.__contains__(key):
            result += '\n\t' + str(key) + '/' + user[key]['name'] + '：' + str(value['number']) + '次'
        else:
            result += '\n\t' + str(key) + '：' + str(value['number']) + '次'
    return result


def closeGod(id):
    global systemData
    if id in systemData['god']:
        systemData['god'].remove(id)
    if systemData['tmpGod'].__contains__(id):
        del systemData['tmpGod'][id]
    return '关闭成功！'


def changeToGod(id):
    global systemData
    if id in systemData['god']:
        return '该用户已经是无敌模式了哦~'
    else:
        systemData['god'].append(id)
        return '开启无敌模式成功'


def changeToTmpGod(id, number):
    global systemData
    if systemData['tmpGod'].__contains__(id):
        systemData['tmpGod'][id]['number'] += number
    else:
        systemData['tmpGod'][id] = {}
        systemData['tmpGod'][id]['number'] = number
    if systemData['tmpGod'][id]['number'] <= 0:
        del systemData['tmpGod'][id]
    return '已经为其开启' + str(number) + '次无敌模式'


def changeToRampage1(id, number):
    global systemData
    if systemData['rampage-1'].__contains__(id):
        systemData['rampage-1'][id]['number'] += number
    else:
        systemData['rampage-1'][id] = {}
        systemData['rampage-1'][id]['number'] = number
    if systemData['rampage-1'][id]['number'] <= 0:
        del systemData['rampage-1'][id]
    return '已经为其开启' + str(number) + '次1级进攻'


def changeToRampage2(id, number):
    global systemData
    if systemData['rampage-2'].__contains__(id):
        systemData['rampage-2'][id]['number'] += number
    else:
        systemData['rampage-2'][id] = {}
        systemData['rampage-2'][id]['number'] = number
    if systemData['rampage-2'][id]['number'] <= 0:
        del systemData['rampage-2'][id]
    return '已经为其开启' + str(number) + '次2级进攻'


def changeToRampage3(id, number):
    global systemData
    if systemData['rampage-3'].__contains__(id):
        systemData['rampage-3'][id]['number'] += number
    else:
        systemData['rampage-3'][id] = {}
        systemData['rampage-3'][id]['number'] = number
    if systemData['rampage-3'][id]['number'] <= 0:
        del systemData['rampage-3'][id]
    return '已经为其开启' + str(number) + '次3级进攻'


def changeToRampage4(id, number):
    global systemData
    if systemData['rampage-4'].__contains__(id):
        systemData['rampage-4'][id]['number'] += number
    else:
        systemData['rampage-4'][id] = {}
        systemData['rampage-4'][id]['number'] = number
    if systemData['rampage-4'][id]['number'] <= 0:
        del systemData['rampage-4'][id]
    return '已经为其开启' + str(number) + '次4级进攻'


def changeToRampage5(id, number):
    global systemData
    if systemData['rampage-5'].__contains__(id):
        systemData['rampage-5'][id]['number'] += number
    else:
        systemData['rampage-5'][id] = {}
        systemData['rampage-5'][id]['number'] = number
    if systemData['rampage-5'][id]['number'] <= 0:
        del systemData['rampage-5'][id]
    return '已经为其开启' + str(number) + '次5级进攻'


def changeToDefense1(id, number):
    global systemData
    if systemData['defense-1'].__contains__(id):
        systemData['defense-1'][id]['number'] += number
    else:
        systemData['defense-1'][id] = {}
        systemData['defense-1'][id]['number'] = number
    if systemData['defense-1'][id]['number'] <= 0:
        del systemData['defense-1'][id]
    return '已经为其开启' + str(number) + '次1级防御'


def changeToDefense2(id, number):
    global systemData
    if systemData['defense-2'].__contains__(id):
        systemData['defense-2'][id]['number'] += number
    else:
        systemData['defense-2'][id] = {}
        systemData['defense-2'][id]['number'] = number
    if systemData['defense-2'][id]['number'] <= 0:
        del systemData['defense-2'][id]
    return '已经为其开启' + str(number) + '次2级防御'


def changeToDefense3(id, number):
    global systemData
    if systemData['defense-3'].__contains__(id):
        systemData['defense-3'][id]['number'] += number
    else:
        systemData['defense-3'][id] = {}
        systemData['defense-3'][id]['number'] = number
    if systemData['defense-3'][id]['number'] <= 0:
        del systemData['defense-3'][id]
    return '已经为其开启' + str(number) + '次3级防御'


def changeToDefense4(id, number):
    global systemData
    if systemData['defense-4'].__contains__(id):
        systemData['defense-4'][id]['number'] += number
    else:
        systemData['defense-4'][id] = {}
        systemData['defense-4'][id]['number'] = number
    if systemData['defense-4'][id]['number'] <= 0:
        del systemData['defense-4'][id]
    return '已经为其开启' + str(number) + '次4级防御'


def changeToDefense5(id, number):
    global systemData
    if systemData['defense-5'].__contains__(id):
        systemData['defense-5'][id]['number'] += number
    else:
        systemData['defense-5'][id] = {}
        systemData['defense-5'][id]['number'] = number
    if systemData['defense-5'][id]['number'] <= 0:
        del systemData['defense-3'][id]
    return '已经为其开启' + str(number) + '次5级防御'


def changeToNoLoss(id, number):
    global systemData
    if systemData['noLoss'].__contains__(id):
        systemData['noLoss'][id]['number'] += number
    else:
        systemData['noLoss'][id] = {}
        systemData['noLoss'][id]['number'] = number
    if systemData['noLoss'][id]['number'] <= 0:
        del systemData['noLoss'][id]
    return '已经为其开启' + str(number) + '次击剑不掉积分'


def changeToHalveGold(id, number):
    global systemData
    if systemData['halveGold'].__contains__(id):
        systemData['halveGold'][id]['number'] += number
    else:
        systemData['halveGold'][id] = {}
        systemData['halveGold'][id]['number'] = number
    if systemData['halveGold'][id]['number'] <= 0:
        del systemData['halveGold'][id]
    return '已经为其开启' + str(number) + '次积分收益减半'


def changeToDoubleGold(id, number):
    global systemData
    if systemData['doubleGold'].__contains__(id):
        systemData['doubleGold'][id]['number'] += number
    else:
        systemData['doubleGold'][id] = {}
        systemData['doubleGold'][id]['number'] = number
    if systemData['doubleGold'][id]['number'] <= 0:
        del systemData['doubleGold'][id]
    return '已经为其开启' + str(number) + '次双倍积分收益'


def changeToTripleGold(id, number):
    global systemData
    if systemData['tripleGold'].__contains__(id):
        systemData['tripleGold'][id]['number'] += number
    else:
        systemData['tripleGold'][id] = {}
        systemData['tripleGold'][id]['number'] = number
    if systemData['tripleGold'][id]['number'] <= 0:
        del systemData['tripleGold'][id]
    return '已经为其开启' + str(number) + '次三倍积分收益'


def changeToFixedGold(id, number, gold):
    global systemData

    systemData['fixedGold'][id] = {}
    systemData['fixedGold'][id]['number'] = number
    systemData['fixedGold'][id]['gold'] = gold
    if systemData['fixedGold'][id]['number'] <= 0:
        del systemData['fixedGold'][id]
    return '已经为其开启' + str(number) + '次固定增减积分收益'


# ============================================
# 强化操作

def strengthenAttack(id):
    if user[id]['attribute']['attack'] >= 25:
        return '你的进攻已经达到最高等级，暂时不能强化了'
    else:
        if user[id]['gold'] < 100:
            return '你的积分值小于100'
        times = user[id]['match']['win'] + user[id]['match']['lose']
        times_target = (user[id]['attribute']['attack'] - 4) * 50
        if times < times_target:
            return '你的场次不足' + str(times_target) + '不能强化'

        update(id, -2, -100, 0)
        user[id]['attribute']['attack'] += 1
        user[id]['attribute']['strengthen'] += 1

        return '强化成功！'


def strengthenDefense(id):
    if user[id]['attribute']['defense'] >= 20:
        return '你的防御已经达到最高等级，暂时不能强化了'
    else:
        if user[id]['gold'] < 100:
            return '你的积分值小于100'
        times = user[id]['match']['win'] + user[id]['match']['lose']
        times_target = user[id]['attribute']['defense'] * 50 + 50
        if times < times_target:
            return '你的场次不足' + str(times_target) + '不能强化'

        update(id, -2, -100, 0)
        user[id]['attribute']['defense'] += 1
        user[id]['attribute']['strengthen'] += 1
        return '强化成功！'
