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
from plugins import operator

remainTimeHour = 23
remainTimeMinute = 0

clock = {}
config = {}
statistics = {}


def loadFile():
    global clock
    global config
    global statistics
    clock = dataManage.read_clock()
    config = dataManage.read_config()
    statistics = dataManage.read_statistics()

def saveFile():
    global clock
    dataManage.save_clock(clock)

def timeSub(h1, m1, h2, m2):
    minute = (h2 - h1) * 60
    minute += m2 - m1
    return minute

# ============================================
# 定义全局信息
loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",  # 填入 httpapi 服务运行的地址
        authKey="INITKEYvTyDBWZQ",  # 填入 authKey myBotXiaoQi
        account=1622057984,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

# ==========================================================
# 监听模块


async def sendMessage(groupId):
    global app
    global clock

    group = await app.getGroup(groupId)
    if group == None:
        del clock['dictClockPeople'][group]
        del clock['groupClock'][group]
        print('已删除群：' + str(groupId))
        return

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
    global config
    global statistics
    group = await app.getGroup(groupId)
    today = str(datetime.date.today())
    reply = '已经重置打卡日期到' + today

    logManage.log(getNow.toString(), '已重置打卡日期到：' + today)

    print('开始重置统计信息')
    statistics = dataManage.read_statistics()
    reply += '\n统计信息如下：'
    reply += '\n被踢出群数：' + str(statistics['kick'])
    reply += '\n退群数：' + str(statistics['quit'])
    reply += '\n禁言次数：' + str(statistics['mute'])
    reply += '\n解除禁言次数：' + str(statistics['unmute'])
    reply += '\n唤醒次数：' + str(statistics['awaken'])
    reply += '\n帮助文档获取次数：' + str(statistics['help'])
    reply += '\n基础功能调用次数：' + str(statistics['base_function'])
    reply += '\ntalk模块调用次数：' + str(statistics['talk'])
    reply += '\nclock_activity模块调用次数：' + str(statistics['clock_activity'])
    reply += '\nimage_search模块调用次数：' + str(statistics['image_search'])
    reply += '\ncommand模块调用次数：' + str(statistics['command'])
    reply += '\noperate模块调用次数：' + str(statistics['operate'])
    reply += '\ngame模块调用次数：' + str(statistics['game'])
    reply += '\n自动加一次数：' + str(statistics['auto_repeat'])
    reply += '\n自主回复次数：' + str(statistics['auto_reply'])
    reply += '\n部落冲突调用次数：' + str(statistics['clash'])
    reply += '\n新好友：' + str(statistics['new_friend'])
    reply += '\n新群：' + str(statistics['new_group'])

    statistics['kick'] = 0
    statistics['quit'] = 0
    statistics['mute'] = 0
    statistics['unmute'] = 0
    statistics['new_friend'] = 0
    statistics['new_group'] = 0

    statistics['awaken'] = 0
    statistics['help'] = 0
    statistics['base_function'] = 0
    statistics['talk'] = 0
    statistics['clock_activity'] = 0
    statistics['image_search'] = 0
    statistics['command'] = 0
    statistics['operate'] = 0
    statistics['game'] = 0
    statistics['auto_repeat'] = 0
    statistics['auto_reply'] = 0
    statistics['clash'] = 0
    dataManage.save_statistics(statistics)

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

    nullGroup = []

    for key, value in clock['dictClockPeople'].items():
        group = await app.getGroup(key)
        if group == None:
            nullGroup.append(group)
            continue
        
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
    
    for group in nullGroup:
        del clock['dictClockPeople'][group]
        del clock['groupClock'][group]

    saveFile()


async def timeWatcher():
    global statistics
    while True:
        global remainTimeHour
        global remainTimeMinute
        global clock
        global config
        global app

        curr_time = datetime.datetime.now()
        if curr_time.hour == remainTimeHour and curr_time.minute == remainTimeMinute:
            print('到达时间点！开始提醒各群。')
            loadFile()
            for groupId, value in clock['groupClock'].items():
                print('提醒：', groupId)
                groups = dataManage.read_group(groupId)
                if not groups['config']['mute']:
                    await sendMessage(groupId)

        elif curr_time.hour == 0 and curr_time.minute == 0:
            print('重置打卡数据')
            loadFile()
            await resetClock()
            for groupId in config['test_group']:
                await sendClockResetMessage(groupId)

        activityList = dataManage.load_obj('data/ClockActivity/activity')
        delActivityList = {}
        for key, activityDict in activityList.items():
            for activityName, value in activityDict.items():
                minute = timeSub(value['beginTime']['hour'], value['beginTime']['minute'], curr_time.hour, curr_time.minute)
                if minute >= value['lastMinute']:
                    reply = await operator.view_activity(key, activityName, app)
                    message = MessageChain.create([
                        At(value['admin']),
                        Plain(reply)
                    ])
                    groups = dataManage.read_group(key)
                    if not groups['config']['mute']:
                        group = await app.getGroup(key)
                        if group != None:
                            await app.sendGroupMessage(group, message)
                    delActivityList[key] = []
                    delActivityList[key].append(activityName)
        for key, activityName in delActivityList.items():
            for i in activityName:
                del activityList[key][i]
                if len(activityList[key]) == 0:
                    del activityList[key]
                print('删除活动：' + str(key) + '/' + i)
        dataManage.save_obj(activityList, 'data/ClockActivity/activity')

        print(curr_time.hour, '：', curr_time.minute, '：')
        statistics = dataManage.read_statistics()
        print('\t*上一分钟回复为：', statistics['last_minute'])
        statistics['last_minute'] = 0
        dataManage.save_statistics(statistics)
        print('\t*已将上一分钟回复其置为：0')
        time.sleep(60)


loadFile()
logManage.log(getNow.toString(), config['name'] + '的监听模块 启动！')

loop.run_until_complete(timeWatcher())
