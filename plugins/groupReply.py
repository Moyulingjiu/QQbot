
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
    reply = ''

    groupId = member.group.id
    memberId = member.id
    blacklist = (groupId in botBaseInformation['blacklistGroup']) or (memberId in botBaseInformation['blacklistMember'])

    if (not blacklist) and (len(messages) != 0):

        # 打卡计划
        if clock['groupClock'].__contains__(groupId):
            if messages == '打卡':
                reply = member.name + clockIn.clockIn(groupId, memberId)
                #needAt = True
                needReply = True
            elif messages == '加入打卡计划':
                reply = member.name + clockIn.joinClockIn(groupId, memberId)
                # needAt = True
                needReply = True
            elif messages == '退出打卡计划':
                reply = member.name + clockIn.quitClockIn(groupId, memberId)
                # needAt = True
                needReply = True
            elif messages == '终止打卡计划' and (memberId in botBaseInformation['administrator'] or memberId in botBaseInformation['contributors']):
                reply = member.name + clockIn.stopClockIn(groupId)
                # needAt = True
                needReply = True
            elif messages == '锁定打卡计划' and (memberId in botBaseInformation['administrator'] or memberId in botBaseInformation['contributors']):
                pass
            elif messages == '解锁打卡计划' and (memberId in botBaseInformation['administrator'] or memberId in botBaseInformation['contributors']):
                pass
        # 正常回复部分
        if not needReply:
            if messages.find('@' + str(Bot_QQ)) != -1:
                beAt = True
            else:
                if messages[0] == '*':
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
                    elif messages == '骂我一句' and groupId in botBaseInformation['cursePlanGroup']:
                        reply = talk.swear()
                        needReply = True
                    elif messages == '运势':
                        reply = lucky.luck(memberId)
                        needAt = True
                        needReply = True
                    elif messages == '打卡帮助':
                        reply = command.helpClock()
                        needReply = True
                    elif messages == '小柒测运气':
                        reply = 'jrrp'
                        needReply = True
                    elif messages == '微博热搜':
                        reply = weiboHot.getHot()
                        needReply = True


                    # ==========================================
                    # 之下为管理员模块
                    elif memberId in botBaseInformation['contributors'] or memberId in botBaseInformation['administrator']:
                        (needReply, needAt, reply) = await operator.administratorOperation(messages, groupId, memberId, app, member, botBaseInformation)

        # ==========================================
        # 此处为整活
        if not needReply:
            (needReply, needAt, reply) = autoReply.reply(messages, beAt, botBaseInformation, app, member)
            

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
    return (needReply, needAt, reply)