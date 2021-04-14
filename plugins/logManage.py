# 日志书写

def log(data):
    with open('data/bot.log', 'a+', encoding='utf-8') as f:
        f.write(data)