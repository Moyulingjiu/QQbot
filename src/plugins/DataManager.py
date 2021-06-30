
class DataManager:

    def __init__(self):
        pass


class BaseData:
    bot_information = {}
    clock = {}
    lucky = {}
    bot_qq = 0
    bot_name = '小柒'

    def __init__(self):
        pass


class replyData:
    need_reply = False
    reply_text = ''  # 回复的文本内容
    reply_image = ''  # 回复的图片
    need_at = False  # 是否需要at
    at_qq = 0  # at的qq是谁
    be_at = False  # 是否被at

    def __init__(self):
        pass