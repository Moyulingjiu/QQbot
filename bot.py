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

import os

# =============================================================
# 附加功能类
from plugins import dataManage
from plugins import groupReply
from plugins import friendReply
from plugins import getNow
from plugins import logManage


# ==========================================================
# 基本信息

botBaseInformation = {}

def init():
    global botBaseInformation

    # 基本信息重置
    if not os.path.exists('data/baseInformation.pkl'):
        Master_QQ = int(input('请输入主人的QQ（不可更改！）：'))
        botBaseInformation = {
            'baseInformation': {
                'Bot_Name': '小柒',
                'Bot_Age': 20,
                'Bot_Color': '天蓝色',
                'Bot_QQ': 123456,
                'Master_QQ': Master_QQ,
                'version': 'unknown version'
            },
            'administrator': [],
            'contributors': [],
            'blacklistGroup': [],
            'blacklistMember': [],
            'testGroup': [],
            'cursePlanGroup': [],
        }
        save_obj(botBaseInformation, 'baseInformation')
    else:
        botBaseInformation = dataManage.load_obj('baseInformation')
    
    # 打卡信息
    if not os.path.exists('data/clockIn.pkl'):
        clockIn = {
            'groupClock': {},
            'dictClockPeople': {},
            'clockDate': 'xx-xx-xx'
        }
        save_obj(clockIn, 'clockIn')

    # 幸运信息
    if not os.path.exists('data/luck.pkl'):
        luck = {
            'luck': {},
            'luckDate': 'xx-xx-xx' 
        }
        save_obj(luck, 'luck')
        
    # 屏蔽词
    if not os.path.exists('data/AIScreenWords.pkl'):
        screenWords = []
        save_obj(screenWords, 'AIScreenWords')

    
    if not os.path.exists('data/lovetalk.txt'):
        with open('data/lovetalk.txt', 'w', encoding='utf-8') as f:
            f.write('1\n1.我大约真的没有什么才华，只是因为有幸见着了你，于是这颗庸常的心中才凭空生出好些浪漫。')
    if not os.path.exists('data/poem.txt'):
        with open('data/poem.txt', 'w', encoding='utf-8') as f:
            f.write('1\n1.我们趋行在人生这个恒古的旅途，在坎坷中奔跑，在挫折里涅槃，忧愁缠满全身，痛苦飘洒一地。我们累，却无从止歇；我们苦，却无法回避。——《百年孤独》')
    if not os.path.exists('data/swear.txt'):
        with open('data/swear.txt', 'w', encoding='utf-8') as f:
            f.write('1\n1.我无外乎也就讨厌两种人，一种是你这样的，另一种是不管你以后变成什么样那样的。')
            
    if not os.path.exists('data/tarot.txt'):
        return False
    if not os.path.exists('data/tarot2.txt'):
        return False

    return True

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

# 好友消息


@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend, source: Source):
    global botBaseInformation
    botBaseInformation = dataManage.load_obj('baseInformation')

    getMessage = await app.messageFromId(source)
    strMessage = getMessage.messageChain.asDisplay()

    (needReply, reply) = await friendReply.reply(botBaseInformation, strMessage, app, friend)

    if needReply:
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(reply)
        ]))

# 群聊消息


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, member: Member, source: Source):
    global botBaseInformation
    botBaseInformation = dataManage.load_obj('baseInformation')

    getMessage = await app.messageFromId(source)
    strMessage = getMessage.messageChain.asDisplay()

    (needReply, needAt, reply) = await groupReply.reply(botBaseInformation, strMessage, app, member)

    if needReply:
        if needAt:
            await app.sendGroupMessage(member.group, MessageChain.create([
                At(member.id),
                Plain(reply)
            ]))
        else:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain(reply)
            ]))


@bcc.receiver("TempMessage")
async def group_message_listener(app: GraiaMiraiApplication, member: Member, source: Source):
    getMessage = await app.messageFromId(source)
    strMessage = getMessage.messageChain.asDisplay()

    await app.sendTempMessage(member.group.id, member.id, MessageChain.create([
        Plain('暂时不能支持临时消息，请联系管理员1597867839添加小柒好友')
    ]))

if init():
    logManage.log(getNow.toString(), 0, botBaseInformation['baseInformation']['Bot_Name'] + '启动！')
    # loop.run_until_complete(timeWatcher())
    app.launch_blocking()
else:
    logManage.log(getNow.toString(), 0, '——————————————————————————\n启动失败！！！\n')
    print('文件缺失！')
