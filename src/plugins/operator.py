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
async def administrator_operation(message, group_id, qq, app, member, bot_information, right, group_right, mode):
    bot_qq = bot_information['baseInformation']['Bot_QQ']
    bot_name = bot_information['baseInformation']['Bot_Name']
    master_qq = bot_information['baseInformation']['Master_QQ']
    clock = dataManage.load_obj('clockIn')

    message_len = len(message)
    message4 = message[:4]
    message5 = message[:5]
    message6 = message[:6]
    message7 = message[:7]

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
            logManage.log(getNow.toString(), 0, bot_name + '关机！')
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
            tmp = message[7:].strip()
            if tmp.isdigit():
                reply_text = add_blacklist_group(int(tmp), bot_information)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message7 == '添加黑名单 人' and message_len > 7:
        if right < 1:
            tmp = message[7:].strip()
            if tmp.isdigit():
                reply_text = add_blacklist_member(int(tmp), bot_information)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message7 == '移除黑名单 群' and message_len > 7:
        if right < 1:
            tmp = message[7:].strip()
            if tmp.isdigit():
                reply_text = remove_blacklist_group(int(tmp), bot_information)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message7 == '移除黑名单 人' and message_len > 7:
        if right < 1:
            tmp = message[7:].strip()
            if tmp.isdigit():
                reply_text = remove_blacklist_member(int(tmp), bot_information)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    elif message6 == '修改版本信息' and message_len > 6:
        if right < 1:
            reply_text = change_version(message[6:].strip(), bot_information)
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message7 == '修改机器人名字' and message_len > 7:
        if right < 1:
            reply_text = change_bot_name(message[7:].strip(), bot_information)
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message7 == '修改机器人QQ' and message_len > 7:
        if right < 1:
            tmp = message[7:].strip()
            if tmp.isdigit():
                reply_text = change_bot_qq(int(tmp), bot_information)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    # 屏蔽词不用strip，因为可能有一些带空格屏蔽词
    elif message6 == '添加屏蔽词 ' and message_len > 6:
        if right < 1:
            reply_text = add_screen_word(message[6:], bot_information)
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message6 == '删除屏蔽词 ' and message_len > 6:
        if right < 1:
            reply_text = del_screen_word(message[6:], bot_information)
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message == '查看屏蔽词':
        if right < 1:
            reply_text = view_screen_word(bot_information)
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    elif message == '查看管理员':
        if right < 1:
            reply_text = str(bot_information["administrator"])
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message5 == '添加管理员' and message_len > 5:
        if right < 1:
            tmp = message[5:].strip()
            if tmp.isdigit():
                reply_text = add_administrator(int(tmp), bot_information)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message5 == '删除管理员' and message_len > 5:
        if right < 1:
            tmp = message[5:].strip()
            if tmp.isdigit():
                reply_text = del_administrator(int(tmp), bot_information)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    elif message4 == '开启脏话' and message_len > 4:
        if right < 1:
            tmp = message[4:].strip()
            if tmp.isdigit():
                reply_text = add_curse_plan_group(int(tmp), bot_information)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message4 == '关闭脏话' and message_len > 4:
        if right < 1:
            tmp = message[4:].strip()
            if tmp.isdigit():
                reply_text = del_curse_plan_group(int(tmp), bot_information)
            else:
                reply_text = '格式错误'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    elif message == '清空每分钟回复条数':
        if right < 1:
            bot_information['reply']['lastMinute'] = 0
            dataManage.save_obj(bot_information, 'baseInformation')
            reply_text = '清空成功！'
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True

    elif message == '开启涩图' and mode == 1:
        if right < 1:
            reply_text = add_image_search_group(group_id, bot_information)
        else:
            reply_text = '权限不足，请输入"我的权限"查看'
        need_reply = True
    elif message == '关闭涩图' and mode == 1:
        if right < 1:
            reply_text = del_image_search_group(group_id, bot_information)
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
                    reply_text = add_contributors(int(tmp), bot_information)
                else:
                    reply_text = '格式错误'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message5 == '删除贡献者' and message_len > 5:
            if right < 2:
                tmp = message[5:].strip()
                if tmp.isdigit():
                    reply_text = del_contributors(int(tmp), bot_information)
                else:
                    reply_text = '格式错误'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message == '查看贡献者':
            if right < 2:
                reply_text = str(bot_information["contributors"])
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif message == '查看黑名单 人':
            if right < 2:
                reply_text = str(bot_information["blacklistMember"])
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message == '查看黑名单 群':
            if right < 2:
                reply_text = str(bot_information["blacklistGroup"])
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
                reply_text = '当前版本为：' + bot_information['baseInformation']['version']
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif (message == '开启脏话' or message == '脏话开启') and mode == 1:
            if right < 2 or group_right < 2:
                reply_text = add_curse_plan_group(group_id, bot_information)
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif (message == '关闭脏话' or message == '脏话关闭') and mode == 1:
            if right < 2 or group_right < 2:
                reply_text = del_curse_plan_group(group_id, bot_information)
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
                    reply_text = add_question_reply(stringList[1], stringList[2], member)
                elif len(stringList) == 4:
                    reply_text = add_question_reply_at(stringList[1], stringList[2], stringList[3], member)
                else:
                    reply_text = '格式错误！请检查空格'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message5 == '删除回复 ' and message_len > 5 and mode == 1:
            if right < 3:
                stringList = message.split(' ')
                if len(stringList) == 3:
                    reply_text = del_question_reply(stringList[1], stringList[2], member)
                elif len(stringList) == 4:
                    reply_text = del_question_reply_at(stringList[1], stringList[2], stringList[3], member)
                else:
                    reply_text = '格式错误！请检查空格'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message5 == '添加回复*' and message_len > 5 and mode == 1:
            if right < 3:
                stringList = message.split('*')
                if len(stringList) == 3:
                    reply_text = add_question_reply(stringList[1], stringList[2], member)
                elif len(stringList) == 4:
                    reply_text = add_question_reply_at(stringList[1], stringList[2], stringList[3], member)
                else:
                    reply_text = '格式错误！请检查星号'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message5 == '删除回复*' and message_len > 5 and mode == 1:
            if right < 3:
                stringList = message.split('*')
                if len(stringList) == 3:
                    reply_text = del_question_reply(stringList[1], stringList[2], member)
                elif len(stringList) == 4:
                    reply_text = del_question_reply_at(stringList[1], stringList[2], stringList[3], member)
                else:
                    reply_text = '格式错误！请检查星号'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif message6 == '添加关键词 ' and message_len > 6 and mode == 1:
            if right < 3:
                stringList = message.split(' ')
                if len(stringList) == 3:
                    reply_text = add_key_reply(stringList[1], stringList[2], member)
                elif len(stringList) == 4:
                    reply_text = add_key_reply_at(stringList[1], stringList[2], stringList[3], member)
                else:
                    reply_text = '格式错误！请检查空格'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message6 == '删除关键词 ' and message_len > 6 and mode == 1:
            if right < 3:
                stringList = message.split(' ')
                if len(stringList) == 3:
                    reply_text = del_key_reply(stringList[1], stringList[2], member)
                elif len(stringList) == 4:
                    reply_text = del_key_reply_at(stringList[1], stringList[2], stringList[3], member)
                else:
                    reply_text = '格式错误！请检查空格'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message6 == '添加关键词*' and message_len > 6 and mode == 1:
            if right < 3:
                stringList = message.split('*')
                if len(stringList) == 3:
                    reply_text = add_key_reply(stringList[1], stringList[2], member)
                elif len(stringList) == 4:
                    reply_text = add_key_reply_at(stringList[1], stringList[2], stringList[3], member)
                else:
                    reply_text = '格式错误！请检查星号'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True
        elif message6 == '删除关键词*' and message_len > 6 and mode == 1:
            if right < 3:
                stringList = message.split('*')
                if len(stringList) == 3:
                    reply_text = del_key_reply(stringList[1], stringList[2], member)
                elif len(stringList) == 4:
                    reply_text = del_key_reply_at(stringList[1], stringList[2], stringList[3], member)
                else:
                    reply_text = '格式错误！请检查星号'
            else:
                reply_text = '权限不足，请输入"我的权限"查看'
            need_reply = True

        elif message7 == '关键词回复概率' and message_len > 7 and mode == 1:
            if right < 3:
                reply_text = edit_key_probability(message[7:].strip(), member)
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
                    reply_text = add_contributors(qq, bot_information)
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

    if need_reply:
        if message != '贡献者帮助' and message != '管理员帮助' and message != '主人帮助':
            logManage.log(getNow.toString(), qq, message + "; 执行结果：" + reply_text)
        else:
            logManage.log(getNow.toString(), qq, message + "; 执行结果：参见command.py里的帮助内容")

    return need_reply, need_at, reply_text, reply_image


# ==========================================================
# 权限操作

# 添加贡献者
def add_contributors(qq, bot_information):
    if qq > 0:
        if qq == bot_information['baseInformation']['Master_QQ']:
            reply_text = '他是主人哦~'
        elif qq in bot_information["administrator"]:
            reply_text = '该成员已经是管理员了'
        elif qq in bot_information["contributors"]:
            reply_text = '该成员已经在贡献者计划中了哦~'
        else:
            bot_information["contributors"].append(qq)
            dataManage.save_obj(bot_information, 'baseInformation')
            reply_text = '添加成功~'
    else:
        reply_text = '诶？这个QQ正确吗？'
    return reply_text


# 移除贡献者
def del_contributors(qq, bot_information):
    if qq > 0:
        if qq == bot_information['baseInformation']['Master_QQ']:
            reply_text = '他是主人哦~'
        elif qq in bot_information["administrator"]:
            reply_text = '该成员已经是管理员啦，不是贡献者'
        elif not (qq in bot_information["contributors"]):
            reply_text = '该成员不在贡献者计划中哦~'
        else:
            bot_information["contributors"].remove(qq)
            dataManage.save_obj(bot_information, 'baseInformation')
            reply_text = '删除成功~'
    else:
        reply_text = '诶？这个QQ正确吗？'
    return reply_text


# 添加管理员
def add_administrator(qq, bot_information):
    if qq > 0:
        if qq == bot_information['baseInformation']['Master_QQ']:
            reply_text = '他是主人哦~'
        elif qq in bot_information["administrator"]:
            reply_text = '该成员已经是管理员了'
        elif qq in bot_information["contributors"]:
            bot_information["contributors"].remove(qq)
            bot_information["administrator"].append(qq)
            dataManage.save_obj(bot_information, 'baseInformation')
            reply_text = '已将该成员的权限从贡献者升为了管理员'
        else:
            bot_information["administrator"].append(qq)
            dataManage.save_obj(bot_information, 'baseInformation')
            reply_text = '添加成功~'
    else:
        reply_text = '诶？这个QQ正确吗？'
    return reply_text


# 移除管理员
def del_administrator(qq, bot_information):
    if qq > 0:
        if qq == bot_information['baseInformation']['Master_QQ']:
            reply_text = '他是主人哦~不能从管理员中移除'
        elif not (qq in bot_information["administrator"]):
            reply_text = '该成员不是管理员哦~'
            if qq in bot_information["contributors"]:
                reply_text += '但是该成员是贡献者，已经移除他的权限'
                bot_information["contributors"].remove(qq)
                dataManage.save_obj(bot_information, 'baseInformation')
        else:
            bot_information["administrator"].remove(qq)
            dataManage.save_obj(bot_information, 'baseInformation')
            reply_text = '删除成功~'
    else:
        reply_text = '诶？这个QQ正确吗？'
    return reply_text


# ==========================================================
# 基本信息

# 修改版本
def change_version(version, bot_information):
    bot_information['baseInformation']['version'] = version
    dataManage.save_obj(bot_information, 'baseInformation')
    return '修改成功！当前版本：' + version


# 修改名字
def change_bot_name(name, bot_information):
    bot_information['baseInformation']['Bot_Name'] = name
    dataManage.save_obj(bot_information, 'baseInformation')
    return '修改成功！当前名字：' + name


# 修改机器人QQ
def change_bot_qq(qq, bot_information):
    bot_information['baseInformation']['Bot_QQ'] = qq
    dataManage.save_obj(bot_information, 'baseInformation')
    return '修改成功！当前QQ：' + qq


# ==========================================================
# 黑名单操作

def add_blacklist_group(group_id, bot_information):
    if group_id in bot_information["blacklistGroup"]:
        return '该群已经在黑名单里了'
    if group_id in bot_information["testGroup"]:
        return '该群为测试群聊，不能添加黑名单，请先将其移除测试群聊'

    bot_information["blacklistGroup"].append(group_id)
    dataManage.save_obj(bot_information, 'baseInformation')
    return '已经将群' + str(group_id) + '加入黑名单'


def add_blacklist_member(qq, bot_information):
    if qq in bot_information["blacklistMember"]:
        return '该人已经在黑名单里了'
    if qq in bot_information["administrator"]:
        return '对方是管理员，不能加入黑名单'

    bot_information["blacklistMember"].append(qq)
    dataManage.save_obj(bot_information, 'baseInformation')
    return '已经将人' + str(qq) + '加入黑名单'


def remove_blacklist_group(group_id, bot_information):
    if group_id not in bot_information["blacklistGroup"]:
        return '该群不在黑名单里'
    del bot_information["blacklistGroup"][bot_information["blacklistGroup"].index(group_id)]
    dataManage.save_obj(bot_information, 'baseInformation')
    return '已经将群' + str(group_id) + '移除黑名单'


def remove_blacklist_member(qq, bot_information):
    if qq not in bot_information["blacklistMember"]:
        return '该人不在黑名单里'
    del bot_information["blacklistMember"][bot_information["blacklistMember"].index(qq)]
    dataManage.save_obj(bot_information, 'baseInformation')
    return '已经将人' + str(qq) + '移除黑名单'


# ==========================================================
# 屏蔽词操作

# 添加屏蔽词
def add_screen_word(word, bot_information):
    screenWords = dataManage.load_obj('AIScreenWords')
    if word in screenWords:
        return '已经有该屏蔽词了'

    screenWords.append(word)
    dataManage.save_obj(screenWords, 'AIScreenWords')
    return '添加成功~！'


# 删除屏蔽词
def del_screen_word(word, bot_information):
    screenWords = dataManage.load_obj('AIScreenWords')
    if word not in screenWords:
        return '没有这个词语哦！'
    screenWords.remove(word)
    dataManage.save_obj(screenWords, 'AIScreenWords')
    return '删除成功'


# 查看屏蔽词
def view_screen_word(bot_information):
    screenWords = dataManage.load_obj('AIScreenWords')
    return str(screenWords)


# ==========================================================
# 关键词操作
KeyScreenWord = ['RecoveryProbability', 'reply_text', '~$~']


# 添加绝对匹配
def add_question_reply(word, reply_text, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以添加'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以添加'

    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id))
    if len(keyReply) >= 100:
        return '最多只可以添加100个回复哦~'

    if keyReply.__contains__(word):
        if reply_text in keyReply[word]:
            return '已经有该回复了'
        else:
            if len(keyReply[word]) >= 15:
                return '单个关键词只能添加15个回复~'
            keyReply[word].append(reply_text)
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id))
            return '添加成功~'
    else:
        keyReply[word] = [reply_text]
        dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id))
        return '添加成功~'


# 删除绝对匹配
def del_question_reply(word, reply_text, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以删除'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以删除'

    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id))
    if keyReply.__contains__(word):
        if reply_text in keyReply[word]:
            keyReply[word].remove(reply_text)
            if len(keyReply[word]) == 0:
                del keyReply[word]
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id))
            return '删除成功~！'
        else:
            return '没有该词组配对~'
    else:
        return '没有该词组配对~'


# 添加绝对匹配（带at）
def add_question_reply_at(word, reply_text, at, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以添加'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以添加'

    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'at')
    if len(keyReply) >= 100:
        return '最多只可以添加100个回复哦~'

    if at == '全体成员':
        at = -1
    else:
        at = int(at)
    if at != -1 and at <= 0:
        return '艾特对象格式错误'

    reply_text = reply_text + '~$~' + str(at)

    if keyReply.__contains__(word):
        if reply_text in keyReply[word]:
            return '已经有该回复了'
        else:
            if len(keyReply[word]) >= 15:
                return '单个关键词只能添加15个回复~'
            keyReply[word].append(reply_text)
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'at')
            return '添加成功~'
    else:
        keyReply[word] = [reply_text]
        dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'at')
        return '添加成功~'


# 删除绝对匹配（带at）
def del_question_reply_at(word, reply_text, at, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以删除'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以删除'

    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'at')
    if at == '全体成员':
        at = -1
    else:
        at = int(at)
    if at != -1 and at <= 0:
        return '艾特对象格式错误'

    reply_text = reply_text + '~$~' + str(at)

    if keyReply.__contains__(word):
        if reply_text in keyReply[word]:
            keyReply[word].remove(reply_text)
            if len(keyReply[word]) == 0:
                del keyReply[word]
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'at')
            return '删除成功~！'
        else:
            return '没有该词组配对~'
    else:
        return '没有该词组配对~'


# =====================
# 添加关键词匹配
def add_key_reply(word, reply_text, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以添加'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以添加'

    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'key')
    if len(keyReply) >= 100:
        return '最多只可以添加100个回复哦~'

    if keyReply.__contains__(word):
        if reply_text in keyReply[word]:
            return '已经有该回复了'
        else:
            if len(keyReply[word]) >= 15:
                return '单个关键词只能添加15个回复~'
            keyReply[word].append(reply_text)
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'key')
            return '添加成功~'
    else:
        keyReply[word] = [reply_text]
        dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'key')
        return '添加成功~'


# 删除关键词匹配
def del_key_reply(word, reply_text, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以删除'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以删除'

    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'key')
    if keyReply.__contains__(word):
        if reply_text in keyReply[word]:
            keyReply[word].remove(reply_text)
            if len(keyReply[word]) == 0:
                del keyReply[word]
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'key')
            return '删除成功~！'
        else:
            return '没有该词组配对~'
    else:
        return '没有该词组配对~'


# 添加关键词匹配（带at）
def add_key_reply_at(word, reply_text, at, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以添加'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以添加'

    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'keyAt')
    if len(keyReply) >= 100:
        return '最多只可以添加100个回复哦~'

    if at == '全体成员':
        at = -1
    else:
        at = int(at)
    if at != -1 and at <= 0:
        return '艾特对象格式错误'

    reply_text = reply_text + '~$~' + str(at)

    if keyReply.__contains__(word):
        if reply_text in keyReply[word]:
            return '已经有该回复了'
        else:
            if len(keyReply[word]) >= 15:
                return '单个关键词只能添加15个回复~'
            keyReply[word].append(reply_text)
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'keyAt')
            return '添加成功~'
    else:
        keyReply[word] = [reply_text]
        dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'keyAt')
        return '添加成功~'


# 删除关键词匹配（带at）
def del_key_reply_at(word, reply_text, at, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以删除'
    if reply_text in KeyScreenWord:
        return reply_text + '为保留字，不可以删除'

    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'keyAt')
    if at == '全体成员':
        at = -1
    else:
        at = int(at)
    if at != -1 and at <= 0:
        return '艾特对象格式错误'

    reply_text = reply_text + '~$~' + str(at)

    if keyReply.__contains__(word):
        if reply_text in keyReply[word]:
            keyReply[word].remove(reply_text)
            if len(keyReply[word]) == 0:
                del keyReply[word]
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'keyAt')
            return '删除成功~！'
        else:
            return '没有该词组配对~'
    else:
        return '没有该词组配对~'


def edit_key_probability(probability, member):
    if not probability.isdigit():
        return '格式错误，请输入0~100的数字'
    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'key')
    p = int(probability)
    if p < 0 or p > 100:
        return '概率只能在0到100之间'
    keyReply['RecoveryProbability'] = p
    dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'key')
    return '已将关键词回复概率修改为了' + str(p) + '%'


# =====================
# 添加复杂回复(带艾特)
def add_complex_reply(word, reply_text, member):
    pass


# 删除复杂回复（带艾特）
def del_complex_reply(word, reply_text, member):
    pass


# 添加复杂关键词(带艾特)
def add_complex_key(word, reply_text, member):
    pass


# 删除复杂关键词（带艾特）
def del_complex_key(word, reply_text, member):
    pass


# ==========================================================
# 骂人计划操作

def add_curse_plan_group(group_id, bot_information):
    if group_id in bot_information['cursePlanGroup']:
        return '该群已经开启了脏话哦~'
    bot_information['cursePlanGroup'].append(group_id)
    dataManage.save_obj(bot_information, 'baseInformation')
    return '已开启∑(っ°Д°;)っ'


def del_curse_plan_group(group_id, bot_information):
    if group_id not in bot_information['cursePlanGroup']:
        return '该群本来就没有开启脏话!!!∑(ﾟДﾟノ)ノ'
    bot_information['cursePlanGroup'].remove(group_id)
    dataManage.save_obj(bot_information, 'baseInformation')
    return '已关闭，切，懦夫~'


def add_image_search_group(group_id, bot_information):
    if group_id in bot_information['pixiv']:
        return '该群已经开启了涩图哦~'
    bot_information['pixiv'].append(group_id)
    dataManage.save_obj(bot_information, 'baseInformation')
    return '已开启ヾ(･ω･*)ﾉ'


def del_image_search_group(group_id, bot_information):
    if group_id not in bot_information['pixiv']:
        return '该群本来就没有开启涩图!!!∑(ﾟДﾟノ)ノ'
    bot_information['pixiv'].remove(group_id)
    dataManage.save_obj(bot_information, 'baseInformation')
    return '已关闭，(灬°ω°灬) '


# ==========================================================
# 活动

# 增加活动
def add_activity(group_id, qq, activity_name, lastMinute):
    activityList = dataManage.load_obj('activity')
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
            dataManage.save_obj(activityList, 'activity')
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
        dataManage.save_obj(activityList, 'activity')
        return '活动 ' + activity_name + '已开启，请在' + str(lastMinute) + '分钟内输入\"参加活动 ' + activity_name + '\"报名'


# 参与活动
def join_activity(group_id, qq, activity_name):
    activityList = dataManage.load_obj('activity')
    if activityList.__contains__(group_id):
        if activityList[group_id].__contains__(activity_name):
            if qq in activityList[group_id][activity_name]['member']:
                return '你已经参加了该活动哦~'
            else:
                activityList[group_id][activity_name]['member'].append(qq)
                dataManage.save_obj(activityList, 'activity')
                return '参加活动' + activity_name + '成功！'
        else:
            return '不存在该活动！'
    else:
        return '不存在该活动！'


# 退出活动
def quit_activity(group_id, qq, activity_name):
    activityList = dataManage.load_obj('activity')
    if activityList.__contains__(group_id):
        if activityList[group_id].__contains__(activity_name):
            if qq in activityList[group_id][activity_name]['member']:
                activityList[group_id][activity_name]['member'].remove(qq)
                dataManage.save_obj(activityList, 'activity')
                return '退出成功！'
            else:
                return '你本来就没有参与这个活动~'
        else:
            return '不存在该活动！'
    else:
        return '不存在该活动！'


# 删除活动
def del_activity(group_id, qq, activity_name):
    activityList = dataManage.load_obj('activity')
    if activityList.__contains__(group_id):
        if activityList[group_id].__contains__(activity_name):
            del activityList[group_id][activity_name]
            if len(activityList[group_id]) == 0:
                del activityList[group_id]
            dataManage.save_obj(activityList, 'activity')
            return '删除成功！'
        else:
            return '不存在该活动！'
    else:
        return '不存在该活动！'


# 活动名单
async def view_activity(group_id, activity_name, app):
    activityList = dataManage.load_obj('activity')
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
    activityList = dataManage.load_obj('activity')
    if activityList.__contains__(group_id):
        if len(activityList[group_id]) > 0:
            reply_text = '本群当前活动如下：'
            for key, value in activityList[group_id].items():
                reply_text += '\n' + key + '(参与人数：' + str(len(value['member'])) + ')'
            return reply_text
    return '本群暂无活动'
