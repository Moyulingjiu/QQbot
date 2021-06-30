# 这部分是独立成立的词集

from plugins import dataManage
import random


def reply(strMessage, member, botBaseInformation):
    questionReply = dataManage.load_obj('keyReply/' + str(member.group.id))
    KeyReply = dataManage.load_obj('keyReply/' + str(member.group.id) + 'key')
    questionReplyAt = dataManage.load_obj('keyReply/' + str(member.group.id) + 'at')
    KeyReplyAt = dataManage.load_obj('keyReply/' + str(member.group.id) + 'keyAt')

    needReply = False
    needAt = False
    reply = ''
    AtId = 0

    p = random.randrange(0, 100)
    if not KeyReply.__contains__('RecoveryProbability'):
        KeyReply['RecoveryProbability'] = 100
        dataManage.save_obj(KeyReply, 'keyReply/' + str(member.group.id) + 'key')

    if botBaseInformation['reply']['lastMinute'] <= 10:
        # 全字段匹配
        if questionReply.__contains__(strMessage):
            replyList = questionReply[strMessage]
            if len(replyList) > 0:
                tmpNumber = random.randrange(0, len(replyList))
                reply = replyList[tmpNumber]
                needReply = True
                botBaseInformation['reply']['lastMinute'] += 1
                dataManage.save_obj(botBaseInformation, 'baseInformation')

        # 全字段匹配带at
        if not needReply:
            if questionReplyAt.__contains__(strMessage):
                replyList = questionReplyAt[strMessage]
                if len(replyList) > 0:
                    tmpNumber = random.randrange(0, len(replyList))
                    tmp = replyList[tmpNumber].split('~$~')
                    reply = tmp[0]
                    AtId = int(tmp[1])
                    needReply = True
                    needAt = True
                    botBaseInformation['reply']['lastMinute'] += 1
                    dataManage.save_obj(botBaseInformation, 'baseInformation')

        # 关键词匹配
        if not needReply:
            if p < KeyReply['RecoveryProbability']:
                for i in KeyReply:
                    if i in strMessage:
                        replyList = KeyReply[i]
                        if len(replyList) > 0:
                            tmpNumber = random.randrange(0, len(replyList))
                            reply = replyList[tmpNumber]
                            needReply = True
                            botBaseInformation['reply']['lastMinute'] += 1
                            dataManage.save_obj(botBaseInformation, 'baseInformation')
                            break

        # 关键词匹配（带艾特）
        if not needReply:
            if p < KeyReply['RecoveryProbability']:
                for i in KeyReplyAt:
                    if i in strMessage:
                        replyList = KeyReplyAt[i]
                        if len(replyList) > 0:
                            tmpNumber = random.randrange(0, len(replyList))
                            tmp = replyList[tmpNumber].split('~$~')
                            reply = tmp[0]
                            AtId = int(tmp[1])
                            needReply = True
                            needAt = True
                            botBaseInformation['reply']['lastMinute'] += 1
                            dataManage.save_obj(botBaseInformation, 'baseInformation')
                            break

    print('KeyReply AtId:', AtId)
    print('KeyReply Reply:', reply)
    return needReply, reply, '', AtId, needAt
