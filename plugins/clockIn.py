import datetime

import plugins.dataManage as dataManage
import plugins.getNow as getNow

# ==========================================================
# 打卡模块
clock = {}

def loadFile():
    global clock
    clock = dataManage.load_obj('clockIn')

# 打卡
def clockIn(groupId, memberId):
    loadFile()
    global clock
    print(memberId)
    if not clock['dictClockPeople'][groupId].__contains__(memberId):
        return '你不在打卡计划内哦~请输入\"加入打卡计划\"'

    hour = getNow.getHour()
    minute = getNow.getMinute()
    if hour == 0 and (minute >= 0 and minute <= 5):
        return '每天00:00——00:05更新系统数据，不能打卡！'

    today = str(datetime.date.today())

    if clock['clockDate'] != today:
        clock['clockDate'] = today
        print('打卡日期调整为：', today)
        reloadClockIn(today)

    if clock['dictClockPeople'][groupId][memberId]['clockIn']:
        reply = '，今天你已经打卡啦，没必要再打一次！'
    else:
        clock['dictClockPeople'][groupId][memberId]['clockIn'] = True
        clock['dictClockPeople'][groupId][memberId]['consecutiveDays'] += 1
        reply = '，打卡成功哦！已经连续打卡 ' + str(clock['dictClockPeople'][groupId][memberId]['consecutiveDays']) + ' 天请继续坚持！'
    writeClockIn()
    return reply

# 添加打卡计划
def addClockIn(groupId):
    loadFile()
    global clock
    if clock['dictClockPeople'].__contains__(groupId):
        return '本群已有打卡计划'
    clock['dictClockPeople'][groupId] = {}
    clock['groupClock'][groupId] = {
            'remind': True,
            'summary': True,
            'exitPermission': False,
            'enterPermission': False,
            'administratorRemind': False,
            'administrator': []
    }
    writeClockIn()
    return '已为本群开启打卡计划，各位可以输入\"加入打卡计划\"来加入打卡计划'

# 终止打卡计划
def stopClockIn(groupId):
    loadFile()
    global clock
    del clock['groupClock'][groupId]
    del clock['dictClockPeople'][groupId]
    writeClockIn()
    return '已为本群停止打卡计划'

# 加入打卡计划
def joinClockIn(groupId, memberId):
    loadFile()
    global clock
    if clock['dictClockPeople'][groupId].__contains__(memberId):
        return ',你已在本群的打卡计划内哦~'
        
    if not clock['groupClock'][groupId]['enterPermission']:
        clock['dictClockPeople'][groupId][memberId] = {
            'clockIn': False,
            'consecutiveDays': 0
        }
        writeClockIn()
        return '加入成功！'
    else:
        return ',本群打卡计划已被锁定，不能加入'

# 退出打卡计划
def quitClockIn(groupId, memberId):
    loadFile()
    global clock
    # 既没有被锁定，也没有禁止退出
    if not clock['groupClock'][groupId]['exitPermission']:
        del clock['dictClockPeople'][groupId][memberId]
        writeClockIn()
        return '退出成功'
    else:
        return ',本群打卡计划已被锁定，不能退出'


def writeClockIn():
    global clock
    dataManage.save_obj(clock, 'clockIn')


def reloadClockIn(today):
    global clock
    clock['clockDate'] = today
    for key, value in clock['dictClockPeople'].items():
        for key2, value2 in clock['dictClockPeople'][key].items():
            clock['dictClockPeople'][key][key2]['clockIn'] = False
    writeClockIn()


# 锁定打卡计划
def lockClockIn(groupId): # 已经确保groupId在打卡计划内，这句话才能响应
    loadFile()
    global clock

    if clock['groupClock'][groupId]['enterPermission'] and clock['groupClock'][groupId]['exitPermission']:
        return '打卡计划现在已经是锁定状态~'
    clock['groupClock'][groupId]['enterPermission'] = True
    clock['groupClock'][groupId]['exitPermission'] = True
    writeClockIn()
    return '管理员已锁定本群打卡计划，现在不允许退出与加入'

# 解锁打卡计划
def unlockClockIn(groupId):
    loadFile()
    global clock

    if not (clock['groupClock'][groupId]['enterPermission'] or clock['groupClock'][groupId]['exitPermission']):
        return '本群打卡计划本来就没有锁定啦~'

    clock['groupClock'][groupId]['enterPermission'] = False
    clock['groupClock'][groupId]['exitPermission'] = False
    writeClockIn()
    return '管理员已解锁本群打卡计划，现在允许退出与加入'

# 锁定打卡计划 进入
def lockClockInEnter(groupId): # 已经确保groupId在打卡计划内，这句话才能响应
    loadFile()
    global clock

    if clock['groupClock'][groupId]['enterPermission']:
        return '打卡计划现在已经是锁定加入状态~'
    clock['groupClock'][groupId]['enterPermission'] = True
    writeClockIn()
    return '管理员已锁定本群打卡计划，现在不允许加入'

# 解锁打卡计划 进入
def unlockClockInEnter(groupId):
    loadFile()
    global clock

    if not clock['groupClock'][groupId]['enterPermission']:
        return '本群打卡计划本来就没有锁定加入啦~'
    clock['groupClock'][groupId]['enterPermission'] = False
    writeClockIn()
    return '管理员已解锁本群打卡计划，现在允许加入'

# 锁定打卡计划 退出
def lockClockInExit(groupId): # 已经确保groupId在打卡计划内，这句话才能响应
    loadFile()
    global clock

    if clock['groupClock'][groupId]['exitPermission']:
        return '打卡计划现在已经是锁定退出状态~'
    clock['groupClock'][groupId]['exitPermission'] = True
    writeClockIn()
    return '管理员已锁定本群打卡计划，现在不允许退出'

# 解锁打卡计划 退出
def unlockClockInExit(groupId):
    loadFile()
    global clock


    if not clock['groupClock'][groupId]['exitPermission']:
        return '本群打卡计划本来就没有锁定退出啦~'
    clock['groupClock'][groupId]['exitPermission'] = False
    writeClockIn()
    return '管理员已解锁本群打卡计划，现在允许退出'

# 开启打卡计划提醒
def onRemind(groupId):
    loadFile()
    global clock

    if clock['groupClock'][groupId]['remind']:
        return '本群打卡计划本来就要提醒哦~'
    clock['groupClock'][groupId]['remind'] = True
    writeClockIn()
    return '管理员已开启本群打卡计划提醒，每天23点将会提醒未打卡的人打卡'

# 关闭打卡计划提醒
def offRemind(groupId):
    loadFile()
    global clock

    if not clock['groupClock'][groupId]['remind']:
        return '本群打卡计划本来就没有提醒哦~'
    clock['groupClock'][groupId]['remind'] = False
    writeClockIn()
    return '管理员已关闭本群打卡计划提醒，现在不会再有提醒了'

# 开启打卡计划总结
def onSummary(groupId):
    loadFile()
    global clock

    if clock['groupClock'][groupId]['summary']:
        return '本群打卡计划本来就要每日总结哦~'
    clock['groupClock'][groupId]['summary'] = True
    writeClockIn()
    return '管理员已开启本群打卡计划总结，新的一天将会总结昨日有哪些人没有打卡'

# 关闭打卡计划总结
def offSummary(groupId):
    loadFile()
    global clock

    if not clock['groupClock'][groupId]['summary']:
        return '本群打卡计划本来就没有每日总结哦~'
    clock['groupClock'][groupId]['summary'] = False
    writeClockIn()
    return '管理员已关闭本群打卡计划总结，新的一天将不会总结昨日有哪些人没有打卡'