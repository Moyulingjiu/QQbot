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

import plugins.dataManage as dataManage
from plugins import talk
from plugins import command
from plugins import clockIn
from plugins import logManage
from plugins import getNow

import sys


# ==========================================================
# 监听模块
async def send_clock_message(group_id, clock, app):
    group = await app.getGroup(group_id)

    if clock['groupClock'].__contains__(group_id):
        reply_text = '记得打卡呀：'
        message = MessageChain.create([
            Plain(reply_text)
        ])
        for key, value in clock['dictClockPeople'][group_id].items():
            if not value['clockIn']:
                message.plus(MessageChain.create([
                    Plain('\n'),
                    At(key)
                ]))

        await app.sendGroupMessage(group, message)
        return True
    return False


# ==========================================================
# 管理员模块
async def administrator_operation(app, message, qq, name, group_id, mode, member, bot_config, config, statistics, right, group_right):
    bot_qq = bot_config['qq']
    bot_name = bot_config['name']
    master_qq = bot_config['master']
    clock = dataManage.read_clock()

    message_len = len(message)
    message4 = message[:4]
    message5 = message[:5]
    message6 = message[:6]
    message7 = message[:7]
    message8 = message[:8]

    need_reply = False
    need_at = False
    reply_text = ''
    reply_image = ''

    # ===================================================================================
    # ===================================================================================
    # 主人权限
    if message == '主人帮助':
        if right < 1:
            reply_image = command.help_master()
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message == bot_name + '关机':
        if right < 1:
            logManage.log(getNow.toString(), bot_name + '关机！')
            if group_id == 0:
                await app.sendFriendMessage(member, MessageChain.create([
                    Plain('小柒已关机~请手动重新启动小柒')
                ]))
            else:
                await app.sendGroupMessage(member.group, MessageChain.create([
                    Plain('小柒已关机~请手动重新启动小柒')
                ]))

            print('退出')
            sys.exit()
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

    elif message == '查看机器人信息':
        if right < 1:
            reply_text = '机器人名字：' + bot_name + '\n机器人QQ：' + str(bot_qq) + '\n主人QQ：' + str(master_qq)
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    elif message4 == '删除文摘' and message_len > 4:
        if right < 1:
            tmp = message[4:].strip()
            if tmp.isdigit():
                reply_text = talk.delPoem(int(tmp))
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message4 == '删除情话' and message_len > 4:
        if right < 1:
            tmp = message[4:].strip()
            if tmp.isdigit():
                reply_text = talk.delLoveTalk(int(tmp))
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message4 == '删除脏话' and message_len > 4:
        if right < 1:
            tmp = message[4:].strip()
            if tmp.isdigit():
                reply_text = talk.delSwear(int(tmp))
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    elif message7 == '添加黑名单 群' and message_len > 7:
        if right < 1:
            tmp = message[7:].strip().split(' ')
            if len(tmp) == 2 and tmp[0].isdigit():
                reply_text = add_blacklist_group(int(tmp[0]), tmp[1], bot_config)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message7 == '添加黑名单 人' and message_len > 7:
        if right < 1:
            tmp = message[7:].strip().split(' ')
            if len(tmp) == 2 and tmp[0].isdigit():
                reply_text = add_blacklist_member(int(tmp[0]), tmp[1], bot_config)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message7 == '移除黑名单 群' and message_len > 7:
        if right < 1:
            tmp = message[7:].strip()
            if tmp.isdigit():
                reply_text = remove_blacklist_group(int(tmp), bot_config)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message7 == '移除黑名单 人' and message_len > 7:
        if right < 1:
            tmp = message[7:].strip()
            if tmp.isdigit():
                reply_text = remove_blacklist_member(int(tmp), bot_config)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    elif message6 == '修改版本信息' and message_len > 6:
        if right < 1:
            reply_text = change_version(message[6:].strip(), bot_config)
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message7 == '修改机器人名字' and message_len > 7:
        if right < 1:
            reply_text = change_bot_name(message[7:].strip(), bot_config)
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message7 == '修改机器人QQ' and message_len > 7:
        if right < 1:
            tmp = message[7:].strip()
            if tmp.isdigit():
                reply_text = change_bot_qq(int(tmp), bot_config)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    # 屏蔽词不用strip，因为可能有一些带空格屏蔽词
    elif message8 == '添加全局屏蔽词 ' and message_len > 8:
        if right < 1:
            reply_text = add_screen_word(message[8:])
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message8 == '删除全局屏蔽词 ' and message_len > 8:
        if right < 1:
            reply_text = del_screen_word(message[8:])
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message == '查看全局屏蔽词':
        if right < 1:
            reply_text = view_screen_word()
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    elif message == '查看管理员':
        if right < 1:
            reply_text = str(bot_config["administrator"])
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message5 == '添加管理员' and message_len > 5:
        if right < 1:
            tmp = message[5:].strip()
            if tmp.isdigit():
                reply_text = add_administrator(int(tmp), bot_config)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message5 == '删除管理员' and message_len > 5:
        if right < 1:
            tmp = message[5:].strip()
            if tmp.isdigit():
                reply_text = del_administrator(int(tmp), bot_config)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    elif message4 == '开启脏话' and message_len > 4:
        if right < 1:
            tmp = message[4:].strip()
            if tmp.isdigit():
                reply_text = add_curse_plan_group(dataManage.read_group(int(tmp)), int(tmp))
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message4 == '关闭脏话' and message_len > 4:
        if right < 1:
            tmp = message[4:].strip()
            if tmp.isdigit():
                reply_text = del_curse_plan_group(dataManage.read_group(int(tmp)), int(tmp))
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    elif message == '清空每分钟回复条数':
        if right < 1:
            statistics['lastMinute'] = 0
            dataManage.save_statistics(statistics)
            reply_text = '清空成功！'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    elif message == '开启涩图' and mode == 1:
        if right < 1:
            reply_text = add_image_search_group(config, group_id)
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message == '关闭涩图' and mode == 1:
        if right < 1:
            reply_text = del_image_search_group(config, group_id)
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    # ===================================================================================
    # ===================================================================================
    # 管理员权限
    if not need_reply:
        if message == '管理员帮助':
            if right < 2:
                reply_image = command.help_administrator()
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif message5 == '添加贡献者' and message_len > 5:
            if right < 2:
                tmp = message[5:].strip()
                if tmp.isdigit():
                    reply_text = add_contributors(int(tmp), bot_config)
                else:
                    reply_text = '格式错误'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message5 == '删除贡献者' and message_len > 5:
            if right < 2:
                tmp = message[5:].strip()
                if tmp.isdigit():
                    reply_text = del_contributors(int(tmp), bot_config)
                else:
                    reply_text = '格式错误'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message == '查看贡献者':
            if right < 2:
                reply_text = str(bot_config["contributor"])
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif message == '查看黑名单 人':
            if right < 2:
                reply_text = str(bot_config["blacklist_member"])
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message == '查看黑名单 群':
            if right < 2:
                reply_text = str(bot_config["blacklist_group"])
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif message4 == '添加文摘' and message_len > 4:
            if right < 2:
                poem_list = message.split(' ')
                del poem_list[0]
                reply_text = talk.addPoem(poem_list)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message4 == '添加情话' and message_len > 4:
            if right < 2:
                love_talk_list = message.split(' ')
                del love_talk_list[0]
                reply_text = talk.addLoveTalk(love_talk_list)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message4 == '添加脏话' and message_len > 4:
            if right < 2:
                swear_list = message.split(' ')
                del swear_list[0]
                reply_text = talk.addSwear(swear_list)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message == '文摘条数':
            if right < 2:
                reply_text = talk.numPoem()
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message == '情话条数':
            if right < 2:
                reply_text = talk.numLoveTalk()
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message == '脏话条数':
            if right < 2:
                reply_text = talk.numSwear()
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message == '版本信息' or message == '查看版本信息':
            if right < 2:
                reply_text = '当前版本为：' + bot_config['version']
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif (message == '开启脏话' or message == '脏话开启') and mode == 1:
            if right < 2 or group_right < 2:
                reply_text = add_curse_plan_group(config, group_id)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif (message == '关闭脏话' or message == '脏话关闭') and mode == 1:
            if right < 2 or group_right < 2:
                reply_text = del_curse_plan_group(config, group_id)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
    # ===================================================================================
    # ===================================================================================
    # 贡献者权限
    if not need_reply:
        if message == '贡献者帮助':
            if right < 3:
                reply_image = command.help_contributor()
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif message == '添加打卡计划' and mode == 1:
            if right < 3:
                reply_text = clockIn.addClockIn(group_id)
                need_at = True
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message == '打卡提醒' and clock['groupClock'].__contains__(group_id):
            if right < 3:
                reply_text = await send_clock_message(group_id, clock, app)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = False
        elif message4 == '打卡情况' and message_len > 4:
            if right < 3:
                tmp = message[4:].strip()
                if tmp.isdigit():
                    tmp = int(tmp)
                    if clock['groupClock'].__contains__(tmp):
                        reply_text = '未打卡名单：\n'
                        for key, value in clock['dictClockPeople'][tmp].items():
                            if not value['clockIn']:
                                member_tmp = await app.getMember(tmp, key)
                                reply_text += member_tmp.name + '(' + str(key) + ')\n'
                    else:
                        reply_text = '该群没有打卡计划哦！'
                else:
                    reply_text = '格式错误'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = False
        elif message == '打卡情况' and mode == 1:
            if right < 3:
                if clock['groupClock'].__contains__(group_id):
                    reply_text = '未打卡名单：\n'
                    for key, value in clock['dictClockPeople'][group_id].items():
                        if not value['clockIn']:
                            member_tmp = await app.getMember(group_id, key)
                            reply_text += member_tmp.name + '(' + str(key) + ')\n'
                else:
                    reply_text = '本群没有打卡计划哦！'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif message5 == '添加回复 ' and message_len > 5 and mode == 1:
            if right < 3:
                stringList = message.split(' ')
                if len(stringList) == 3:
                    reply_text = add_question_reply(stringList[1], stringList[2], config, group_id)
                elif len(stringList) == 4:
                    reply_text = add_question_reply_at(stringList[1], stringList[2], stringList[3], config, group_id)
                else:
                    reply_text = '格式错误！请检查空格'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message5 == '删除回复 ' and message_len > 5 and mode == 1:
            if right < 3:
                stringList = message.split(' ')
                if len(stringList) == 3:
                    reply_text = del_question_reply(stringList[1], stringList[2], config, group_id)
                elif len(stringList) == 4:
                    reply_text = del_question_reply_at(stringList[1], stringList[2], stringList[3], config, group_id)
                else:
                    reply_text = '格式错误！请检查空格'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message5 == '添加回复*' and message_len > 5 and mode == 1:
            if right < 3:
                stringList = message.split('*')
                if len(stringList) == 3:
                    reply_text = add_question_reply(stringList[1], stringList[2], config, group_id)
                elif len(stringList) == 4:
                    reply_text = add_question_reply_at(stringList[1], stringList[2], stringList[3], config, group_id)
                else:
                    reply_text = '格式错误！请检查星号'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message5 == '删除回复*' and message_len > 5 and mode == 1:
            if right < 3:
                stringList = message.split('*')
                if len(stringList) == 3:
                    reply_text = del_question_reply(stringList[1], stringList[2], config, group_id)
                elif len(stringList) == 4:
                    reply_text = del_question_reply_at(stringList[1], stringList[2], stringList[3], config, group_id)
                else:
                    reply_text = '格式错误！请检查星号'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif message6 == '添加关键词 ' and message_len > 6 and mode == 1:
            if right < 3:
                stringList = message.split(' ')
                if len(stringList) == 3:
                    reply_text = add_key_reply(stringList[1], stringList[2], config, group_id)
                elif len(stringList) == 4:
                    reply_text = add_key_reply_at(stringList[1], stringList[2], stringList[3], config, group_id)
                else:
                    reply_text = '格式错误！请检查空格'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message6 == '删除关键词 ' and message_len > 6 and mode == 1:
            if right < 3:
                stringList = message.split(' ')
                if len(stringList) == 3:
                    reply_text = del_key_reply(stringList[1], stringList[2], config, group_id)
                elif len(stringList) == 4:
                    reply_text = del_key_reply_at(stringList[1], stringList[2], stringList[3], config, group_id)
                else:
                    reply_text = '格式错误！请检查空格'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message6 == '添加关键词*' and message_len > 6 and mode == 1:
            if right < 3:
                stringList = message.split('*')
                if len(stringList) == 3:
                    reply_text = add_key_reply(stringList[1], stringList[2], config, group_id)
                elif len(stringList) == 4:
                    reply_text = add_key_reply_at(stringList[1], stringList[2], stringList[3], config, group_id)
                else:
                    reply_text = '格式错误！请检查星号'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message6 == '删除关键词*' and message_len > 6 and mode == 1:
            if right < 3:
                stringList = message.split('*')
                if len(stringList) == 3:
                    reply_text = del_key_reply(stringList[1], stringList[2], config, group_id)
                elif len(stringList) == 4:
                    reply_text = del_key_reply_at(stringList[1], stringList[2], stringList[3], config, group_id)
                else:
                    reply_text = '格式错误！请检查星号'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif message7 == '关键词回复概率' and message_len > 7 and mode == 1:
            if right < 3:
                reply_text = edit_key_probability(message[7:].strip(), config, group_id)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif message4 == '发起活动' and message_len > 4 and mode == 1:
            if right < 3:
                stringList = message[4:].strip().split(' ')
                if len(stringList) != 2:
                    reply_text = '参数错误'
                else:
                    activity_name = stringList[0]
                    lastMinute = 1
                    if stringList[1][-2:] == '分钟':
                        lastMinute = int(stringList[1][:-2])
                    elif stringList[1][-2:] == '小时':
                        lastMinute = int(stringList[1][:-2]) * 60
                    elif stringList[1][-1:] == '天':
                        lastMinute = int(stringList[1][:-1]) * 1440
                    else:
                        lastMinute = int(stringList[1])

                    if len(activity_name) == 0:
                        reply_text = '活动名不能为空'
                    elif lastMinute <= 0:
                        reply_text = '报名时间必须大于0'
                    else:
                        reply_text = add_activity(group_id, qq, activity_name, lastMinute)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message4 == '删除活动' and message_len > 4 and mode == 1:
            if right < 3:
                activity_name = message[4:].strip()
                if len(activity_name) == 0:
                    reply_text = '活动名不能为空'
                else:
                    reply_text = del_activity(group_id, qq, activity_name)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message6 == '查看活动名单' and message_len > 6 and mode == 1:
            if right < 3:
                activity_name = message[6:].strip()
                if len(activity_name) == 0:
                    reply_text = '活动名不能为空'
                else:
                    reply_text = await view_activity(group_id, activity_name, app)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif message == '申请权限' and mode == 1:
            if group_right == 0:
                member_list = await app.memberList(group_id)
                if len(member_list) > 5:
                    reply_text = add_contributors(qq, bot_config)
                    if reply_text == '添加成功~':
                        reply_text = '申请贡献者权限成功，可以输入“贡献者帮助”获取管理指令，需要更高权限的请前往' + bot_name + '官方群(479504567)找主人要'
                    elif '正确' in reply_text:
                        reply_text = '因为未知原因申请失败，请稍后重试'
                    else:
                        reply_text = reply_text.replace('他', '你').replace('该成员', '你')
                else:
                    reply_text = '你的群需要超过5人，请去' + bot_name + '官方群(479504567)找主人要权限'
            else:
                reply_text = '你并非群主（群需要超过5人），请去' + bot_name + '官方群(479504567)找主人要权限'
            need_reply = True

        # 屏蔽词不用strip，因为可能有一些带空格屏蔽词
        elif message6 == '添加屏蔽词 ' and message_len > 6 and mode == 1:
            if group_right < 2 or right < 2:
                reply_text = add_group_screen_word(group_id, config, message[6:])
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message6 == '删除屏蔽词 ' and message_len > 6 and mode == 1:
            if group_right < 2 or right < 2:
                reply_text = del_group_screen_word(group_id, config, message[6:])
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message == '查看屏蔽词' and mode == 1:
            if group_right < 2 or right < 2:
                reply_text = view_group_screen_word(config)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message == '清空屏蔽词' and mode == 1:
            if group_right < 2 or right < 2:
                reply_text = clear_group_screen_word(qq, group_id, config)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
            

    if need_reply:
        if message != '贡献者帮助' and message != '管理员帮助' and message != '主人帮助':
            logManage.member_log(getNow.toString(), qq, message + "; 执行结果：" + reply_text)
        else:
            logManage.member_log(getNow.toString(), qq, message + "; 执行结果：参见command.py里的帮助内容")

    return need_reply, need_at, reply_text, reply_image


# ==========================================================
# 权限操作

# 添加贡献者
def add_contributors(qq, config):
    if qq > 0:
        if qq == config['master']:
            reply_text = '他是主人哦~'
        elif qq in config['administrator']:
            reply_text = '该成员已经是管理员了'
        elif qq in config['contributor']:
            reply_text = '该成员已经在贡献者计划中了哦~'
        else:
            config['contributor'].append(qq)
            dataManage.save_config(config)
            reply_text = '添加成功~'
    else:
        reply_text = '诶？这个QQ正确吗？'
    return reply_text


# 移除贡献者
def del_contributors(qq, config):
    if qq > 0:
        if qq == config['master']:
            reply_text = '他是主人哦~'
        elif qq in config['administrator']:
            reply_text = '该成员已经是管理员啦，不是贡献者'
        elif not qq in config['contributor']:
            reply_text = '该成员不在贡献者计划中哦~'
        else:
            config['contributor'].remove(qq)
            dataManage.save_config(config)
            reply_text = '删除成功~'
    else:
        reply_text = '诶？这个QQ正确吗？'
    return reply_text


# 添加管理员
def add_administrator(qq, config):
    if qq > 0:
        if qq == config['master']:
            reply_text = '他是主人哦~'
        elif qq in config['administrator']:
            reply_text = '该成员已经是管理员了'
        elif qq in config['contributor']:
            config["contributor"].remove(qq)
            config["administrator"].append(qq)
            dataManage.save_config(config)
            reply_text = '已将该成员的权限从贡献者升为了管理员'
        else:
            config["administrator"].append(qq)
            dataManage.save_config(config)
            reply_text = '添加成功~'
    else:
        reply_text = '诶？这个QQ正确吗？'
    return reply_text


# 移除管理员
def del_administrator(qq, config):
    if qq > 0:
        if qq == config['master']:
            reply_text = '他是主人哦~不能从管理员中移除'
        elif not (qq in config["administrator"]):
            reply_text = '该成员不是管理员哦~'
            if qq in config["contributor"]:
                reply_text += '但是该成员是贡献者，已经移除他的权限'
                config["contributor"].remove(qq)
                dataManage.save_config(config)
        else:
            config["administrator"].remove(qq)
            dataManage.save_config(config)
            reply_text = '删除成功~'
    else:
        reply_text = '诶？这个QQ正确吗？'
    return reply_text


# ==========================================================
# 基本信息

# 修改版本
def change_version(version, config):
    config['version'] = version
    dataManage.save_config(config)
    return '修改成功！当前版本：' + version


# 修改名字
def change_bot_name(name, config):
    config['name'] = name
    dataManage.save_config(config)
    return '修改成功！当前名字：' + name


# 修改机器人QQ
def change_bot_qq(qq, config):
    config['qq'] = qq
    dataManage.save_config(config)
    return '修改成功！当前QQ：' + str(qq)


# ==========================================================
# 黑名单操作

def add_blacklist_group(group_id, reason, config):
    if config['blacklist_group'].__contains__(group_id):
        return '该群已经因为“' + config['blacklist_group'][group_id] + '”被列入黑名单'
    config['blacklist_group'][group_id] = reason
    dataManage.save_config(config)
    return '已经将群' + str(group_id) + '加入黑名单'


def add_blacklist_member(qq, reason, config):
    if config['blacklist_member'].__contains__(qq):
        return '该人已经因为“' + config['blacklist_member'][qq] + '”被列入黑名单'
    config['blacklist_member'][qq] = reason
    dataManage.save_config(config)
    return '已经将人' + str(qq) + '加入黑名单'


def remove_blacklist_group(group_id, config):
    if not config['blacklist_group'].__contains__(group_id):
        return '该群不在黑名单里'
    del config["blacklistGroup"][group_id]
    dataManage.save_config(config)
    return '已经将群' + str(group_id) + '移除黑名单'


def remove_blacklist_member(qq, config):
    if not config['blacklist_group'].__contains__(qq):
        return '该人不在黑名单里'
    del config["blacklist_group"][qq]
    dataManage.save_config(config)
    return '已经将人' + str(qq) + '移除黑名单'


# ==========================================================
# 屏蔽词操作

# 添加屏蔽词
def add_screen_word(word):
    screenWords = dataManage.read_screen_word()
    if word in screenWords:
        return '已经有该屏蔽词了'

    screenWords.append(word)
    dataManage.save_screen_word(screenWords)
    return '添加成功~！'


# 删除屏蔽词
def del_screen_word(word):
    screenWords = dataManage.read_screen_word()
    if word not in screenWords:
        return '没有这个词语哦！'
    screenWords.remove(word)
    dataManage.save_screen_word(screenWords)
    return '删除成功'


# 查看屏蔽词
def view_screen_word():
    screenWords = dataManage.read_screen_word()
    return str(screenWords)

# 添加群内屏蔽词
def add_group_screen_word(group_id, config, word):
    if word in config['prohibited_word']:
        return '已经有该屏蔽词了'
    if word.isdigit():
        return '屏蔽词不能为纯数字哦~'

    config['prohibited_word'].append(word)
    dataManage.save_group(group_id, config)
    return '添加成功~！目前屏蔽词个数：' + str(len(config['prohibited_word']))


# 删除群内屏蔽词
def del_group_screen_word(group_id, config, word):
    if word not in config['prohibited_word']:
        return '没有这个词语哦！'
    config['prohibited_word'].remove(word)
    dataManage.save_group(group_id, config)
    return '删除成功目前屏蔽词个数：' + str(len(config['prohibited_word']))


# 查看群内屏蔽词
def view_group_screen_word(config):
    if len(config['prohibited_word']) == 0:
        return '暂无任何屏蔽词'
    reply = '开启的屏蔽词如下：'
    for key in config['prohibited_word']:
        reply += '\n' + key
    return reply


# 清空群内屏蔽词
def clear_group_screen_word(qq, group_id, config):
    if len(config['prohibited_word']) == 0:
        return '暂无任何屏蔽词'
    user = dataManage.read_user(qq)
    user['buffer']['id'] = 2
    user['buffer']['buffer'] = group_id
    dataManage.save_user(qq, user)
    return '请问是否清空屏蔽词，回答“是”或者“否”'


# ==========================================================
# 关键词操作
KeyScreenWord = ['RecoveryProbability', 'reply_text', '~$~']


# 添加绝对匹配
def add_question_reply(word, reply_text, config, group_id):
    if word in KeyScreenWord:
        return word + '为保留字，不可以添加'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以添加'

    if len(config['key_reply']['question']) >= 100:
        return '最多只可以添加100个回复哦~'

    if config['key_reply']['question'].__contains__(word):
        if reply_text in config['key_reply']['question'][word]:
            return '已经有该回复了'
        else:
            if len(config['key_reply']['question'][word]) >= 15:
                return '单个关键词只能添加15个回复~'
            config['key_reply']['question'][word].append(reply_text)
            dataManage.save_group(group_id, config)
            return '添加成功~'
    else:
        config['key_reply']['question'][word] = [reply_text]
        dataManage.save_group(group_id, config)
        return '添加成功~'


# 删除绝对匹配
def del_question_reply(word, reply_text, config, group_id):
    if word in KeyScreenWord:
        return word + '为保留字，不可以删除'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以删除'

    if config['key_reply']['question'].__contains__(word):
        if reply_text in config['key_reply']['question'][word]:
            config['key_reply']['question'][word].remove(reply_text)
            if len(config['key_reply']['question'][word]) == 0:
                del config['key_reply']['question'][word]
            dataManage.save_group(group_id, config)
            return '删除成功~！'
        else:
            return '没有该词组配对~'
    else:
        return '没有该词组配对~'


# 添加绝对匹配（带at）
def add_question_reply_at(word, reply_text, at, config, group_id):
    if word in KeyScreenWord:
        return word + '为保留字，不可以添加'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以添加'

    if len(config['key_reply']['question_at']) >= 100:
        return '最多只可以添加100个回复哦~'

    if at == '全体成员':
        at = -1
    elif at == '触发人':
        at = 0
    elif at.isdigit():
        at = int(at)
    else:
        return '艾特对象格式错误'
    if at != -1 and at < 0:
        return '艾特对象格式错误'

    reply_text = reply_text + '~$~' + str(at)

    if config['key_reply']['question_at'].__contains__(word):
        if reply_text in config['key_reply']['question_at'][word]:
            return '已经有该回复了'
        else:
            if len(config['key_reply']['question_at'][word]) >= 15:
                return '单个关键词只能添加15个回复~'
            config['key_reply']['question_at'][word].append(reply_text)
            dataManage.save_group(group_id, config)
            return '添加成功~'
    else:
        config['key_reply']['question_at'][word] = [reply_text]
        dataManage.save_group(group_id, config)
        return '添加成功~'


# 删除绝对匹配（带at）
def del_question_reply_at(word, reply_text, at, config, group_id):
    if word in KeyScreenWord:
        return word + '为保留字，不可以删除'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以删除'

    if at == '全体成员':
        at = -1
    elif at == '触发人':
        at = 0
    elif at.isdigit():
        at = int(at)
    else:
        return '艾特对象格式错误'
    if at != -1 and at < 0:
        return '艾特对象格式错误'

    reply_text = reply_text + '~$~' + str(at)

    if config['key_reply']['question_at'].__contains__(word):
        if reply_text in config['key_reply']['question_at'][word]:
            config['key_reply']['question_at'][word].remove(reply_text)
            if len(config['key_reply']['question_at'][word]) == 0:
                del config['key_reply']['question_at'][word]
            dataManage.save_group(group_id, config)
            return '删除成功~！'
        else:
            return '没有该词组配对~'
    else:
        return '没有该词组配对~'


# =====================
# 添加关键词匹配
def add_key_reply(word, reply_text, config, group_id):
    if word in KeyScreenWord:
        return word + '为保留字，不可以添加'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以添加'

    if len(config['key_reply']['key']) >= 100:
        return '最多只可以添加100个回复哦~'

    if config['key_reply']['key'].__contains__(word):
        if reply_text in config['key_reply']['key'][word]:
            return '已经有该回复了'
        else:
            if len(config['key_reply']['key'][word]) >= 15:
                return '单个关键词只能添加15个回复~'
            config['key_reply']['key'][word].append(reply_text)
            dataManage.save_group(group_id, config)
            return '添加成功~'
    else:
        config['key_reply']['key'][word] = [reply_text]
        dataManage.save_group(group_id, config)
        return '添加成功~'


# 删除关键词匹配
def del_key_reply(word, reply_text, config, group_id):
    if word in KeyScreenWord:
        return word + '为保留字，不可以删除'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以删除'

    if config['key_reply']['key'].__contains__(word):
        if reply_text in config['key_reply']['key'][word]:
            config['key_reply']['key'][word].remove(reply_text)
            if len(config['key_reply']['key'][word]) == 0:
                del config['key_reply']['key'][word]
            dataManage.save_group(group_id, config)
            return '删除成功~！'
        else:
            return '没有该词组配对~'
    else:
        return '没有该词组配对~'


# 添加关键词匹配（带at）
def add_key_reply_at(word, reply_text, at, config, group_id):
    if word in KeyScreenWord:
        return word + '为保留字，不可以添加'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以添加'

    if len(config['key_reply']['key_at']) >= 100:
        return '最多只可以添加100个回复哦~'

    if at == '全体成员':
        at = -1
    elif at == '触发人':
        at = 0
    elif at.isdigit():
        at = int(at)
    else:
        return '艾特对象格式错误'
    if at != -1 and at < 0:
        return '艾特对象格式错误'

    reply_text = reply_text + '~$~' + str(at)

    if config['key_reply']['key_at'].__contains__(word):
        if reply_text in config['key_reply']['key_at'][word]:
            return '已经有该回复了'
        else:
            if len(config['key_reply']['key_at'][word]) >= 15:
                return '单个关键词只能添加15个回复~'
            config['key_reply']['key_at'][word].append(reply_text)
            dataManage.save_group(group_id, config)
            return '添加成功~'
    else:
        config['key_reply']['key_at'][word] = [reply_text]
        dataManage.save_group(group_id, config)
        return '添加成功~'


# 删除关键词匹配（带at）
def del_key_reply_at(word, reply_text, at, config, group_id):
    if word in KeyScreenWord:
        return word + '为保留字，不可以删除'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以删除'

    if at == '全体成员':
        at = -1
    elif at == '触发人':
        at = 0
    elif at.isdigit():
        at = int(at)
    else:
        return '艾特对象格式错误'
    if at != -1 and at < 0:
        return '艾特对象格式错误'

    reply_text = reply_text + '~$~' + str(at)

    if config['key_reply']['key_at'].__contains__(word):
        if reply_text in config['key_reply']['key_at'][word]:
            config['key_reply']['key_at'][word].remove(reply_text)
            if len(config['key_reply']['key_at'][word]) == 0:
                del config['key_reply']['key_at'][word]
            dataManage.save_group(group_id, config)
            return '删除成功~！'
        else:
            return '没有该词组配对~'
    else:
        return '没有该词组配对~'


def edit_key_probability(probability, config, group_id):
    if not probability.isdigit():
        return '格式错误，请输入0~100的数字'
    p = int(probability)
    if p < 0 or p > 100:
        return '概率只能在0到100之间'
    config['key_reply']['key']['RecoveryProbability'] = p
    dataManage.save_group(group_id, config)
    return '已将关键词回复概率修改为了' + str(p) + '%'


# =====================
# 添加复杂回复(带艾特)
def add_complex_reply(word, reply_text, config):
    pass


# 删除复杂回复（带艾特）
def del_complex_reply(word, reply_text, config):
    pass


# 添加复杂关键词(带艾特)
def add_complex_key(word, reply_text, config):
    pass


# 删除复杂关键词（带艾特）
def del_complex_key(word, reply_text, config):
    pass


# ==========================================================
# 骂人计划操作

def add_curse_plan_group(config, group_id):
    if config['config']['curse']:
        return '该群已经开启了脏话哦~'
    config['config']['curse'] = True
    dataManage.save_group(group_id, config)
    return '已开启∑(っ°Д°;)っ'


def del_curse_plan_group(config, group_id):
    if not config['config']['curse']:
        return '该群本来就没有开启脏话!!!∑(ﾟДﾟノ)ノ'
    config['config']['curse'] = False
    dataManage.save_group(group_id, config)
    return '已关闭，切，懦夫~'


def add_image_search_group(config, group_id):
    if config['config']['image']:
        return '该群已经开启了涩图哦~'
    config['config']['image'] = True
    dataManage.save_group(group_id, config)
    return '已开启ヾ(･ω･*)ﾉ'


def del_image_search_group(config, group_id):
    if not config['config']['image']:
        return '该群本来就没有开启涩图!!!∑(ﾟДﾟノ)ノ'
    config['config']['image'] = False
    dataManage.save_group(group_id, config)
    return '已关闭，(灬°ω°灬) '


# ==========================================================
# 活动

# 增加活动
def add_activity(group_id, qq, activity_name, lastMinute):
    activityList = dataManage.load_obj('data/ClockActivity/activity')
    if activityList.__contains__(group_id):
        if activityList[group_id].__contains__(activity_name):
            return '已经存在该活动了'
        else:
            activityList[group_id][activity_name] = {
                'admin': qq,
                'beginTime': {
                    'hour': getNow.getHour(),
                    'minute': getNow.getMinute()
                },
                'lastMinute': lastMinute,
                'member': []
            }
            dataManage.save_obj(activityList, 'data/ClockActivity/activity')
            return '活动 ' + activity_name + '已开启，请在' + str(lastMinute) + '分钟内报名'
    else:
        activityList[group_id] = {}
        activityList[group_id][activity_name] = {
            'admin': qq,
            'beginTime': {
                'hour': getNow.getHour(),
                'minute': getNow.getMinute()
            },
            'lastMinute': lastMinute,
            'member': []
        }
        dataManage.save_obj(activityList, 'data/ClockActivity/activity')
        return '活动 ' + activity_name + '已开启，请在' + str(lastMinute) + '分钟内输入\"参加活动 ' + activity_name + '\"报名'


# 参与活动
def join_activity(group_id, qq, activity_name):
    activityList = dataManage.load_obj('data/ClockActivity/activity')
    if activityList.__contains__(group_id):
        if activityList[group_id].__contains__(activity_name):
            if qq in activityList[group_id][activity_name]['member']:
                return '你已经参加了该活动哦~'
            else:
                activityList[group_id][activity_name]['member'].append(qq)
                dataManage.save_obj(activityList, 'data/ClockActivity/activity')
                return '参加活动' + activity_name + '成功！'
        else:
            return '不存在该活动！'
    else:
        return '不存在该活动！'


# 退出活动
def quit_activity(group_id, qq, activity_name):
    activityList = dataManage.load_obj('data/ClockActivity/activity')
    if activityList.__contains__(group_id):
        if activityList[group_id].__contains__(activity_name):
            if qq in activityList[group_id][activity_name]['member']:
                activityList[group_id][activity_name]['member'].remove(qq)
                dataManage.save_obj(activityList, 'data/ClockActivity/activity')
                return '退出成功！'
            else:
                return '你本来就没有参与这个活动~'
        else:
            return '不存在该活动！'
    else:
        return '不存在该活动！'


# 删除活动
def del_activity(group_id, qq, activity_name):
    activityList = dataManage.load_obj('data/ClockActivity/activity')
    if activityList.__contains__(group_id):
        if activityList[group_id].__contains__(activity_name):
            del activityList[group_id][activity_name]
            if len(activityList[group_id]) == 0:
                del activityList[group_id]
            dataManage.save_obj(activityList, 'data/ClockActivity/activity')
            return '删除成功！'
        else:
            return '不存在该活动！'
    else:
        return '不存在该活动！'


# 活动名单
async def view_activity(group_id, activity_name, app):
    activityList = dataManage.load_obj('data/ClockActivity/activity')
    if activityList.__contains__(group_id):
        if activityList[group_id].__contains__(activity_name):
            reply_text = '活动' + activity_name + '名单如下：'
            for i in activityList[group_id][activity_name]['member']:
                member = await app.getMember(group_id, i)
                if member is None:
                    continue
                print(member)
                print(i)
                reply_text += '\n' + member.name + '(' + str(i) + ')'
            return reply_text
        else:
            return '不存在该活动！'
    else:
        return '不存在该活动！'


def get_activity_list(group_id, app):
    activityList = dataManage.load_obj('data/ClockActivity/activity')
    if activityList.__contains__(group_id):
        if len(activityList[group_id]) > 0:
            reply_text = '本群当前活动如下：'
            for key, value in activityList[group_id].items():
                reply_text += '\n' + key + '(参与人数：' + str(len(value['member'])) + ')'
            return reply_text
    return '本群暂无活动'
