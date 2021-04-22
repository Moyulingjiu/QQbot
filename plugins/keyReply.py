# 这部分是独立成立的词集

from plugins import dataManage
import random

def reply(strMessage, member):
    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id))
    needReply = False
    needAt = False
    reply = ''

    rand = random.randrange(0, 100)
    if rand < 50:
        if keyReply.__contains__(strMessage):
            replyList = keyReply[strMessage]
            if len(replyList) > 0:
                tmpNumber = random.randrange(0, len(replyList))
                reply = replyList[tmpNumber]
                needReply = True

    return (needReply, needAt, reply)