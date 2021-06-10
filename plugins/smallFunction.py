
import random

from plugins import dataManage

# ==========================================================
# 丢色子

def coin():
    ran = random.randint(1, 6)
    if ran % 2 == 0:
        return '你抛出的硬币是：正面'
    else:
        return '你抛出的硬币是：反面'
    # return '你抛出的硬币是：反面'

def dick():
    return '你丢出的点数是：' + str(random.randint(1, 6))

def dick_sys(max_range):
    return random.randint(1, max_range)

# ==========================================================
# 丢色子

def rasan(groupId, memberId):
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        return '意志属性，请使用rd命令手动检验'
    if not coc[groupId].__contains__(memberId):
        return '意志属性，请使用rd命令手动检验'

    powe = -1
    if coc[groupId][memberId].__contains__('意志'):
        powe = coc[groupId][memberId]['意志']
    elif coc[groupId][memberId].__contains__('pow'):
        powe = coc[groupId][memberId]['pow']


    tmp = dick_sys(100)
    if tmp <= powe:
        return '你扔出来的点数为：' + str(tmp) + '（意志：' + str(powe) + '） 鉴定成功！小柒也在为你祈祷哦~'
    else:
        return '你扔出来的点数为：' + str(tmp) + '（意志：' + str(powe) + '） 鉴定失败！摸摸头，不要哭'

def sc(success, fail_dick_number, fail_dick_size, fail_dick_base, groupId, memberId):
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        return '未能找到san值、意志两个属性，请使用rd命令手动检验'
    if not coc[groupId].__contains__(memberId):
        return '未能找到san值、意志两个属性，请使用rd命令手动检验'

    san = -1
    powe = -1
    result = '鉴定结果如下：'

    if coc[groupId][memberId].__contains__('san'):
        san = coc[groupId][memberId]['san']
    elif coc[groupId][memberId].__contains__('san值'):
        san = coc[groupId][memberId]['san值']
    elif coc[groupId][memberId].__contains__('理智'):
        san = coc[groupId][memberId]['理智']
    elif coc[groupId][memberId].__contains__('理智值'):
        san = coc[groupId][memberId]['理智值']

    if coc[groupId][memberId].__contains__('意志'):
        powe = coc[groupId][memberId]['意志']
    elif coc[groupId][memberId].__contains__('pow'):
        powe = coc[groupId][memberId]['pow']

    if san == -1 or powe == -1:
        return '未能找到san值、意志两个属性，请使用rd命令手动检验'

    tmp = dick_sys(100)
    if tmp <= powe:
        result = '鉴定成功！'
        san -= success
        if san <= 0:
            san = 0
        result += '\nsan值减少：' + str(success)
        result += '\n目前san值：' + str(san) + '/' + str(powe)
        coc[groupId][memberId]['san'] = san
        coc[groupId][memberId]['san值'] = san
        coc[groupId][memberId]['理智'] = san
        coc[groupId][memberId]['理智值'] = san
    else:
        sum = fail_dick_base
        while fail_dick_number > 0:
            fail_dick_number -= 1
            sum += dick_sys(fail_dick_size)
        result = '鉴定失败！'
        san -= sum
        if san <= 0:
            san = 0
        result += '\nsan值减少：' + str(sum)
        result += '\n目前san值：' + str(san) + '/' + str(powe)
        coc[groupId][memberId]['san'] = san
        coc[groupId][memberId]['san值'] = san
        coc[groupId][memberId]['理智'] = san
        coc[groupId][memberId]['理智值'] = san
    dataManage.save_obj(coc, 'coc')
    return result

def sa(num, groupId, memberId):
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        return '未能找到san值、意志两个属性，请先使用sta指令为你自己添加这个两个属性'
    if not coc[groupId].__contains__(memberId):
        return '未能找到san值、意志两个属性，请先使用sta指令为你自己添加这个两个属性'

    san = -1
    powe = -1

    if coc[groupId][memberId].__contains__('san'):
        san = coc[groupId][memberId]['san']
    elif coc[groupId][memberId].__contains__('san值'):
        san = coc[groupId][memberId]['san值']
    elif coc[groupId][memberId].__contains__('理智'):
        san = coc[groupId][memberId]['理智']
    elif coc[groupId][memberId].__contains__('理智值'):
        san = coc[groupId][memberId]['理智值']

    if coc[groupId][memberId].__contains__('意志'):
        powe = coc[groupId][memberId]['意志']
    elif coc[groupId][memberId].__contains__('pow'):
        powe = coc[groupId][memberId]['pow']

    if san == -1 or powe == -1:
        return '未能找到san值、意志两个属性，请先使用sta指令为你自己添加这个两个属性'

    san += num
    if san > powe:
        san = powe
    coc[groupId][memberId]['san'] = san
    coc[groupId][memberId]['san值'] = san
    coc[groupId][memberId]['理智'] = san
    coc[groupId][memberId]['理智值'] = san
    return '恢复' + str(num) + 'san值，当前san值：' + str(san) + '/' + str(powe)


def coc7(num):
    result = '你的人物制作：'

    if num <= 0:
        return result
    elif num > 20:
        return 'emmm，你确定要那么多板子吗？输入一个小于20的数字试试吧~'

    for i in range(num):
        strength = (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5
        con = (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5
        size = (random.randint(1, 6) + random.randint(1, 6) + 6) * 5
        dex = (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5
        appe = (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5
        intt = (random.randint(1, 6) + random.randint(1, 6) + 6) * 5
        powe = (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5
        edu = (random.randint(1, 6) + random.randint(1, 6) + 6) * 5

        lucky = (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5

        result += '\n力量：' + str(strength)
        result += ' 体质：' + str(con)
        result += ' 体型：' + str(size)
        result += ' 敏捷：' + str(dex)
        result += ' 外貌：' + str(appe)
        result += ' 智力：' + str(intt)
        result += ' 意志：' + str(powe)
        result += ' 教育：' + str(edu)
        result += ' 幸运：' + str(lucky)

        result += ' 共计：'
        total = strength + con + size + dex + appe + intt + powe + edu + lucky
        result += str(total) + '/' + str(total + lucky)

    return result

def rd(num, size, times):
    if num > 5 or times != 1:
        if num > 200:
            return '诶诶诶！投那么骰子，我会晕掉的'
        else:
            sumDick = 0
            result = '点数：'
            if times != 1:
                result += '('
            for i in range(0, num):
                if i != 0:
                    result += '+'
                tmp = random.randint(1, size)
                sumDick += tmp
                result += str(tmp)
            if times != 1:
                result += ')X' + str(times) + '=' + str(sumDick * times)
            else:
                result += '=' + str(sumDick)
            return result
    if size > 1000:
        return '啊？那么多面，这个骰子做不出来诶'
    if num < 1 or size < 2:
        return '啊嘞？'
    
    if num == 1:
        return '扔出的点数为：' + str(random.randint(1, size))

    result = '\n'
    sumDick = 0
    for i in range(0, num):
        dicks = random.randint(1, size)
        sumDick += dicks
        result += '骰子' + str(i + 1) + '：' + str(dicks) + '\n'
    return result + '合计点数为：' + str(sumDick)

def st(attribute, groupId, memberId):
    coc = dataManage.load_obj('coc')
    if coc.__contains__(groupId):
        del coc[groupId]
    dataManage.save_obj(coc, 'coc')
    sta(attribute, groupId, memberId)
    coc = dataManage.load_obj('coc')
    return '修改成功！目前有属性个数：' + str(len(coc[groupId][memberId]))

def sta(attribute, groupId, memberId):
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        coc[groupId] = {}
    if not coc[groupId].__contains__(memberId):
        coc[groupId][memberId] = {}

    name = ''
    number = 0
    lenghth = len(attribute)
    i = 0
    while i < lenghth:
        if attribute[i].isdigit():
            while attribute[i].isdigit():
                number = number * 10 + int(attribute[i])
                i += 1
                if i >= lenghth:
                    break
            if number > 100:
                number = 100
            name = name.strip()
            if len(name) > 0:
                coc[groupId][memberId][name] = number
            name = ''
            number = 0

        if i >= lenghth:
            break
        name += attribute[i]
        i += 1
            
    dataManage.save_obj(coc, 'coc')
    return '追加成功！目前有属性个数：' + str(len(coc[groupId][memberId]))

def stc(attribute, groupId, memberId):
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        return '不存在该属性'
    if not coc[groupId].__contains__(memberId):
        return '不存在该属性'


    name = ''
    number = 0
    lenghth = len(attribute)
    i = 0
    index = 0
    while i < lenghth:
        if attribute[i].isdigit():
            while attribute[i].isdigit():
                number = number * 10 + int(attribute[i])
                i += 1
                if i >= lenghth:
                    break
            if number > 100:
                number = 100
            name = name.strip()
            if len(name) > 0:
                if coc[groupId][memberId].__contains__(name):
                    coc[groupId][memberId][name] = number
                    index += 1
            name = ''
            number = 0

        if i >= lenghth:
            break
        name += attribute[i]
        i += 1

    dataManage.save_obj(coc, 'coc')
    return '成功修改' + str(index) + '个属性'

def std(attribute, groupId, memberId):
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        return '不存在该属性'
    if not coc[groupId].__contains__(memberId):
        return '不存在该属性'

    attributeList = attribute.split(' ')
    index = 0
    for i in attributeList:
        i = i.strip()
        if not coc[groupId][memberId].__contains__(i):
            continue
        index += 1
        del coc[groupId][memberId][i]
    dataManage.save_obj(coc, 'coc')
    return '成功删除' + str(index) + '个属性'

def stClear(groupId):
    coc = dataManage.load_obj('coc')
    if coc.__contains__(groupId):
        del coc[groupId]
    dataManage.save_obj(coc, 'coc')
    return '清空成功！'

def show(groupId, memberId):
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        return '暂无属性'
    if not coc[groupId].__contains__(memberId):
        return '暂无属性'
    if len(coc[groupId][memberId]) == 0:
        return '暂无属性'
    
    result = '你的20及以上的属性如下：'
    for key, value in coc[groupId][memberId].items():
        if value >= 20:
            result += '\n' + key + '：' + str(value)
    return result

def showSingle(name, groupId, memberId):
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        return '你没有属性' + name
    if not coc[groupId].__contains__(memberId):
        return '你没有属性' + name
    if not coc[groupId][memberId].__contains__(name):
        return '你没有属性' + name
    return '属性：' + name + '值：' + str(coc[groupId][memberId][name])

def showAll(groupId, memberId):
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        return '暂无属性'
    if not coc[groupId].__contains__(memberId):
        return '暂无属性'
    if len(coc[groupId][memberId]) == 0:
        return '暂无属性'
    
    result = '你的属性如下：'
    for key, value in coc[groupId][memberId].items():
        result += '\n' + key + '：' + str(value)
    return result

# 鉴定属性
def ra(attribute, groupId, memberId):
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        return '不存在该属性'
    if not coc[groupId].__contains__(memberId):
        return '不存在该属性'
    if attribute[len(attribute) - 1].isdigit():
        index = len(attribute) - 2
        while index >= 0:
            if not attribute[index].isdigit():
                break
            index -= 1
        name = ''
        if index == -1:
            name = '[未知属性]'
        else:
            name = attribute[:index + 1]
        number = int(attribute[index + 1:])
        if number > 100:
            number = 100
        elif number < 0:
            number = 0
        dicks = random.randint(1, 100)
        if dicks < number:
            return '点数：' + str(dicks) + '\n' + name + ':' + str(number) + '\n鉴定成功！'
        else:
            return '点数：' + str(dicks) + '\n' + name + ':' + str(number) + '\n鉴定失败！'

    if not coc[groupId][memberId].__contains__(attribute):
        return '不存在该属性'
    dicks = random.randint(1, 100)
    if dicks <= coc[groupId][memberId][attribute]:
        return '点数：' + str(dicks) + '\n' + attribute + ':' + str(coc[groupId][memberId][attribute]) + '\n鉴定成功！'
    else:
        return '点数：' + str(dicks) + '\n' + attribute + ':' + str(coc[groupId][memberId][attribute]) + '\n鉴定失败！'


def export(groupId, memberId):
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        return '*st '
    if not coc[groupId].__contains__(memberId):
        return '*st '
    if len(coc[groupId][memberId]) == 0:
        return '*st '

    result = '*st '
    for key, value in coc[groupId][memberId].items():
        result +=  key + str(value)
    return result

def addRole(attribute, groupId, roleName):
    coc = dataManage.load_obj('cocRole')
    if roleName.isdigit():
        return '人物模板名不能全为数字！'
    if coc.__contains__(roleName):
        del coc[roleName]
    coc[roleName] = {}

    name = ''
    number = 0
    lenghth = len(attribute)
    i = 0
    while i < lenghth:
        if attribute[i].isdigit():
            while attribute[i].isdigit():
                number = number * 10 + int(attribute[i])
                i += 1
                if i >= lenghth:
                    break
            if number > 100:
                number = 100
            name = name.strip()
            if len(name) > 0:
                coc[roleName][name] = number
            name = ''
            number = 0

        if i >= lenghth:
            break
        name += attribute[i]
        i += 1

    dataManage.save_obj(coc, 'cocRole')
    return '人物' + roleName + '已修改'

def removeRole(groupId, roleName):
    coc = dataManage.load_obj('cocRole')
    if coc.__contains__(roleName):
        del coc[roleName]
        dataManage.save_obj(coc, 'cocRole')
        return '人物' + roleName + '已删除'
    else:
        return '人物' + roleName + '不存在'

def showRole(groupId, roleName):
    coc = dataManage.load_obj('cocRole')
    if not coc.__contains__(roleName):
        return '人物' + roleName + '不存在'
    result = '人物' + roleName + '的属性如下：'
    for key, value in coc[roleName].items():
        result += '\n' + key + '：' + str(value)
    return result

def showRoleList(groupId):
    coc = dataManage.load_obj('cocRole')
    if len(coc) == 0:
        return '暂无人物'

    result = '人物列表如下：'
    for key, value in coc.items():
        result += '\n' + key
    return result

def copyRole(roleName, groupId, memberId):
    cocRole = dataManage.load_obj('cocRole')
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        coc[groupId] = {}
    if not coc[groupId].__contains__(memberId):
        coc[groupId][memberId] = {}
    if not cocRole.__contains__(roleName):
        return '不存在该人物'

    coc[groupId][memberId] = cocRole[roleName]
    dataManage.save_obj(coc, 'coc')
    return '已将人物模板' + roleName + '的属性复制给你~'
