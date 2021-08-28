from mirai import Mirai, WebSocketAdapter
from mirai import FriendMessage, GroupMessage, TempMessage
from mirai import Plain, At, AtAll, Face
from mirai.models.events import MemberJoinEvent, NewFriendRequestEvent, BotLeaveEventKick, BotInvitedJoinGroupRequestEvent
from mirai.models.events import NudgeEvent

# =============================================================
# 附加功能类
from plugins import getNow
from plugins import logManage
from plugins import MessageProcessing

# ==========================================================
# 基本信息

message_processing = MessageProcessing.MessageProcessing()
init = message_processing.loadfile()


# 主程序类
if __name__ == '__main__':
    bot = Mirai(
        qq=1812322920, # 改成你的机器人的 QQ 号
        adapter=WebSocketAdapter(
            verify_key='Xiao_Qi_Key', host='localhost', port=8080
        )
    )

    # 朋友消息
    @bot.on(FriendMessage)
    async def on_friend_message(event: FriendMessage):
        await message_processing.run(bot, event, 0, event.message_chain, At(bot.qq) in event.message_chain)

    # 群消息
    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        await message_processing.run(bot, event, 1, event.message_chain, At(bot.qq) in event.message_chain)

    # 临时消息
    @bot.on(TempMessage)
    async def on_temp_message(event: TempMessage):
        await message_processing.run(bot, event, 2, event.message_chain, At(bot.qq) in event.message_chain)

    # 新成员加入
    @bot.on(MemberJoinEvent)
    async def on_member_join(event: MemberJoinEvent):
        await message_processing.join(bot, event)
    
    # 新好友请求
    @bot.on(NewFriendRequestEvent)
    async def new_friend(event: NewFriendRequestEvent):
        await message_processing.new_friend(bot, event)
    
    # 新群请求
    @bot.on(BotInvitedJoinGroupRequestEvent)
    async def new_friend(event: BotInvitedJoinGroupRequestEvent):
        await message_processing.new_group(bot, event)
    
    # 被踢出群
    @bot.on(BotLeaveEventKick)
    async def new_friend(event: BotLeaveEventKick):
        await message_processing.kick(bot, event)
    
    # 戳一戳
    @bot.on(NudgeEvent)
    async def new_friend(event: NudgeEvent):
        await message_processing.nudge(bot, event)


    # ==========================================================
    # 启动机器人
    if not init:
        logManage.log(getNow.toString(), '——————————————————————————\n启动失败！！！\n')
        print('文件缺失！')
        exit(0)
        
    qq = message_processing.get_qq()
    name = message_processing.get_name()
    logManage.log(getNow.toString(), name + '(' + str(qq) + ')初始化成功，开始运行！')

    bot.run()  # 机器人启动