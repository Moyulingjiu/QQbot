import asyncio
from pathlib import Path
# 所有事件监听都在entry中可以找到
from graia.application.entry import (
    GraiaMiraiApplication, Session,
    MessageChain, Group, Friend, Member, MemberInfo,
    Plain, Image, AtAll, At, Face, Source
)
from graia.application.entry import (
    BotMuteEvent, BotGroupPermissionChangeEvent
)
from graia.broadcast import Broadcast
# from graia.template import Template     # 模板功能
# from graia.component import Components  # 检索器

# =============================================================
# 以下为附加功能头文件

import os
from bs4 import BeautifulSoup  # 用来代替正则表达式取源码中相应标签的内容
import random
import requests  # 用来抓取网页的html源代码
import socket  # 用做异常处理
import time
import http.client  # 用做异常处理
import csv
import execjs
import numpy as np
from matplotlib import pyplot as plt
import uuid
import linecache
import datetime
import threading

# =============================================================
# 附加功能类
from plugins import talk
from plugins import weather
from plugins import smallFunction
from plugins import lucky
from plugins import command


# ==========================================================
# 基本信息
Bot_Name = '小柒'
Bot_Age = 14
Bot_Color = '天蓝色'
Bot_QQ = 1622057984
Master_QQ = 1597867839
version = '1.8'

groupClock = []
dictClockPeople = {
    0: [1]
}
clockDate = '2021-2-28'

administrator = []
contributors = []
blacklistGroup = []
blacklistMember = []
testGroup = []
cursePlanGroup = []
isInit = False

lastAutorepeat = ''
lastMessage = ''

fileTree = [
    'data/adminstrators.txt',
    'data/baseInfor.txt',
    'data/blacklistGroup.txt',
    'data/blacklistMember.txt',
    'data/contributors.txt',
    'data/cursePlanGroup.txt',
    'data/groupClock.txt',
    'data/testGroup.txt',
]


# ==========================================================
# 自我检查模块

def init():
    for path in fileTree:
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write('')
    

# ==========================================================
# 管理员模块


async def administratorOperation(strMessage, groupId, memberId, app, member):
    needReply = False
    needAt = False
    reply = ''

    if memberId in administrator:
        # 管理员权限
        if (strMessage == '重新加载配置文件') and (groupId in testGroup):
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('正在执行管理员操作，重新加载所有配置文件，' +
                      Bot_Name + '将会离开一会儿，请稍后...')
            ]))
            loadFile()
            reply = '重新加载完成\n'
            reply += '管理员：' + str(administrator) + '\n'
            reply += '贡献者计划名单：' + str(contributors) + '\n'
            reply += '黑名单（群）：' + str(blacklistGroup) + '\n'
            reply += '黑名单（人）：' + str(blacklistMember) + '\n'
            reply += '测试群名单：' + str(testGroup) + '\n\n'
            reply += '打卡计划群名单：' + str(groupClock) + '\n'
            reply += '打卡计划当前执行日期：' + clockDate + '\n\n'
            reply += '骂人计划群：：' + str(cursePlanGroup)
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain(reply)
            ]))
        elif strMessage[:6] == '添加管理员 ':
            reply = addContributors(int(strMessage[6:]))
            needReply = True
        elif strMessage == '命令大全':
            reply = command.allCommand()
            needReply = True
        elif strMessage[:5] == '删除文摘 ':
            reply = talk.delPoem(int(strMessage[5:]))
            needReply = True
        elif strMessage[:5] == '删除情话 ':
            reply = talk.delLoveTalk(int(strMessage[5:]))
            needReply = True
        elif strMessage[:5] == '删除脏话 ':
            reply = talk.delSwear(int(strMessage[5:]))
            needReply = True
        elif strMessage[:8] == '添加黑名单 群 ':
            reply = addBlacklistGroup(int(strMessage[8:]))
            needReply = True
        elif strMessage[:8] == '添加黑名单 人 ':
            reply = addBlacklistMember(int(strMessage[8:]))
            needReply = True
        elif strMessage[:8] == '移除黑名单 群 ':
            reply = removeBlacklistGroup(int(strMessage[8:]))
            needReply = True
        elif strMessage[:8] == '移除黑名单 人 ':
            reply = removeBlacklistMember(int(strMessage[8:]))
            needReply = True

    # 非管理员权限
    if (strMessage == '小柒报告状况'):
        reply = Bot_Name + '运行良好'
        needReply = True
    elif strMessage == '添加打卡计划' and groupId != 0:
        reply = addClockIn(groupId)
        needAt = True
        needReply = True
    elif strMessage[:4] == '添加文摘':
        poemlist = strMessage.split(' ')
        del poemlist[0]
        reply = talk.addPoem(poemlist)
        needReply = True
    elif strMessage[:4] == '添加情话':
        loveTalklist = strMessage.split(' ')
        del loveTalklist[0]
        reply = talk.addLoveTalk(loveTalklist)
        needReply = True
    elif strMessage[:4] == '添加脏话':
        swearlist = strMessage.split(' ')
        del swearlist[0]
        reply = talk.addSwear(swearlist)
        needReply = True
    elif strMessage == '管理员帮助':
        reply = command.helpAdministrators()
        needReply = True
    elif strMessage == '打卡提醒' and (groupId in groupClock):
        reply = await sendMessage(groupId)
        needReply = False
    elif strMessage == '文摘条数':
        reply = talk.numPoem()
        needReply = True
    elif strMessage == '情话条数':
        reply = talk.numLoveTalk()
        needReply = True
    elif strMessage == '脏话条数':
        reply = talk.numSwear()
        needReply = True
    elif strMessage[:5] == '打卡情况 ':
        loadFile()
        global dictClockPeople
        tmp = int(strMessage[5:])
        if tmp in groupClock:
            reply = '未打卡名单：\n'
            for key, value in dictClockPeople[tmp].items():
                if not value:
                    reply += str(key) + '\n'
        else:
            reply = '该群没有打卡计划哦！'
        needReply = True
    elif strMessage == '版本信息':
        global version
        reply = '当前版本为：' + version
        needReply = True
    
    elif strMessage[:7] == '加入打卡计划 ':
        pass
    elif strMessage[:7] == '退出打卡计划 ':
        pass
    elif strMessage[:7] == '锁定打卡计划':
        pass
    elif strMessage[:7] == '解锁打卡计划':
        pass


    return (needReply, needAt, reply)


def addContributors(memberId):
    global contributors
    if memberId != 0:
        if memberId in contributors:
            reply = '该成员已经在贡献者计划中了哦~'
        else:
            contributors.append(memberId)
            with open('data/contributors.txt', 'a', encoding='utf-8') as f:
                f.write(str(memberId) + '\n')
            reply = '添加成功~'
    else:
        reply = '诶？这个QQ正确吗？'
    return reply

# ==========================================================
# 文件操作


def loadFile():
    global isInit
    isInit = True
    with open('data/administrators.txt', 'r+', encoding='utf-8') as f:
        global administrator
        administrator.clear()
        tmpList = f.readlines()
        for i in tmpList:
            if len(i.strip()) != 0:
                administrator.append(int(i))
        print('添加管理员', administrator)

    with open('data/contributors.txt', 'r+', encoding='utf-8') as f:
        global contributors
        contributors.clear()
        tmpList = f.readlines()
        for i in tmpList:
            if len(i.strip()) != 0:
                contributors.append(int(i))
        print('添加贡献者', contributors)

    with open('data/groupClock.txt', 'r+', encoding='utf-8') as f:
        global groupClock
        groupClock.clear()
        tmpList = f.readlines()
        for i in tmpList:
            if len(i.strip()) != 0:
                groupClock.append(int(i))
        print('添加打卡群', groupClock)

    with open('data/testGroup.txt', 'r+', encoding='utf-8') as f:
        global testGroup
        testGroup.clear()
        tmpList = f.readlines()
        for i in tmpList:
            if len(i.strip()) != 0:
                testGroup.append(int(i))
        print('添加测试群', testGroup)

    with open('data/cursePlanGroup.txt', 'r+', encoding='utf-8') as f:
        global cursePlanGroup
        cursePlanGroup.clear()
        tmpList = f.readlines()
        for i in tmpList:
            if len(i.strip()) != 0:
                cursePlanGroup.append(int(i))
        print('添加骂人计划群', cursePlanGroup)

    with open('data/blacklistGroup.txt', 'r+', encoding='utf-8') as f:
        global blacklistGroup
        blacklistGroup.clear()
        tmpList = f.readlines()
        for i in tmpList:
            if len(i.strip()) != 0:
                blacklistGroup.append(int(i))
        print('添加黑名单群', blacklistGroup)

    with open('data/blacklistMember.txt', 'r+', encoding='utf-8') as f:
        global blacklistMember
        blacklistMember.clear()
        tmpList = f.readlines()
        for i in tmpList:
            if len(i.strip()) != 0:
                blacklistMember.append(int(i))
        print('添加黑名单人', blacklistMember)

    with open('data/clockInData/clockDate.txt', 'r+', encoding='utf-8') as f:
        global clockDate
        clockDate = f.readline()
        print('获取打卡日期', clockDate)

    global dictClockPeople
    dictClockPeople.clear()
    for groupNumber in groupClock:
        with open('data/clockInData/' + str(groupNumber) + '.txt', 'r+', encoding='utf-8') as f:
            dictClockPeople[groupNumber] = {}
            clockMember = f.readlines()
            for line in clockMember:
                if len(line.strip()) != 0:
                    lines = line.split(' ')
                    if lines[1][0] == 'T':
                        dictClockPeople[groupNumber][int(lines[0])] = True
                    else:
                        dictClockPeople[groupNumber][int(lines[0])] = False
    print('获取打卡人', dictClockPeople)

    isInit = False


def addBlacklistGroup(groupId):
    global blacklistGroup
    if groupId in blacklistGroup:
        return '该群已经在黑名单里了'
    if groupId in testGroup:
        return '该群为测试群聊，不能添加黑名单，请先将其移除测试群聊'

    blacklistGroup.append(groupId)
    with open('data/blacklistGroup.txt', 'a', encoding='utf-8') as f:
        f.write(str(groupId) + '\n')
    return '已经将群' + str(groupId) + '加入黑名单'


def addBlacklistMember(memberId):
    global blacklistMember
    if memberId in blacklistMember:
        return '该人已经在黑名单里了'
    if memberId in administrator:
        return '对方是管理员，不能加入黑名单'

    blacklistMember.append(memberId)
    with open('data/blacklistMember.txt', 'a', encoding='utf-8') as f:
        f.write(str(memberId) + '\n')
    return '已经将人' + str(memberId) + '加入黑名单'


def removeBlacklistGroup(groupId):
    global blacklistGroup
    if not groupId in blacklistGroup:
        return '该群不在黑名单里'
    del blacklistGroup[blacklistGroup.index(groupId)]
    with open('data/blacklistGroup.txt', 'w', encoding='utf-8') as f:
        for i in blacklistGroup:
            f.write(str(i) + '\n')
    return '已经将群' + str(groupId) + '移除黑名单'


def removeBlacklistMember(memberId):
    global blacklistMember
    if not memberId in blacklistMember:
        return '该人不在黑名单里'
    del blacklistMember[blacklistMember.index(memberId)]
    with open('data/blacklistMember.txt', 'w', encoding='utf-8') as f:
        for i in blacklistMember:
            f.write(str(i) + '\n')
    return '已经将人' + str(memberId) + '移除黑名单'

# ==========================================================
# 打卡模块


def clockIn(groupId, memberId):
    global dictClockPeople
    if not dictClockPeople[groupId].__contains__(memberId):
        return '你不在打卡计划内哦~请输入\"加入打卡计划\"'

    today = str(datetime.date.today())

    global clockDate
    if clockDate != today:
        clockDate = today
        print('打卡日期调整为：', today)
        reloadClockIn(today)

    if dictClockPeople[groupId][memberId]:
        reply = '，今天你已经打卡啦，没必要再打一次！'
    else:
        dictClockPeople[groupId][memberId] = True
        reply = '，打卡成功哦！请继续坚持！'
    writeClockIn(groupId)
    return reply


def addClockIn(groupId):
    global dictClockPeople
    if dictClockPeople.__contains__(groupId):
        return '本群已有打卡计划'
    with open('data/groupClock.txt', 'a+', encoding='utf-8') as f:
        f.write(str(groupId) + '\n')
        dictClockPeople[groupId] = {}
    with open('data/clockInData/' + str(groupId) + '.txt', 'w', encoding='utf-8') as f:
        f.write('')
    loadFile()
    return '已为本群开启打卡计划，各位可以输入\"加入打卡计划\"来加入打卡计划'


def stopClockIn(groupId):
    global dictClockPeople
    del groupClock[groupClock.index(groupId)]
    with open('data/groupClock.txt', 'w', encoding='utf-8') as f:
        for i in groupClock:
            f.write(str(i) + '\n')
    loadFile()
    return '已为本群停止打卡计划'


def joinClockIn(groupId, memberId):
    global dictClockPeople
    if dictClockPeople[groupId].__contains__(memberId):
        return '你已在本群的打卡计划内哦~'
    with open('data/clockInData/' + str(groupId) + '.txt', 'a+', encoding='utf-8') as f:
        f.write(str(memberId) + ' F\n')
        dictClockPeople[groupId][memberId] = False
        return '加入成功！'


def quitClockIn(groupId, memberId):
    global dictClockPeople
    del dictClockPeople[groupId][memberId]
    writeClockIn(groupId)
    return '退出成功'


def writeClockIn(groupId):
    global dictClockPeople
    with open('data/clockInData/' + str(groupId) + '.txt', 'w', encoding='utf-8') as f:
        for key, value in dictClockPeople[groupId].items():
            text = 'F'
            if value:
                text = 'T'
            f.write(str(key) + ' ' + text + '\n')


def reloadClockIn(today):
    global dictClockPeople
    with open('data/clockInData/clockDate.txt', 'w', encoding='utf-8') as f:
        f.write(today)

    for key, group in dictClockPeople.items():
        for key2, value in group.items():
            dictClockPeople[key][key2] = False
        writeClockIn(key)

    dictClockPeople.clear()
    for groupNumber in groupClock:
        with open('data/clockInData/' + str(groupNumber) + '.txt', 'r+', encoding='utf-8') as f:
            dictClockPeople[groupNumber] = {}
            clockMember = f.readlines()
            for line in clockMember:
                if len(line.strip()) != 0:
                    lines = line.split(' ')
                    if lines[1][0] == 'T':
                        dictClockPeople[groupNumber][int(lines[0])] = True
                    else:
                        dictClockPeople[groupNumber][int(lines[0])] = False


# ============================================
# 定义全局信息
loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",  # 填入 httpapi 服务运行的地址
        authKey="INITKEYvTyDBWZQ",  # 填入 authKey
        account=399608601,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

# ==========================================================
# 监听模块


async def sendMessage(groupId):
    global app
    group = await app.getGroup(groupId)

    if groupId in groupClock:
        reply = '记得打卡呀：\n'
        message = MessageChain.create([
            Plain(reply)
        ])
        for key, value in dictClockPeople[groupId].items():
            if not value:
                message.plus(MessageChain.create([
                    At(key),
                    Plain('\n')
                ]))

        await app.sendGroupMessage(group, message)
        return True
    return False

# 好友消息


@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend, source: Source):

    getMessage = await app.messageFromId(source)
    strMessage = getMessage.messageChain.asDisplay()

    needReply = False
    needAt = False
    reply = ''
    blacklist = (friend.id in blacklistMember)

    if not blacklist:
        if strMessage[0] == '*':
            reply = function(strMessage[1:])
            needReply = True
        else:
            if strMessage[:3] == '天气 ':
                reply = weather.getWeather(strMessage[3:])
                needReply = True
            elif strMessage == '色子' or strMessage == '骰子':
                reply = smallFunction.dick()
                needReply = True
            elif strMessage == '抛硬币':
                reply = smallFunction.coin()
                needReply = True
            elif strMessage == '文摘':
                reply = talk.poem()
                needReply = True
            elif strMessage == '情话':
                reply = talk.loveTalk()
                needReply = True
            elif strMessage == '你好':
                reply = '你好呀，' + friend.nickname + "。小柒很高兴遇见你！"
                needReply = True
            elif strMessage == '晚安':
                reply = '晚安呀！' + friend.nickname
                needReply = True
            elif strMessage == '早安':
                reply = '早哦，' + friend.nickname
                needReply = True
        if not needReply:
            if friend.id in contributors or friend.id in administrator:
                (needReply, needAt, reply) = await administratorOperation(strMessage, 0, friend.id, app, friend)

    if needReply:
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(reply)
        ]))

# 群聊消息


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, member: Member, source: Source):
    getMessage = await app.messageFromId(source)
    strMessage = getMessage.messageChain.asDisplay()
    print(strMessage)

    global isInit

    beAt = False
    needReply = False
    needAt = False
    reply = ''

    groupId = member.group.id
    memberId = member.id
    blacklist = (groupId in blacklistGroup) or (memberId in blacklistMember)

    if not blacklist:
        # +1部分
        global lastMessage
        global lastAutorepeat
        if lastMessage == strMessage and lastAutorepeat != strMessage and strMessage[0] != '[' and strMessage[:-1] != ']':
            reply = strMessage
            lastAutorepeat = strMessage
            needReply = True
        lastMessage = strMessage

        # 打卡计划
        if groupId in groupClock:
            isInit = True  # 涉及到文本操作，皆需要暂时终止相应
            if strMessage == '打卡':
                reply = member.name + clockIn(groupId, memberId)
                #needAt = True
                needReply = True
            elif strMessage == '加入打卡计划':
                reply = member.name + joinClockIn(groupId, memberId)
                # needAt = True
                needReply = True
            elif strMessage == '退出打卡计划':
                reply = member.name + quitClockIn(groupId, memberId)
                # needAt = True
                needReply = True
            elif strMessage == '终止打卡计划' and (memberId in administrator or memberId in contributors):
                reply = member.name + stopClockIn(groupId)
                # needAt = True
                needReply = True
            isInit = False
        # 正常回复部分
        if not needReply:
            if strMessage.find('@' + str(Bot_QQ)) != -1:
                beAt = True
                AtMessage = strMessage[len(str(Bot_QQ)) + 2:]
                if AtMessage == '你好':
                    reply = '你好呀，' + member.name + '。小柒很高兴遇见你！'
                    needAt = True
                    needReply = True
                elif AtMessage == '抱抱':
                    replylist = ['抱抱呀！', Bot_Name +
                                '才不要和你抱抱！', '抱抱', '抱抱' + member.name]
                    reply = replylist[random.randrange(0, len(replylist))]
                    needReply = True
                elif AtMessage == '贴贴':
                    replylist = ['贴贴', '快来贴贴，嘿嘿！', '不贴不贴']
                    reply = replylist[random.randrange(0, len(replylist))]
                    needReply = True
                elif AtMessage == '晚安':
                    replylist = ['晚安', '晚安哦' + member.name,
                                '记得要梦见' + Bot_Name, '快睡吧']
                    reply = replylist[random.randrange(0, len(replylist))]
                    needReply = True
                elif AtMessage == '谢谢':
                    replylist = ['嘿嘿', '不用谢啦', '要时刻想着' + Bot_Name, '没事啦']
                    reply = replylist[random.randrange(0, len(replylist))]
                elif AtMessage == '快来' or AtMessage == '快来快来':
                    replylist = ['游戏启动', '来了来了', '不要着急嘛']
                    reply = replylist[random.randrange(0, len(replylist))]
                    needReply = True
                elif AtMessage == '傻子':
                    reply = '你才是傻子，' + Bot_Name + '才不傻'
                    needReply = True
                elif AtMessage == '笨蛋':
                    reply = Bot_Name + '才不要理你了'
                    needReply = True
                elif AtMessage == '蠢货':
                    reply = '哼'
                    needReply = True
                elif AtMessage == '你是猪吗' or AtMessage == '猪':
                    reply = '你以为谁都像你一天天哼唧哼唧的'
                    needReply = True
                else:
                    reply = '诶，叫我干嘛'
                    needReply = True
            else:
                if strMessage[0] == '*':
                    reply = command.function(strMessage[1:])
                    needReply = True
                else:
                    if strMessage[:3] == '天气 ':
                        reply = weather.getWeather(strMessage[3:])
                        needAt = False
                        needReply = True
                    elif strMessage == '色子' or strMessage == '骰子':
                        reply = smallFunction.dick()
                        needAt = True
                        needReply = True
                    elif strMessage == '抛硬币':
                        reply = smallFunction.coin()
                        needAt = True
                        needReply = True
                    elif strMessage == '文摘':
                        reply = talk.poem()
                        needReply = True
                    elif strMessage == '情话':
                        reply = talk.loveTalk()
                        needReply = True
                    elif strMessage == '骂我一句' and groupId in cursePlanGroup:
                        reply = talk.swear()
                        needReply = True
                    elif strMessage == '运势':
                        reply = lucky.luck(memberId)
                        needAt = True
                        needReply = True
                    elif strMessage == '打卡帮助':
                        reply = command.helpClock()
                        needReply = True
                    elif strMessage == '小柒测运气':
                        reply = 'jrrp'
                        needReply = True

                    # ==========================================
                    # 之下为管理员模块
                    elif memberId in contributors or memberId in administrator:
                        (needReply, needAt, reply) = await administratorOperation(strMessage, groupId, memberId, app, member)

        # ==========================================
        # 此处为整活
        if not needReply:
            if strMessage == 'yjy爬':
                reply = 'yjy快爬'
                needReply = True
            elif strMessage == '我是fw':
                reply = '在' + Bot_Name + '心中，' + member.name + '一直都很厉害的哦~'
                needReply = True
            elif strMessage == '好家伙':
                tmpNumber = random.randrange(0, 5)
                if tmpNumber == 3:
                    reply = '又发生什么辣？'
                    needReply = True
            elif strMessage == '你们早上都没课的嘛':
                reply = Bot_Name + '还没有开始上课呢'
                needReply = True
            elif strMessage == '摸了':
                reply = member.name + '桑怎么可以摸鱼呢'
                needReply = True
            elif strMessage == '也不是不行':
                reply = member.name + '那就快冲！'
                needReply = True
            elif strMessage[-3:] == '多好啊':
                reply = '是呀是呀'
                needReply = True
            elif strMessage == '上课':
                reply = Bot_Name + '陪你一起上课'
                needReply = True
            elif strMessage == '满课':
                reply = '好惨哦'
                needReply = True
            elif strMessage == '谢谢':
                reply = '嘿嘿'
                needReply = True
            elif strMessage == '有人ow吗':
                reply = Bot_Name + '也想来'
                needReply = True
            elif strMessage[-2:] == '快来':
                reply = Bot_Name + '来了来了'
                needReply = True
            elif strMessage == '晚安':
                reply = '晚安呀！' + member.name
                needReply = True
            elif strMessage == '早安':
                reply = '早哦，' + member.name
                needReply = True
            elif strMessage == '来一张涩图':
                reply = '能不能多读书，少看涩图'
                needReply = True
            elif strMessage == '？':
                tmpNumber = random.randrange(0, 5)
                if tmpNumber == 2:
                    reply = '怎么啦'
                    needReply = True

    if needReply:
        lastMessage = reply
        if needAt:
            await app.sendGroupMessage(member.group, MessageChain.create([
                At(member.id),
                Plain(reply)
            ]))
        else:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain(reply)
            ]))



init()
loadFile()

# loop.run_until_complete(timeWatcher())
app.launch_blocking()
