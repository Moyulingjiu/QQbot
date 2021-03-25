
import random
import datetime

# ==========================================================
# 运势

lucky = {}

def loadLuckFile():
    global lucky
    lucky.clear()

    clockDate = ''
    with open('data/clockInData/luckyDate.txt', 'r+', encoding='utf-8') as f:
        clockDate = f.readline()
    today = str(datetime.date.today())
    if clockDate == today:
        with open('data/clockInData/luck.txt', 'r+', encoding='utf-8') as f:
            text = f.readlines()
            for i in text:
                i = i.strip()
                if len(i) == 0:
                    continue
                luckData = i.split(' ')
                lucky[int(luckData[0])] = int(luckData[1])
    else:
        with open('data/clockInData/luckyDate.txt', 'w', encoding='utf-8') as f:
            f.write(today)

def writeFile():
    with open('data/clockInData/luck.txt', 'w', encoding='utf-8') as f:
        for key, value in lucky.items():
            f.write(str(key) + ' ' + str(value) + '\n')



def luck(memberId):
    global lucky
    loadLuckFile()
    if lucky.__contains__(memberId):
        return '你今天的运势是：' + str(lucky[memberId])
    a = random.random()
    b = random.random()
    c = ((a*a + b*b) / 2) ** 0.5
    c *= 100
    lucky[memberId] = int(c)
    writeFile()
    return '你今天的运势是：' + str(int(c))
