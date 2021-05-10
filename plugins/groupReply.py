
import random
import asyncio # 异步

# 群消息回复
from plugins import talk
from plugins import weather
from plugins import smallFunction
from plugins import lucky
from plugins import command
from plugins import weiboHot
from plugins import clockIn
from plugins import operator
from plugins import dataManage
from plugins import autoReply
from plugins import baidu
from plugins import logManage
from plugins import getNow
from plugins import keyReply
from plugins import vocabulary

lastAutorepeat = '' # 上一次加一的消息
lastMessage = ''    # 上一条消息

# 这里的messages是一个列表，因为发送的可能是多行信息，需要进行一定的处理
async def reply(botBaseInformation, messages, app, member):
    Bot_QQ = botBaseInformation['baseInformation']['Bot_QQ']
    Bot_Name = botBaseInformation['baseInformation']['Bot_Name']
    clock = dataManage.load_obj('clockIn')

    beAt = False
    needReply = False
    needAt = False
    AtId = 0
    reply = ''

    groupId = member.group.id
    memberId = member.id
    blacklist = (groupId in botBaseInformation['blacklistGroup']) or (memberId in botBaseInformation['blacklistMember'])
    isAdministrator = (memberId in botBaseInformation['administrator']) or (memberId in botBaseInformation['contributors']) or (memberId == botBaseInformation['baseInformation']['Master_QQ'])

    if (not blacklist) and (len(messages) != 0):

        # 打卡计划
        if clock['groupClock'].__contains__(groupId):
            if messages == '打卡':
                reply = member.name + clockIn.clockIn(groupId, memberId)
                needReply = True
            elif messages == '加入打卡计划':
                reply = member.name + clockIn.joinClockIn(groupId, memberId)
                needReply = True
            elif messages == '退出打卡计划':
                reply = member.name + clockIn.quitClockIn(groupId, memberId)
                needReply = True
            elif messages == '终止打卡计划' and isAdministrator:
                reply = member.name + clockIn.stopClockIn(groupId)
                needReply = True

            elif messages == '锁定打卡计划' and isAdministrator:
                reply = clockIn.lockClockIn(groupId)
                needReply = True
            elif messages == '解锁打卡计划' and isAdministrator:
                reply = clockIn.unlockClockIn(groupId)
                needReply = True
            elif messages == '锁定打卡计划 加入' and isAdministrator:
                reply = clockIn.lockClockInEnter(groupId)
                needReply = True
            elif messages == '解锁打卡计划 加入' and isAdministrator:
                reply = clockIn.unlockClockInEnter(groupId)
                needReply = True
            elif messages == '锁定打卡计划 退出' and isAdministrator:
                reply = clockIn.lockClockInExit(groupId)
                needReply = True
            elif messages == '解锁打卡计划 退出' and isAdministrator:
                reply = clockIn.unlockClockInExit(groupId)
                needReply = True

            elif messages == '取消打卡提醒' and isAdministrator:
                reply = clockIn.offRemind(groupId)
                needReply = True
            elif messages == '开启打卡提醒' and isAdministrator:
                reply = clockIn.onRemind(groupId)
                needReply = True
            elif messages == '取消打卡总结' and isAdministrator:
                reply = clockIn.offSummary(groupId)
                needReply = True
            elif messages == '开启打卡总结' and isAdministrator:
                reply = clockIn.onSummary(groupId)
                needReply = True

            if needReply:
                logManage.groupLog(getNow.toString(), memberId, groupId, member.group.name, messages + "; 执行结果：" + reply)
        # 正常回复部分
        if not needReply:
            if messages.find('@' + str(Bot_QQ)) != -1:
                beAt = True
            else:
                if messages[0] == '*' and messages[1] != '由' and messages[1] != '*':
                    reply = command.function(messages[1:])
                    needReply = True
                else:
                    if messages[:3] == '天气 ':
                        reply = weather.getWeather(messages[3:])
                        needAt = False
                        needReply = True
                    elif messages == '色子' or messages == '骰子':
                        reply = smallFunction.dick()
                        needAt = True
                        needReply = True
                    elif messages == '抛硬币':
                        reply = smallFunction.coin()
                        needAt = True
                        needReply = True
                    elif messages == '文摘':
                        reply = talk.poem()
                        needReply = True
                    elif messages == '情话':
                        reply = talk.loveTalk()
                        needReply = True
                    elif (messages == '骂我一句' or messages == '骂我' or messages == '再骂' or messages == '你再骂') and groupId in botBaseInformation['cursePlanGroup']:
                        reply = talk.swear()
                        needReply = True
                    elif messages == '运势':
                        reply = lucky.luck(memberId)
                        needAt = True
                        needReply = True
                    elif messages == '打卡帮助':
                        reply = command.helpClock()
                        needReply = True
                    elif messages == '活动帮助':
                        reply = command.helpActivity()
                        needReply = True
                    
                    elif messages == '小柒测运气':
                        reply = 'jrrp'
                        needReply = True
                    elif messages == '微博热搜':
                        reply = weiboHot.getHot()
                        needReply = True
                    elif messages == '百度热搜':
                        reply = baidu.getHot()
                        needReply = True
                    elif messages == Bot_Name:
                        reply = '我在！'
                        needReply = True

                    elif messages[:5] == '参加活动 ' or messages[:5] == '参与活动 ':
                        activityName = messages[5:].strip()
                        if len(activityName) == 0:
                            reply = '活动名不能为空'
                            needReply = True
                        else:
                            reply = operator.joinActivity(groupId, memberId, activityName)
                            needAt = True
                            needReply = True
                    elif messages[:5] == '退出活动 ':
                        activityName = messages[5:].strip()
                        if len(activityName) == 0:
                            reply = '活动名不能为空'
                            needReply = True
                        else:
                            reply = operator.quitActivity(groupId, memberId, activityName)
                            needAt = True
                            needReply = True
                    elif messages == '活动清单':
                        reply = operator.getActivityList(groupId, app)
                        needReply = True

                    elif messages == '四级词汇':
                        vocabularyNumber = 1
                        reply = vocabulary.getVocabulary4(vocabularyNumber)
                        needReply = True
                    elif messages[:5] == '四级词汇 ':
                        vocabularyNumber = int(messages[5:].strip())
                        if vocabularyNumber <= 0:
                            vocabularyNumber = 1
                        reply = vocabulary.getVocabulary4(vocabularyNumber)
                        needReply = True
                    elif messages == '六级词汇':
                        vocabularyNumber = 1
                        reply = vocabulary.getVocabulary6(vocabularyNumber)
                        needReply = True
                    elif messages[:5] == '六级词汇 ':
                        vocabularyNumber = int(messages[5:].strip())
                        if vocabularyNumber <= 0:
                            vocabularyNumber = 1
                        reply = vocabulary.getVocabulary6(vocabularyNumber)
                        needReply = True

                    # ==========================================
                    # 之下为管理员模块
                    elif isAdministrator:
                        (needReply, needAt, reply) = await operator.administratorOperation(messages, groupId, memberId, app, member, botBaseInformation)
                    elif messages == '我的权限':
                        reply = '当前权限：普通用户\n可以输入*help来获取指令帮助哦~'
                        needReply = True
        # ==========================================
        # 此处为整活
        if not needReply:
            (needReply, needAt, reply, AtId) = keyReply.reply(messages, member, botBaseInformation)
        if not needReply:
            (needReply, needAt, reply) = autoReply.reply(messages, beAt, botBaseInformation, app, member.name)
            

        # +1部分
        if not needReply: # 如果需要回复，那么+1就被舍弃了
            global lastMessage
            global lastAutorepeat
            if lastMessage == messages and lastAutorepeat != messages and messages[0] != '[' and messages[:-1] != ']':
                reply = messages
                lastAutorepeat = messages
                needReply = True
        lastMessage = messages # 无论如何上一条消息得改为本次的message
    
    if needReply:
        lastAutorepeat = reply
        lastMessage = reply
    return (needReply, needAt, reply, AtId)