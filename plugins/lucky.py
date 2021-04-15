
import random
import datetime
import plugins.dataManage as dataManage

# ==========================================================
# 运势

lucky = {}
luckfile = 'luck'

def loadLuckFile():
    global lucky
    lucky = dataManage.load_obj(luckfile)

    clockDate = lucky["luckDate"]
    today = str(datetime.date.today())
    if clockDate != today:
        lucky["luck"].clear()
        lucky["luckDate"] = today

def writeFile():
    global lucky
    dataManage.save_obj(lucky, luckfile)


def luck(memberId):
    global lucky
    loadLuckFile()
    if lucky["luck"].__contains__(memberId):
        return '你今天的运势是：' + str(lucky["luck"][memberId])
    
    c = random.normalvariate(50, 15)
    if c < 0:
        c = 0
    elif c > 100:
        c = 100
    lucky["luck"][memberId] = int(c)
    writeFile()
    return '你今天的运势是：' + str(int(c))
