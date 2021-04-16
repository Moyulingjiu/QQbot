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

# ==========================================================
# 监听模块


async def sendMessage(groupId, clock, app):
    group = await app.getGroup(groupId)

    if clock['groupClock'].__contains__(groupId):
        reply = '记得打卡呀：'
        message = MessageChain.create([
            Plain(reply)
        ])
        for key, value in clock['dictClockPeople'][groupId].items():
            if not value:
                message.plus(MessageChain.create([
                    Plain('\n'),
                    At(key)
                ]))

        await app.sendGroupMessage(group, message)
        return True
    return False

# ==========================================================
# 管理员模块


async def administratorOperation(strMessage, groupId, memberId, app, member, botBaseInformation):
    Bot_QQ = botBaseInformation['baseInformation']['Bot_QQ']
    Bot_Name = botBaseInformation['baseInformation']['Bot_Name']
    clock = dataManage.load_obj('clockIn')

    needReply = False
    needAt = False
    reply = ''

    if memberId in botBaseInformation["administrator"]:
        # 管理员权限
        if strMessage[:6] == '添加管理员 ':
            reply = addContributors(int(strMessage[6:]))
            needReply = True
        elif strMessage == '命令大全':
            reply = command.allCommand()
            needReply = True
        elif strMessage[:5] == '删除文摘 ':
            reply = talk.delPoem(int(strMessage[5:]))
            needReply = True
        elif strMessage[:5] == '删除情话 ':
            reply = talk.delLoveTalk(int(strMessage[5:]))
            needReply = True
        elif strMessage[:5] == '删除脏话 ':
            reply = talk.delSwear(int(strMessage[5:]))
            needReply = True
        elif strMessage[:8] == '添加黑名单 群 ':
            reply = addBlacklistGroup(int(strMessage[8:]), botBaseInformation)
            needReply = True
        elif strMessage[:8] == '添加黑名单 人 ':
            reply = addBlacklistMember(int(strMessage[8:]), botBaseInformation)
            needReply = True
        elif strMessage[:8] == '移除黑名单 群 ':
            reply = removeBlacklistGroup(int(strMessage[8:]), botBaseInformation)
            needReply = True
        elif strMessage[:8] == '移除黑名单 人 ':
            reply = removeBlacklistMember(int(strMessage[8:]), botBaseInformation)
            needReply = True
        elif strMessage[:7] == '修改版本信息 ':
            reply = changeVersion(strMessage[7:], botBaseInformation)
            needReply = True
        elif strMessage[:8] == '修改机器人名字 ':
            reply = changeName(strMessage[8:], botBaseInformation)
            needReply = True
        elif strMessage[:8] == '修改机器人QQ ':
            reply = changeQQ(strMessage[8:], botBaseInformation)
            needReply = True

    # 非管理员权限
    if (strMessage == '小柒报告状况'):
        reply = Bot_Name + '运行良好'
        needReply = True
    elif strMessage == '添加打卡计划' and groupId != 0:
        reply = clockIn.addClockIn(groupId)
        needAt = True
        needReply = True
    elif strMessage[:4] == '添加文摘':
        poemlist = strMessage.split(' ')
        del poemlist[0]
        reply = talk.addPoem(poemlist)
        needReply = True
    elif strMessage[:4] == '添加情话':
        loveTalklist = strMessage.split(' ')
        del loveTalklist[0]
        reply = talk.addLoveTalk(loveTalklist)
        needReply = True
    elif strMessage[:4] == '添加脏话':
        swearlist = strMessage.split(' ')
        del swearlist[0]
        reply = talk.addSwear(swearlist)
        needReply = True
    elif strMessage == '管理员帮助':
        reply = command.helpAdministrators()
        needReply = True
    elif strMessage == '打卡提醒' and clock['groupClock'].__contains__(groupId):
        reply = await sendMessage(groupId, clock, app)
        needReply = False
    elif strMessage == '文摘条数':
        reply = talk.numPoem()
        needReply = True
    elif strMessage == '情话条数':
        reply = talk.numLoveTalk()
        needReply = True
    elif strMessage == '脏话条数':
        reply = talk.numSwear()
        needReply = True
    elif strMessage[:5] == '打卡情况 ':
        tmp = int(strMessage[5:])
        if clock['groupClock'].__contains__(tmp):
            reply = '未打卡名单：\n'
            for key, value in clock['dictClockPeople'][tmp].items():
                if not value:
                    member_tmp = await app.getMember(tmp, key)
                    reply += member_tmp.name + '(' + str(key) + ')\n'
        else:
            reply = '该群没有打卡计划哦！'
        needReply = True
    elif strMessage == '版本信息':
        reply = '当前版本为：' + botBaseInformation['baseInformation']['version']
        needReply = True
    
    
    if needReply:
        if strMessage != '命令大全' and strMessage != '管理员帮助':
            logManage.log(getNow.toString(), memberId, strMessage + "; 执行结果：" + reply)
        else:
            logManage.log(getNow.toString(), memberId, strMessage + "; 执行结果：参见command.py里的帮助内容")

    return (needReply, needAt, reply)


def addContributors(memberId, botBaseInformation):
    if memberId != 0:
        if memberId in botBaseInformation["contributors"]:
            reply = '该成员已经在贡献者计划中了哦~'
        else:
            botBaseInformation["contributors"].append(memberId)
            dataManage.save_obj(botBaseInformation, 'baseInformation')
            reply = '添加成功~'
    else:
        reply = '诶？这个QQ正确吗？'
    return reply

# ==========================================================
# 基本信息

# 修改版本
def changeVersion(version, botBaseInformation):
    botBaseInformation['baseInformation']['version'] = version
    dataManage.save_obj(botBaseInformation, 'baseInformation')
    return '修改成功！当前版本：' + version

# 修改名字
def changeName(name, botBaseInformation):
    botBaseInformation['baseInformation']['Bot_Name'] = name
    dataManage.save_obj(botBaseInformation, 'baseInformation')
    return '修改成功！当前名字：' + name

# 修改机器人QQ
def changeQQ(qq, botBaseInformation):
    botBaseInformation['baseInformation']['Bot_QQ'] = qq
    dataManage.save_obj(botBaseInformation, 'baseInformation')
    return '修改成功！当前QQ：' + qq

# ==========================================================
# 文件操作

def addBlacklistGroup(groupId, botBaseInformation):
    if groupId in botBaseInformation["blacklistGroup"]:
        return '该群已经在黑名单里了'
    if groupId in botBaseInformation["testGroup"]:
        return '该群为测试群聊，不能添加黑名单，请先将其移除测试群聊'

    botBaseInformation["blacklistGroup"].append(groupId)
    dataManage.save_obj(botBaseInformation, 'baseInformation')
    return '已经将群' + str(groupId) + '加入黑名单'


def addBlacklistMember(memberId, botBaseInformation):
    if memberId in botBaseInformation["blacklistMember"]:
        return '该人已经在黑名单里了'
    if memberId in botBaseInformation["administrator"]:
        return '对方是管理员，不能加入黑名单'

    botBaseInformation["blacklistMember"].append(memberId)
    dataManage.save_obj(botBaseInformation, 'baseInformation')
    return '已经将人' + str(memberId) + '加入黑名单'


def removeBlacklistGroup(groupId, botBaseInformation):
    if not groupId in botBaseInformation["blacklistGroup"]:
        return '该群不在黑名单里'
    del botBaseInformation["blacklistGroup"][botBaseInformation["blacklistGroup"].index(groupId)]
    dataManage.save_obj(botBaseInformation, 'baseInformation')
    return '已经将群' + str(groupId) + '移除黑名单'


def removeBlacklistMember(memberId, botBaseInformation):
    if not memberId in botBaseInformation["blacklistMember"]:
        return '该人不在黑名单里'
    del botBaseInformation["blacklistMember"][botBaseInformation["blacklistMember"].index(memberId)]
    dataManage.save_obj(botBaseInformation, 'baseInformation')
    return '已经将人' + str(memberId) + '移除黑名单'
