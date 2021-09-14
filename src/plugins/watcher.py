from mirai import Mirai, WebSocketAdapter
from mirai import FriendMessage, GroupMessage, TempMessage
from mirai import Plain, At, AtAll, Face
from mirai.models.events import MemberJoinEvent, NewFriendRequestEvent, BotLeaveEventKick, \
    BotInvitedJoinGroupRequestEvent
from mirai.models.events import NudgeEvent

# =============================================================
# 需求类
import asyncio
import datetime

# =============================================================
# 附加功能类
from plugins import getNow
from plugins import logManage
from plugins import dataManage
from plugins import Clock


# =============================================================
# 主程序
async def new_day(bot):
    today = str(datetime.date.today())
    reply = '已经重置打卡日期到' + today

    logManage.log(getNow.toString(), '已重置打卡日期到：' + today)

    print('开始重置统计信息')
    statistics = dataManage.read_statistics()  # 读取统计信息
    reply += '\n统计信息如下：'
    reply += '\n被踢出群数：' + str(statistics['kick'])
    reply += '\n退群数：' + str(statistics['quit'])
    reply += '\n禁言次数：' + str(statistics['mute'])
    reply += '\n解除禁言次数：' + str(statistics['unmute'])
    reply += '\n唤醒次数：' + str(statistics['awaken'])
    reply += '\n帮助文档获取次数：' + str(statistics['help'])
    reply += '\n基础功能调用次数：' + str(statistics['base_function'])
    reply += '\ntalk模块调用次数：' + str(statistics['talk'])
    reply += '\nclock_activity模块调用次数：' + str(statistics['clock_activity'])
    reply += '\nimage_search模块调用次数：' + str(statistics['image_search'])
    reply += '\ncommand模块调用次数：' + str(statistics['command'])
    reply += '\noperate模块调用次数：' + str(statistics['operate'])
    reply += '\ngame模块调用次数：' + str(statistics['game'])
    reply += '\n自动加一次数：' + str(statistics['auto_repeat'])
    reply += '\n自主回复次数：' + str(statistics['auto_reply'])
    reply += '\n部落冲突调用次数：' + str(statistics['clash'])
    reply += '\n新好友：' + str(statistics['new_friend'])
    reply += '\n新群：' + str(statistics['new_group'])

    statistics['kick'] = 0
    statistics['quit'] = 0
    statistics['mute'] = 0
    statistics['unmute'] = 0
    statistics['new_friend'] = 0
    statistics['new_group'] = 0

    statistics['awaken'] = 0
    statistics['help'] = 0
    statistics['base_function'] = 0
    statistics['talk'] = 0
    statistics['clock_activity'] = 0
    statistics['image_search'] = 0
    statistics['command'] = 0
    statistics['operate'] = 0
    statistics['game'] = 0
    statistics['auto_repeat'] = 0
    statistics['auto_reply'] = 0
    statistics['clash'] = 0
    dataManage.save_statistics(statistics)

    config = dataManage.read_config()
    for group_id in config['test_group']:
        await bot.send_group_message(group_id, reply)

    return True


async def reset_clock(bot):
    today = str(datetime.date.today())
    clock = dataManage.read_clock()
    del_key = []
    for group_id, clock_dict in clock.items():
        if 'int' not in str(type(group_id)):
            del_key.append(group_id)
            continue
        member_list_origin = await bot.member_list(group_id)
        member_list = {}
        for member in member_list_origin.data:
            if not member_list.__contains__(member.id):
                member_list[member.id] = member.member_name

        for name, members in clock_dict.items():
            del_member = []
            at_member = []
            for member in members['member']:
                if not member_list.__contains__(member['qq']):
                    del_member.append(member)
                elif not Clock.is_yesterday(member['last']):
                    at_member.append(member['qq'])
            message = []
            if len(at_member) != 0:
                message.append(Plain('打卡<' + name + '>昨日未打卡的人公示：'))
                for qq in at_member:
                    message.append(At(qq))
                message.append(Plain('\n'))
                await bot.send_group_message(group_id, message)
            else:
                message.append(Plain('打卡<' + name + '>昨日所有人都完成了打卡'))
                await bot.send_group_message(group_id, message)

            for member in del_member:
                clock[group_id][name]['member'].remove(member)
            dataManage.save_clock(clock)

    for key in del_key:
        del clock[key]
    dataManage.save_clock(clock)


async def clock_check(bot, hour, minute):
    today = str(datetime.date.today())
    clock = dataManage.read_clock()
    del_key = []
    for group_id, clock_dict in clock.items():
        if 'int' not in str(type(group_id)):
            del_key.append(group_id)
            continue
        member_list_origin = await bot.member_list(group_id)
        member_list = {}
        for member in member_list_origin.data:
            if not member_list.__contains__(member.id):
                member_list[member.id] = member.member_name

        for name, members in clock_dict.items():
            # 如果需要提醒才进行提醒
            if members['remind']['hour'] and hour == members['remind']['hour'] and minute == members['remind']['minute']:
                del_member = []
                at_member = []
                for member in members['member']:
                    if not member_list.__contains__(member['qq']):
                        del_member.append(member)
                    elif member['last'] != today:
                        at_member.append(member['qq'])
                message = []
                if len(at_member) != 0:
                    message.append(Plain('打卡<' + name + '>还未打卡的人：'))
                    for qq in at_member:
                        message.append(At(qq))
                    message.append(Plain('\n记得打卡呀~'))
                    await bot.send_group_message(group_id, message)

                for member in del_member:
                    clock[group_id][name]['member'].remove(member)
                dataManage.save_clock(clock)

    for key in del_key:
        del clock[key]
    dataManage.save_clock(clock)
