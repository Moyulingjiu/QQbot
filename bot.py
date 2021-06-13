import asyncio
# 所有事件监听都在entry中可以找到
from graia.application.entry import (
    GraiaMiraiApplication, Session,
    MessageChain, Group, Friend, Member, MemberInfo,
    Plain, Image, AtAll, At, Face, Source
)
from graia.application.entry import (
    BotMuteEvent, BotGroupPermissionChangeEvent
)
from graia.application.event.mirai import NewFriendRequestEvent
from graia.broadcast import Broadcast

# =============================================================
# 附加功能类
from plugins import getNow
from plugins import logManage
from plugins import MessageProcessing

# ==========================================================
# 基本信息

message_processing = MessageProcessing.MessageProcessing()
init = message_processing.loadfile()
if not init:
    logManage.log(getNow.toString(), 0, '——————————————————————————\n启动失败！！！\n')
    print('文件缺失！')
    exit(0)


# ============================================
# 定义全局信息
loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
apps = GraiaMiraiApplication(
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
    global message_processing
    await message_processing.run(app, 0, friend, source)


# 群聊消息
@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, member: Member, source: Source):
    global message_processing
    await message_processing.run(app, 1, member, source)


# 临时消息
@bcc.receiver("TempMessage")
async def group_temp_message_listener(app: GraiaMiraiApplication, member: Member, source: Source):
    global message_processing
    await message_processing.run(app, 2, member, source)


# 好友邀请
@bcc.receiver("NewFriendRequestEvent")
async def new_friend(app: GraiaMiraiApplication, event: NewFriendRequestEvent):
    global message_processing
    await message_processing.new_friend(app, event)


qq = message_processing.get_qq()
name = message_processing.get_name()
logManage.log(getNow.toString(), 0, name + '(' + str(qq) + ')启动！')
apps.launch_blocking()
