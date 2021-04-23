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


async def administratorOperation(strMessage, groupId, memberId, app, member, botBaseInformation):
    Bot_QQ = botBaseInformation['baseInformation']['Bot_QQ']
    Bot_Name = botBaseInformation['baseInformation']['Bot_Name']
    clock = dataManage.load_obj('clockIn')

    needReply = False
    needAt = False
    reply = ''
    passport = False

    # 主人权限
    if memberId ==  botBaseInformation['baseInformation']['Master_QQ']:
        passport = True
        if strMessage == '主人帮助':
            reply = command.helpMaster()
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
        elif strMessage[:6] == '添加屏蔽词 ':
            reply = addScreenWord(strMessage[6:], botBaseInformation)
            needReply = True
        elif strMessage == '查看管理员':
            reply = str(botBaseInformation["administrator"])
            needReply = True
        elif strMessage[:6] == '添加管理员 ':
            reply = addAdministrator(int(strMessage[6:]), botBaseInformation)
            needReply = True
        elif strMessage[:6] == '删除管理员 ':
            reply = delAdministrator(int(strMessage[6:]), botBaseInformation)
            needReply = True

    # 管理员权限
    if memberId in botBaseInformation["administrator"] or passport:
        passport = True
        if strMessage == '管理员帮助':
            reply = command.helpAdmministor()
            needReply = True
        elif strMessage[:6] == '添加贡献者 ':
            reply = addContributors(int(strMessage[6:]), botBaseInformation)
            needReply = True
        elif strMessage[:6] == '删除贡献者 ':
            reply = delContributors(int(strMessage[6:]), botBaseInformation)
            needReply = True
        elif strMessage == '查看贡献者':
            reply = str(botBaseInformation["contributors"])
            needReply = True
        elif strMessage == '查看黑名单 人':
            reply = str(botBaseInformation["blacklistMember"])
            needReply = True
        elif strMessage == '查看黑名单 群':
            reply = str(botBaseInformation["blacklistGroup"])
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
        elif strMessage == '文摘条数':
            reply = talk.numPoem()
            needReply = True
        elif strMessage == '情话条数':
            reply = talk.numLoveTalk()
            needReply = True
        elif strMessage == '脏话条数':
            reply = talk.numSwear()
            needReply = True
        elif strMessage == '版本信息':
            reply = '当前版本为：' + botBaseInformation['baseInformation']['version']
            needReply = True


    # 贡献者权限
    if memberId in botBaseInformation["contributors"] or passport:
        if (strMessage == Bot_Name):
            reply = '我在！'
            needReply = True
        elif strMessage == '贡献者帮助':
            reply = command.helpContributor()
            needReply = True

        elif strMessage == '添加打卡计划' and groupId != 0:
            reply = clockIn.addClockIn(groupId)
            needAt = True
            needReply = True
        elif strMessage == '打卡提醒' and clock['groupClock'].__contains__(groupId):
            reply = await sendMessage(groupId, clock, app)
            needReply = False
        elif strMessage[:5] == '打卡情况 ':
            tmp = int(strMessage[5:])
            if clock['groupClock'].__contains__(tmp):
                reply = '未打卡名单：\n'
                for key, value in clock['dictClockPeople'][tmp].items():
                    if not value['clockIn']:
                        member_tmp = await app.getMember(tmp, key)
                        reply += member_tmp.name + '(' + str(key) + ')\n'
            else:
                reply = '该群没有打卡计划哦！'
            needReply = True
        elif strMessage == '打卡情况':
            tmp = groupId
            if clock['groupClock'].__contains__(tmp):
                reply = '未打卡名单：\n'
                for key, value in clock['dictClockPeople'][tmp].items():
                    if not value['clockIn']:
                        member_tmp = await app.getMember(tmp, key)
                        reply += member_tmp.name + '(' + str(key) + ')\n'
            else:
                reply = '本群没有打卡计划哦！'
            needReply = True
        elif strMessage == '打卡计划管理帮助':
            reply = command.helpClockAdmministor()
            needReply = True

        elif strMessage[:5] == '添加回复 ':
            stringList = strMessage.split(' ')
            if len(stringList) >= 3:
                reply = addKeyReply(stringList[1], stringList[2], member)
                needReply = True
        elif strMessage[:5] == '删除回复 ':
            stringList = strMessage.split(' ')
            if len(stringList) >= 3:
                reply = delKeyReply(stringList[1], stringList[2], member)
                needReply = True
        elif strMessage[:5] == '添加回复*':
            stringList = strMessage.split('*')
            if len(stringList) >= 3:
                reply = addKeyReply(stringList[1], stringList[2], member)
                needReply = True
        elif strMessage[:5] == '删除回复*':
            stringList = strMessage.split('*')
            if len(stringList) >= 3:
                reply = delKeyReply(stringList[1], stringList[2], member)
                needReply = True
        
    if strMessage == '我的权限':
        if memberId ==  botBaseInformation['baseInformation']['Master_QQ']:
            reply = '当前权限：主人\n可以输入主人帮助来获取指令帮助哦~'
            needReply = True
        elif memberId in botBaseInformation["administrator"]:
            reply = '当前权限：管理员\n可以输入管理员帮助来获取指令帮助哦~'
            needReply = True
        elif memberId in botBaseInformation["contributors"]:
            reply = '当前权限：贡献者\n可以输入贡献者帮助来获取指令帮助哦~~'
            needReply = True

    
    if needReply:
        if strMessage != '贡献者帮助' and strMessage != '管理员帮助' and strMessage != '打卡计划管理帮助' and strMessage != '主人帮助':
            logManage.log(getNow.toString(), memberId, strMessage + "; 执行结果：" + reply)
        else:
            logManage.log(getNow.toString(), memberId, strMessage + "; 执行结果：参见command.py里的帮助内容")

    return (needReply, needAt, reply)


# 添加贡献者
def addContributors(memberId, botBaseInformation):
    if memberId > 0:
        if memberId ==  botBaseInformation['baseInformation']['Master_QQ']:
            reply = '他是主人哦~'
        elif memberId in botBaseInformation["administrator"]:
            reply = '该成员已经是管理员了'
        elif memberId in botBaseInformation["contributors"]:
            reply = '该成员已经在贡献者计划中了哦~'
        else:
            botBaseInformation["contributors"].append(memberId)
            dataManage.save_obj(botBaseInformation, 'baseInformation')
            reply = '添加成功~'
    else:
        reply = '诶？这个QQ正确吗？'
    return reply

# 移除贡献者
def delContributors(memberId, botBaseInformation):
    if memberId > 0:
        if memberId ==  botBaseInformation['baseInformation']['Master_QQ']:
            reply = '他是主人哦~'
        elif memberId in botBaseInformation["administrator"]:
            reply = '该成员已经是管理员啦，不是贡献者'
        elif not (memberId in botBaseInformation["contributors"]):
            reply = '该成员不在贡献者计划中哦~'
        else:
            botBaseInformation["contributors"].remove(memberId)
            dataManage.save_obj(botBaseInformation, 'baseInformation')
            reply = '删除成功~'
    else:
        reply = '诶？这个QQ正确吗？'
    return reply

# 添加管理员
def addAdministrator(memberId, botBaseInformation):
    if memberId > 0:
        if memberId ==  botBaseInformation['baseInformation']['Master_QQ']:
            reply = '他是主人哦~'
        elif memberId in botBaseInformation["administrator"]:
            reply = '该成员已经是管理员了'
        elif memberId in botBaseInformation["contributors"]:
            botBaseInformation["contributors"].remove(memberId)
            botBaseInformation["administrator"].append(memberId)
            dataManage.save_obj(botBaseInformation, 'baseInformation')
            reply = '已将该成员的权限从贡献者升为了管理员'
        else:
            botBaseInformation["administrator"].append(memberId)
            dataManage.save_obj(botBaseInformation, 'baseInformation')
            reply = '添加成功~'
    else:
        reply = '诶？这个QQ正确吗？'
    return reply

# 移除管理员
def delAdministrator(memberId, botBaseInformation):
    if memberId > 0:
        if memberId ==  botBaseInformation['baseInformation']['Master_QQ']:
            reply = '他是主人哦~不能从管理员中移除'
        elif not (memberId in botBaseInformation["administrator"]):
            reply = '该成员不是管理员哦~'
            if memberId in botBaseInformation["contributors"]:
                reply += '但是该成员是贡献者，已经移除他的权限'
                botBaseInformation["contributors"].remove(memberId)
                dataManage.save_obj(botBaseInformation, 'baseInformation')
        else:
            botBaseInformation["administrator"].remove(memberId)
            dataManage.save_obj(botBaseInformation, 'baseInformation')
            reply = '删除成功~'
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


def addScreenWord(word, botBaseInformation):
    screenWords = dataManage.load_obj('AIScreenWords')
    if word in screenWords:
        return '已经有该屏蔽词了'
    
    screenWords.append(word)
    dataManage.save_obj(screenWords, 'AIScreenWords')
    return '添加成功~！'

def addKeyReply(word, reply, member):
    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id))
    if keyReply.__contains__(word):
        if reply in keyReply[word]:
            return '已经有该回复了'
        else:
            keyReply[word].append(reply)
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id))
            return '添加成功~'
    else:
        keyReply[word] = [reply]
        dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id))
        return '添加成功~'

def delKeyReply(word, reply, member):
    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id))
    if keyReply.__contains__(word):
        if reply in keyReply[word]:
            keyReply[word].remove(reply)
            if len(keyReply[word]) == 0:
                del keyReply[word]
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id))
            return '删除成功~！'
        else:
            return '没有该词组配对~'
    else:
        return '没有该词组配对~'

