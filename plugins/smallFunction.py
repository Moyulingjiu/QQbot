
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

def rd(num, size):
    if num > 20:
        return '诶诶诶！投那么骰子，我会晕掉的'
    if size > 1000:
        return '啊？那么多面，这个骰子做不出来诶'
    if num < 1 or size < 2:
        return '啊嘞？'
    
    if num == 1:
        return '扔出的点数为：' + str(random.randint(1, size))

    result = ''
    sum = 0
    for i in range(0, num):
        dicks = random.randint(1, size)
        sum += dicks
        result += '骰子' + str(i + 1) + '：' + str(dicks) + '\n'
    return result + '合计点数为：' + str(sum)

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
    attributeList = attribute.split(' ')
    for i in attributeList:
        i = i.strip()
        if len(i) > 0:
            a = ''
            number = 0
            for j in range(0, len(i)):
                if i[j].isdigit():
                    if i[j:].isdigit():
                        a = i[:j]
                        number = int(i[j:])
                    break
            if len(a) > 0:
                coc[groupId][memberId][a] = number
            
    dataManage.save_obj(coc, 'coc')
    return '追加成功！目前有属性个数：' + str(len(coc[groupId][memberId]))

def stc(attribute, groupId, memberId):
    coc = dataManage.load_obj('coc')
    if not coc.__contains__(groupId):
        return '不存在该属性'
    if not coc[groupId].__contains__(memberId):
        return '不存在该属性'
        
    attributeList = attribute.split(' ')
    index = 0
    for i in attributeList:
        i = i.strip()
        if len(i) > 0:
            a = ''
            number = 0
            for j in range(0, len(i)):
                if i[j].isdigit():
                    if i[j:].isdigit():
                        a = i[:j]
                        number = int(i[j:])
                    break
            if len(a) > 0:
                if coc[groupId][memberId].__contains__(a):
                    coc[groupId][memberId][a] = number
                    index += 1
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
    
    result = '你的超过20的属性如下：'
    for key, value in coc[groupId][memberId].items():
        if value >= 20:
            result += '\n' + key + '：' + str(value)
    return result

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
    if not coc[groupId][memberId].__contains__(attribute):
        return '不存在该属性'
    dicks = random.randint(1, 100)
    if dicks <= coc[groupId][memberId][attribute]:
        return '点数：' + str(dicks) + '\n鉴定成功！'
    else:
        return '点数：' + str(dicks) + '\n鉴定失败！'
    