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
    isImage = ''

    # 主人权限
    if memberId ==  botBaseInformation['baseInformation']['Master_QQ']:
        passport = True
        if strMessage == '主人帮助':
            isImage = command.helpMaster()
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
        elif strMessage[:6] == '删除屏蔽词 ':
            reply = delScreenWord(strMessage[6:], botBaseInformation)
            needReply = True
        elif strMessage == '查看屏蔽词':
            reply = viewScreenWord(botBaseInformation)
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

        elif strMessage[:5] == '开启脏话 ':
            reply = addcursePlanGroup(int(strMessage[5:]), botBaseInformation)
            needReply = True
        elif strMessage[:5] == '关闭脏话 ':
            reply = delcursePlanGroup(int(strMessage[5:]), botBaseInformation)
            needReply = True
        elif strMessage == '清空每分钟回复条数':
            botBaseInformation['reply']['lastMinute'] = 0
            dataManage.save_obj(botBaseInformation, 'baseInformation')
            reply = '清空成功！'
            needReply = True
        
    # 管理员权限
    if memberId in botBaseInformation["administrator"] or passport:
        passport = True
        if strMessage == '管理员帮助':
            isImage = command.helpAdmministor()
            needReply = True
        elif strMessage[:6] == '添加贡献者 ':
            reply = ''
            try:
                reply = addContributors(int(strMessage[6:]), botBaseInformation)
            except ValueError as e:
                pass
            needReply = True
        elif strMessage[:6] == '删除贡献者 ':
            reply = ''
            try:
                reply = delContributors(int(strMessage[6:]), botBaseInformation)
            except ValueError as e:
                pass
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

        elif strMessage == '开启脏话':
            if groupId > 0:
                reply = addcursePlanGroup(groupId, botBaseInformation)
                needReply = True
        elif strMessage == '关闭脏话':
            if groupId > 0:
                reply = delcursePlanGroup(groupId, botBaseInformation)
                needReply = True
        

    # 贡献者权限
    if memberId in botBaseInformation["contributors"] or passport:
        if strMessage == '贡献者帮助':
            isImage = command.helpContributor()
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
        elif strMessage == '打卡情况' and groupId != 0:
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


        elif strMessage[:5] == '添加回复 ' and groupId != 0:
            stringList = strMessage.split(' ')
            if len(stringList) == 3:
                reply = addQuestionReply(stringList[1], stringList[2], member)
                needReply = True
            elif len(stringList) == 4:
                reply = addQuestionReplyAt(stringList[1], stringList[2], stringList[3], member)
                needReply = True
            else:
                reply = '格式错误！请检查空格'
                needReply = True
        elif strMessage[:5] == '删除回复 ' and groupId != 0:
            stringList = strMessage.split(' ')
            if len(stringList) == 3:
                reply = delQuestionReply(stringList[1], stringList[2], member)
                needReply = True
            elif len(stringList) == 4:
                reply = delQuestionReplyAt(stringList[1], stringList[2], stringList[3], member)
                needReply = True
            else:
                reply = '格式错误！请检查空格'
                needReply = True
        elif strMessage[:5] == '添加回复*' and groupId != 0:
            stringList = strMessage.split('*')
            if len(stringList) == 3:
                reply = addQuestionReply(stringList[1], stringList[2], member)
                needReply = True
            elif len(stringList) == 4:
                reply = addQuestionReplyAt(stringList[1], stringList[2], stringList[3], member)
                needReply = True
            else:
                reply = '格式错误！请检查星号'
                needReply = True
        elif strMessage[:5] == '删除回复*' and groupId != 0:
            stringList = strMessage.split('*')
            if len(stringList) == 3:
                reply = delQuestionReply(stringList[1], stringList[2], member)
                needReply = True
            elif len(stringList) == 4:
                reply = delQuestionReplyAt(stringList[1], stringList[2], stringList[3], member)
                needReply = True
            else:
                reply = '格式错误！请检查星号'
                needReply = True
        
        elif strMessage[:6] == '添加关键词 ' and groupId != 0:
            stringList = strMessage.split(' ')
            if len(stringList) == 3:
                reply = addKeyReply(stringList[1], stringList[2], member)
                needReply = True
            elif len(stringList) == 4:
                reply = addKeyReplyAt(stringList[1], stringList[2], stringList[3], member)
                needReply = True
            else:
                reply = '格式错误！请检查空格'
                needReply = True
        elif strMessage[:6] == '删除关键词 ' and groupId != 0:
            stringList = strMessage.split(' ')
            if len(stringList) == 3:
                reply = delKeyReply(stringList[1], stringList[2], member)
                needReply = True
            elif len(stringList) == 4:
                reply = delKeyReplyAt(stringList[1], stringList[2], stringList[3], member)
                needReply = True
            else:
                reply = '格式错误！请检查空格'
                needReply = True
        elif strMessage[:6] == '添加关键词*' and groupId != 0:
            stringList = strMessage.split('*')
            if len(stringList) == 3:
                reply = addKeyReply(stringList[1], stringList[2], member)
                needReply = True
            elif len(stringList) == 4:
                reply = addKeyReplyAt(stringList[1], stringList[2], stringList[3], member)
                needReply = True
            else:
                reply = '格式错误！请检查星号'
                needReply = True
        elif strMessage[:6] == '删除关键词*' and groupId != 0:
            stringList = strMessage.split('*')
            if len(stringList) == 3:
                reply = delKeyReply(stringList[1], stringList[2], member)
                needReply = True
            elif len(stringList) == 4:
                reply = delKeyReplyAt(stringList[1], stringList[2], stringList[3], member)
                needReply = True
            else:
                reply = '格式错误！请检查星号'
                needReply = True
        
        elif strMessage[:8] == '关键词回复概率 ' and groupId != 0:
            reply = editKeyProbability(strMessage[8:], member)
            needReply = True

        elif strMessage[:5] == '发起活动 ' and groupId != 0:
            stringList = strMessage[5:].strip().split(' ')
            if len(stringList) != 2:
                reply = '参数错误'
                needReply = True
            else:
                activityName = stringList[0]
                lastMinute = 1
                if stringList[1][-2:] == '分钟':
                    lastMinute = int(stringList[1][:-2])
                elif stringList[1][-2:] == '小时':
                    lastMinute = int(stringList[1][:-2]) * 60
                elif stringList[1][-1:] == '天':
                    lastMinute = int(stringList[1][:-1]) * 1440
                else:
                    lastMinute = int(stringList[1])

                if len(activityName) == 0:
                    reply = '活动名不能为空'
                    needReply = True
                elif lastMinute <= 0:
                    reply = '报名时间必须大于0'
                    needReply = True
                else:
                    reply = addActivity(groupId, memberId, activityName, lastMinute)
                    needReply = True
        elif strMessage[:5] == '删除活动 ' and groupId != 0:
            activityName = strMessage[5:].strip()
            if len(activityName) == 0:
                reply = '活动名不能为空'
                needReply = True
            else:
                reply = delActivity(groupId, memberId, activityName)
                needReply = True
        elif strMessage[:7] == '查看活动名单 ' and groupId != 0:
            activityName = strMessage[7:].strip()
            if len(activityName) == 0:
                reply = '活动名不能为空'
                needReply = True
            else:
                reply = await viewActivity(groupId, activityName, app)
                needReply = True

    if strMessage == '我的权限':
        if memberId ==  botBaseInformation['baseInformation']['Master_QQ']:
            reply = '当前权限：主人\n可以输入主人帮助来获取指令帮助哦~'
            needAt = True
            needReply = True
        elif memberId in botBaseInformation["administrator"]:
            reply = '当前权限：管理员\n可以输入管理员帮助来获取指令帮助哦~'
            needAt = True
            needReply = True
        elif memberId in botBaseInformation["contributors"]:
            reply = '当前权限：贡献者\n可以输入贡献者帮助来获取指令帮助哦~~'
            needAt = True
            needReply = True

    
    if needReply:
        if strMessage != '贡献者帮助' and strMessage != '管理员帮助' and strMessage != '主人帮助':
            logManage.log(getNow.toString(), memberId, strMessage + "; 执行结果：" + reply)
        else:
            logManage.log(getNow.toString(), memberId, strMessage + "; 执行结果：参见command.py里的帮助内容")

    return (needReply, needAt, reply, isImage)


# ==========================================================
# 权限操作

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
# 黑名单操作

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

# ==========================================================
# 屏蔽词操作

# 添加屏蔽词
def addScreenWord(word, botBaseInformation):
    screenWords = dataManage.load_obj('AIScreenWords')
    if word in screenWords:
        return '已经有该屏蔽词了'
    
    screenWords.append(word)
    dataManage.save_obj(screenWords, 'AIScreenWords')
    return '添加成功~！'

# 删除屏蔽词
def delScreenWord(word, botBaseInformation):
    screenWords = dataManage.load_obj('AIScreenWords')
    if not word in screenWords:
        return '没有这个词语哦！'
    screenWords.remove(word)
    dataManage.save_obj(screenWords, 'AIScreenWords')
    return '删除成功'

# 查看屏蔽词
def viewScreenWord(botBaseInformation):
    screenWords = dataManage.load_obj('AIScreenWords')
    return str(screenWords)

# ==========================================================
# 关键词操作
KeyScreenWord = ['RecoveryProbability', 'reply', '~$~']

# 添加绝对匹配
def addQuestionReply(word, reply, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以添加'
    if reply in KeyScreenWord:
        return reply + '为保留字，不可以添加'

    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id))
    if len(keyReply) >= 100:
        return '最多只可以添加100个回复哦~'

    if keyReply.__contains__(word):
        if reply in keyReply[word]:
            return '已经有该回复了'
        else:
            if len(keyReply[word]) >= 15:
                return '单个关键词只能添加15个回复~'
            keyReply[word].append(reply)
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id))
            return '添加成功~'
    else:
        keyReply[word] = [reply]
        dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id))
        return '添加成功~'

# 删除绝对匹配
def delQuestionReply(word, reply, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以删除'
    if reply in KeyScreenWord:
        return reply + '为保留字，不可以删除'
        
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

# 添加绝对匹配（带at）
def addQuestionReplyAt(word, reply, at, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以添加'
    if reply in KeyScreenWord:
        return reply + '为保留字，不可以添加'
        
    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'at')
    if len(keyReply) >= 100:
        return '最多只可以添加100个回复哦~'

    if at == '全体成员':
        at = -1
    else:
        at = int(at)
    if at != -1 and at <= 0:
        return '艾特对象格式错误'
    
    reply = reply + '~$~' + str(at)

    if keyReply.__contains__(word):
        if reply in keyReply[word]:
            return '已经有该回复了'
        else:
            if len(keyReply[word]) >= 15:
                return '单个关键词只能添加15个回复~'
            keyReply[word].append(reply)
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'at')
            return '添加成功~'
    else:
        keyReply[word] = [reply]
        dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'at')
        return '添加成功~'

# 删除绝对匹配（带at）
def delQuestionReplyAt(word, reply, at, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以删除'
    if reply in KeyScreenWord:
        return reply + '为保留字，不可以删除'
        
    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'at')
    if at == '全体成员':
        at = -1
    else:
        at = int(at)
    if at != -1 and at <= 0:
        return '艾特对象格式错误'
    
    reply = reply + '~$~' + str(at)

    if keyReply.__contains__(word):
        if reply in keyReply[word]:
            keyReply[word].remove(reply)
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
def addKeyReply(word, reply, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以添加'
    if reply in KeyScreenWord:
        return reply + '为保留字，不可以添加'
        
    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'key')
    if len(keyReply) >= 100:
        return '最多只可以添加100个回复哦~'

    if keyReply.__contains__(word):
        if reply in keyReply[word]:
            return '已经有该回复了'
        else:
            if len(keyReply[word]) >= 15:
                return '单个关键词只能添加15个回复~'
            keyReply[word].append(reply)
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'key')
            return '添加成功~'
    else:
        keyReply[word] = [reply]
        dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'key')
        return '添加成功~'

# 删除关键词匹配
def delKeyReply(word, reply, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以删除'
    if reply in KeyScreenWord:
        return reply + '为保留字，不可以删除'
        
    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'key')
    if keyReply.__contains__(word):
        if reply in keyReply[word]:
            keyReply[word].remove(reply)
            if len(keyReply[word]) == 0:
                del keyReply[word]
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'key')
            return '删除成功~！'
        else:
            return '没有该词组配对~'
    else:
        return '没有该词组配对~'

# 添加关键词匹配（带at）
def addKeyReplyAt(word, reply, at, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以添加'
    if reply in KeyScreenWord:
        return reply + '为保留字，不可以添加'
        
    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'keyAt')
    if len(keyReply) >= 100:
        return '最多只可以添加100个回复哦~'

    if at == '全体成员':
        at = -1
    else:
        at = int(at)
    if at != -1 and at <= 0:
        return '艾特对象格式错误'
    
    reply = reply + '~$~' + str(at)

    if keyReply.__contains__(word):
        if reply in keyReply[word]:
            return '已经有该回复了'
        else:
            if len(keyReply[word]) >= 15:
                return '单个关键词只能添加15个回复~'
            keyReply[word].append(reply)
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'keyAt')
            return '添加成功~'
    else:
        keyReply[word] = [reply]
        dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'keyAt')
        return '添加成功~'

# 删除关键词匹配（带at）
def delKeyReplyAt(word, reply, at, member):
    if word in KeyScreenWord:
        return word + '为保留字，不可以删除'
    if reply in KeyScreenWord:
        return reply + '为保留字，不可以删除'
        
    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'keyAt')
    if at == '全体成员':
        at = -1
    else:
        at = int(at)
    if at != -1 and at <= 0:
        return '艾特对象格式错误'
    
    reply = reply + '~$~' + str(at)

    if keyReply.__contains__(word):
        if reply in keyReply[word]:
            keyReply[word].remove(reply)
            if len(keyReply[word]) == 0:
                del keyReply[word]
            dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'keyAt')
            return '删除成功~！'
        else:
            return '没有该词组配对~'
    else:
        return '没有该词组配对~'

def editKeyProbability(probability, member):
    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'key')
    p = int(probability)
    if p < 0 or p > 100:
        return '概率只能在0到100之间'
    keyReply['RecoveryProbability'] = p
    dataManage.save_obj(keyReply, 'keyReply/' + str(member.group.id) + 'key')
    return '已将关键词回复概率修改为了' + str(p) + '%'


# =====================
# 添加复杂回复(带艾特)
def addComplexReply(word, reply, member):
    pass

# 删除复杂回复（带艾特）
def delComplexReply(word, reply, member):
    pass

# 添加复杂关键词(带艾特)
def addComplexKey(word, reply, member):
    pass

# 删除复杂关键词（带艾特）
def delComplexKey(word, reply, member):
    pass

# ==========================================================
# 骂人计划操作

def addcursePlanGroup(groupId, botBaseInformation):
    if groupId in botBaseInformation['cursePlanGroup']:
        return '该群已经开启了骂人哦~'
    botBaseInformation['cursePlanGroup'].append(groupId)
    dataManage.save_obj(botBaseInformation, 'baseInformation')
    return '已开启∑(っ°Д°;)っ'
    
def delcursePlanGroup(groupId, botBaseInformation):
    if not groupId in botBaseInformation['cursePlanGroup']:
        return '该群本来就没有开启了骂人!!!∑(ﾟДﾟノ)ノ'
    botBaseInformation['cursePlanGroup'].remove(groupId)
    dataManage.save_obj(botBaseInformation, 'baseInformation')
    return '已关闭，切，懦夫~'

# ==========================================================
# 活动

# 增加活动
def addActivity(groupId, memberId, activityName, lastMinute):
    activityList = dataManage.load_obj('activity')
    if activityList.__contains__(groupId):
        if activityList[groupId].__contains__(activityName):
            return '已经存在该活动了'
        else:
            activityList[groupId][activityName] = {
                'admin': memberId,
                'beginTime': {
                    'hour': getNow.getHour(),
                    'minute': getNow.getMinute()
                },
                'lastMinute': lastMinute,
                'member': []
            }
            dataManage.save_obj(activityList, 'activity')
            return '活动 ' + activityName + '已开启，请在' + str(lastMinute) + '分钟内报名'
    else:
        activityList[groupId] = {}
        activityList[groupId][activityName] = {
            'admin': memberId,
            'beginTime': {
                'hour': getNow.getHour(),
                'minute': getNow.getMinute()
            },
            'lastMinute': lastMinute,
            'member': []
        }
        dataManage.save_obj(activityList, 'activity')
        return '活动 ' + activityName + '已开启，请在' + str(lastMinute) + '分钟内输入\"参加活动 ' + activityName + '\"报名'

# 参与活动
def joinActivity(groupId, memberId, activityName):
    activityList = dataManage.load_obj('activity')
    if activityList.__contains__(groupId):
        if activityList[groupId].__contains__(activityName):
            if memberId in activityList[groupId][activityName]['member']:
                return '你已经参加了该活动哦~'
            else:
                activityList[groupId][activityName]['member'].append(memberId)
                dataManage.save_obj(activityList, 'activity')
                return '参加活动' + activityName + '成功！'
        else:
            return '不存在该活动！'
    else:
        return '不存在该活动！'

# 退出活动
def quitActivity(groupId, memberId, activityName):
    activityList = dataManage.load_obj('activity')
    if activityList.__contains__(groupId):
        if activityList[groupId].__contains__(activityName):
            if memberId in activityList[groupId][activityName]['member']:
                activityList[groupId][activityName]['member'].remove(memberId)
                dataManage.save_obj(activityList, 'activity')
                return '退出成功！'
            else:
                return '你本来就没有参与这个活动~'
        else:
            return '不存在该活动！'
    else:
        return '不存在该活动！'

# 删除活动
def delActivity(groupId, memberId, activityName):
    activityList = dataManage.load_obj('activity')
    if activityList.__contains__(groupId):
        if activityList[groupId].__contains__(activityName):
            del activityList[groupId][activityName]
            if len(activityList[groupId]) == 0:
                del activityList[groupId]
            dataManage.save_obj(activityList, 'activity')
            return '删除成功！'
        else:
            return '不存在该活动！'
    else:
        return '不存在该活动！'

# 活动名单
async def viewActivity(groupId, activityName, app):
    activityList = dataManage.load_obj('activity')
    if activityList.__contains__(groupId):
        if activityList[groupId].__contains__(activityName):
            reply = '活动' + activityName + '名单如下：'
            for i in activityList[groupId][activityName]['member']:
                member = await app.getMember(groupId, i)
                if member == None:
                    continue
                print(member)
                print(i)
                reply += '\n' + member.name + '(' + str(i) + ')'
            return reply
        else:
            return '不存在该活动！'
    else:
        return '不存在该活动！'

def getActivityList(groupId, app):
    activityList = dataManage.load_obj('activity')
    if activityList.__contains__(groupId):
        if len(activityList[groupId]) > 0:
            reply = '本群当前活动如下：'
            for key, value in activityList[groupId].items():
                reply += '\n' + key + '(参与人数：' + str(len(value['member'])) + ')'
            return reply
    return '本群暂无活动'
