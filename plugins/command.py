
from plugins import tarot
from plugins import game

# ==========================================================


def help():
    result = '帮助如下\n'
    result += '--------------------------\n'
    result += '(以下为不需要加*的内容)\n'
    result += '1.天气 城市名称：查询指定城市天气\n'
    result += '2.色子/骰子：随机产生一个1——6的随机数\n'
    result += '3.抛硬币：抛掷一枚硬币\n'
    result += '4.文摘：随机返回一句文摘\n'
    result += '5.情话：随机返回一句情话\n'
    result += '6.骂我一句：随机返回一句脏话（非所有群可用）\n'
    result += '7.运势：测现在的运气\n'
    result += '8.打卡：请输入\"打卡帮助\"查询\n'
    result += '9.微博热搜 ：返回微博热搜\n'
    result += '10.百度热搜 ：返回百度热搜\n'
    result += '--------------------------\n'
    result += '(以下为需要加*的内容)\n'
    result += '(请在指令之前加上*，无需@，以便于识别)\n'
    result += '1.help 帮助\n'
    result += '2.tarot 塔罗牌（其他牌阵请输入help tarot查看）\n'
    result += '(请注意占卜类的东西看看就好)\n'
    return result


def helpClock():
    result = '打卡帮助如下\n'
    result += '--------------------------\n'
    result += '1.打卡：完成当天的打卡\n'
    result += '2.添加打卡计划：为当前群聊开启打卡计划（注1）\n'
    result += '3.终止打卡计划：终止当前群聊的打卡计划（注1）\n'
    result += '4.加入打卡计划：加入本群的打卡计划（本群得要有打卡计划）\n'
    result += '5.退出打卡计划：退出本群的打卡计划\n'
    result += '6.打卡计划管理帮助：查看如何管理本群的打卡计划（注1）\n'
    result += '--------------------------\n'
    result += '注1：该命令的执行需要加入贡献者计划（为小柒的开发做出贡献）或者成为管理员\n'
    return result

def helpClockAdmministor():
    result = '打卡管理帮助如下：\n'
    result += '1.添加打卡计划：为当前群聊开启打卡计划\n'
    result += '2.终止打卡计划：终止当前群聊的打卡计划\n'
    result += '3.打卡提醒：展示本群还有哪些人没打卡\n'
    result += '4.锁定打卡计划：不允许加入与退出打卡计划\n'
    result += '5.解锁打卡计划：允许加入与退出打卡计划\n'
    result += '6.锁定打卡计划 加入：不允许加入打卡计划\n'
    result += '7.解锁打卡计划 加入：允许加入打卡计划\n'
    result += '8.锁定打卡计划 退出：不允许退出打卡计划\n'
    result += '9.解锁打卡计划 退出：允许退出打卡计划\n'
    result += '10.开启打卡提醒：开启本群的打卡提醒，每天23:00将会提醒打卡\n'
    result += '11.取消打卡提醒：关闭本群的打卡提醒\n'
    result += '12.开启打卡总结：开启本群的打卡总结，新的一天将会总结昨天谁没有打卡\n'
    result += '13.取消打卡总结：关闭本群的打卡总结\n'
    result += '14.打卡情况：返回本群的打卡情况\n'
    result += '15.打卡情况 群号：返回某个群的打卡情况\n'
    return result



def helpAdministrators():
    result = '管理员/贡献者计划帮助如下：\n'
    result += '--------------------------\n'
    result += '1.添加文摘 文摘1 文摘2：多个文摘之间以空格分隔\n'
    result += '2.添加情话 情话1 情话2：多个情话之间以空格分隔\n'
    result += '3.添加脏话 脏话1 脏话2：多个脏话之间以空格分隔\n'
    result += '4.文摘条数：返回当前有多少条文摘\n'
    result += '5.情话条数：返回当前有多少条情话\n'
    result += '6.脏话条数：返回当前有多少条脏话\n'
    result += '7.小柒报告状况：报告小柒的运行状况\n'
    result += '8.版本信息：返回小柒的版本信息\n'
    result += '9.添加回复 关键词 回复内容：添加一个关键词回复，如果输入这个关键词，小柒将会自动回复回复内容\n'
    result += '10.删除回复 关键词 回复内容：删除一个关键词回复配对\n'
    result += '9.添加回复*关键词*回复内容：（以*分割，可以带空格）添加一个关键词回复，如果输入这个关键词，小柒将会自动回复回复内容\n'
    result += '10.删除回复*关键词*回复内容：（以*分割，可以带空格）删除一个关键词回复配对\n'
    result += '--------------------------\n'
    result += '注：小柒的操作权限分为三类，由高到低分别为：管理员（仅有1人）、贡献者计划、用户\n'
    return result

def allCommand():
    result = '管理员/贡献者计划帮助如下：\n'
    result += '--------------------------\n'
    result += '1.重新加载配置文件：重新加载所有的数据以及配置文件\n'
    result += '2.添加贡献者 账号：向贡献者计划中加入新人\n'
    result += '3.删除贡献者 账号：向贡献者计划中移除某个人\n'
    result += '4.命令大全：返回命令大全\n'
    result += '5.删除文摘 序号：删除某一条文摘\n'
    result += '6.删除情话 序号：删除某一条情话\n'
    result += '7.添加黑名单 群 群号：将该群加入黑名单\n'
    result += '8.添加黑名单 人 QQ号：将该人加入黑名单\n'
    result += '9.移除黑名单 群 群号：将该群移除黑名单\n'
    result += '10.移除黑名单 人 QQ号：将该人移除黑名单\n'
    result += '11.修改版本信息 版本号：远程修改版本信息\n'
    result += '12.查看贡献者计划：查看贡献者计划名单\n'
    result += '13.查看黑名单 人：查看黑名单（人）\n'
    result += '14.查看黑名单 群：查看黑名单（群）\n'
    return result


def helpTarot():
    result = '帮助如下：\n'
    result += '1.tarot 【塔罗牌】\n'
    result += '2.tarotB 【大阿卡那牌】\n'
    result += '3.tarotL 【小阿卡那牌】\n'
    result += '4.tarot 时间 【改变未来最好的时间在于过去，如果发现占卜的未来塔罗牌含义不理想，可以想想过去塔罗牌所表示的问题加以改正。】（用于占卜一段时间）\n'
    result += '5.tarot 是非 【正位表示你需要继续发扬的，逆位表示你需要改正的。】（用于占卜是否能够做成一件事）\n'
    result += '6.tarot 圣三角 【三张牌解读时尽可能的形成逻辑链。】（用于占卜某件事情）\n'
    result += '7.help tarot 页数 (总计3页)\n'
    result += '（目前以支持合计14种牌阵）'

    return result


def helpTarot2():
    result = '帮助如下：\n'
    result += '1.tarot 钻石展开法 【一般情况下二或三号塔罗牌正位表示做过头的事情，逆位表示哪些方面做的还不够好。这是占卜中泰极否来的思想。比如说，对某人好，但好过头反而造成坏结果，凡事都要适度。】（用于占卜事业）\n'
    result += '2.tarot 恋人金字塔 【感情的发展由三号塔罗牌转变至四号塔罗牌，结合一号与二号塔罗牌，分析转变的原因，基本可以回答问卜者的感情问题。】（用于占卜爱情）\n'
    result += '3.tarot 自我探索 【】（用于占卜自己）\n'
    result += '4.tarot 吉普赛十字 【】（用于占卜爱情主题）\n'
    result += '5.tarot 二选一 【】（用于占卜多种选择）\n'
    result += '6.tarot 关系发展 【】（用于占卜你与对方的关系发展）\n'
    result += '7.help tarot 页数 (总计3页)'
    return result


def helpTarot3():
    result = '帮助如下：\n'
    result += '（请注意这一页的塔罗牌阵型都较为复杂，请合理使用避免刷屏）\n'
    result += '1.tarot 六芒星 【】（用于占卜事业）\n'
    result += '2.tarot 凯尔特十字 【】（用于占卜爱情或事业）\n'
    result += '3.help tarot 页数 (总计3页)'
    return result


def function(code):
    if code == 'help':
        result = help()
    elif code == 'help tarot' or code == 'help tarot 1':
        result = helpTarot()
    elif code == 'help tarot 2':
        result = helpTarot2()
    elif code == 'help tarot 3':
        result = helpTarot3()
    elif code == 'tarotB':
        result = tarot.GetTarot()
    elif code == 'tarotL':
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
    else:
        result = '未知指令：' + code + '\n请输入\"*help\"查看帮助'
    return result
