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

import datetime
import time
# ==========================================================
from plugins import dataManage
from plugins import logManage

remainTimeHour = 23
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
    reply = '记得打卡呀~\n以下为未打卡名单：'
    message = MessageChain.create([
        Plain(reply)
    ])
    for key, value in clock['dictClockPeople'][groupId].items():
        if not value:
            message.plus(MessageChain.create([
                Plain('\n'),
                At(key)
            ]))

    await app.sendGroupMessage(group, message)
    return True

# 告诉管理员，已经重置打卡日期
async def sendClockResetMessage(groupId):
    global app
    group = await app.getGroup(groupId)
    today = str(datetime.date.today())
    reply = '已经重置打卡日期到' + today
    logManage.log(today + ' 00:00\t已重置打卡日期')
    message = MessageChain.create([
        Plain(reply)
    ])
    await app.sendGroupMessage(group, message)
    return True

# 重置打卡数据
async def resetClock():
    global clock
    today = str(datetime.date.today())
    clock['clockDate'] = today

    for key, value in clock['dictClockPeople'].items():
        group = await app.getGroup(key)
        reply = '以下为昨天未打卡名单：'
        message = MessageChain.create([
            Plain(reply)
        ])

        for key2, value2 in clock['dictClockPeople'][key]:
            if not clock['dictClockPeople'][key][key2]:
                message.plus(MessageChain.create([
                    Plain('\n'),
                    At(key2)
                ]))
            clock['dictClockPeople'][key][key2] = False
        await app.sendGroupMessage(group, message)
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
            loadFile()
            await resetClock()
            for groupId, value in botBaseInformation['testGroup'].items():
                await sendClockResetMessage(groupId)

        print(curr_time.hour, '：', curr_time.minute, '，监听中...')
        time.sleep(60)


loadFile()

loop.run_until_complete(timeWatcher())
