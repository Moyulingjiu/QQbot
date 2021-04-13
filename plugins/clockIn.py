import datetime

import plugins.dataManage as dataManage

# ==========================================================
# 打卡模块
clock = {}

def loadFile():
    global clock
    clock = dataManage.load_obj('clockIn')

def clockIn(groupId, memberId):
    loadFile()
    global clock
    print(memberId)
    if not clock['dictClockPeople'][groupId].__contains__(memberId):
        return '你不在打卡计划内哦~请输入\"加入打卡计划\"'

    today = str(datetime.date.today())

    if clock['clockDate'] != today:
        clock['clockDate'] = today
        print('打卡日期调整为：', today)
        reloadClockIn(today)

    if clock['dictClockPeople'][groupId][memberId]:
        reply = '，今天你已经打卡啦，没必要再打一次！'
    else:
        clock['dictClockPeople'][groupId][memberId] = True
        reply = '，打卡成功哦！请继续坚持！'
    writeClockIn()
    return reply


def addClockIn(groupId):
    loadFile()
    global clock
    if clock['dictClockPeople'].__contains__(groupId):
        return '本群已有打卡计划'
    clock['dictClockPeople'][groupId] = {}
    clock['groupClock'][groupId] = {
            'remind': True,
            'summary': True,
            'administrator': []
    }
    writeClockIn()
    return '已为本群开启打卡计划，各位可以输入\"加入打卡计划\"来加入打卡计划'


def stopClockIn(groupId):
    loadFile()
    global clock
    del clock['groupClock'][groupId]
    del clock['dictClockPeople'][groupId]
    writeClockIn()
    return '已为本群停止打卡计划'


def joinClockIn(groupId, memberId):
    loadFile()
    global clock
    if clock['dictClockPeople'][groupId].__contains__(memberId):
        return '你已在本群的打卡计划内哦~'
    clock['dictClockPeople'][groupId][memberId] = False
    writeClockIn()
    return '加入成功！'


def quitClockIn(groupId, memberId):
    loadFile()
    global clock
    del clock['dictClockPeople'][groupId][memberId]
    writeClockIn()
    return '退出成功'


def writeClockIn():
    global clock
    dataManage.save_obj(clock, 'clockIn')


def reloadClockIn(today):
    global clock
    clock['clockDate'] = today
    for key, value in clock['dictClockPeople'].items():
        for key2, value2 in clock['dictClockPeople'][key].items():
            clock['dictClockPeople'][key][key2] = False
    writeClockIn()


