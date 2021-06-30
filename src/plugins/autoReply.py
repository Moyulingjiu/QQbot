import random

from plugins import AIchat
from plugins import dataManage

# 自动回复部分

screenWords = []
unknown_reply = ['诶？', '你说的话太深奥了', '我也不是很清楚呢', '不知道哦~', '你猜']


def reply(messages, beAt, botBaseInformation, app, nickname, groupId, memberId):
    global screenWords
    screenWords = dataManage.load_obj('AIScreenWords')

    Bot_QQ = botBaseInformation['baseInformation']['Bot_QQ']
    Bot_Name = botBaseInformation['baseInformation']['Bot_Name']
    needReply = False
    needAt = False
    reply = ''
    isImage = ''

    if groupId == 0:
        if memberId in botBaseInformation['noAI']['friend']:
            return needReply, reply, isImage, 0, needAt
    else:
        if groupId in botBaseInformation['noAI']['group']:
            return needReply, reply, isImage, 0, needAt

    if beAt:
        print('被艾特：' + messages)
        if messages == '你好':
            reply = '你好呀，' + nickname + '。小柒很高兴遇见你！'
            needAt = True
            needReply = True
        elif messages == '抱抱':
            replylist = ['抱抱呀！', Bot_Name +
                         '才不要和你抱抱！', '抱抱', '抱抱' + nickname]
            reply = replylist[random.randrange(0, len(replylist))]
            needReply = True
        elif messages == '贴贴':
            replylist = ['贴贴', 'image贴贴', '快来贴贴，嘿嘿！', '不贴不贴']
            reply = replylist[random.randrange(0, len(replylist))]
            if reply == 'image贴贴':
                reply = ''
                isImage = '贴贴.jpg'
            needReply = True
        elif messages == '晚安':
            replylist = ['晚安', 'image晚安', '晚安哦' + nickname,
                         '记得要梦见' + Bot_Name, '快睡吧']
            reply = replylist[random.randrange(0, len(replylist))]
            if reply == 'image晚安':
                reply = ''
                isImage = '晚安.png'
            needReply = True
        elif messages == '谢谢':
            replylist = ['嘿嘿', '不用谢啦', '要时刻想着' + Bot_Name, '没事啦']
            reply = replylist[random.randrange(0, len(replylist))]
        elif messages == '快来' or messages == '快来快来':
            replylist = ['游戏启动', '来了来了', '不要着急嘛']
            reply = replylist[random.randrange(0, len(replylist))]
            needReply = True
        elif messages == '傻子':
            reply = '你才是傻子，' + Bot_Name + '才不傻'
            needReply = True
        elif messages == '笨蛋':
            reply = Bot_Name + '才不要理你了'
            needReply = True
        elif messages == '蠢货':
            reply = '哼'
            needReply = True
        elif messages == '你是猪吗' or messages == '猪':
            reply = '你以为谁都像你一天天哼唧哼唧的'
            needReply = True
        elif messages == '早安':
            reply = '早哦，' + nickname
            needReply = True
        elif messages == '帮助':
            reply = '你可以输入*help来查询帮助哦~'
            needReply = True
        else:
            reply = AIchat.getReply(botBaseInformation, messages)
            needReply = True
            for i in screenWords:
                if reply.find(i) != -1:
                    reply = random.choice(unknown_reply)
    else:
        if messages == 'yjy爬':
            reply = 'yjy快爬'
            needReply = True
        elif messages == '我是fw' or messages == '我是废物':
            reply = '在' + Bot_Name + '心中，' + nickname + '一直都很厉害的哦~'
            needReply = True
        elif messages == '好家伙':
            tmpNumber = random.randrange(0, 7)
            if tmpNumber == 3:
                reply = '又发生什么辣？'
                needReply = True
            elif tmpNumber == 1:
                isImage == '问号.jpg'
                needReply = True
        elif messages == '你们早上都没课的嘛':
            reply = Bot_Name + '还没有开始上课呢'
            needReply = True
        elif messages == '摸了':
            reply = nickname + '桑怎么可以摸鱼呢'
            needReply = True
        elif messages == '也不是不行':
            reply = nickname + '那就快冲！'
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
            replylist = ['晚安', 'image晚安', '晚安哦' + nickname,
                         '记得要梦见' + Bot_Name, '快睡吧']
            reply = replylist[random.randrange(0, len(replylist))]
            if reply == 'image晚安':
                reply = ''
                isImage = '晚安.png'
            needReply = True
        elif messages == '早安':
            reply = '早哦，' + nickname
            needReply = True
        elif messages == '来一张涩图':
            reply = '能不能多读书，少看涩图'
            needReply = True
        elif messages == '？':
            tmpNumber = random.randrange(0, 10)
            if tmpNumber == 2:
                reply = '怎么啦'
                needReply = True
            elif tmpNumber == 1:
                isImage == '问号.jpg'
                needReply = True
        else:
            tmpNumber = random.randrange(0, 1000)
            if tmpNumber < 10:
                if botBaseInformation['reply']['lastMinute'] <= 10:
                    reply = AIchat.getReply(botBaseInformation, messages)
                    needReply = True
                    for i in screenWords:
                        if reply.find(i) != -1:
                            needReply = False
                    if needReply:
                        botBaseInformation['reply']['lastMinute'] += 1
                        dataManage.save_obj(botBaseInformation, 'baseInformation')
    return needReply, reply, isImage, 0, needAt