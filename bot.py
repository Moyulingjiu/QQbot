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
    botBaseInformation = dataManage.load_obj('baseInformation')

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
    init()
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
    init()
    getMessage = await app.messageFromId(source)
    strMessage = getMessage.messageChain.asDisplay()
    print(strMessage)

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



init()
logManage.log(getNow.toString(), 0, botBaseInformation['baseInformation']['Bot_Name'] + '启动！')
# loop.run_until_complete(timeWatcher())
app.launch_blocking()
