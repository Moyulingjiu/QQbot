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
        bot_name = input('请输入机器人名字：')
        bot_QQ = int(input('请输入机器人的QQ：'))
        bot_age = int(input('请输入机器人的年龄：'))

        botBaseInformation = {
            'baseInformation': {
                'Bot_Name': bot_name,
                'Bot_Age': bot_age,
                'Bot_Color': '天蓝色',
                'Bot_QQ': bot_QQ,
                'Master_QQ': Master_QQ,
                'version': 'unknown version'
            },
            'administrator': [],
            'contributors': [],
            'blacklistGroup': [],
            'blacklistMember': [],
            'testGroup': [],
            'cursePlanGroup': [],
            'mute': []
        }
        dataManage.save_obj(botBaseInformation, 'baseInformation')
    else:
        botBaseInformation = dataManage.load_obj('baseInformation')
        if not botBaseInformation.__contains__('mute'):
            botBaseInformation['mute'] = []
    
    # 打卡信息
    if not os.path.exists('data/clockIn.pkl'):
        clockIn = {
            'groupClock': {},
            'dictClockPeople': {},
            'clockDate': 'xx-xx-xx'
        }
        dataManage.save_obj(clockIn, 'clockIn')

    # 幸运信息
    if not os.path.exists('data/luck.pkl'):
        luck = {
            'luck': {},
            'luckDate': 'xx-xx-xx' 
        }
        dataManage.save_obj(luck, 'luck')
        
    # 屏蔽词
    if not os.path.exists('data/AIScreenWords.pkl'):
        screenWords = []
        dataManage.save_obj(screenWords, 'AIScreenWords')

    
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

    # 四六级词汇
    if not os.path.exists('data/vocabulary-4.txt'):
        return False
    if not os.path.exists('data/vocabulary-4-index.txt'):
        with open('data/vocabulary-4-index.txt', 'w', encoding='utf-8') as f:
            f.write('1')
    if not os.path.exists('data/vocabulary-6.txt'):
        return False
    if not os.path.exists('data/vocabulary-6-index.txt'):
        with open('data/vocabulary-6-index.txt', 'w', encoding='utf-8') as f:
            f.write('1')

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
    print('\n收到消息<' + friend.nickname + '/' + str(friend.id) + '>：' + strMessage)

    if strMessage[:5] == '*send':
        master = await app.getFriend(botBaseInformation['baseInformation']['Master_QQ'])

        if master != None and len(strMessage) > 5:
            await app.sendFriendMessage(master, MessageChain.create([
                Plain(friend.nickname + '(' + str(friend.id) + ')：' + strMessage[5:])
            ]))
            await app.sendFriendMessage(friend, MessageChain.create([
                Plain('已经报告给主人了~')
            ]))
            needReply = True
        return
    elif strMessage == '*ai on':
        if friend.id in botBaseInformation['noAI']['friend']:
            botBaseInformation['noAI']['friend'].remove(friend.id)
            dataManage.save_obj(botBaseInformation, 'baseInformation')
            await app.sendFriendMessage(friend, MessageChain.create([
                Plain('已开启智能回复~')
            ]))
        return
    elif strMessage == '*ai off':
        if not friend.id in botBaseInformation['noAI']['friend']:
            botBaseInformation['noAI']['friend'].append(friend.id)
            dataManage.save_obj(botBaseInformation, 'baseInformation')
            await app.sendFriendMessage(friend, MessageChain.create([
                Plain('已关闭智能回复~')
            ]))
        return

    (needReply, reply, isImage) = await friendReply.reply(botBaseInformation, strMessage, app, friend, getMessage.messageChain)

    if needReply:
        print('回复消息<' + friend.nickname + '/' + str(friend.id) + '>：' + reply + '\n')
        if len(isImage) > 0:
            filepath = 'data/face/' + isImage
            if os.path.exists(filepath):
                await app.sendFriendMessage(friend, MessageChain.create([
                    Image.fromLocalFile(filepath)
                ]))
        if len(reply) > 0:
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
    print('\n\t收到消息<' + member.group.name + '/' + str(member.group.id) + '>[' + member.name + '/' + str(member.id) + ']：' + strMessage)

    if str(member.permission) == 'MemberPerm.Owner' or str(member.permission) == 'MemberPerm.Administrator' or (member.id in botBaseInformation['administrator']) or (member.id in botBaseInformation['contributors']) or (member.id == botBaseInformation['baseInformation']['Master_QQ']):
        if strMessage == '*quit':
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('再见啦~各位！我会想你们的')
            ]))
            await app.quit(member.group)
            logManage.groupLog(getNow.toString(), member.id, member.group.id, member.group.name, strMessage + '; 小柒退群！')
            return
        elif strMessage == '*mute':
            if not member.group.id in botBaseInformation['mute']:
                botBaseInformation['mute'].append(member.group.id)
                dataManage.save_obj(botBaseInformation, 'baseInformation')
                await app.sendGroupMessage(member.group, MessageChain.create([
                    Plain('QAQ，那我闭嘴了')
                ]))
            logManage.groupLog(getNow.toString(), member.id, member.group.id, member.group.name, strMessage + '; 小柒禁言！')
            return
        elif strMessage == '*unmute':
            if member.group.id in botBaseInformation['mute']:
                botBaseInformation['mute'].remove(member.group.id)
                dataManage.save_obj(botBaseInformation, 'baseInformation')
                await app.sendGroupMessage(member.group, MessageChain.create([
                    Plain('呜呜呜，憋死我了，终于可以说话了')
                ]))
            logManage.groupLog(getNow.toString(), member.id, member.group.id, member.group.name, strMessage + '; 小柒解出禁言！')
            return
        elif strMessage == '*game on':
            if member.group.id in botBaseInformation['gameOff']:
                botBaseInformation['gameOff'].remove(member.group.id)
                dataManage.save_obj(botBaseInformation, 'baseInformation')
                await app.sendGroupMessage(member.group, MessageChain.create([
                    Plain('本群已开启游戏功能~')
                ]))
            return
        elif strMessage == '*game off':
            if not member.group.id in botBaseInformation['gameOff']:
                botBaseInformation['gameOff'].append(member.group.id)
                dataManage.save_obj(botBaseInformation, 'baseInformation')
                await app.sendGroupMessage(member.group, MessageChain.create([
                    Plain('本群已关闭游戏功能~')
                ]))
            return
        elif strMessage == '*ai on':
            if member.group.id in botBaseInformation['noAI']['group']:
                botBaseInformation['noAI']['group'].remove(member.group.id)
                dataManage.save_obj(botBaseInformation, 'baseInformation')
                await app.sendGroupMessage(member.group, MessageChain.create([
                    Plain('本群已开启艾特的智能回复~')
                ]))
            return
        elif strMessage == '*ai off':
            if not member.group.id in botBaseInformation['noAI']['group']:
                botBaseInformation['noAI']['group'].append(member.group.id)
                dataManage.save_obj(botBaseInformation, 'baseInformation')
                await app.sendGroupMessage(member.group, MessageChain.create([
                    Plain('本群已关闭艾特的智能回复~')
                ]))
            return
    if strMessage[:5] == '*send':
        friend = await app.getFriend(botBaseInformation['baseInformation']['Master_QQ'])
        print(friend)
        if friend != None and len(strMessage) > 5:
            await app.sendFriendMessage(friend, MessageChain.create([
                Plain(member.name + '(' + str(member.id) + ')：' + strMessage[5:])
            ]))
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('已经报告给主人了~')
            ]))
            needReply = True
        return


    if not member.group.id in botBaseInformation['mute']:
        (needReply, needAt, reply, AtId, isImage) = await groupReply.reply(botBaseInformation, strMessage, app, member, getMessage.messageChain)

        if needReply:
            print('\t回复消息<' + member.group.name + '/' + str(member.group.id) + '>[' + member.name + '/' + str(member.id) + ']：' + reply + '\n')

            if needAt:
                if AtId == 0: # At发言者
                    await app.sendGroupMessage(member.group, MessageChain.create([
                        At(member.id),
                        Plain(reply)
                    ]))
                elif AtId > 0: # At指定人
                    member_target = await app.getMember(member.group.id, AtId)
                    if member_target != None:
                        await app.sendGroupMessage(member.group, MessageChain.create([
                            At(AtId),
                            Plain(reply)
                        ]))
                    else:
                        await app.sendGroupMessage(member.group, MessageChain.create([
                            Plain('@' + str(AtId) + ' '),
                            Plain(reply)
                        ]))
                elif AtId == -1: # At全体
                    await app.sendGroupMessage(member.group, MessageChain.create([
                        AtAll(),
                        Plain(reply)
                    ]))
            else:
                if len(isImage) > 0:
                    filepath = 'data/face/' + isImage
                    if os.path.exists(filepath):
                        await app.sendGroupMessage(member.group, MessageChain.create([
                            Image.fromLocalFile(filepath)
                        ]))
                if len(reply) > 0:
                    await app.sendGroupMessage(member.group, MessageChain.create([
                        Plain(reply)
                    ]))

# 临时消息
@bcc.receiver("TempMessage")
async def groupTemp_message_listener(app: GraiaMiraiApplication, member: Member, source: Source):
    global botBaseInformation
    botBaseInformation = dataManage.load_obj('baseInformation')

    getMessage = await app.messageFromId(source)
    strMessage = getMessage.messageChain.asDisplay()
    print('\n\t收到消息<' + member.group.name + '/' + str(member.group.id) + '>[' + member.name + '/' + str(member.id) + ']：' + strMessage)


    if str(member.permission) == 'MemberPerm.Owner' or str(member.permission) == 'MemberPerm.Administrator' or (member.id in botBaseInformation['administrator']) or (member.id in botBaseInformation['contributors']) or (member.id == botBaseInformation['baseInformation']['Master_QQ']):
        if strMessage == '*quit':
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('再见啦~各位！我会想你们的')
            ]))
            await app.quit(member.group)
            logManage.groupLog(getNow.toString(), member.id, member.group.id, member.group.name, strMessage + '; 小柒退群！')
            return
        elif strMessage == '*mute':
            if not member.group.id in botBaseInformation['mute']:
                botBaseInformation['mute'].append(member.group.id)
                dataManage.save_obj(botBaseInformation, 'baseInformation')
                await app.sendGroupMessage(member.group, MessageChain.create([
                    Plain('QAQ，那我闭嘴了')
                ]))
            logManage.groupLog(getNow.toString(), member.id, member.group.id, member.group.name, strMessage + '; 小柒禁言！')
            return
        elif strMessage == '*unmute':
            if member.group.id in botBaseInformation['mute']:
                botBaseInformation['mute'].remove(member.group.id)
                dataManage.save_obj(botBaseInformation, 'baseInformation')
                await app.sendGroupMessage(member.group, MessageChain.create([
                    Plain('呜呜呜，憋死我了，终于可以说话了')
                ]))
            logManage.groupLog(getNow.toString(), member.id, member.group.id, member.group.name, strMessage + '; 小柒解出禁言！')
            return
    if strMessage[:5] == '*send':
        friend = await app.getFriend(botBaseInformation['baseInformation']['Master_QQ'])
        print(friend)
        if friend != None and len(strMessage) > 5:
            await app.sendFriendMessage(friend, MessageChain.create([
                Plain(member.name + '(' + str(member.id) + ')：' + strMessage[5:])
            ]))
            await app.sendTempMessage(member.group.id, member.id, MessageChain.create([
                Plain('已经报告给主人了~')
            ]))
            needReply = True
        return


    (needReply, needAt, reply, AtId, isImage) = await groupReply.reply(botBaseInformation, strMessage, app, member, getMessage.messageChain)
    
    if needReply:
        print('\t回复消息<' + member.group.name + '/' + str(member.group.id) + '>[' + member.name + '/' + str(member.id) + ']：' + reply + '\n')
        if len(isImage) > 0:
            filepath = 'data/face/' + isImage
            if os.path.exists(filepath):
                await app.sendTempMessage(member.group.id, member.id, MessageChain.create([
                    Image.fromLocalFile(filepath)
                ]))
        if len(reply) > 0:
            await app.sendTempMessage(member.group.id, member.id, MessageChain.create([
                Plain(reply)
            ]))

# 好友邀请
@bcc.receiver("NewFriendRequestEvent")
async def newFriend(app: GraiaMiraiApplication):
    master = await app.getFriend(botBaseInformation['baseInformation']['Master_QQ'])

    if master != None:
        await app.sendFriendMessage(master, MessageChain.create([
            Plain('有新的好友申请！')
        ]))

# ======================
# @sche.schedule(timers.every_custom_seconds(60))
# async def test():
#     print("60s一次")

# ======================

if __name__ == '__main__':
    print('初始化...')
    if init():
        logManage.log(getNow.toString(), 0, botBaseInformation['baseInformation']['Bot_Name'] + '启动！')
        app.launch_blocking()
    else:
        logManage.log(getNow.toString(), 0, '——————————————————————————\n启动失败！！！\n')
        print('文件缺失！')
