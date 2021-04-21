# 日志书写

def log(data):
    with open('data/bot.log', 'a+', encoding='utf-8') as f:
        f.write(data + '\n')

def log(time, data):
    with open('data/bot.log', 'a+', encoding='utf-8') as f:
        f.write('[' + time + '] 执行操作：' + data + '\n')
        
def log(time, id, data):
    with open('data/bot.log', 'a+', encoding='utf-8') as f:
        if id != 0:
            f.write('[' + time + '](' + str(id) + ') 执行操作：' + data + '\n')
        else:
            f.write('[' + time + ']() 执行操作：' + data + '\n')

def groupLog(time, id, groupId, groupName, data):
    with open('data/bot.log', 'a+', encoding='utf-8') as f:
        if id != 0 and groupId != 0:
            f.write('[' + time + '](' + str(id) + ')<' + groupName + '/' + str(groupId) + '> 执行操作：' + data + '\n')
        elif id != 0:
            f.write('[' + time + '](' + str(id) + ')<> 执行操作：' + data + '\n')
        elif id != 0:
            f.write('[' + time + ']()<' + groupName + '/'  + str(groupId) + '> 执行操作：' + data + '\n')
        else:
            f.write('[' + time + ']()<> 执行操作：' + data + '\n')