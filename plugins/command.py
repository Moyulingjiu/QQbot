import re

from plugins import tarot
from plugins import game
from plugins import smallFunction

# ==========================================================


def help():
    return 'help/帮助.png'

def helpThrower():
    return 'help/骰娘帮助.png'


def helpClock():
    return 'help/打卡帮助.png'

def helpActivity():
    return 'help/活动帮助.png'

def helpContributor():
    return 'help/贡献者帮助.png'

def helpAdmministor():
    return 'help/管理员帮助.png'

def helpMaster():
    return 'help/主人帮助.png'

def helpTarot():
    return 'help/塔罗牌帮助.png'

def helpGame():
    return 'help/游戏帮助.png'


def function(code, member, app, groupId):
    needAt = False
    result = ''
    isImage = ''

    if code == 'help':
        isImage = help()
    elif code == 'help tarot':
        isImage = helpTarot()

    elif code == 'tarotB' or code == 'tarotb':
        result = tarot.GetTarot()
    elif code == 'tarotL' or code == 'tarotl':
        result = tarot.GetTarot2()
    elif code == 'tarot':
        result = tarot.tarot()
    elif code == 'tarot 时间':
        result = tarot.tarotTime()
    elif code == 'tarot 是非':
        result = tarot.tarotIs()
    elif code == 'tarot 圣三角':
        result = tarot.tarotIs()
    elif code == 'tarot 钻石展开法':
        result = tarot.tarotBussiness()
    elif code == 'tarot 恋人金字塔':
        result = tarot.tarotLove()
    elif code == 'tarot 自我探索':
        result = tarot.tarotSelf()
    elif code == 'tarot 吉普赛十字':
        result = tarot.tarotCross()
    elif code == 'tarot 二选一':
        result = tarot.tarotChoose()
    elif code == 'tarot 关系发展':
        result = tarot.tarotForward()
    elif code == 'tarot 六芒星':
        result = tarot.tarotHexagram()
    elif code == 'tarot 凯尔特十字':
        result = tarot.tarotCelticCross()

    elif code == 'game':
        result = game.game()

    elif code == 'rd':
        result = smallFunction.rd(1, 100)
        needAt = True
    elif code == 'rp':
        result = smallFunction.rd(1, 20)
        needAt = True
    elif code[:2] == 'rd':
        size = 0
        if code[2:].isdigit():
            size = int(code[2:])
        result = smallFunction.rd(1, size)
    elif code[0] == 'r' and 'd' in code and code[len(code) - 1] != 'd':
        num = 0
        size = 0
        try:
            num = int(code[1: code.find('d')])
            size = int(code[code.find('d') + 1: len(code)])
        except ValueError as e:
            pass
        result = smallFunction.rd(num, size)
        if result != '啊嘞？':
            needAt = True
    elif code[:3] == 'sta' and groupId != 0: # 追加属性
        if len(code) > 4:
            attribute = code[3:].strip()
            result = smallFunction.sta(attribute, groupId, member.id)
            needAt = True
    elif code[:3] == 'stc' and groupId != 0: # 修改属性
        if len(code) > 4:
            attribute = code[3:].strip()
            result = smallFunction.stc(attribute, groupId, member.id)
            needAt = True
    elif code[:3] == 'std' and groupId != 0: # 删除属性
        if len(code) > 4:
            attribute = code[4:]
            result = smallFunction.std(attribute, groupId, member.id)
            needAt = True
    elif code[:2] == 'st' and groupId != 0: # 设置属性
        if len(code) > 3:
            attribute = code[2:].strip()
            result = smallFunction.st(attribute, groupId, member.id)
            needAt = True
    elif code == 'show' and groupId != 0: # 展示属性
        result = smallFunction.show(groupId, member.id)
        needAt = True
    elif (code == 'show all' or code == 'showall') and groupId != 0: # 展示属性
        result = smallFunction.showAll(groupId, member.id)
        needAt = True
    elif code[:2] == 'ra' and groupId != 0: # 鉴定属性
        if len(code) > 3:
            attribute = code[2:].strip()
            result = smallFunction.ra(attribute, groupId, member.id)
        needAt = True
    elif code == 'clear' and groupId != 0: # 清空属性
        result = smallFunction.stClear(groupId)
        needAt = True


    if result == '' and isImage == '':
        result = '未知指令：' + code + '\n请输入\"*help\"查看帮助'
    return (result, needAt, isImage)
