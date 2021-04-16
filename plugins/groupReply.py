
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

    if not blacklist:

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
        # 正常回复部分
        if not needReply:
            if messages.find('@' + str(Bot_QQ)) != -1:
                beAt = True
                AtMessage = messages[len(str(Bot_QQ)) + 2:]
                if AtMessage == '你好':
                    reply = '你好呀，' + member.name + '。小柒很高兴遇见你！'
                    needAt = True
                    needReply = True
                elif AtMessage == '抱抱':
                    replylist = ['抱抱呀！', Bot_Name +
                                '才不要和你抱抱！', '抱抱', '抱抱' + member.name]
                    reply = replylist[random.randrange(0, len(replylist))]
                    needReply = True
                elif AtMessage == '贴贴':
                    replylist = ['贴贴', '快来贴贴，嘿嘿！', '不贴不贴']
                    reply = replylist[random.randrange(0, len(replylist))]
                    needReply = True
                elif AtMessage == '晚安':
                    replylist = ['晚安', '晚安哦' + member.name,
                                '记得要梦见' + Bot_Name, '快睡吧']
                    reply = replylist[random.randrange(0, len(replylist))]
                    needReply = True
                elif AtMessage == '谢谢':
                    replylist = ['嘿嘿', '不用谢啦', '要时刻想着' + Bot_Name, '没事啦']
                    reply = replylist[random.randrange(0, len(replylist))]
                elif AtMessage == '快来' or AtMessage == '快来快来':
                    replylist = ['游戏启动', '来了来了', '不要着急嘛']
                    reply = replylist[random.randrange(0, len(replylist))]
                    needReply = True
                elif AtMessage == '傻子':
                    reply = '你才是傻子，' + Bot_Name + '才不傻'
                    needReply = True
                elif AtMessage == '笨蛋':
                    reply = Bot_Name + '才不要理你了'
                    needReply = True
                elif AtMessage == '蠢货':
                    reply = '哼'
                    needReply = True
                elif AtMessage == '你是猪吗' or AtMessage == '猪':
                    reply = '你以为谁都像你一天天哼唧哼唧的'
                    needReply = True
                else:
                    reply = '诶，叫我干嘛'
                    needReply = True
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
            if messages == 'yjy爬':
                reply = 'yjy快爬'
                needReply = True
            elif messages == '我是fw':
                reply = '在' + Bot_Name + '心中，' + member.name + '一直都很厉害的哦~'
                needReply = True
            elif messages == '好家伙':
                tmpNumber = random.randrange(0, 5)
                if tmpNumber == 3:
                    reply = '又发生什么辣？'
                    needReply = True
            elif messages == '你们早上都没课的嘛':
                reply = Bot_Name + '还没有开始上课呢'
                needReply = True
            elif messages == '摸了':
                reply = member.name + '桑怎么可以摸鱼呢'
                needReply = True
            elif messages == '也不是不行':
                reply = member.name + '那就快冲！'
                needReply = True
            elif messages[-3:] == '多好啊':
                reply = '是呀是呀'
                needReply = True
            elif messages == '上课':
                reply = Bot_Name + '陪你一起上课'
                needReply = True
            elif messages == '满课':
                reply = '好惨哦'
                needReply = True
            elif messages == '谢谢':
                reply = '嘿嘿'
                needReply = True
            elif messages == '有人ow吗':
                reply = Bot_Name + '也想来'
                needReply = True
            elif messages[-2:] == '快来':
                reply = Bot_Name + '来了来了'
                needReply = True
            elif messages == '晚安':
                reply = '晚安呀！' + member.name
                needReply = True
            elif messages == '早安':
                reply = '早哦，' + member.name
                needReply = True
            elif messages == '来一张涩图':
                reply = '能不能多读书，少看涩图'
                needReply = True
            elif messages == '？':
                tmpNumber = random.randrange(0, 5)
                if tmpNumber == 2:
                    reply = '怎么啦'
                    needReply = True

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