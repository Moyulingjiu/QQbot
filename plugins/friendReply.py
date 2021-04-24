
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
from plugins import autoReply
from plugins import baidu

# 朋友消息回复

# 这里的messages是一个列表，因为发送的可能是多行信息，需要进行一定的处理
async def reply(botBaseInformation, messages, app, friend):
    Bot_QQ = botBaseInformation['baseInformation']['Bot_QQ']
    Bot_Name = botBaseInformation['baseInformation']['Bot_Name']

    
    needReply = False
    reply = ''
    blacklist = (friend.id in botBaseInformation['blacklistMember'])

    if (not blacklist) and (len(messages) != 0):
        if messages[0] == '*':
            reply = command.function(messages[1:])
            needReply = True
        else:
            if messages[:3] == '天气 ':
                reply = weather.getWeather(messages[3:])
                needReply = True
            elif messages == '色子' or messages == '骰子':
                reply = smallFunction.dick()
                needReply = True
            elif messages == '抛硬币':
                reply = smallFunction.coin()
                needReply = True
            elif messages == '文摘':
                reply = talk.poem()
                needReply = True
            elif messages == '情话':
                reply = talk.loveTalk()
                needReply = True
            elif messages == '骂我一句':
                reply = talk.swear()
                needReply = True
            elif messages == '打卡帮助':
                reply = command.helpClock()
                needReply = True
            elif messages == '微博热搜':
                reply = weiboHot.getHot()
                needReply = True
            elif messages == '百度热搜':
                reply = baidu.getHot()
                needReply = True
            elif messages == '运势':
                reply = lucky.luck(friend.id)
                needReply = True
            elif messages == Bot_Name:
                reply = '我在！'
                needReply = True
        if not needReply:
            if friend.id in botBaseInformation['contributors'] or friend.id in botBaseInformation['administrator']:
                (needReply, needAt, reply) = await operator.administratorOperation(messages, 0, friend.id, app, friend, botBaseInformation)
            elif messages == '我的权限':
                reply = '当前权限：普通用户\n可以输入*help来获取指令帮助哦~'
                needReply = True
        if not needReply:
            (needReply, needAt, reply) = autoReply.reply(messages, True, botBaseInformation, app, friend.nickname)
    
    return (needReply, reply)