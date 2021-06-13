import re

from plugins import tarot
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
    code = code.lower()

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

    elif code[:8] == 'role add': # 添加人物
        tmp = code[8:].strip().split(' ')
        if len(tmp) == 2:
            result = smallFunction.addRole(tmp[1], groupId, tmp[0])
    elif code[:11] == 'role remove': # 删除人物
        result = smallFunction.removeRole(groupId, code[11:].strip())
    elif code == 'role list':
        result = smallFunction.showRoleList(groupId)
    elif code[:9] == 'role show':
        result = smallFunction.showRole(groupId, code[9:].strip())
    elif code[:9] == 'role copy':
        if groupId != 0:
            result = smallFunction.copyRole(code[9:].strip(), groupId, member.id)
            needAt = True
        else:
            result = '这是群聊命令，请在骰娘群里复制属性，因为每个群之间的属性是不共通的哦~'

    elif code[:7] == 'roleadd': # 添加人物
        tmp = code[7:].strip().split(' ')
        if len(tmp) == 2:
            result = smallFunction.addRole(tmp[1], groupId, tmp[0])
    elif code[:10] == 'roleremove': # 删除人物
        result = smallFunction.removeRole(groupId, code[10:].strip())
    elif code == 'rolelist':
        result = smallFunction.showRoleList(groupId)
    elif code[:8] == 'roleshow':
        result = smallFunction.showRole(groupId, code[8:].strip())
    elif code[:8] == 'rolecopy':
        if groupId != 0:
            result = smallFunction.copyRole(code[8:].strip(), groupId, member.id)
            needAt = True
        else:
            result = '这是群聊命令，请在骰娘群里复制属性，因为每个群之间的属性是不共通的哦~'

    elif code[:3] == 'coc':
        tmp = code[3:].strip()
        if tmp.isdigit():
            result = smallFunction.coc7(int(tmp))
            needAt = True
        elif len(tmp) == 0:
            result = smallFunction.coc7(1)
            needAt = True
    elif code[:2] == 'sa':
        if groupId != 0:
            tmp = code[2:].strip()
            if tmp.isdigit():
                result = smallFunction.sa(int(tmp), groupId, member.id)
                needAt = True
        else:
            result = '这是群聊命令'
    elif code == 'sc':
        if groupId != 0:
            result = smallFunction.rasan(groupId, member.id)
            needAt = True
        else:
            result = '这是群聊命令'
    elif code[:2] == 'sc':
        if groupId != 0:
            tmp1 = code[2:].strip()
            tmp2 = tmp1.split('/')

            success = 0
            fail_dick_number = 0
            fail_dick_size = 1
            fail_dick_base = 0
            if len(tmp2) == 2 and tmp2[0].isdigit():
                success = int(tmp2[0])
                if tmp2[1][0] == 'd':
                    fail_dick_number = 1  # 默认投一个骰子
                    tmp3 = tmp2[1][1:].split('+')
                    if len(tmp3) == 1 and tmp3[0].isdigit():
                        fail_dick_size = int(tmp3[0])
                    elif len(tmp3) == 2 and tmp3[0].isdigit() and tmp3[1].isdigit():
                        fail_dick_size = int(tmp3[0])
                        fail_dick_base = int(tmp3[1])
                else:
                    tmp3 = tmp2[1].split('d')
                    if len(tmp3) == 2 and tmp3[0].isdigit():
                        fail_dick_number = int(tmp3[0])
                        tmp4 = tmp3[1].split('+')
                        if len(tmp4) == 1 and tmp4[0].isdigit():
                            fail_dick_size = int(tmp4[0])
                        elif len(tmp4) == 2 and tmp4[0].isdigit() and tmp4[1].isdigit():
                            fail_dick_size = int(tmp4[0])
                            fail_dick_base = int(tmp4[1])
            if fail_dick_number > 0 and fail_dick_size > 0:
                result = smallFunction.sc(success, fail_dick_number, fail_dick_size, fail_dick_base, groupId, member.id)
                needAt = True
        else:
            result = '这是群聊命令'


    elif code == 'rd':
        result = smallFunction.rd(1, 100, 1)
        needAt = True
    elif code == 'rp':
        result = smallFunction.rd(1, 20, 1)
        needAt = True
    elif code[:2] == 'rd':
        size = 0
        times = 1
        if code[2:].isdigit():
            size = int(code[2:])
        else:
            tmp = code[2:].split('*')
            if len(tmp) == 2 and tmp[0].isdigit() and tmp[1].isdigit():
                size = int(tmp[0])
                times = int(tmp[1])
        result = smallFunction.rd(1, size, times)
    elif code[0] == 'r' and 'd' in code and code[len(code) - 1] != 'd':
        num = 0
        size = 0
        times = 1
        index = code.find('d')
        if code[1: index].isdigit():
            num = int(code[1: index])
        if code[code.find('d') + 1:].isdigit():
            size = int(code[code.find('d') + 1:])
        tmp = code[code.find('d') + 1:].split('*')
        if len(tmp) == 2 and tmp[0].isdigit() and tmp[1].isdigit():
            size = int(tmp[0])
            times = int(tmp[1])

        result = smallFunction.rd(num, size, times)
        if result != '啊嘞？':
            needAt = True
    elif code[:3] == 'sta': # 追加属性
        if groupId != 0:
            if len(code) > 4:
                attribute = code[3:].strip()
                result = smallFunction.sta(attribute, groupId, member.id)
                needAt = True
        else:
            result = '这是群聊命令'
    elif code[:3] == 'stc': # 修改属性
        if groupId != 0:
            if len(code) > 4:
                attribute = code[3:].strip()
                result = smallFunction.stc(attribute, groupId, member.id)
                needAt = True
        else:
            result = '这是群聊命令'
    elif code[:3] == 'std': # 删除属性
        if groupId != 0:
            if len(code) > 4:
                attribute = code[4:]
                result = smallFunction.std(attribute, groupId, member.id)
                needAt = True
        else:
            result = '这是群聊命令'

    elif code[:7] == 'st from': # 设置属性
        if groupId != 0:
            attribute = code[7:].strip()
            result = smallFunction.copyRole(code[7:].strip(), groupId, member.id)
            needAt = True
        else:
            result = '这是群聊命令'
    elif code[:2] == 'st': # 设置属性
        if groupId != 0:
            if len(code) > 3:
                attribute = code[2:].strip()
                result = smallFunction.st(attribute, groupId, member.id)
                needAt = True
        else:
            result = '这是群聊命令'
    elif code == 'show': # 展示属性
        if groupId != 0:
            result = smallFunction.show(groupId, member.id)
            needAt = True
        else:
            result = '这是群聊命令'
    elif code == 'show all' or code == 'showall': # 展示属性
        if groupId != 0:
            result = smallFunction.showAll(groupId, member.id)
            needAt = True
        else:
            result = '这是群聊命令'
    elif code[:4] == 'show':
        if groupId != 0:
            result = smallFunction.showSingle(code[4:].strip(), groupId, member.id)
        else:
            result = '这是群聊命令'
    elif code[:2] == 'ra': # 鉴定属性
        if groupId != 0:
            if len(code) > 3:
                attribute = code[2:].strip()
                result = smallFunction.ra(attribute, groupId, member.id)
                needAt = True
        else:
            result = '这是群聊命令'
    elif code == 'clear': # 清空属性
        if groupId != 0:
            result = smallFunction.stClear(groupId)
            needAt = True
        else:
            result = '这是群聊命令'
    elif code == 'ex': # 清空属性
        if groupId != 0:
            result = '复制下面冒号后面这段话就可以导出属性：' + smallFunction.export(groupId, member.id)
        else:
            result = '这是群聊命令'


    if result == '' and isImage == '':
        result = '未知指令：' + code + '\n请输入\"帮助\"查看帮助\n请输入\"骰娘\"查看骰娘帮助\n请输入\"游戏帮助\"查看游戏帮助'
    return (result, needAt, isImage)
