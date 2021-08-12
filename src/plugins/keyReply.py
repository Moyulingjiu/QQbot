# 这部分是独立成立的词集

from plugins import dataManage
import random


def reply(strMessage, member, config, statistics):
    questionReply = {}
    KeyReply = {}
    questionReplyAt = {}
    KeyReplyAt = {}

    if config['key_reply'].__contains__('question'):
        questionReply = config['key_reply']['question']
    if config['key_reply'].__contains__('key'):
        KeyReply = config['key_reply']['key']
    if config['key_reply'].__contains__('question_at'):
        questionReplyAt = config['key_reply']['question_at']
    if config['key_reply'].__contains__('key_at'):
        KeyReplyAt = config['key_reply']['key_at']

    needReply = False
    needAt = False
    reply = ''
    AtId = 0

    p = random.randrange(0, 100)
    if not KeyReply.__contains__('RecoveryProbability'):
        KeyReply['RecoveryProbability'] = 100
        config['key_reply']['key'] = KeyReply
        dataManage.save_group(member.group.id, config)

    # if statistics['last_minute'] <= 10:
    # 全字段匹配
    if questionReply.__contains__(strMessage):
        replyList = questionReply[strMessage]
        if len(replyList) > 0:
            tmpNumber = random.randrange(0, len(replyList))
            reply = replyList[tmpNumber]
            needReply = True
            statistics['last_minute'] += 1
            dataManage.save_statistics(statistics)

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
                statistics['last_minute'] += 1
                dataManage.save_statistics(statistics)

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
                        statistics['last_minute'] += 1
                        dataManage.save_statistics(statistics)
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
                        statistics['last_minute'] += 1
                        dataManage.save_statistics(statistics)
                        break

    print('\tKeyReply AtId:', AtId)
    print('\tKeyReply Reply:', reply)
    return needReply, reply, '', AtId, needAt
