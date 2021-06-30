
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
