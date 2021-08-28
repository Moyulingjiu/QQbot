import asyncio

# =============================================================
# 以下为附加功能头文件

import datetime
import time
# ==========================================================
from plugins import dataManage
from plugins import logManage
from plugins import getNow
from plugins import operator

config = {}
statistics = {}


def loadFile():
    global statistics
    global config
    statistics = dataManage.read_statistics()
    config = dataManage.read_config()

def timeSub(h1, m1, h2, m2):
    minute = (h2 - h1) * 60
    minute += m2 - m1
    return minute

# ============================================
# 定义全局信息
loop = asyncio.get_event_loop()

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



async def timeWatcher():
    global statistics
    while True:
        global config

        curr_time = datetime.datetime.now()

        # if curr_time.hour == 17 and curr_time.minute == 24:
        #     print('重置打卡数据')
        #     loadFile()
        #     for groupId in config['test_group']:
        #         await sendClockResetMessage(groupId)

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
