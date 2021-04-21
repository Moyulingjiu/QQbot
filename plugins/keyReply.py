# 这部分是独立成立的词集

from plugins import dataManage
import random

def reply(strMessage):
    keyReply = dataManage.load_obj('keyReply')
    needReply = False
    needAt = False
    reply = ''

    if keyReply.__contains__(strMessage):
        replyList = keyReply[strMessage]
        tmpNumber = random.randrange(0, len(replyList))
        reply = replyList[tmpNumber]
        needReply = True

    return (needReply, needAt, reply)