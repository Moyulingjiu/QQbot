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
from plugins import dataManage

remainTimeHour = 21
remainTimeMinute = 00

clock = {}
botBaseInformation = {}

def loadFile():
    global clock
    global botBaseInformation
    clock = dataManage.load_obj('clockIn')
    botBaseInformation = dataManage.load_obj('baseInformation')

def saveFile():
    global clock
    dataManage.save_obj(clock, 'clockIn')

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
    global clock
    group = await app.getGroup(groupId)
    reply = '记得打卡呀~\n以下为未打卡名单：\n'
    message = MessageChain.create([
        Plain(reply)
    ])
    for key, value in clock['dictClockPeople'][groupId].items():
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
    global clock
    for key, value in clock['dictClockPeople'][groupId]:
        clock['dictClockPeople'][groupId][key] = False


def resetClock():
    global clock
    today = str(datetime.date.today())
    clock['clockDate'] = today

    for key, group in clock['dictClockPeople'].items():
        writeClockIn(key)
    saveFile()


async def timeWatcher():
    while True:
        global remainTimeHour
        global remainTimeMinute
        global clock
        global botBaseInformation
        curr_time = datetime.datetime.now()
        if curr_time.hour == remainTimeHour and curr_time.minute == remainTimeMinute:
            print('到达时间点！开始提醒各群。')
            loadFile()
            for groupId, value in clock['groupClock'].items():
                print('提醒：', groupId)
                await sendMessage(groupId)

        elif curr_time.hour == 0 and curr_time.minute == 0:
            print('重置打卡数据')
            resetClock()
            for groupId, value in botBaseInformation['testGroup'].items():
                await sendClockResetMessage(groupId)

        print(curr_time.hour, '：', curr_time.minute, '，监听中...')
        time.sleep(60)


loadFile()

loop.run_until_complete(timeWatcher())
