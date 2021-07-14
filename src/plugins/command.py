from plugins import tarot
from plugins import dataManage
from plugins import TRPG

# ==========================================================

key_allow = [
    '#',
    ',', '，',
    '.', '。',
    '!', '！',
    '?', '？',
    ':', '：',
    ';', '；',
    '+',
    '-',
    '/',
    '='
]
table = TRPG.TableRolePlayGame()


# =========================================================
# 触发词
def add_key(key, member, group_id, bot_information):
    if group_id == 0:
        qq = member.id
        if bot_information['keyToken']['friend'].__contains__(qq):
            if key in bot_information['keyToken']['friend'][qq]:
                return '已启用该关键字'
            else:
                bot_information['keyToken']['friend'][qq].append(key)
                dataManage.save_obj(bot_information, 'baseInformation')
                return '操作成功！启用关键字“' + key + '”，使用“*key list”命令可以查看当前启用的关键字'
        else:
            bot_information['keyToken']['friend'][qq] = []
            bot_information['keyToken']['friend'][qq].append(key)
            dataManage.save_obj(bot_information, 'baseInformation')
            return '操作成功！启用关键字“' + key + '”，使用“*key list”命令可以查看当前启用的关键字'
    else:
        if bot_information['keyToken']['group'].__contains__(group_id):
            if key in bot_information['keyToken']['group'][group_id]:
                return '已启用该关键字'
            else:
                bot_information['keyToken']['group'][group_id].append(key)
                dataManage.save_obj(bot_information, 'baseInformation')
                return '操作成功！群内启用关键字“' + key + '”，使用“*key list”命令可以查看当前启用的关键字'
        else:
            bot_information['keyToken']['group'][group_id] = []
            bot_information['keyToken']['group'][group_id].append(key)
            dataManage.save_obj(bot_information, 'baseInformation')
            return '操作成功！群内启用关键字“' + key + '”，使用“*key list”命令可以查看当前启用的关键字'


def remove_key(key, member, group_id, bot_information):
    if group_id == 0:
        qq = member.id
        if bot_information['keyToken']['friend'].__contains__(qq):
            if key in bot_information['keyToken']['friend'][qq]:
                del bot_information['keyToken']['friend'][qq][key]
                if len(bot_information['keyToken']['friend'][qq]) == 0:
                    del bot_information['keyToken']['friend'][qq]
                dataManage.save_obj(bot_information, 'baseInformation')
                return '已关闭该关键字'
            else:
                return '该关键字未启用'
        else:
            return '该关键字未启用'
    else:
        if bot_information['keyToken']['group'].__contains__(group_id):
            if key in bot_information['keyToken']['group'][group_id]:
                bot_information['keyToken']['group'][group_id].remove(key)
                if len(bot_information['keyToken']['group'][group_id]) == 0:
                    del bot_information['keyToken']['group'][group_id]
                dataManage.save_obj(bot_information, 'baseInformation')
                return '已关闭该关键字'
            else:
                return '该关键字未启用'
        else:
            return '该关键字未启用'


def show_key(member, group_id, bot_information):
    if group_id == 0:
        qq = member.id
        if bot_information['keyToken']['friend'].__contains__(qq):
            result = '启用关键字如下：'
            for i in bot_information['keyToken']['friend'][qq]:
                result += i
            return result
        else:
            return '未启用任何附加关键字'
    else:
        if bot_information['keyToken']['group'].__contains__(group_id):
            result = '启用关键字如下：'
            for i in bot_information['keyToken']['group'][group_id]:
                result += i
            return result
        else:
            return '未启用任何附加关键字'


# ==========================================================

def help_function():
    return 'help/帮助.png'


def help_thrower():
    return 'help/骰娘帮助.png'


def help_clock():
    return 'help/打卡帮助.png'


def help_activity():
    return 'help/活动帮助.png'


def help_contributor():
    return 'help/贡献者帮助.png'


def help_administrator():
    return 'help/管理员帮助.png'


def help_master():
    return 'help/主人帮助.png'


def help_tarot():
    return 'help/塔罗牌帮助.png'


def help_game():
    return 'help/游戏帮助.png'


def function(code, member, app, group_id, bot_information, mode):
    global key_allow

    needAt = False
    result = ''
    isImage = ''

    if mode == 0:
        name = member.nickname
    else:
        name = member.name

    if code == 'help':
        isImage = help_function()
    elif code == 'help tarot':
        isImage = help_tarot()

    elif code[:7] == 'key add':
        tmp = code[7:].strip()
        if len(tmp) == 1:
            if tmp in key_allow:
                result = add_key(tmp, member, group_id, bot_information)
            else:
                result = '不允许这个符号，仅允许扩展以下符号：'
                for i in key_allow:
                    result += i
        else:
            result = '格式错误！'
    elif code[:10] == 'key remove':
        tmp = code[10:].strip()
        if len(tmp) == 1:
            result = remove_key(tmp, member, group_id, bot_information)
        else:
            result = '格式错误！'
    elif code == 'key list':
        result = show_key(member, group_id, bot_information)

    elif code == 'tarotb':
        result = tarot.GetTarot()
    elif code == 'tarotl':
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

    elif code == 'jrrp':
        result = '*运势*'

    elif code[:8] == 'role add':  # 添加人物
        tmp = code[8:].strip().split(' ')
        if len(tmp) == 2:
            result = table.add_role(tmp[1], group_id, tmp[0])
    elif code[:11] == 'role remove':  # 删除人物
        result = table.remove_role(group_id, code[11:].strip())
    elif code == 'role list':
        result = table.show_role_list(group_id)
    elif code[:9] == 'role show':
        result = table.show_role(group_id, code[9:].strip())
    elif code[:9] == 'role copy':
        if group_id != 0:
            result = table.copy_role(code[9:].strip(), group_id, member.id)
            needAt = True
        else:
            result = '这是群聊命令，请在骰娘群里复制属性，因为每个群之间的属性是不共通的哦~'

    elif code[:3] == 'coc':
        tmp = code[3:].strip()
        if tmp.isdigit():
            result = table.coc7(int(tmp))
            needAt = True
        elif len(tmp) == 0:
            result = table.coc7(1)
            needAt = True
    elif code[:2] == 'sa':
        if group_id != 0:
            tmp = code[2:].strip()
            if tmp.isdigit():
                result = table.sa(int(tmp), group_id, member.id)
                needAt = True
        else:
            result = '这是群聊命令'
    elif code == 'sc':
        if group_id != 0:
            result = table.rasan(group_id, member.id)
            needAt = True
        else:
            result = '这是群聊命令'
    elif code[:2] == 'sc':
        if group_id != 0:
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
                result = table.sc(success, fail_dick_number, fail_dick_size, fail_dick_base, group_id,
                                  member.id)
                needAt = True
        else:
            result = '这是群聊命令'


    elif code == 'rd':
        result = table.rd(1, 100, 1)
        needAt = True
    elif code == 'rp':
        result = table.rd(1, 20, 1)
        needAt = True
    elif code[:2] == 'rd':
        size = 1
        times = 1
        if code[2:].isdigit():
            size = int(code[2:])
        else:
            tmp = code[2:].split('*')
            if len(tmp) == 2 and tmp[0].isdigit() and tmp[1].isdigit():
                size = int(tmp[0])
                times = int(tmp[1])
        if size > 0:
            result = table.rd(1, size, times)
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
        if size > 0 and num > 0:
            result = table.rd(num, size, times)
            if result != '啊嘞？':
                needAt = True
    elif code[:3] == 'sta':  # 追加属性
        if group_id != 0:
            if len(code) > 4:
                attribute = code[3:].strip()
                result = table.sta(attribute, group_id, member.id)
                needAt = True
        else:
            result = '这是群聊命令'
    elif code[:3] == 'stc':  # 修改属性
        if group_id != 0:
            if len(code) > 4:
                attribute = code[3:].strip()
                result = table.stc(attribute, group_id, member.id)
                needAt = True
        else:
            result = '这是群聊命令'
    elif code[:3] == 'std':  # 删除属性
        if group_id != 0:
            if len(code) > 4:
                attribute = code[4:]
                result = table.std(attribute, group_id, member.id)
                needAt = True
        else:
            result = '这是群聊命令'

    elif code[:7] == 'st from':  # 设置属性
        if group_id != 0:
            role_name = code[7:].strip()
            result = table.copy_role(role_name, group_id, member.id)
            needAt = True
        else:
            result = '这是群聊命令'
    elif code[:5] == 'st to':  # 把属性设置到人物卡
        if group_id != 0:
            role_name = code[5:].strip()
            result = table.copy_to_role(role_name, group_id, member.id)
            needAt = True
        else:
            result = '这是群聊命令'
    elif code[:2] == 'st':  # 设置属性
        if group_id != 0:
            if len(code) > 3:
                attribute = code[2:].strip()
                result = table.st(attribute, group_id, member.id)
                needAt = True
        else:
            result = '这是群聊命令'

    elif code == 'show':  # 展示属性
        if group_id != 0:
            result = table.show(group_id, member.id)
            needAt = True
        else:
            result = '这是群聊命令'
    elif code == 'show all' or code == 'showall':  # 展示属性
        if group_id != 0:
            result = table.show_all(group_id, member.id)
            needAt = True
        else:
            result = '这是群聊命令'
    elif code[:4] == 'show':
        if group_id != 0:
            result = table.show_single(code[4:].strip(), group_id, member.id)
        else:
            result = '这是群聊命令'
    elif code[:2] == 'ra':  # 鉴定属性
        if group_id != 0:
            if len(code) > 3:
                attribute = code[2:].strip()
                result = table.ra(attribute, group_id, member.id)
                needAt = True
        else:
            result = '这是群聊命令'
    elif code == 'clear all':  # 清空属性
        if group_id != 0:
            result = table.clear_all(group_id)
            needAt = True
        else:
            result = '这是群聊命令'
    elif code == 'clear':  # 清空属性
        if group_id != 0:
            result = table.clear_single(group_id, member.id)
            needAt = True
        else:
            result = '这是群聊命令'
    elif code == 'ex':  # 清空属性
        if group_id != 0:
            result = table.export(group_id, member.id)
        else:
            result = '这是群聊命令'
    elif code == 'name':  # 随机名字
        result = name + TRPG.random_name(1)
    elif code[:4] == 'name':  # 随机名字
        tmp = code[4:].strip()
        if tmp.isdigit():
            result = name + TRPG.random_name(int(tmp))

    if result == '':
        express = TRPG.Expression(code.replace(' ', ''))
        try:
            result = code + '=' + str(express.show())
        except OverflowError as e:
            result = '运算超时'
        except ArithmeticError as e:
            err = str(e)
            if err == 'Non-expression':
                print('Non-expression')
            elif err == 'wrong format':
                result = '表达式无法解析'

    if result == '' and isImage == '' and code.isalnum():
        result = '未知指令：' + code + '\n请输入\"帮助\"查看帮助\n请输入\"骰娘\"查看骰娘帮助\n请输入\"游戏帮助\"查看游戏帮助'

    return result, needAt, isImage
