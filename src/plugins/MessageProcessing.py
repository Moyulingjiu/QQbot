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
from graia.application.event.mirai import NewFriendRequestEvent
from graia.broadcast import Broadcast

import os
import time

from plugins import talk
from plugins import weather
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
from plugins import rpg
from plugins import PixivImage
from plugins import BaseFunction


# 发送消息
async def send_message(app, mode, member, reply_text, reply_image, need_at, at_qq):
    reply_text_len = len(reply_text)
    reply_image_len = len(reply_image)

    if mode == 0:
        if reply_image_len > 0:
            filepath = 'data/image/' + reply_image
            if os.path.exists(filepath):
                await app.sendFriendMessage(member, MessageChain.create([
                    Image.fromLocalFile(filepath)
                ]))
        if reply_text_len > 0:
            await app.sendFriendMessage(member, MessageChain.create([
                Plain(reply_text)
            ]))
    elif mode == 1:
        if need_at:
            if at_qq == 0:  # At发言者
                if reply_image_len > 0:
                    filepath = 'data/face/' + reply_image
                    if os.path.exists(filepath):
                        await app.sendGroupMessage(member.group, MessageChain.create([
                            Image.fromLocalFile(filepath)
                        ]))
                await app.sendGroupMessage(member.group, MessageChain.create([
                    At(member.id),
                    Plain(reply_text)
                ]))
            elif at_qq > 0:  # At指定人
                member_target = await app.getMember(member.group.id, at_qq)
                if member_target is not None:
                    if reply_image_len > 0:
                        filepath = 'data/face/' + reply_image
                        if os.path.exists(filepath):
                            await app.sendGroupMessage(member.group, MessageChain.create([
                                Image.fromLocalFile(filepath)
                            ]))
                    await app.sendGroupMessage(member.group, MessageChain.create([
                        At(at_qq),
                        Plain(reply_text)
                    ]))
                else:
                    if reply_image_len > 0:
                        filepath = 'data/face/' + reply_image
                        if os.path.exists(filepath):
                            await app.sendGroupMessage(member.group, MessageChain.create([
                                Image.fromLocalFile(filepath)
                            ]))
                    await app.sendGroupMessage(member.group, MessageChain.create([
                        Plain('@' + str(at_qq) + ' '),
                        Plain(reply_text)
                    ]))
            elif at_qq == -1:  # At全体
                if reply_image_len > 0:
                    filepath = 'data/face/' + reply_image
                    if os.path.exists(filepath):
                        await app.sendGroupMessage(member.group, MessageChain.create([
                            Image.fromLocalFile(filepath)
                        ]))
                await app.sendGroupMessage(member.group, MessageChain.create([
                    AtAll(),
                    Plain(reply_text)
                ]))
        else:
            if reply_image_len > 0:
                filepath = 'data/image/' + reply_image
                if os.path.exists(filepath):
                    await app.sendGroupMessage(member.group, MessageChain.create([
                        Image.fromLocalFile(filepath)
                    ]))
            if reply_text_len > 0:
                await app.sendGroupMessage(member.group, MessageChain.create([
                    Plain(reply_text)
                ]))
    elif mode == 2:
        if reply_image_len > 0:
            filepath = 'data/image/' + reply_image
            if os.path.exists(filepath):
                await app.sendTempMessage(member.group.id, member.id, MessageChain.create([
                    Image.fromLocalFile(filepath)
                ]))
        if reply_text_len > 0:
            await app.sendTempMessage(member.group.id, member.id, MessageChain.create([
                Plain(reply_text)
            ]))


class MessageProcessing:
    bot_information = {}
    clock = {}
    bot_qq = 0
    bot_name = '小柒'

    message_tmp = {}
    last_reply = ''

    luck = BaseFunction.luck()
    bottle = BaseFunction.DriftingBottle()

    def loadfile(self):
        # 基本信息重置
        if not os.path.exists('data/baseInformation.pkl'):
            Master_QQ = int(input('请输入主人的QQ（不可更改！）：'))
            bot_name = input('请输入机器人名字：')
            bot_QQ = int(input('请输入机器人的QQ：'))
            bot_age = int(input('请输入机器人的年龄：'))

            self.bot_information = {
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
                'mute': [],
                'pixiv': []
            }
            dataManage.save_obj(self.bot_information, 'baseInformation')
        else:
            self.bot_information = dataManage.load_obj('baseInformation')
            if not self.bot_information.__contains__('mute'):
                self.bot_information['mute'] = []

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

    def get_name(self):
        return self.bot_name

    def get_qq(self):
        return self.bot_qq

    def __init__(self):
        self.pixiv = PixivImage.pixiv()

    def get_right(self, qq):
        if qq == self.bot_information['baseInformation']['Master_QQ']:
            return 0
        elif qq in self.bot_information["administrator"]:
            return 1
        elif qq in self.bot_information["contributors"]:
            return 2
        else:
            return 3

    def get_blacklist(self, qq, group_id):
        if qq in self.bot_information['blacklistMember']:
            return 1
        elif group_id > 0 and group_id in self.bot_information['blacklistGroup']:
            return 2
        return 0

    # 0：朋友消息，1：群消息，2：临时消息
    async def run(self, app, mode, member, message_source):
        self.bot_information = dataManage.load_obj('baseInformation')
        self.bot_qq = self.bot_information['baseInformation']['Bot_QQ']
        self.bot_name = self.bot_information['baseInformation']['Bot_Name']
        self.clock = dataManage.load_obj('clockIn')

        # ===================================================================================
        # ===================================================================================
        # 消息表获取
        get_message = await app.messageFromId(message_source)
        message = str(get_message.messageChain.asDisplay())

        # ===================================================================================
        # ===================================================================================
        # 基本信息获取
        # interceptable_need_reply = False  # 可被打断的回复
        need_reply = False  # 是否需要回复
        reply_text = ''  # 回复的文本内容
        reply_image = ''  # 回复的图片
        need_at = False  # 是否需要at
        at_qq = 0  # at的qq是谁
        be_at = False  # 是否被at
        group_right = 2  # 在群里的权限（群主、管理员、成员）
        if mode == 0:
            name = member.nickname  # 发消息的人的名字
            group_id = 0  # 发消息的人的群号（如果是群聊消息）
        else:
            name = member.name
            group_id = member.group.id
            tmp = str(member.permission)
            if tmp == 'MemberPerm.Owner':
                group_right = 0
            elif tmp == 'MemberPerm.Administrator':
                group_right = 1

        qq = member.id  # (发消息人的qq)
        right = self.get_right(qq)  # 对于小柒的权限（主人、管理员、贡献者）
        blacklist = self.get_blacklist(qq, group_id)

        if mode == 1 and '@' + str(self.bot_qq) in message:
            be_at = True
            message = message.replace('@' + str(self.bot_qq) + ' ', '')
            message = message.replace('@' + str(self.bot_qq), '')
            message = message.replace('@' + str(self.bot_name), '')
        elif mode == 0 or mode == 2:
            be_at = True

        key_allow = []
        if mode == 1:
            if self.bot_information['keyToken']['group'].__contains__(group_id):
                key_allow = self.bot_information['keyToken']['group'][group_id]
        elif mode == 0 or mode == 2:
            if self.bot_information['keyToken']['friend'].__contains__(qq):
                key_allow = self.bot_information['keyToken']['friend'][qq]

        message = message.strip()
        message_len = len(message)
        message_code = message.lower()
        if message_code[0] == '*' or message_code[0] in key_allow:
            message_code = message_code[1:]
        else:
            message_code = ''
        message_code_len = len(message_code)

        be_mute = (mode == 1 and group_id in self.bot_information['mute'])
        print(message)
        print(message_code)

        # ===================================================================================
        # ===================================================================================
        # 消息处理开始
        if message == '我的权限':
            need_at = True
            if blacklist == 1:
                reply_text = '你当前在黑名单中~'
            elif blacklist == 2:
                reply_text = '本群当前在黑名单中'
            elif right == 0:
                reply_text = '当前权限：主人\n可以输入“主人帮助”来获取指令帮助哦~'
            elif right == 1:
                reply_text = '当前权限：管理员\n可以输入“管理员帮助”来获取指令帮助哦~'
            elif right == 2:
                reply_text = '当前权限：贡献者\n可以输入“贡献者帮助”来获取指令帮助哦~'
            elif right == 3:
                reply_text = '当前权限：普通用户\n可以输入“*help”来获取指令帮助；输入“骰娘”来获取骰娘帮助；输入“游戏帮助”来获取游戏帮助'

            if be_mute:
                reply_text += '\n在本群中' + self.bot_name + '被禁言了'

            await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
            return

        # 如果是黑名单那么不会回复任何消息
        if blacklist != 0 or message_len == 0:
            return

        # 如果被限制那么只回复at消息
        if mode == 1:
            if group_id in self.bot_information['limit']:
                if not be_at:
                    return

        # 如果是群聊消息，并且具有小柒的操作权限，那么就可以进行退群和禁言的操作
        if mode == 1:
            if message_code == 'quit' or message_code == 'dismiss':
                if group_right < 2 or right < 3:
                    await app.sendGroupMessage(member.group, MessageChain.create([
                        Plain('再见啦~各位！我会想你们的')
                    ]))
                    await app.quit(member.group)
                    self.bot_information['statistics']['quit'] += 1
                    dataManage.save_obj(self.bot_information, 'baseInformation')
                    logManage.groupLog(getNow.toString(), qq, group_id, member.group.name, message + '; 小柒退群！')
                else:
                    reply_text = '权限不足，需要群管理或群主'
                    await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
                return
            elif message_code == 'mute' or message_code == 'bot off':
                if group_right < 2 or right < 3:
                    if group_id not in self.bot_information['mute']:
                        self.bot_information['mute'].append(group_id)
                        dataManage.save_obj(self.bot_information, 'baseInformation')
                        await app.sendGroupMessage(member.group, MessageChain.create([
                            Plain('QAQ，那我闭嘴了')
                        ]))
                    self.bot_information['statistics']['mute'] += 1
                    dataManage.save_obj(self.bot_information, 'baseInformation')
                    logManage.groupLog(getNow.toString(), qq, group_id, member.group.name, message + '; 小柒禁言！')
                else:
                    reply_text = '权限不足，需要群管理或群主'
                    await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
                return
            elif message_code == 'unmute' or message_code == 'bot on':
                if group_right < 2 or right < 3:
                    if group_id in self.bot_information['mute']:
                        self.bot_information['mute'].remove(group_id)
                        dataManage.save_obj(self.bot_information, 'baseInformation')
                        await app.sendGroupMessage(member.group, MessageChain.create([
                            Plain('呜呜呜，憋死我了，终于可以说话了')
                        ]))
                    self.bot_information['statistics']['unmute'] += 1
                    dataManage.save_obj(self.bot_information, 'baseInformation')
                    logManage.groupLog(getNow.toString(), qq, group_id, member.group.name, message + '; 小柒解除禁言！')
                else:
                    reply_text = '权限不足，需要群管理或群主'
                    await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
                return
            elif message_code == 'limit on':
                if group_right < 2 or right < 3:
                    if group_id not in self.bot_information['limit']:
                        self.bot_information['limit'].append(group_id)
                        dataManage.save_obj(self.bot_information, 'baseInformation')
                        await app.sendGroupMessage(member.group, MessageChain.create([
                            Plain('限制模式已开启，指令需艾特才能回复。解禁指令也别忘记艾特哦~')
                        ]))
                    self.bot_information['statistics']['operate'] += 1
                    dataManage.save_obj(self.bot_information, 'baseInformation')
                    logManage.groupLog(getNow.toString(), qq, group_id, member.group.name, message + '; 小柒解除禁言！')
                else:
                    reply_text = '权限不足，需要群管理或群主或小柒的管理'
                    await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
                return
            elif message_code == 'limit off':
                if group_right < 2 or right < 3:
                    if group_id in self.bot_information['limit']:
                        self.bot_information['limit'].remove(group_id)
                        dataManage.save_obj(self.bot_information, 'baseInformation')
                        await app.sendGroupMessage(member.group, MessageChain.create([
                            Plain('从现在起，指令无需艾特也能回复~')
                        ]))
                    self.bot_information['statistics']['operate'] += 1
                    dataManage.save_obj(self.bot_information, 'baseInformation')
                    logManage.groupLog(getNow.toString(), qq, group_id, member.group.name, message + '; 小柒解除限制！')
                else:
                    reply_text = '权限不足，需要群管理或群主或小柒的管理'
                    await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
                return

        # 如果被禁言那么直接返回
        if be_mute:
            return

        # 基本权限管理
        if message_code[:5] == 'send':
            master = await app.getFriend(self.bot_information['baseInformation']['Master_QQ'])

            if master is not None and len(message) > 5:
                await app.sendFriendMessage(master, MessageChain.create([
                    Plain(name + '(' + str(qq) + ')：' + message[5:].strip())
                ]))
                reply_text = '已经报告给主人了~'
                await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)

                self.bot_information['statistics']['operate'] += 1
                dataManage.save_obj(self.bot_information, 'baseInformation')
            return
        elif message_code == 'ai on':
            if mode == 0 or mode == 2:
                if qq in self.bot_information['noAI']['friend']:
                    self.bot_information['noAI']['friend'].remove(qq)
                    self.bot_information['statistics']['operate'] += 1
                    dataManage.save_obj(self.bot_information, 'baseInformation')
                    reply_text = '已开启智能回复~'
                else:
                    reply_text = '智能回复本身就是开启的'
                await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
            elif mode == 1:  # 如果是群聊则需要有权限，才能够操作
                if group_right < 2 or right < 3:
                    if group_id in self.bot_information['noAI']['group']:
                        self.bot_information['noAI']['group'].remove(group_id)
                        self.bot_information['statistics']['operate'] += 1
                        dataManage.save_obj(self.bot_information, 'baseInformation')
                        reply_text = '本群已开启艾特的智能回复~'
                    else:
                        reply_text = '本群本身就是开启艾特智能回复的'
                    await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
                else:
                    reply_text = '权限不足，需要群管理或群主'
                    await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
            return
        elif message_code == 'ai off':
            if mode == 0 or mode == 2:
                if qq not in self.bot_information['noAI']['friend']:
                    self.bot_information['noAI']['friend'].append(qq)
                    dataManage.save_obj(self.bot_information, 'baseInformation')
                    reply_text = '已关闭智能回复~'
                else:
                    reply_text = '智能回复本身就是关闭的'
                await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
            elif mode == 1:
                if group_right < 2 or right < 3:
                    if group_id not in self.bot_information['noAI']['group']:
                        self.bot_information['noAI']['group'].append(group_id)
                        dataManage.save_obj(self.bot_information, 'baseInformation')
                        reply_text = '本群已关闭艾特的智能回复~'
                    else:
                        reply_text = '本群本身就是关闭艾特智能回复的'
                    await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
                else:
                    reply_text = '权限不足，需要群管理或群主'
                    await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
            return
        elif mode == 1:
            if message_code == 'game on':
                if group_right < 2 or right < 3:
                    if group_id in self.bot_information['gameOff']:
                        self.bot_information['gameOff'].remove(group_id)
                        self.bot_information['statistics']['operate'] += 1
                        dataManage.save_obj(self.bot_information, 'baseInformation')
                        reply_text = '本群已开启游戏功能~'
                        await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
                else:
                    reply_text = '权限不足，需要群管理或群主'
                    await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
                return
            elif message_code == 'game off':
                if group_right < 2 or right < 3:
                    if group_id not in self.bot_information['gameOff']:
                        self.bot_information['gameOff'].append(group_id)
                        self.bot_information['statistics']['operate'] += 1
                        dataManage.save_obj(self.bot_information, 'baseInformation')
                        reply_text = '本群已关闭游戏功能~'
                        await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
                else:
                    reply_text = '权限不足，需要群管理或群主'
                    await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)
                return

        # -----------------------------------------------------------------------------------
        # 通过名字唤醒
        if message == self.bot_name:
            reply_text = '我在！'
            need_reply = True
            self.bot_information['statistics']['awaken'] += 1
            dataManage.save_obj(self.bot_information, 'baseInformation')

        # 帮助内容
        if not need_reply:
            if message == '帮助':
                reply_image = command.help_function()
                need_reply = True
            elif message == '打卡帮助':
                reply_image = command.help_clock()
                if mode == 0 or mode == 2:
                    reply_text = '这部分命令，只支持群聊哦~'
                need_reply = True
            elif message == '活动帮助':
                reply_image = command.help_activity()
                if mode == 0 or mode == 2:
                    reply_text = '这部分命令，只支持群聊哦~'
                need_reply = True
            elif message == '骰娘' or message == '骰娘帮助':
                reply_image = command.help_thrower()
                if mode == 0 or mode == 2:
                    reply_text = '这部分命令，只支持群聊哦~'
                need_reply = True
            elif message == '塔罗牌帮助':
                reply_image = command.help_tarot()
                need_reply = True
            elif message == '游戏帮助':
                reply_image = command.help_game()
                need_reply = True

            if need_reply:
                self.bot_information['statistics']['help'] += 1
                dataManage.save_obj(self.bot_information, 'baseInformation')

        # 打卡&活动
        if not need_reply and mode == 1:
            if message[:4] == '参加活动' or message[:4] == '参与活动':
                activityName = message[4:].strip()
                if len(activityName) == 0:
                    reply_text = '活动名不能为空'
                    need_reply = True
                else:
                    reply_text = operator.join_activity(group_id, qq, activityName)
                    need_at = True
                    need_reply = True
            elif message[:4] == '退出活动':
                activityName = message[4:].strip()
                if len(activityName) == 0:
                    reply_text = '活动名不能为空'
                    need_reply = True
                else:
                    reply_text = operator.quit_activity(group_id, qq, activityName)
                    need_at = True
                    need_reply = True
            elif message == '活动清单' or message == '活动列表':
                reply_text = operator.get_activity_list(group_id, app)
                need_reply = True
            elif self.clock['groupClock'].__contains__(group_id):
                if message == '打卡':
                    reply_text = name + clockIn.clockIn(group_id, qq)
                    need_reply = True
                elif message == '加入打卡计划':
                    reply_text = name + clockIn.joinClockIn(group_id, qq)
                    need_reply = True
                elif message == '退出打卡计划':
                    reply_text = name + clockIn.quitClockIn(group_id, qq)
                    need_reply = True
                elif message == '终止打卡计划' and right < 3:
                    reply_text = name + clockIn.stopClockIn(group_id)
                    need_reply = True

                elif message == '锁定打卡计划' and right < 3:
                    reply_text = clockIn.lockClockIn(group_id)
                    need_reply = True
                elif message == '解锁打卡计划' and right < 3:
                    reply_text = clockIn.unlockClockIn(group_id)
                    need_reply = True
                elif message == '锁定打卡计划 加入' and right < 3:
                    reply_text = clockIn.lockClockInEnter(group_id)
                    need_reply = True
                elif message == '解锁打卡计划 加入' and right < 3:
                    reply_text = clockIn.unlockClockInEnter(group_id)
                    need_reply = True
                elif message == '锁定打卡计划 退出' and right < 3:
                    reply_text = clockIn.lockClockInExit(group_id)
                    need_reply = True
                elif message == '解锁打卡计划 退出' and right < 3:
                    reply_text = clockIn.unlockClockInExit(group_id)
                    need_reply = True

                elif message == '取消打卡提醒' and right < 3:
                    reply_text = clockIn.offRemind(group_id)
                    need_reply = True
                elif message == '开启打卡提醒' and right < 3:
                    reply_text = clockIn.onRemind(group_id)
                    need_reply = True
                elif message == '取消打卡总结' and right < 3:
                    reply_text = clockIn.offSummary(group_id)
                    need_reply = True
                elif message == '开启打卡总结' and right < 3:
                    reply_text = clockIn.onSummary(group_id)
                    need_reply = True

            if need_reply:
                self.bot_information['statistics']['clock_activity'] += 1
                dataManage.save_obj(self.bot_information, 'baseInformation')
                logManage.groupLog(getNow.toString(), qq, group_id, member.group.name, message + "; 执行结果：" + reply_text)

        # 基础功能
        if not need_reply:
            if message[:2] == '天气':  # 开始的天气
                tmp = message[2:].strip()
                if tmp[0] != '#':
                    reply_text = weather.getWeather(tmp)
                    need_at = False
                    need_reply = True
            elif message[-2:] == '天气':  # 结尾的天气
                tmp = message[:-2].strip()
                if '这鬼' not in tmp and tmp[0] != '#':  # 语言优化处理（避免“这鬼天气”的语气词）
                    reply_text = weather.getWeather(tmp)
                    need_at = False
                    need_reply = True
            elif message[-3:] == '的天气':  # 结尾的天气
                tmp = message[:-3].strip()
                if tmp[0] != '#':
                    reply_text = weather.getWeather(tmp)
                    need_at = False
                    need_reply = True

            elif message == '色子' or message == '骰子':
                reply_text = BaseFunction.dice()
                need_at = True
                need_reply = True
            elif message == '抛硬币' or message == '硬币':
                reply_text = BaseFunction.coin()
                need_at = True
                need_reply = True
            elif message == '运势':
                reply_text = self.luck.get_luck(qq)
                need_at = True
                need_reply = True

            elif message == '微博热搜':
                reply_text = weiboHot.getHot()
                need_reply = True
            elif message == '百度热搜':
                reply_text = baidu.getHot()
                need_reply = True

            elif message == '四级词汇' or message == '四级单词' or message == '4级词汇' or message == '4级单词':
                vocabularyNumber = 1
                reply_text = BaseFunction.get_vocabulary4(vocabularyNumber)
                need_reply = True
            elif message[:5] == '四级词汇 ' or message[:5] == '四级单词 ' or message[:5] == '4级词汇 ' or message[:5] == '4级单词 ':
                vocabularyNumber = int(message[5:].strip())
                if vocabularyNumber <= 0:
                    vocabularyNumber = 1
                reply_text = BaseFunction.get_vocabulary4(vocabularyNumber)
                need_reply = True
            elif message == '六级词汇' or message == '六级单词' or message == '6级词汇' or message == '6级单词':
                vocabularyNumber = 1
                reply_text = BaseFunction.get_vocabulary6(vocabularyNumber)
                need_reply = True
            elif message[:5] == '六级词汇 ' or message[:5] == '六级单词 ' or message[:5] == '6级词汇 ' or message[:5] == '6级单词 ':
                vocabularyNumber = int(message[5:].strip())
                if vocabularyNumber <= 0:
                    vocabularyNumber = 1
                reply_text = BaseFunction.get_vocabulary6(vocabularyNumber)
                need_reply = True

            elif message == '拾取漂流瓶' or message == '捡漂流瓶' or message == '捞漂流瓶':
                reply_text = self.bottle.pick()
                need_reply = True
            elif message[:4] == '扔漂流瓶' and message_len > 4:
                text = message[4:].strip()
                if len(text) > 0:
                    reply_text = self.bottle.throw(qq, text)
                    need_reply = True


            if need_reply:
                self.bot_information['statistics']['base_function'] += 1
                dataManage.save_obj(self.bot_information, 'baseInformation')

        # 文摘、脏话、情话
        if not need_reply:
            if message == '文摘':
                reply_text = talk.poem()
                need_reply = True
            elif message == '情话':
                reply_text = talk.loveTalk()
                need_reply = True
            elif message == '骂我一句' or message == '骂我' or message == '再骂' or message == '你再骂' or message == '脏话':
                if mode == 0 or mode == 2 or (mode == 1 and group_id in self.bot_information['cursePlanGroup']):
                    reply_text = talk.swear()
                    need_reply = True

            if need_reply:
                self.bot_information['statistics']['talk'] += 1
                dataManage.save_obj(self.bot_information, 'baseInformation')

        # 涩图
        if not need_reply and mode == 1 and group_id in self.bot_information['pixiv']:
            if message == '涩图':
                await app.sendGroupMessage(member.group, MessageChain.create([
                    Plain('该功能并未优化暂时被锁定，不开放。具体开放日期待定，是开发情况而定。')
                ]))
                need_reply = True
                # image = self.pixiv.search('lolicon')
                # if len(image) > 0:
                #     for url in image:
                #         await app.sendGroupMessage(member.group, MessageChain.create([
                #             Image.fromNetworkAddress(url)
                #         ]))
                #     need_reply = True
                # else:
                #     reply_text = '获取失败！请联系主人，可能梯子又挂了'
                #     need_reply = True
            elif message[:2] == '搜图':
                await app.sendGroupMessage(member.group, MessageChain.create([
                    Plain('稍等片刻，马上就来~(测试功能，不对外开放)')
                ]))
                image = self.pixiv.search(message[2:].strip())
                if len(image) > 0:
                    for url in image:
                        await app.sendGroupMessage(member.group, MessageChain.create([
                            Image.fromNetworkAddress(url)
                        ]))
                    need_reply = True
                else:
                    reply_text = '获取失败！请联系主人，可能梯子又挂了'
                    need_reply = True

            if need_reply:
                self.bot_information['statistics']['image_search'] += 1
                dataManage.save_obj(self.bot_information, 'baseInformation')

        # 指令
        if not need_reply:
            if 0 < message_code_len < 1000 and message_code[0].isalnum():
                (reply_text, need_at, reply_image) = command.function(message_code, member, app, group_id, self.bot_information, mode)
                need_reply = True

                if reply_text == '*运势*':
                    reply_text = self.luck.get_luck(qq)
                    need_at = True

            if need_reply:
                self.bot_information['statistics']['command'] += 1
                dataManage.save_obj(self.bot_information, 'baseInformation')

        # -----------------------------------------------------------------------------------
        # 管理员操作
        if not need_reply:
            if not need_reply:
                (need_reply, need_at, reply_text, reply_image) = await operator.administrator_operation(
                    message,
                    group_id,
                    qq,
                    app,
                    member,
                    self.bot_information,
                    right,
                    group_right,
                    mode)

            if need_reply:
                self.bot_information['statistics']['operate'] += 1
                dataManage.save_obj(self.bot_information, 'baseInformation')

        # -----------------------------------------------------------------------------------
        # rpg游戏
        if not need_reply:
            (need_reply, reply_text, reply_image, at_qq, need_at) = await rpg.menu(
                message,
                group_id,
                member,
                app,
                self.bot_information,
                right,
                be_at)

            if need_reply:
                self.bot_information['statistics']['game'] += 1
                dataManage.save_obj(self.bot_information, 'baseInformation')

        # -----------------------------------------------------------------------------------
        # 群自己设定的关键词回复
        if not need_reply and mode == 1:
            (need_reply, reply_text, reply_image, at_qq, need_at) = keyReply.reply(
                message,
                member,
                self.bot_information)

            if need_reply:
                self.bot_information['statistics']['auto_reply'] += 1
                dataManage.save_obj(self.bot_information, 'baseInformation')

        # -----------------------------------------------------------------------------------
        # 自动加一
        if not need_reply and mode == 1:
            if not self.message_tmp.__contains__(group_id):
                self.message_tmp[group_id] = get_message.messageChain
            else:
                reply_chain = self.message_tmp[group_id]
                tmp = str(reply_chain.asDisplay())
                self.message_tmp[group_id] = get_message.messageChain  # 将记录的上一次的消息更改为这次收到的消息
                if 'xml' not in tmp and tmp[0] != '[' and tmp[-1] != ']':
                    if tmp == message and tmp != self.last_reply:
                        await app.sendGroupMessage(member.group, reply_chain.asSendable())
                        need_reply = True
                        self.last_reply = tmp

            if need_reply:
                self.bot_information['statistics']['auto_repeat'] += 1
                dataManage.save_obj(self.bot_information, 'baseInformation')

        # 智能回复
        if not need_reply:
            (need_reply, reply_text, reply_image, at_qq, need_at) = autoReply.reply(
                message,
                be_at,
                self.bot_information,
                name,
                group_id,
                qq,
                mode)

            if need_reply:
                self.bot_information['statistics']['auto_reply'] += 1
                dataManage.save_obj(self.bot_information, 'baseInformation')

        if need_reply:
            if reply_text != '':
                self.last_reply = reply_text
            await send_message(app, mode, member, reply_text, reply_image, need_at, at_qq)

    async def new_friend(self, app, event):
        self.bot_information = dataManage.load_obj('baseInformation')
        master = await app.getFriend(self.bot_information['baseInformation']['Master_QQ'])

        if master is not None:
            await app.sendFriendMessage(master, MessageChain.create([
                Plain('有新的好友申请' + str(event.supplicant) + '！')
            ]))
        await event.accept()

        time.sleep(10)

        qq = event.supplicant
        name = event.nickname
        member = await app.getFriend(qq)
        print(member)
        if member is not None:
            reply = '你好呀！' + name + '\n'
            reply += '小柒的快速上手指南：\n'
            reply += '可以通过输入“帮助”来获取所有的指令帮助；如果只是为了刷游戏，记得先输入指令“*ai off”；如果是骰娘呢，请先输入“骰娘帮助”；'
            reply += '；如果有任何疑问可以加小柒的官方Q群：479504567，在群聊里可以告诉主人通过群邀请，以及获取到管理员权限解锁一些新功能\n'
            reply += '特别申明：不要将小柒踢出任何群聊，或者在任何群聊禁言小柒，这些都有专门的指令代替！！！邀请加入群聊要主人人工审核一下，可能会有延迟（取决于那个笨蛋主人有没有起床）。'
            await app.sendFriendMessage(member, MessageChain.create([
                Plain(reply)
            ]))

    async def nudge(self, app, event):
        print(event.target)
        print(event.subject)