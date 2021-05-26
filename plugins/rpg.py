# 一个rpg游戏，附带在小柒上
import asyncio # 异步
from graia.application.entry import (
    GraiaMiraiApplication, Session,
    MessageChain, Group, Friend, Member, MemberInfo,
    Plain, Image, AtAll, At, Face, Source
)
from graia.application.entry import (
    BotMuteEvent, BotGroupPermissionChangeEvent
)
from graia.broadcast import Broadcast


import random
import datetime
import linecache

from plugins import dataManage

maxStrength = 120 # 最大体力
signStrength = 20 # 签到体力
user = {} # 用户数据
systemData = {}
init = True

goods = {
    '破旧的木剑': {
        'attack': 1
    },
    '破旧的布甲': {
        'defense': 1
    }
}

async def menu(strMessage, groupId, member, app, botBaseInformation, messageChain):
    global user
    global systemData
    Bot_QQ = botBaseInformation['baseInformation']['Bot_QQ']
    Bot_Name = botBaseInformation['baseInformation']['Bot_Name']

    needReply = False
    needAt = False
    reply = ''
    isImage = ''

    memberName = ''
    if groupId != 0:
        memberName = member.name
    else:
        memberName = member.nickname

    newUser(member.id, memberName)

    if strMessage.strip() == '签到':
        id = member.id
        reply = memberName + sign(id)
        needReply = True
    elif '击剑' in strMessage and groupId != 0:
        tmp = strMessage.replace('击剑', '').strip()
        if tmp[0] == '@' and tmp[1:].isdigit():
            target = int(tmp[1:])
            if target != Bot_QQ:
                await fencing(member, target, app)
            else:
                replylist = [
                    '一把把你按在了地上',
                    '敲了敲你的脑袋', 
                    '摸了摸你的头说：“乖，一边去~”',
                    '白了你一眼',
                    '并不想理你',
                    '对你感到了无语'
                ]
                reply = Bot_Name + random.choice(replylist)
        needReply = True
    elif strMessage == '我的积分' or strMessage == '积分':
        id = member.id
        reply = memberName + getGold(id)
        needReply = True
    elif strMessage == '我的体力' or strMessage == '体力':
        id = member.id
        reply = memberName + getStrength(id)
        needReply = True
    elif strMessage == '我的胜率' or strMessage == '胜率':
        id = member.id
        reply = memberName + getRate(id)
        needReply = True
    elif strMessage == '排行榜':
        reply = getRank()
        needReply = True
    elif strMessage == '兑换体力':
        reply = memberName + rechargeStrength(member.id)
        needReply = True
    elif strMessage == '模拟抽卡' or strMessage == '模拟单抽':
        reply = MRFZ_card()
        needReply = True
    elif strMessage == '模拟十连':
        reply = MRFZ_card10()
        needReply = True
    elif strMessage == '围攻榜首' and groupId != 0:
        await fencingTop(member, app)
        needReply = True
    elif strMessage == '探险':
        reply = fishing(member.id, memberName)
        needReply = True
    elif strMessage == '闲逛':
        reply = memberName + hangOut(member.id)
        needReply = True
    elif '摸摸' in strMessage and groupId != 0:
        tmp = strMessage.replace('摸摸', '').strip()
        if tmp[0] == '@' and tmp[1:].isdigit():
            target = int(tmp[1:])
            print(target)
            print(Bot_QQ)
            print(str(target) == str(Bot_QQ))
            if str(target) == str(Bot_QQ):
                reply = Bot_Name + touch(member.id, memberName)
                print(reply)
        needReply = True
    elif strMessage == '强化进攻' or strMessage == '强化攻击' or strMessage == '强化攻击力':
        reply = memberName + strengthenAttack(member.id)
        needReply = True
    elif strMessage == '强化防守' or strMessage == '强化防御' or strMessage == '强化防御力':
        reply = memberName + strengthenDefense(member.id)
        needReply = True
    elif strMessage == '数据' or strMessage == '我的数据':
        reply = getMyData(member.id)
        needReply = True
    elif strMessage == '背包' or strMessage == '我的背包':
        reply = memberName + getWarehouse(member.id)
        needReply = True
    elif strMessage == '装备' or strMessage == '我的装备':
        reply = memberName + getEquipment(member.id)
        needReply = True
    elif strMessage == 'BUFF' or strMessage == 'buff' or strMessage == 'Buff' or strMessage == '我的BUFF' or strMessage == '我的buff' or strMessage == '我的Buff':
        reply = memberName + getBuff(member.id)
        needReply = True
    elif strMessage[:2] == '装备' or strMessage[:2] == '使用':
        pass
        needReply = True
    elif strMessage[:2] == '取下':
        pass
        needReply = True
    elif strMessage == '商店':
        reply = getShop()
        needReply = True
    elif strMessage[:2] == '购买':
        pass
        needReply = True
    elif strMessage[:2] == '出售':
        pass
        needReply = True
    elif strMessage[:2] == '丢弃' or strMessage[:2] == '丢掉':
        pass
        needReply = True
    elif '决斗' in strMessage and groupId != 0:
        tmp = strMessage.replace('决斗', '').strip()
        if tmp[0] == '@' and tmp[1:].isdigit():
            target = int(tmp[1:])
            if target != Bot_QQ:
                await fencing(member, target, app) # 挑战
            else:
                replylist = [
                    '一把把你按在了地上',
                    '敲了敲你的脑袋', 
                    '摸了摸你的头说：“乖，一边去~”',
                    '白了你一眼',
                    '并不想理你',
                    '对你感到了无语'
                ]
                reply = Bot_Name + random.choice(replylist)
        needReply = True
    elif strMessage[:4] == '修改昵称' or strMessage[:4] == '修改名字' or strMessage[:4] == '修改姓名':
        tmpName = strMessage[4:].strip()
        reply = changeName(member.id, tmpName)
        needReply = True

    if member.id ==  botBaseInformation['baseInformation']['Master_QQ']:
        if strMessage == '重新加载游戏数据':
            user = dataManage.load_obj('user/information')
            reply = '重新加载完成'
            needReply = True
        elif strMessage[:5] == '修改体力 ':
            strList = strMessage.split(' ')
            
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = editStrength(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = editStrength(int(strList[1]), int(strList[2]))
                    needReply = True
        elif strMessage[:5] == '修改积分 ':
            strList = strMessage.split(' ')

            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = editGold(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = editGold(int(strList[1]), int(strList[2]))
                    needReply = True
        elif strMessage[:5] == '查看数据 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = viewUser(int(strList[1]))
                    needReply = True
        elif strMessage[:5] == '查看胜率 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = viewRate(int(strList[1]))
                    needReply = True
        elif strMessage[:5] == '查看背包 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = viewWarehouse(int(strList[1]))
                    needReply = True
        elif strMessage[:5] == '查看装备 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = viewEquipment(int(strList[1]))
                    needReply = True
        elif strMessage[:7] == '查看BUFF ' or strMessage[:7] == '查看buff ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = viewBuff(int(strList[1]))
                    needReply = True        

        elif strMessage == '开启无敌':
            reply = changeToGod(member.id)
            needReply = True
        elif strMessage[:5] == '开启无敌 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToGod(int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToTmpGod(int(strList[1]), int(strList[2]))
                    needReply = True
        elif strMessage[:7] == '开启临时无敌 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToTmpGod(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToTmpGod(int(strList[1]), int(strList[2]))
                    needReply = True
        elif strMessage == '关闭无敌':
            reply = closeGod(member.id)
            needReply = True
        elif strMessage[:5] == '关闭无敌 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = closeGod(int(strList[1]))
                    needReply = True
            needReply = True
        elif strMessage == '查看无敌的人':
            reply = viewGod()
            needReply = True


        elif strMessage[:7] == '开启1级防御 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToDefense1(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToDefense1(int(strList[1]), int(strList[2]))
                    needReply = True 
        elif strMessage[:7] == '开启2级防御 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToDefense2(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToDefense2(int(strList[1]), int(strList[2]))
                    needReply = True  
        elif strMessage[:7] == '开启3级防御 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToDefense3(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToDefense3(int(strList[1]), int(strList[2]))
                    needReply = True
        elif strMessage[:7] == '开启1级进攻 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToRampage1(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToRampage1(int(strList[1]), int(strList[2]))
                    needReply = True 
        elif strMessage[:7] == '开启2级进攻 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToRampage2(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToRampage2(int(strList[1]), int(strList[2]))
                    needReply = True  
        elif strMessage[:7] == '开启3级进攻 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToRampage3(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToRampage3(int(strList[1]), int(strList[2]))
                    needReply = True
        elif strMessage[:9] == '开启积分收益减半 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToHalveGold(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToHalveGold(int(strList[1]), int(strList[2]))
                    needReply = True
        elif strMessage[:9] == '开启击剑不掉积分 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToNoLoss(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToNoLoss(int(strList[1]), int(strList[2]))
                    needReply = True
        elif strMessage[:9] == '开启双倍积分收益 ' or strMessage[:9] == '开启两倍积分收益 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToDoubleGold(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToDoubleGold(int(strList[1]), int(strList[2]))
                    needReply = True
        elif strMessage[:9] == '开启三倍积分收益 ':
            strList = strMessage.split(' ')
            if len(strList) == 2:
                if strList[1].isdigit():
                    reply = changeToTripleGold(member.id, int(strList[1]))
                    needReply = True
            elif len(strList) == 3:
                if strList[1].isdigit() and strList[2].isdigit():
                    reply = changeToTripleGold(int(strList[1]), int(strList[2]))
                    needReply = True
        elif strMessage[:11] == '开启固定增减积分收益 ':
            strList = strMessage.split(' ')
            if len(strList) == 3:
                if strList[1].isdigit():
                    if strList[2].isdigit():
                        reply = changeToFixedGold(member.id, int(strList[1]), int(strList[2]))
                        needReply = True
                    elif strList[2][:1] == '-' and strList[2][1:].isdigit():
                        reply = changeToFixedGold(member.id, int(strList[1]), -int(strList[2][1:]))
                        needReply = True
            elif len(strList) == 4:
                if strList[1].isdigit() and strList[2].isdigit():
                    if strList[3].isdigit():
                        reply = changeToFixedGold(int(strList[1]), int(strList[2]), int(strList[3]))
                        needReply = True
                    elif strList[3][:1] == '-' and strList[3][1:].isdigit():
                        reply = changeToFixedGold(int(strList[1]), int(strList[2]), -int(strList[3][1:]))
                        needReply = True

    if needReply:
        dataManage.save_obj(user, 'user/information')
        dataManage.save_obj(systemData, 'user/system')
    return (needReply, needAt, reply, isImage)

# ============================================
# 基础操作

def update(id, mode, gold, strength): # mode值表示了该击剑由什么模式产生的（-1：管理员权限、0：击剑、1：探险、2：闲逛）
    global user
    global systemData
    if user.__contains__(id):
        if gold > 0: # 增益buff
            if systemData['halveGold'].__contains__(id): # 积分收益减半
                systemData['halveGold'][id]['number'] -= 1
                if systemData['halveGold'][id]['number'] <= 0:
                    del systemData['halveGold'][id]
                gold *= 0.5
                gold = int(gold)
            elif systemData['doubleGold'].__contains__(id): # 双倍积分收益
                systemData['doubleGold'][id]['number'] -= 1
                if systemData['doubleGold'][id]['number'] <= 0:
                    del systemData['doubleGold'][id]
                gold *= 2
            elif systemData['tripleGold'].__contains__(id): # 三倍积分收益
                systemData['tripleGold'][id]['number'] -= 1
                if systemData['tripleGold'][id]['number'] <= 0:
                    del systemData['tripleGold'][id]
                gold *= 3
            elif systemData['fixedGold'].__contains__(id): # 固定增减积分收益
                systemData['fixedGold'][id]['number'] -= 1
                gold += systemData['fixedGold'][id]['gold']
                if gold < 0: # 收益不能减少为负数
                    gold = 0
                if systemData['fixedGold'][id]['number'] <= 0:
                    del systemData['fixedGold'][id]
        elif gold < 0: # 负收益buff
            if systemData['noLoss'].__contains__(id): # 击剑不掉积分
                if mode == 0:
                    systemData['noLoss'][id]['number'] -= 1
                    if systemData['noLoss'][id]['number'] <= 0:
                        del systemData['noLoss'][id]
                    gold = 0
        
        user[id]['attribute']['strength'] += strength
        if user[id]['attribute']['strength'] < 0:
            user[id]['attribute']['strength'] = 0
        if mode != -1:
            user[id]['gold'] += gold
        else:
            user[id]['gold'] = gold

        # ===============================
        # 排行榜更新
        times = user[id]['match']['win'] + user[id]['match']['lose']
        rate = float(user[id]['match']['win']) / float(user[id]['match']['win'] + user[id]['match']['lose']) if (user[id]['match']['win'] + user[id]['match']['lose'] > 0) else 0.0
        
        if times > systemData['rank']['field']['number']: # 场次第一
            systemData['rank']['field']['number'] = times
            systemData['rank']['field']['id'] = id
        if rate > systemData['rank']['rate']['rate']: # 胜率第一
            systemData['rank']['rate']['rate'] = rate
            systemData['rank']['rate']['id'] = id
        if times > 50:
            if rate > systemData['rank']['rate50']['rate']: # 胜率第一（大于50场）
                systemData['rank']['rate50']['rate'] = rate
                systemData['rank']['rate50']['id'] = id
        if user[id]['match']['lostTopTimes'] > systemData['rank']['loser']['number']: # 被击剑的次数
            systemData['rank']['loser']['number'] = user[id]['match']['lostTopTimes']
            systemData['rank']['loser']['id'] = id


        if gold > 0: # 增加收入
            if user[id]['gold'] > systemData['rank']['gold-1']['gold']: # 登顶
                if id == systemData['rank']['gold-1']['id']: # 本来就是榜首，那么就更新数据
                    systemData['rank']['gold-1']['gold'] = user[id]['gold']
                else:
                    user[id]['match']['topTimes'] += 1 # 登顶次数+1
                    if user[id]['match']['topTimes'] > systemData['rank']['challenger']['number']:
                        systemData['rank']['challenger']['number'] = user[id]['match']['topTimes']
                        systemData['rank']['challenger']['id'] = id

                    if id == systemData['rank']['gold-2']['id']:
                        systemData['rank']['gold-2']['gold'] = systemData['rank']['gold-1']['gold']
                        systemData['rank']['gold-2']['id'] = systemData['rank']['gold-1']['id']
                        
                        systemData['rank']['gold-1']['gold'] = user[id]['gold']
                        systemData['rank']['gold-1']['id'] = id
                    else:
                        systemData['rank']['gold-3']['gold'] = systemData['rank']['gold-2']['gold']
                        systemData['rank']['gold-3']['id'] = systemData['rank']['gold-2']['id']
                        
                        systemData['rank']['gold-2']['gold'] = systemData['rank']['gold-1']['gold']
                        systemData['rank']['gold-2']['id'] = systemData['rank']['gold-1']['id']
                        
                        systemData['rank']['gold-1']['gold'] = user[id]['gold']
                        systemData['rank']['gold-1']['id'] = id
            elif user[id]['gold'] > systemData['rank']['gold-2']['gold'] and id != systemData['rank']['gold-1']['id']: # 大于第二，并且不是榜首
                if id == systemData['rank']['gold-2']['id']: # 本来就是第二，那么就更新数据
                    systemData['rank']['gold-2']['gold'] = user[id]['gold']
                else:
                    systemData['rank']['gold-3']['gold'] = systemData['rank']['gold-2']['gold']
                    systemData['rank']['gold-3']['id'] = systemData['rank']['gold-2']['id']
                    
                    systemData['rank']['gold-2']['gold'] = user[id]['gold']
                    systemData['rank']['gold-2']['id'] = id
            elif user[id]['gold'] > systemData['rank']['gold-3']['gold'] and id != systemData['rank']['gold-1']['id'] and id != systemData['rank']['gold-2']['id']: # 大于第三，并且不是榜首和第二
                systemData['rank']['gold-3']['gold'] = user[id]['gold']
                systemData['rank']['gold-3']['id'] = id # 这里就算它本来是第三仍旧没有影响
                
        elif gold < 0: # 收入减少
            if id == systemData['rank']['gold-1']['id'] or id == systemData['rank']['gold-2']['id'] or id == systemData['rank']['gold-3']['id']: # 榜上有名（如果榜上无名，那么他的积分减少对排行榜就没有任何影响）
                goldId = 0
                goldId2 = 0
                goldId3 = 0
                for key, value in user.items():
                    if goldId == 0:
                        goldId = key
                    else:
                        if value['gold'] > user[goldId]['gold']:
                            goldId3 = goldId2
                            goldId2 = goldId
                            goldId = key
                        elif goldId2 == 0 or value['gold'] > user[goldId2]['gold']:
                            goldId3 = goldId2
                            goldId2 = key 
                        elif goldId3 == 0 or value['gold'] > user[goldId3]['gold']:
                            goldId3 = key
                if goldId != systemData['rank']['gold-1']['id']:
                    user[goldId]['match']['topTimes'] += 1 # 登顶次数+1
                    if user[goldId]['match']['topTimes'] > systemData['rank']['challenger']['number']:
                        systemData['rank']['challenger']['number'] = user[goldId]['match']['topTimes']
                        systemData['rank']['challenger']['id'] = goldId

                systemData['rank']['gold-1']['id'] = goldId
                systemData['rank']['gold-1']['gold'] = user[goldId]['gold']
                
                systemData['rank']['gold-2']['id'] = goldId2
                systemData['rank']['gold-2']['gold'] = user[goldId2]['gold'] if goldId2 != 0 else 0
                
                systemData['rank']['gold-3']['id'] = goldId3
                systemData['rank']['gold-3']['gold'] = user[goldId3]['gold'] if goldId3 != 0 else 0



# ============================================
# 操作

def sign(id):
    global user
    today = str(datetime.date.today())

    if today != user[id]['sign-date']:
        user[id]['sign-date'] = today
        user[id]['gold'] += random.randint(5, 10)
        return '签到成功！当前积分：' + str(user[id]['gold'])
    else:
        return '你今天已经签到过了哦~'

def getGold(id):
    global user
    
    return '你的积分为：' + str(user[id]['gold'])
  
def getStrength(id):
    global user
    global maxStrength
    return '你的体力为：' + str(user[id]['attribute']['strength']) + '/' + str(maxStrength)

def getRate(id):
    global user
    if user[id]['match']['win'] + user[id]['match']['lose'] == 0:
        return  '你还暂未进行任何对决'
    rate = float(user[id]['match']['win']) / float(user[id]['match']['win'] + user[id]['match']['lose'])
    rate = round(rate, 2) * 100
    result = '\n总计场次：' + str(user[id]['match']['win'] + user[id]['match']['lose'])
    result += '\n获胜次数：' + str(user[id]['match']['win'])
    result += '\n你的胜率为：' + str(int(rate)) + '%'
    result += '\n登顶次数：' + str(user[id]['match']['topTimes'])
    return result

def getMyData(id):
    global user
    result = '昵称：' + user[id]['name']
    if not user[id]['initName']:
        result += '（自动获取）'
    result += '\n'
    result += '积分：' + str(user[id]['gold']) + '\n'
    result += '攻击力：' + str(user[id]['attribute']['attack']) + '\n'
    result += '护甲：' + str(user[id]['attribute']['defense']) + '\n'
    result += 'San值：' + str(user[id]['attribute']['san']) + '\n'
    result += '体力：' + str(user[id]['attribute']['strength']) + '/' + str(maxStrength) + '\n'
    result += '总计场次：' + str(user[id]['match']['win'] + user[id]['match']['lose'])
    if user[id]['match']['win'] + user[id]['match']['lose'] != 0:
        rate = float(user[id]['match']['win']) / float(user[id]['match']['win'] + user[id]['match']['lose'])
        rate = round(rate, 2) * 100
        result += '（' + str(int(rate)) + '%）\n'
    result += '背包物品数：' + str(len(user[id]['warehouse']))
    return result
    
def getWarehouse(id):
    global user
    result = '你的背包：'
    if len(user[id]['warehouse']) == 0:
        result += '无'
    else:
        for i in user[id]['warehouse']:
            result += '\n'
            result += i['name']
            if i['number'] > 1:
                result += 'X' + str(i['number'])
    return result

def getEquipment(id):
    global user
    result = '你的装备：\n'
    result += '武器：' + (user[id]['equipment']['arms'] if len(user[id]['equipment']['arms']) > 0 else '（暂无）') + '\n'
    result += '头盔：' + (user[id]['equipment']['hat'] if len(user[id]['equipment']['hat']) > 0 else '（暂无）') + '\n'
    result += '胸甲：' + (user[id]['equipment']['jacket'] if len(user[id]['equipment']['jacket']) > 0 else '（暂无）') + '\n'
    result += '护腿：' + (user[id]['equipment']['trousers'] if len(user[id]['equipment']['trousers']) > 0 else '（暂无）') + '\n'
    result += '鞋子：' + (user[id]['equipment']['shoes'] if len(user[id]['equipment']['shoes']) > 0 else '（暂无）') + '\n'
    result += '戒指（左）：' + (user[id]['equipment']['ring-left'] if len(user[id]['equipment']['ring-left']) > 0 else '（暂无）') + '\n'
    result += '戒指（右）：' + (user[id]['equipment']['ring-right'] if len(user[id]['equipment']['ring-right']) > 0 else '（暂无）') + '\n'
    result += '背包：' + (user[id]['equipment']['knapsack'] if len(user[id]['equipment']['knapsack']) > 0 else '（暂无）')
    return result

def getBuff(id):
    global systemData

    result = '你的BUFF如下：'
    if id in systemData['god']: # 用户是无敌模式
        result += '\n永久无敌模式'
    if systemData['tmpGod'].__contains__(id): # 用户是无敌模式
        result += '\n临时无敌模式：' + str(systemData['tmpGod'][id]['number']) + '次'

    if systemData['defense-3'].__contains__(id): # 3级防御
        result += '\n3级防御：' + str(systemData['defense-3'][id]['number']) + '次'
    if systemData['defense-2'].__contains__(id): # 2级防御
        result += '\n2级防御：' + str(systemData['defense-2'][id]['number']) + '次'
    if systemData['defense-1'].__contains__(id): # 1级防御
        result += '\n1级防御：' + str(systemData['defense-1'][id]['number']) + '次'

    if systemData['rampage-3'].__contains__(id): # 3级暴走
        result += '\n3级进攻：' + str(systemData['rampage-3'][id]['number']) + '次'
    if systemData['rampage-2'].__contains__(id): # 2级暴走
        result += '\n2级进攻：' + str(systemData['rampage-2'][id]['number']) + '次'
    if systemData['rampage-1'].__contains__(id): # 1级暴走
        result += '\n1级进攻：' + str(systemData['rampage-1'][id]['number']) + '次'
    
    if systemData['halveGold'].__contains__(id): # 积分收益减半
        result += '\n积分收益减半：' + str(systemData['halveGold'][id]['number']) + '次'
    elif systemData['doubleGold'].__contains__(id): # 双倍积分收益
        result += '\n积分收益双倍：' + str(systemData['doubleGold'][id]['number']) + '次'
    elif systemData['tripleGold'].__contains__(id): # 三倍积分收益
        result += '\n积分收益三倍：' + str(systemData['tripleGold'][id]['number']) + '次'
    elif systemData['fixedGold'].__contains__(id): # 固定增减积分收益
        if systemData['fixedGold'][id]['gold'] > 0:
            result += '\n收益增减固定积分：' + str(systemData['fixedGold'][id]['number']) + '次（积分+' + str(systemData['fixedGold'][id]['gold']) + '）'
        else:
            result += '\n收益增减固定积分：' + str(systemData['fixedGold'][id]['number']) + '次（积分' + str(systemData['fixedGold'][id]['gold']) + '）'
    elif systemData['noLoss'].__contains__(id): # 击剑不掉积分
        result += '\n击剑免掉积分：' + str(systemData['noLoss'][id]['number']) + '次'
    
    if result == '你的BUFF如下：':
        result = '你的BUFF如下：暂无'
    return result

def getShop():
    return '商店暂未开放~'

    result = '商品目录如下：'
    result += '\n破旧的木剑：10'
    result += '\n破旧的布甲：20'
    return result

def changeName(id, name):
    global user
    flag = True
    for key, value in user.items():
        if value['name'] == name:
            return '这个名字已经被其他人占用了哦！'

    user[id]['name'] = name
    user[id]['initName'] = True
    return name + '修改成功~'

def newUser(id, name):
    global user
    global init 
    global systemData
    global maxStrength # 最大体力
    global signStrength # 签到体力
    if init:
        user = dataManage.load_obj('user/information')
        systemData = dataManage.load_obj('user/system')
        init = False
    today = str(datetime.date.today())
    
    if not user.__contains__(id):
        user[id] = {
            'name': name,
            'initName': False,
            'gold': 0,
            'sign-date': '',
            'warehouse': [], # 背包
            'match': { # 比赛场次
                'win': 0,
                'lose': 0,
                'monster': 0,
                'legend': 0,
                'topTimes': 0,
                'lostTopTimes': 0
            },
            'equipment': { # 装备
                'arms': '', # 武器
                'hat': '', # 头部
                'jacket': '', # 身体
                'trousers': '', # 裤子
                'shoes': '', # 鞋子
                'ring-left': '', # 左戒指
                'ring-right': '', # 右戒指
                'knapsack': '' # 背包
            },
            'attribute': {
                'attack': 5, # 攻击力
                'hp': 100, # 生命值
                'defense': 0, # 防御值
                'san': 100, # 精神力
                'strength': 20 # 体力
            },
            'last-operate-date': today
        }
    else:
        if user[id]['last-operate-date'] != today:
            # 体力值修改
            if user[id]['attribute']['strength'] < maxStrength - signStrength:
                user[id]['attribute']['strength'] += signStrength
            elif user[id]['attribute']['strength'] < maxStrength:
                user[id]['attribute']['strength'] = maxStrength
            # san值
            user[id]['attribute']['san'] += 100
            if user[id]['attribute']['san'] > 100:
                user[id]['attribute']['san'] = 100
            user[id]['last-operate-date'] = today
            if not user[id]['initName']:
                user[id]['name'] = name

def rechargeStrength(id):
    global user
    global maxStrength # 最大体力
    cost = 4
    gain = 5
    if user[id]['gold'] < cost:
        return '你的积分小于' + str(cost) + '不能兑换体力'
    
    if user[id]['attribute']['strength'] >= maxStrength:
        return '你的体力值已满不能兑换体力'
    elif user[id]['attribute']['strength'] >= maxStrength - gain:
        user[id]['gold'] -= cost
        user[id]['attribute']['strength'] = maxStrength
        return '你消耗了' + str(cost) + '积分，获得了' + str(gain) + '点体力'
    else:
        user[id]['gold'] -= cost
        user[id]['attribute']['strength'] += gain
        return '你消耗了' + str(cost) + '积分，获得了' + str(gain) + '点体力'

async def fencing(member, id2, app):
    if member.id == id2:
        await app.sendGroupMessage(member.group, MessageChain.create([
            Plain('好家伙，和自己击剑呢？')
        ]))
        return

    other = await app.getMember(member.group.id, id2)

    if other != None:
        newUser(other.id, other.name)
        global user
        global systemData

        # 体力值与积分判断
        if user[other.id]['gold'] <= 1:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain(other.name + '的积分值小于等于1，不能进行击剑')
            ]))
            return
        if user[member.id]['gold'] <= 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('你暂无积分值不可以击剑')
            ]))
            return
        if user[member.id]['attribute']['strength'] <= 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('你今日的体力值已经为0了，不能再击剑啦~')
            ]))
            return
        user[member.id]['attribute']['strength'] -= 1
        user[other.id]['attribute']['san'] -= 1
        user[other.id]['match']['lostTopTimes'] += 1


        ran = random.randrange(0, 1000)
        # 获胜概率为 你的攻击 - 对方防御力 + 你的san值 - 对方san值
        winPoint = 500 + ((user[member.id]['attribute']['attack'] - user[other.id]['attribute']['defense']) * 10 + user[member.id]['attribute']['san'] - user[other.id]['attribute']['san'])

        # BUFF启用
        if member.id in systemData['god']: # 用户是无敌模式
            winPoint = 1000
        elif other.id in systemData['god']: # 被击剑对象是无敌模式
            winPoint = 0
        elif systemData['tmpGod'].__contains__(member.id): # 用户是无敌模式
            winPoint = 1000
            systemData['tmpGod'][member.id]['number'] -= 1
            if systemData['tmpGod'][member.id]['number'] <= 0:
                del systemData['tmpGod'][member.id]
        elif systemData['tmpGod'].__contains__(other.id): # 被击剑对象是无敌模式
            winPoint = 0
            systemData['tmpGod'][other.id]['number'] -= 1
            if systemData['tmpGod'][other.id]['number'] <= 0:
                del systemData['tmpGod'][other.id]
        else:
            if systemData['defense-3'].__contains__(other.id): # 3级防御
                winPoint -= 300
                systemData['defense-3'][other.id]['number'] -= 1
                if systemData['defense-3'][other.id]['number'] <= 0:
                    del systemData['defense-3'][other.id]
            elif systemData['defense-2'].__contains__(other.id): # 2级防御
                winPoint -= 200
                systemData['defense-2'][other.id]['number'] -= 1
                if systemData['defense-2'][other.id]['number'] <= 0:
                    del systemData['defense-2'][other.id]
            elif systemData['defense-1'].__contains__(other.id): # 1级防御
                winPoint -= 100
                systemData['defense-1'][other.id]['number'] -= 1
                if systemData['defense-1'][other.id]['number'] <= 0:
                    del systemData['defense-1'][other.id]

            if systemData['rampage-3'].__contains__(member.id): # 3级暴走
                winPoint += 300
                systemData['rampage-3'][member.id]['number'] -= 1
                if systemData['rampage-3'][member.id]['number'] <= 0:
                    del systemData['rampage-3'][member.id]
            elif systemData['rampage-2'].__contains__(member.id): # 2级暴走
                winPoint += 200
                systemData['rampage-2'][member.id]['number'] -= 1
                if systemData['rampage-2'][member.id]['number'] <= 0:
                    del systemData['rampage-2'][member.id]
            elif systemData['rampage-1'].__contains__(member.id): # 1级暴走
                winPoint += 100
                systemData['rampage-1'][member.id]['number'] -= 1
                if systemData['rampage-1'][member.id]['number'] <= 0:
                    del systemData['rampage-1'][member.id]

        winner = ''
        loser = ''
        result = ''
        maxGetGold = 8
        if ran < winPoint:
            winner = member.name
            loser = other.name
            if user[other.id]['gold'] < maxGetGold:
                maxGetGold = user[other.id]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['match']['win'] += 1
            user[other.id]['match']['lose'] += 1
            result = member.name + '你击剑打败了'+ loser + '，夺走了对方' + str(getGold) + '点节操（积分值）'
            update(member.id, 0, getGold, 0)
            update(other.id, 0, -getGold, 0)
        else:
            winner = other.name
            loser = member.name
            if user[member.id]['gold'] < maxGetGold:
                maxGetGold = user[member.id]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['match']['lose'] += 1
            user[other.id]['match']['win'] += 1
            result = member.name + '你击剑输给了' + winner + '，被夺走了' + str(getGold) + '点节操（积分值）'
            update(member.id, 0, -getGold, 0)
            update(other.id, 0, getGold, 0)

        
        maxLine = int(linecache.getline(r'data/user/fencing.txt', 1))
        x = random.randrange(0, maxLine)
        lineNumber = linecache.getline(r'data/user/fencing.txt', x * 2 + 3)
        process = lineNumber.replace('*name1*', winner).replace('*name2*', loser)

        await app.sendGroupMessage(member.group, MessageChain.create([
            Plain(process),
            Plain('------------\n'),
            Plain(result)
        ]))

async def fencingTop(member, app):
    global user
    global systemData

    goldId = systemData['rank']['gold-1']['id']
    
    if goldId == member.id:
        await app.sendGroupMessage(member.group, MessageChain.create([
            Plain('自己也要围攻自己吗？')
        ]))
        return
    else:
        if user[goldId]['gold'] <= 1:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain(user[goldId]['name'] + '的积分值小于等于1，不能进行击剑')
            ]))
            return
        if user[member.id]['gold'] <= 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('你暂无积分值不可以击剑')
            ]))
            return
        if user[member.id]['attribute']['strength'] <= 0:
            await app.sendGroupMessage(member.group, MessageChain.create([
                Plain('你今日的体力值已经为0了，不能再击剑啦~')
            ]))
            return
        user[member.id]['attribute']['strength'] -= 1
        user[goldId]['attribute']['san'] -= 1
        user[goldId]['match']['lostTopTimes'] += 1
 
        ran = random.randrange(0, 1000)
        # 获胜概率为 你的攻击 - 对方防御力 + 你的san值 - 对方san值
        winPoint = 500 + ((user[member.id]['attribute']['attack'] - user[goldId]['attribute']['defense']) * 10 + user[member.id]['attribute']['san'] - user[goldId]['attribute']['san'])

        # BUFF启用
        if member.id in systemData['god']: # 用户是无敌模式
            winPoint = 1000
        elif goldId in systemData['god']: # 被击剑对象是无敌模式
            winPoint = 0
        elif systemData['tmpGod'].__contains__(member.id): # 用户是无敌模式
            winPoint = 1000
            systemData['tmpGod'][member.id]['number'] -= 1
            if systemData['tmpGod'][member.id]['number'] <= 0:
                del systemData['tmpGod'][member.id]
        elif systemData['tmpGod'].__contains__(goldId): # 被击剑对象是无敌模式
            winPoint = 0
            systemData['tmpGod'][goldId]['number'] -= 1
            if systemData['tmpGod'][goldId]['number'] <= 0:
                del systemData['tmpGod'][goldId]
        else:
            if systemData['defense-3'].__contains__(goldId): # 3级防御
                winPoint -= 300
                systemData['defense-3'][goldId]['number'] -= 1
                if systemData['defense-3'][goldId]['number'] <= 0:
                    del systemData['defense-3'][goldId]
            elif systemData['defense-2'].__contains__(goldId): # 2级防御
                winPoint -= 200
                systemData['defense-2'][goldId]['number'] -= 1
                if systemData['defense-2'][goldId]['number'] <= 0:
                    del systemData['defense-2'][goldId]
            elif systemData['defense-1'].__contains__(goldId): # 1级防御
                winPoint -= 100
                systemData['defense-1'][goldId]['number'] -= 1
                if systemData['defense-1'][goldId]['number'] <= 0:
                    del systemData['defense-1'][goldId]

            if systemData['rampage-3'].__contains__(member.id): # 3级暴走
                winPoint += 300
                systemData['rampage-3'][member.id]['number'] -= 1
                if systemData['rampage-3'][member.id]['number'] <= 0:
                    del systemData['rampage-3'][member.id]
            elif systemData['rampage-2'].__contains__(member.id): # 2级暴走
                winPoint += 200
                systemData['rampage-2'][member.id]['number'] -= 1
                if systemData['rampage-2'][member.id]['number'] <= 0:
                    del systemData['rampage-2'][member.id]
            elif systemData['rampage-1'].__contains__(member.id): # 1级暴走
                winPoint += 100
                systemData['rampage-1'][member.id]['number'] -= 1
                if systemData['rampage-1'][member.id]['number'] <= 0:
                    del systemData['rampage-1'][member.id]

        winner = ''
        loser = ''
        result = ''
        maxGetGold = 8
        if ran < winPoint:
            winner = member.name
            loser = user[goldId]['name']
            if user[goldId]['gold'] < maxGetGold:
                maxGetGold = user[goldId]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['match']['win'] += 1
            user[goldId]['match']['lose'] += 1
            result = member.name + '你击剑打败了'+ loser + '，夺走了对方' + str(getGold) + '点节操（积分值）'
            update(member.id, 0, getGold, 0)
            update(goldId, 0, -getGold, 0)
        else:
            winner = user[goldId]['name']
            loser = member.name
            if user[member.id]['gold'] < maxGetGold:
                maxGetGold = user[member.id]['gold']
            getGold = random.randrange(0, maxGetGold) + 1
            user[member.id]['match']['lose'] += 1
            user[goldId]['match']['win'] += 1
            result = member.name + '你击剑输给了' + winner + '，被夺走了' + str(getGold) + '点节操（积分值）'
            update(member.id, 0, -getGold, 0)
            update(goldId, 0, getGold, 0)
        
        maxLine = int(linecache.getline(r'data/user/fencing.txt', 1))
        x = random.randrange(0, maxLine)
        lineNumber = linecache.getline(r'data/user/fencing.txt', x * 2 + 3)
        process = lineNumber.replace('*name1*', winner).replace('*name2*', loser)

        await app.sendGroupMessage(member.group, MessageChain.create([
            Plain(process),
            Plain('------------\n'),
            Plain(result)
        ]))
        
def getRank():
    global user
    global systemData

    if len(user) == 0:
        return '暂无排行榜'

    result = '排行榜\n'
    result += '----------------\n'
    result += '积分第一：' + user[systemData['rank']['gold-1']['id']]['name'] + '（' + str(user[systemData['rank']['gold-1']['id']]['gold']) + '）\n'
    if systemData['rank']['gold-2']['id'] != 0:
        result += '积分第二：' + user[systemData['rank']['gold-2']['id']]['name'] + '（' + str(user[systemData['rank']['gold-2']['id']]['gold']) + '）\n'
    if systemData['rank']['gold-3']['id'] != 0:
        result += '积分第三：' + user[systemData['rank']['gold-3']['id']]['name'] + '（' + str(user[systemData['rank']['gold-3']['id']]['gold']) + '）\n'
    
    rate = round(systemData['rank']['rate']['rate'], 2) * 100
    result += '胜率第一：' + user[systemData['rank']['rate']['id']]['name'] + '（' + str(int(rate)) + '%）'
    rateValue = round(systemData['rank']['rate50']['rate'], 2) * 100
    if systemData['rank']['rate50']['id'] != 0:
        result += '\n胜率第一（大于50场）：' + user[systemData['rank']['rate50']['id']]['name'] + '（' + str(int(rateValue)) + '%）'

    if systemData['rank']['field']['id'] != 0:
        result += '\n击剑达人：' + user[systemData['rank']['field']['id']]['name'] + '（' + str(systemData['rank']['field']['number']) + '场）'
    if systemData['rank']['challenger']['id'] != 0:
        result += '\n登顶次数最多：' + user[systemData['rank']['challenger']['id']]['name'] + '（' + str(systemData['rank']['challenger']['number']) + '次）'
    if systemData['rank']['loser']['id'] != 0:
        result += '\n被击剑次数最多：' + user[systemData['rank']['loser']['id']]['name'] + '（' + str(systemData['rank']['loser']['number']) + '次）'

    return result

# ============================================
# 明日方舟抽卡模拟器

def MRFZ_card():
    botBaseInformation = dataManage.load_obj('baseInformation')
    if not botBaseInformation['reply'].__contains__('cards'):
        botBaseInformation['reply']['cards'] = 0
    botBaseInformation['reply']['cards'] += 1
    if botBaseInformation['reply']['cards'] > 5:
        return '你抽卡太快了，每分钟最多只能抽5次哦~'
    dataManage.save_obj(botBaseInformation, 'baseInformation')

    card1 = []
    card2 = []
    card3 = []
    card4 = []
    card5 = []
    card6 = []
    information = []
    with open('data/明日方舟/PersonaCard.txt', 'r+', encoding = 'utf-8') as f:
        information = f.readlines()
    for i in information:
        i = i.strip()
        if len(i) > 0:
            tmp = i.split(' ')
            if tmp[0] == '1':
                card1.append(tmp[1])
            elif tmp[0] == '2':
                card2.append(tmp[1])
            elif tmp[0] == '3':
                card3.append(tmp[1])
            elif tmp[0] == '4':
                card4.append(tmp[1])
            elif tmp[0] == '5':
                card5.append(tmp[1])
            elif tmp[0] == '6':
                card6.append(tmp[1])
    random.shuffle(card1)
    random.shuffle(card2)
    random.shuffle(card3)
    random.shuffle(card4)
    random.shuffle(card5)
    random.shuffle(card6)
    card = starProbability()
    result = ''

    if card == 3:
        result += star2string(card) + random.choice(card3) + '\n'
    elif card == 4:
        result += star2string(card) + random.choice(card4) + '\n'
    elif card == 5:
        result += star2string(card) + random.choice(card5) + '\n'
    elif card == 6:
        result += star2string(card) + random.choice(card6) + '\n'
    result += '-------------\n以上数据由夜煞提供，如有错误，请使用命令\"*send 错误内容\"告知'
    return result

def MRFZ_card10():
    botBaseInformation = dataManage.load_obj('baseInformation')
    if not botBaseInformation['reply'].__contains__('cards'):
        botBaseInformation['reply']['cards'] = 0
    botBaseInformation['reply']['cards'] += 1
    if botBaseInformation['reply']['cards'] > 5:
        return '你抽卡太快了，每分钟最多只能抽5次哦~'
    dataManage.save_obj(botBaseInformation, 'baseInformation')

    card1 = []
    card2 = []
    card3 = []
    card4 = []
    card5 = []
    card6 = []
    information = []
    with open('data/明日方舟/PersonaCard.txt', 'r+', encoding = 'utf-8') as f:
        information = f.readlines()
    for i in information:
        i = i.strip()
        if len(i) > 0:
            tmp = i.split(' ')
            if tmp[0] == '1':
                card1.append(tmp[1])
            elif tmp[0] == '2':
                card2.append(tmp[1])
            elif tmp[0] == '3':
                card3.append(tmp[1])
            elif tmp[0] == '4':
                card4.append(tmp[1])
            elif tmp[0] == '5':
                card5.append(tmp[1])
            elif tmp[0] == '6':
                card6.append(tmp[1])
    random.shuffle(card1)
    random.shuffle(card2)
    random.shuffle(card3)
    random.shuffle(card4)
    random.shuffle(card5)
    random.shuffle(card6)
    cards = []
    for i in range(10):
        cards.append(starProbability())
    result = ''
    for card in cards:
        if card == 3:
            result += star2string(card) + ' ' + random.choice(card3) + '\n'
        elif card == 4:
            result += star2string(card) + ' ' + random.choice(card4) + '\n'
        elif card == 5:
            result += star2string(card) + ' ' + random.choice(card5) + '\n'
        elif card == 6:
            result += star2string(card) + ' ' + random.choice(card6) + '\n'
    result += '-------------\n以上数据由夜煞提供，如有错误，请使用命令\"*send 错误内容\"告知'
    return result

def starProbability():
    ran = random.randrange(0, 100)
    if ran < 2:
        return 6
    elif ran < 10:
        return 5
    elif ran < 60:
        return 4
    else:
        return 3

def star2string(star):
    if star == 1:
        return '★☆☆☆☆☆'
    elif star == 2:
        return '★★☆☆☆☆'
    elif star == 3:
        return '★★★☆☆☆'
    elif star == 4:
        return '★★★★☆☆'
    elif star == 5:
        return '★★★★★☆'
    elif star == 6:
        return '★★★★★★'

# ============================================
def touch(id, name):
    global user
    if user[id]['attribute']['strength'] < 1 or user[id]['gold'] > 1:
        return '对' + name + '不屑一顾'
    user[id]['attribute']['strength'] -= 1
    user[id]['gold'] += random.randint(1, 5)
    return '看' + name + '太可怜，于是给了你一些积分'

'''
消耗体力：1

40% 啥也没有
15% BUFF
25% 1点体力 | 1点积分
15% 2点体力 | 2点积分
4.5% 3点积分
0.4% 4点积分
0.1% 10点体力 | 10点积分

E = 0.711
'''
def fishing(id, name):
    global user
    if user[id]['attribute']['strength'] < 1:
        return name + '体力值不足不能探险'
    user[id]['attribute']['strength'] -= 1
    ran = random.randrange(0, 1000)
    ran2 = random.randrange(0, 2)

    describe_dict = [
        '你来到了一个黑漆漆的山洞，四周十分安静，一番探索之后', 
        '你来到一个遗迹，一番探索之后', 
        '你发现了一个宝箱', 
        '在亚马逊的原始森林里，你被讨厌的虫子烦的要死', 
        '你在古玩市场一番搜索之后', 
        '你在一个古代陵墓里，一番探索之后', 
        '你来到了南极，冰天雪地之中，一番探索之后',
        '你在狂风骤雨的大海上航行，遇见了一个廖无人烟的小岛，一番探索之后',
        '你在沙哈拉沙漠中，孤独的一个人前行',
        '你在古埃及的金字塔里，一番探索之后',
        '你在亚特兰蒂斯的遗迹里，一番探索之后',
        '你好像梦见了你在做梦梦你在做梦，等你清醒之后脑袋晕乎乎的，但不知道为什么',
        '你在大荒漠上行走，遇见了黑风暴，因祸得福发现了一个宝箱',
        '你在高山之上探索无人之地',
        '你决定在后院探险，发现了祖辈留下来的宝箱',
        '你走在大路上发现了一个人手里拿着宝箱，于是你来骗、来偷袭，获得了这个宝箱',
        '你乘坐飞船抵达了月球，探索一番后',
        '你来到了九龙城，这里乌烟瘴气，一番探索之后'
    ]

    describe = random.choice(describe_dict)
    result = ''
    gold = 0
    strength = 0

    if ran < 400:
        result = '什么也没有获得'
    elif ran < 550:
        ran = random.randrange(0, 100)
        if ran < 40: # 进攻模式
            ran2 = random.randrange(0, 3)
            if ran2 == 0:
                tmp = random.randrange(0, 10) + 1
                changeToRampage1(id, tmp)
                result += '获得了一个' + str(tmp) + '次的1级进攻BUFF'
            elif ran2 == 1:
                tmp = random.randrange(0, 5) + 1
                changeToRampage2(id, tmp)
                result += '获得了一个' + str(tmp) + '次的2级进攻BUFF'
            elif ran2 == 2:
                tmp = random.randrange(0, 3) + 1
                changeToRampage3(id, tmp)
                result += '获得了一个' + str(tmp) + '次的3级进攻BUFF'
        elif ran < 80: # 防御模式
            ran2 = random.randrange(0, 3)
            if ran2 == 0:
                tmp = random.randrange(0, 10) + 1
                changeToDefense1(id, tmp)
                result += '获得了一个' + str(tmp) + '次的1级防御BUFF'
            elif ran2 == 1:
                tmp = random.randrange(0, 5) + 1
                changeToDefense2(id, tmp)
                result += '获得了一个' + str(tmp) + '次的2级防御BUFF'
            elif ran2 == 2:
                tmp = random.randrange(0, 3) + 1
                changeToDefense3(id, tmp)
                result += '获得了一个' + str(tmp) + '次的3级防御BUFF'
        elif ran < 88: # 减半积分收益
            tmp = random.randrange(0, 3) + 1
            changeToHalveGold(id, tmp)
            result += '获得了一个' + str(tmp) + '次的收益减半BUFF'
        elif ran < 96: # 双倍积分收益
            tmp = random.randrange(0, 3) + 1
            changeToDoubleGold(id, tmp)
            result += '获得了一个' + str(tmp) + '次的双倍积分收益BUFF'
        else: # 固定增减积分收益
            tmp = random.randrange(0, 3) + 1
            tmp2 = random.randrange(0, 11) - 5
            changeToFixedGold(id, tmp, tmp2)
            if tmp2 > 0:
                result += '获得了一个' + str(tmp) + '次的收益积分+' + str(tmp2) + 'BUFF'
            else:
                result += '获得了一个' + str(tmp) + '次的收益积分' + str(tmp2) + 'BUFF'

    elif ran < 800:
        if ran2 == 0:
            strength = 1
            result = '获得了1点体力'
        else:
            gold = 1
            result = '获得了1点积分值'
    elif ran < 950:
        if ran2 == 0:
            strength = 2
            result = '获得了2点体力'
        else:
            gold = 2
            result = '获得了2点积分值'
    elif ran < 995:
        gold = 3
        result = '获得了3点积分值'
    elif ran < 999:
        gold = 4
        result = '获得了4点积分值'
    else:
        if ran2 == 0:
            strength = 10
            result = '获得了10点体力'
        else:
            gold = 10
            result = '获得了10点积分值'

    update(id, 1, gold, strength) # 更新数据
    return name + describe + '，' + result

'''
20% 一无所获
15% BUFF
    2% 无敌模式
    40% 进攻模式
    40% 防御模式
    5% 双倍积分收益
    3% 三倍积分收益
    5% 固定增减积分收益
    5% 减半积分收益
5% 不好不坏
20% 一般好
20% 一般坏
8%  比较好
8%  比较坏
2%   超级好
2%   超级坏
'''

def hangOut(id):
    global user
    if user[id]['gold'] < 1:
        return '你的积分小于1，不能闲逛了'

    probability = random.randrange(0, 1000)
    result = ''
    gold = 0
    strength = 0

    if probability < 200: # 一无所获
        describe_dict = [
            '你闲逛了一圈，啥也没有发生',
            '你在闲逛的时候逛回去了，啥也没获得',
            '你在闲逛的时候踩了一坨便便并且坚信明天会走狗屎运'
        ]
        result = random.choice(describe_dict)

    elif probability < 350: #BUFF
        ran = random.randrange(0, 100)
        if ran < 40: # 进攻模式
            ran2 = random.randrange(0, 3)
            if ran2 == 0:
                tmp = random.randrange(0, 10) + 1
                changeToRampage1(id, tmp)
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的1级进攻BUFF'
            elif ran2 == 1:
                tmp = random.randrange(0, 5) + 1
                changeToRampage2(id, tmp)
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的2级进攻BUFF'
            elif ran2 == 2:
                tmp = random.randrange(0, 3) + 1
                changeToRampage3(id, tmp)
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的3级进攻BUFF'
        elif ran < 80: # 防御模式
            ran2 = random.randrange(0, 3)
            if ran2 == 0:
                tmp = random.randrange(0, 10) + 1
                changeToDefense1(id, tmp)
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的1级防御BUFF'
            elif ran2 == 1:
                tmp = random.randrange(0, 5) + 1
                changeToDefense2(id, tmp)
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的2级防御BUFF'
            elif ran2 == 2:
                tmp = random.randrange(0, 3) + 1
                changeToDefense3(id, tmp)
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的3级防御BUFF'
        elif ran < 85: # 减半积分收益
            tmp = random.randrange(0, 3) + 1
            changeToHalveGold(id, tmp)
            result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的收益减半BUFF'
        elif ran < 90: # 固定增减积分收益
            tmp = random.randrange(0, 3) + 1
            tmp2 = random.randrange(0, 11) - 5
            changeToFixedGold(id, tmp, tmp2)
            if tmp2 > 0:
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的收益积分+' + str(tmp2) + 'BUFF'
            else:
                result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的收益积分' + str(tmp2) + 'BUFF'
        elif ran < 95: # 双倍积分收益
            tmp = random.randrange(0, 3) + 1
            changeToDoubleGold(id, tmp)
            result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的双倍积分收益BUFF'
        elif ran < 98: # 三倍积分收益
            tmp = random.randrange(0, 3) + 1
            changeToTripleGold(id, tmp)
            result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的双倍积分收益BUFF'
        else: # 无敌模式
            tmp = random.randrange(0, 3) + 1
            changeToTmpGod(id, tmp)
            result += '你在闲逛的时候，获得了一个' + str(tmp) + '次的临时击剑无敌BUFF'


    elif probability < 400: # 不好不坏
        ran = random.randrange(0, 3)

        if ran == 0:
            result = '你在闲逛的时候被网红火锅店吸引没忍住冲了进去，积分-1，体力+2'
            gold = -1
            strength = 2
        elif ran == 1:
            result = '你在闲逛的时候，嘴馋买了个冰淇淋，积分-2，体力+2'
            gold = -2
            strength = 2
        if ran == 2:
            result = '你在闲逛的时候被舞女拉进了小树林，积分-2，体力+2'
            gold = -2
            strength = 2

    elif probability < 550: # 一般好
        ran = random.randrange(0, 10)

        if ran == 0:
            result = '你在闲逛的时候遇见了阿拉灯神丁，他说实现你三个愿望然后摸了你的钱包转身就走，积分+3'
            gold = 3
        elif ran == 1:
            result = '你在闲逛的时候邂逅了笑猫，他送给你了一个大大的笑容，体力+3'
            strength = 3
        elif ran == 2:
            result = '你闲逛的时候碰见富豪在路上撒钱，积分+2'
            gold = 2
        elif ran == 3:
            result = '你在闲逛的时候，决定尝试一下彩票，中奖了，积分+1'
            gold = 1
        elif ran == 4:
            result = '你在闲逛的时候，决定尝试一下彩票，中奖了，积分+2'
            gold = 2
        elif ran == 5:
            result = '你在闲逛的时候，决定尝试一下彩票，中奖了，积分+3'
            gold = 3
        elif ran == 6:
            result = '你在闲逛的时候，决定尝试一下刮刮乐，中奖了，积分+1'
            gold = 1
        elif ran == 7:
            result = '你出去闲逛的时候邂逅了霸道总裁，总裁他妈为了拆散你们拿钱羞辱你，积分+2'
            gold = 2
        elif ran == 8:
            result = '你出去闲逛的时候邂逅了富婆，富婆他妈为了拆散你们拿钱羞辱你，积分+2'
            gold = 2
        elif ran == 9:
            result = '你闲逛的时候采到了采女孩的小蘑菇回去当晚饭，积分+1'
            gold = 1
        elif ran == 10:
            result = '你在闲逛的时候遇见了一个要自杀的女孩，将其救下后，她的家人奖励了你一些钱，积分+1'
            gold = 1

    elif probability < 800: # 一般坏
        ran = random.randrange(0, 8)

        if ran == 0:
            result = '你在路上看美女被小柒发现，惨遭暴打，体力-2，积分-2'
            gold = -2
            strength = -2
        elif ran == 1:
            result = '你出门之后天下起了倾盆大雨，狂奔回家之后发现钥匙丢在了咖啡厅，于是去咖啡厅拿了钥匙后折返，体力-1'
            strength = -1
        elif ran == 2:
            result = '你在闲逛的时候逛回去了，啥也没获得,体力-1'
            strength = -1
        elif ran == 3:
            result = '你在闲逛的时候，决定尝试一下彩票，但是没有中奖，积分-2'
            gold = -2
        elif ran == 4:
            result = '你在闲逛的时候，决定尝试一下刮刮乐，但是没有中奖，积分-2'
            gold = -2
        elif ran == 5:
            result = '你在闲逛的时候，嘴馋买了个冰淇淋，积分-2'
            gold = -2
        elif ran == 6:
            result = '你闲逛的时候被牛顿的果子砸了并冒出了一圈星星，体力-2'
            strength = -2
        elif ran == 7:
            result = '你闲逛的时候被狗追，于是选择在树上卡了一天，体力-3'
            strength = -3
            
    elif probability < 880: # 比较好
        ran = random.randrange(0, 4)

        if ran == 0:
            result = '你在闲逛的时候，遇见了一个卖苹果的老婆婆，你买了一些苹果，积分-1，体力+5'
            gold = -1
            strength = 5
        elif ran == 1:
            result = '你出去闲逛的时候碰见npy妈妈，原来Ta是隐藏的富二代，Ta妈妈甩给你五十万让你走，伤害性不大，侮辱性极强，积分+5'
            gold = 5
        elif ran == 2:
            result = '你买彩票中了二等奖，积分+5'
            gold = 5
        elif ran == 3:
            result = '你参加了一场马拉松并且获得了第一名，体力-1，积分+5'
            gold = 5
            strength = -1

    elif probability < 960: # 比较坏
        ran = random.randrange(0, 4)
        
        if ran == 0:
            result = '你在闲逛的时候遇见了一个可怜的乞丐，给了他一些钱，积分-5'
            gold = -5
        elif ran == 1:
            result = '你在闲逛的时候，不小心掉进了下水道，积分-5，体力-5'
            gold = -5
            strength = -5
        elif ran == 2:
            result = '你在闲逛的时候，遇见了一个卖苹果的老婆婆，你买了一些苹果，发现是毒苹果，积分-1，体力-5'
            gold = -1
            strength = -5
        elif ran == 3:
            result = '你在闲逛的时候，遇见了一个歹徒正在欺负一个女孩，你立马飞奔而去打走歹徒，却发现原来他们是在拍戏，只好赔偿医疗费，积分-5'
            gold = -5

    elif probability < 980: # 超级好
        ran = random.randrange(0, 2)

        if ran == 0:
            result = '你在收拾家里的东西的时候发现了祖先留下来的宝贝，积分+10'
            gold = 10
        elif ran == 1:
            result = '你的好朋友成了首富，请你大吃了一顿，体力+10'
            strength = 10

    elif probability < 1000: # 超级坏
        ran = random.randrange(0, 2)

        if ran == 0:
            result = '你在闲逛的时候玩手机没看路，撞上了电线杆，体力值-10'
            strength = -10
        elif ran == 1:
            result = '你在闲逛的时候遇见了阿拉灯神丁，他说实现你三个愿望然后趁你不注意摸偷了你的钱包转身就跑，积分-10'
            gold = -10

    update(id, 2, gold, strength) # 更新数据
    return result
    
# ============================================
# 管理操作

def editGold(id, gold):
    global user
    if user.__contains__(id):
        update(id, -1, gold, 0)
        return '积分修改成功'
    else:
        return '不存在该用户'

def editStrength(id, strength):
    global user
    if user.__contains__(id):
        user[id]['attribute']['strength'] = strength
        return '体力修改成功'
    else:
        return '不存在该用户'

def viewUser(id):
    global user
    if user.__contains__(id):
        return getMyData(id)
    else:
        return '不存在该用户'

def viewRate(id):
    global user
    if user.__contains__(id):
        return user[id]['name'] + getRate(id)
    else:
        return '不存在该用户'

def viewWarehouse(id):
    global user
    if user.__contains__(id):
        return user[id]['name'] + getWarehouse(id)[1:]
    else:
        return '不存在该用户'

def viewEquipment(id):
    global user
    if user.__contains__(id):
        return user[id]['name'] + getEquipment(id)[1:]
    else:
        return '不存在该用户'

def viewBuff(id):
    global user
    if user.__contains__(id):
        return user[id]['name'] + getBuff(id)[1:]
    else:
        return '不存在该用户'


# BUFF启用
def viewGod():
    global systemData
    result = '无敌的人：' + str(systemData['god'])
    result += '\n临时无敌模式：'
    for key, value in systemData['tmpGod'].items():
        result += '\n\t' + str(key) + '：' + str(value['number']) + '次'
    return result

def closeGod(id):
    global systemData
    if id in systemData['god']:
        systemData['god'].remove(id)
    if systemData['tmpGod'].__contains__(id):
        del systemData['tmpGod'][id]
    return '关闭成功！'

def changeToGod(id):
    global systemData
    if id in systemData['god']:
        return '该用户已经是无敌模式了哦~'
    else:
        systemData['god'].append(id)
        return '开启无敌模式成功'

def changeToTmpGod(id, number):
    global systemData
    if systemData['tmpGod'].__contains__(id):
        systemData['tmpGod'][id]['number'] += number
    else:
        systemData['tmpGod'][id] = {}
        systemData['tmpGod'][id]['number'] = number
    if systemData['tmpGod'][id]['number'] <= 0:
        del systemData['tmpGod'][id]
    return '已经为其开启' + str(number) + '次无敌模式'

def changeToRampage1(id, number):
    global systemData
    if systemData['rampage-1'].__contains__(id):
        systemData['rampage-1'][id]['number'] += number
    else:
        systemData['rampage-1'][id] = {}
        systemData['rampage-1'][id]['number'] = number
    if systemData['rampage-1'][id]['number'] <= 0:
        del systemData['rampage-1'][id]
    return '已经为其开启' + str(number) + '次1级进攻'

def changeToRampage2(id, number):
    global systemData
    if systemData['rampage-2'].__contains__(id):
        systemData['rampage-2'][id]['number'] += number
    else:
        systemData['rampage-2'][id] = {}
        systemData['rampage-2'][id]['number'] = number
    if systemData['rampage-2'][id]['number'] <= 0:
        del systemData['rampage-2'][id]
    return '已经为其开启' + str(number) + '次2级进攻'

def changeToRampage3(id, number):
    global systemData
    if systemData['rampage-3'].__contains__(id):
        systemData['rampage-3'][id]['number'] += number
    else:
        systemData['rampage-3'][id] = {}
        systemData['rampage-3'][id]['number'] = number
    if systemData['rampage-3'][id]['number'] <= 0:
        del systemData['rampage-3'][id]
    return '已经为其开启' + str(number) + '次3级进攻'
    
def changeToDefense1(id, number):
    global systemData
    if systemData['defense-1'].__contains__(id):
        systemData['defense-1'][id]['number'] += number
    else:
        systemData['defense-1'][id] = {}
        systemData['defense-1'][id]['number'] = number
    if systemData['defense-1'][id]['number'] <= 0:
        del systemData['defense-1'][id]
    return '已经为其开启' + str(number) + '次1级防御'

def changeToDefense2(id, number):
    global systemData
    if systemData['defense-2'].__contains__(id):
        systemData['defense-2'][id]['number'] += number
    else:
        systemData['defense-2'][id] = {}
        systemData['defense-2'][id]['number'] = number
    if systemData['defense-2'][id]['number'] <= 0:
        del systemData['defense-2'][id]
    return '已经为其开启' + str(number) + '次2级防御'

def changeToDefense3(id, number):
    global systemData
    if systemData['defense-3'].__contains__(id):
        systemData['defense-3'][id]['number'] += number
    else:
        systemData['defense-3'][id] = {}
        systemData['defense-3'][id]['number'] = number
    if systemData['defense-3'][id]['number'] <= 0:
        del systemData['defense-3'][id]
    return '已经为其开启' + str(number) + '次3级防御'

def changeToNoLoss(id, number):
    global systemData
    if systemData['noLoss'].__contains__(id):
        systemData['noLoss'][id]['number'] += number
    else:
        systemData['noLoss'][id] = {}
        systemData['noLoss'][id]['number'] = number
    if systemData['noLoss'][id]['number'] <= 0:
        del systemData['noLoss'][id]
    return '已经为其开启' + str(number) + '次击剑不掉积分'

def changeToHalveGold(id, number):
    global systemData
    if systemData['halveGold'].__contains__(id):
        systemData['halveGold'][id]['number'] += number
    else:
        systemData['halveGold'][id] = {}
        systemData['halveGold'][id]['number'] = number
    if systemData['halveGold'][id]['number'] <= 0:
        del systemData['halveGold'][id]
    return '已经为其开启' + str(number) + '次积分收益减半'

def changeToDoubleGold(id, number):
    global systemData
    if systemData['doubleGold'].__contains__(id):
        systemData['doubleGold'][id]['number'] += number
    else:
        systemData['doubleGold'][id] = {}
        systemData['doubleGold'][id]['number'] = number
    if systemData['doubleGold'][id]['number'] <= 0:
        del systemData['doubleGold'][id]
    return '已经为其开启' + str(number) + '次双倍积分收益'

def changeToTripleGold(id, number):
    global systemData
    if systemData['tripleGold'].__contains__(id):
        systemData['tripleGold'][id]['number'] += number
    else:
        systemData['tripleGold'][id] = {}
        systemData['tripleGold'][id]['number'] = number
    if systemData['tripleGold'][id]['number'] <= 0:
        del systemData['tripleGold'][id]
    return '已经为其开启' + str(number) + '次三倍积分收益'

def changeToFixedGold(id, number, gold):
    global systemData

    systemData['fixedGold'][id] = {}
    systemData['fixedGold'][id]['number'] = number
    systemData['fixedGold'][id]['gold'] = gold
    if systemData['fixedGold'][id]['number'] <= 0:
        del systemData['fixedGold'][id]
    return '已经为其开启' + str(number) + '次固定增减积分收益'


# ============================================
# 强化操作

def strengthenAttack(id):
    if user[id]['attribute']['attack'] >= 25:
        return '你的进攻已经达到最高等级，暂时不能强化了'
    else:
        if user[id]['gold'] < 100:
            return '你的积分值小于100'
        times = user[id]['match']['win'] + user[id]['match']['lose']
        times_target = (user[id]['attribute']['attack'] - 4) * 50
        if times < times_target:
            return '你的场次不足' + str(times_target) + '不能强化'

        user[id]['gold'] -= 100
        user[id]['attribute']['attack'] += 1
        return '强化成功！'

def strengthenDefense(id):
    if user[id]['attribute']['defense'] >= 20:
        return '你的防御已经达到最高等级，暂时不能强化了'
    else:
        if user[id]['gold'] < 100:
            return '你的积分值小于100'
        times = user[id]['match']['win'] + user[id]['match']['lose']
        times_target = user[id]['attribute']['defense'] * 50 + 50
        if times < times_target:
            return '你的场次不足' + str(times_target) + '不能强化'

        user[id]['gold'] -= 100
        user[id]['attribute']['defense'] += 1
        return '强化成功！'