# 这部分是独立成立的词集

from plugins import dataManage
import random

def reply(strMessage, member, botBaseInformation):
    keyReply = dataManage.load_obj('keyReply/' + str(member.group.id))
    needReply = False
    needAt = False
    reply = ''
    if botBaseInformation['reply']['lastMinute'] <= 10:
        if keyReply.__contains__(strMessage):
            replyList = keyReply[strMessage]
            if len(replyList) > 0:
                tmpNumber = random.randrange(0, len(replyList))
                reply = replyList[tmpNumber]
                needReply = True
                botBaseInformation['reply']['lastMinute'] += 1
                dataManage.save_obj(botBaseInformation, 'baseInformation')


    return (needReply, needAt, reply)