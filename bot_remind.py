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
from plugins import getNow

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
    if clock['groupClock'][groupId]['remind']:
        group = await app.getGroup(groupId)
        reply = '记得打卡呀~\n以下为未打卡名单：'
        message = MessageChain.create([
            Plain(reply)
        ])
        numUnClockIn = 0
        for key, value in clock['dictClockPeople'][groupId].items():
            if not value['clockIn']:
                message.plus(MessageChain.create([
                    Plain('\n'),
                    At(key)
                ]))
                numUnClockIn += 1
        if numUnClockIn == 0:
            message = MessageChain.create([
                Plain('所有人都完成了打卡，小柒深感欣慰~')
            ])
        await app.sendGroupMessage(group, message)

# 告诉管理员，已经重置打卡日期
async def sendClockResetMessage(groupId):
    global app
    group = await app.getGroup(groupId)
    today = str(datetime.date.today())
    reply = '已经重置打卡日期到' + today

    logManage.log(getNow.toString(), 0, '已重置打卡日期到：' + today)

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
        
        memberlist = await app.memberList(group.id)
        memberIdList = []
        for i in memberlist:
            memberIdList.append(i.id)
        print(memberIdList)


        reply = '以下为昨天未打卡名单：'
        message = MessageChain.create([
            Plain(reply)
        ])
        numUnClockIn = 0

        # 对于每个群进行提醒
        for key2, value2 in clock['dictClockPeople'][key].items():
            if key2 in memberIdList:
                if not clock['dictClockPeople'][key][key2]['clockIn']:
                    message.plus(MessageChain.create([
                        Plain('\n'),
                        At(key2)
                    ]))
                    clock['dictClockPeople'][key][key2]['consecutiveDays'] = 0 # 如果昨天没有打卡则重置打卡日期
                    numUnClockIn += 1
                else:
                    clock['dictClockPeople'][key][key2]['clockIn'] = False
            else:
                del clock['dictClockPeople'][key][key2] # 如果这个人已经退群，则删除
        if clock['groupClock'][key]['summary']:
            if numUnClockIn == 0:
                message = MessageChain.create([
                    Plain('昨天所有人都完成了打卡，超厉害！')
                ])
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
            for groupId in botBaseInformation['testGroup']:
                await sendClockResetMessage(groupId)

        print(curr_time.hour, '：', curr_time.minute, '：')
        botBaseInformation = dataManage.load_obj('baseInformation')
        print('\t*上一分钟回复为：', botBaseInformation['reply']['lastMinute'])
        botBaseInformation['reply']['lastMinute'] = 0
        dataManage.save_obj(botBaseInformation, 'baseInformation')
        print('\t*已将上一分钟回复其置为：0')
        time.sleep(60)


loadFile()
logManage.log(getNow.toString(), 0, botBaseInformation['baseInformation']['Bot_Name'] + '的监听模块 启动！')

loop.run_until_complete(timeWatcher())
