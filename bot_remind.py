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
# ==========================================================
# 基本信息
Bot_Name = '小柒'
Bot_Age = 14
Bot_Color = '天蓝色'
Bot_QQ = 1622057984
Master_QQ = 1597867839

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

remainTimeHour = 23
remainTimeMinute = 00


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
    reply = '记得打卡呀~\n以下为未打卡名单：\n'
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


async def sendClockResetMessage(groupId):
    global app
    group = await app.getGroup(groupId)
    reply = '已经重置打卡日期'
    message = MessageChain.create([
        Plain(reply)
    ])
    await app.sendGroupMessage(group, message)
    return True


def writeClockIn(groupId):
    global dictClockPeople
    with open('data/clockInData/' + str(groupId) + '.txt', 'w', encoding='utf-8') as f:
        for key, value in dictClockPeople[groupId].items():
            text = 'F'
            if value:
                text = 'T'
            f.write(str(key) + ' ' + text + '\n')


def resetClock():
    global dictClockPeople
    today = str(datetime.date.today())
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


async def timeWatcher():
    while True:
        global remainTimeHour
        global remainTimeMinute
        curr_time = datetime.datetime.now()
        if curr_time.hour == remainTimeHour and curr_time.minute == remainTimeMinute:
            print('到达时间点！开始提醒各群。')
            loadFile()
            for groupId in groupClock:
                print('提醒：', groupId)
                await sendMessage(groupId)

        elif curr_time.hour == 0 and curr_time.minute == 0:
            print('重置打卡数据')
            resetClock()
            for groupId in testGroup:
                await sendClockResetMessage(groupId)

        print(curr_time.hour, '：', curr_time.minute, '，监听中...')
        time.sleep(60)


loadFile()

loop.run_until_complete(timeWatcher())
