class clash:
    def __init__(self):
        pass

    def run(self, message):
        need_reply = False
        reply_text = ''
        reply_image = ''

        message = message.replace(' ', '').lower()

        if message == 'coc商人' or message == 'coc商人刷新表' or message == 'coc商店':
            reply_image = 'data/Clash/商人数据.png'
            need_reply = True
        elif message == 'coc联赛' or message == 'coc联赛奖励':
            reply_image = 'data/Clash/联赛数据.jpg'
            need_reply = True

        elif message == 'coc鱼情' or message == 'coc鱼' or message == 'coc鱼情监控':
            reply_text = 'https://www.cocservice.top/search/'
            need_reply = True
        elif message == 'coc客户端':
            reply_text = 'https://www.cocservice.top/update/apkdownload.html'
            need_reply = True
        elif message == 'coc阵型':
            reply_text = 'https://www.yuque.com/books/share/7a36c5ba-3c5e-492b-82c6-38fa813f9367'
            need_reply = True

        # 圣水部队
        elif message == 'coc野蛮人':
            reply_text = 'https://www.cocservice.top/update/0000-Barbarian'
            need_reply = True
        elif message == 'coc弓箭手':
            reply_text = 'https://www.cocservice.top/update/0001-Archer'
            need_reply = True
        elif message == 'coc巨人' or message == 'coc胖子':
            reply_text = 'https://www.cocservice.top/update/0002-Giant'
            need_reply = True
        elif message == 'coc哥布林':
            reply_text = 'https://www.cocservice.top/update/0003-Goblin'
            need_reply = True
        elif message == 'coc炸弹人':
            reply_text = 'https://www.cocservice.top/update/0004-Wall-Breaker'
            need_reply = True
        elif message == 'coc气球兵' or message == 'coc气球':
            reply_text = 'https://www.cocservice.top/update/0005-Balloon'
            need_reply = True
        elif message == 'coc法师':
            reply_text = 'https://www.cocservice.top/update/0006-Wizard'
            need_reply = True
        elif message == 'coc天使':
            reply_text = 'https://www.cocservice.top/update/0007-Healer'
            need_reply = True
        elif message == 'coc飞龙' or message == 'coc火龙' or message == 'coc红龙' or message == 'coc大龙':
            reply_text = 'https://www.cocservice.top/update/0008-Dragon'
            need_reply = True
        elif message == 'coc皮卡超人' or message == 'coc皮卡':
            reply_text = 'https://www.cocservice.top/update/0009-P.E.K.K.A'
            need_reply = True
        elif message == 'coc飞龙宝宝' or message == 'coc龙宝宝':
            reply_text = 'https://www.cocservice.top/update/000a-Baby-Dragon'
            need_reply = True
        elif message == 'coc掘地矿工' or message == 'coc矿工':
            reply_text = 'https://www.cocservice.top/update/000b-Miner'
            need_reply = True
        elif message == 'coc雷电飞龙' or message == 'coc雷龙' or message == 'coc电龙':
            reply_text = 'https://www.cocservice.top/update/000c-Electro-Dragon'
            need_reply = True
        elif message == 'coc大雪怪':
            reply_text = 'https://www.cocservice.top/update/000d-Yeti'
            need_reply = True
        elif message == 'coc龙骑士':
            reply_text = 'https://www.cocservice.top/update/000e-Dragon-Rider'
            need_reply = True

        # 黑油部队
        elif message == 'coc亡灵':
            reply_text = 'https://www.cocservice.top/update/0080-Minion'
            need_reply = True
        elif message == 'coc野猪骑士' or message == 'coc野猪' or message == 'coc猪':
            reply_text = 'https://www.cocservice.top/update/0081-Hog-Rider'
            need_reply = True
        elif message == 'coc瓦基丽武神' or message == 'coc女武神':
            reply_text = 'https://www.cocservice.top/update/0082-Valkyrie'
            need_reply = True
        elif message == 'coc戈仑石人' or message == 'coc石头人':
            reply_text = 'https://www.cocservice.top/update/0083-Golem'
            need_reply = True
        elif message == 'coc女巫':
            reply_text = 'https://www.cocservice.top/update/0084-Witch'
            need_reply = True
        elif message == 'coc熔岩猎犬' or message == 'coc狗':
            reply_text = 'https://www.cocservice.top/update/0085-Lava-Hound'
            need_reply = True
        elif message == 'coc巨石投手' or message == 'coc蓝胖':
            reply_text = 'https://www.cocservice.top/update/0086-Bowler'
            need_reply = True
        elif message == 'coc戈仑冰人' or message == '冰人':
            reply_text = 'https://www.cocservice.top/update/0087-Ice-Golem'
            need_reply = True
        elif message == 'coc英雄猎手' or message == 'coc头号杀手' or message == 'coc猎头':
            reply_text = 'https://www.cocservice.top/update/0088-Headhunter'
            need_reply = True

        # 法术
        elif message == 'coc雷电法术' or message == 'coc闪电' or message == 'coc雷电' or message == 'coc闪电法术':
            reply_text = 'https://www.cocservice.top/update/0100-Lightning-Spell'
            need_reply = True
        elif message == 'coc疗伤法术' or message == 'coc治疗':
            reply_text = 'https://www.cocservice.top/update/0101-Healing-Spell'
            need_reply = True
        elif message == 'coc狂暴法术' or message == 'coc狂暴':
            reply_text = 'https://www.cocservice.top/update/0102-Rage-Spell'
            need_reply = True
        elif message == 'coc弹跳法术' or message == 'coc弹跳':
            reply_text = 'https://www.cocservice.top/update/0103-Jump-Spell'
            need_reply = True
        elif message == 'coc冰冻法术' or message == 'coc冰冻':
            reply_text = 'https://www.cocservice.top/update/0104-Freeze-Spell'
            need_reply = True
        elif message == 'coc镜像法术' or message == 'coc镜像':
            reply_text = 'https://www.cocservice.top/update/0105-Clone-Spell'
            need_reply = True
        elif message == 'coc隐形法术' or message == 'coc隐形':
            reply_text = 'https://www.cocservice.top/update/0106-Invisibility-Spell'
            need_reply = True
        elif message == 'coc毒药法术' or message == 'coc毒药':
            reply_text = 'https://www.cocservice.top/update/0180-Poison-Spell'
            need_reply = True
        elif message == 'coc地震法术' or message == 'coc地震':
            reply_text = 'https://www.cocservice.top/update/0181-Earthquake-Spell'
            need_reply = True
        elif message == 'coc急速法术' or message == 'coc急速':
            reply_text = 'https://www.cocservice.top/update/0182-Haste-Spell'
            need_reply = True
        elif message == 'coc骷髅法术' or message == 'coc骷髅':
            reply_text = 'https://www.cocservice.top/update/0183-Skeleton-Spell'
            need_reply = True
        elif message == 'coc蝙蝠法术' or message == 'coc蝙蝠':
            reply_text = 'https://www.cocservice.top/update/0184-Bat-Spell'
            need_reply = True

        # 英雄与战宠
        elif message == 'coc野蛮人之王' or message == 'coc男王' or message == 'coc蛮王' or message == 'coc英雄':
            reply_text = 'https://www.cocservice.top/update/0200-Barbarian-King'
            need_reply = True
        elif message == 'coc弓箭女皇' or message == 'coc女王':
            reply_text = 'https://www.cocservice.top/update/0201-Archer-Queen'
            need_reply = True
        elif message == 'coc大守护者' or message == 'coc永王' or message == 'coc咏王':
            reply_text = 'https://www.cocservice.top/update/0202-Grand-Warden'
            need_reply = True
        elif message == 'coc飞盾战神' or message == 'coc闰土':
            reply_text = 'https://www.cocservice.top/update/0203-Royal-Champion'
            need_reply = True
        elif message == 'coc莱希' or message == 'coc战宠':
            reply_text = 'https://www.cocservice.top/update/0280-L.A.S.S.I'
            need_reply = True
        elif message == 'coc闪枭':
            reply_text = 'https://www.cocservice.top/update/0281-Electro-Owl'
            need_reply = True
        elif message == 'coc大牦':
            reply_text = 'https://www.cocservice.top/update/0282-Mighty-Yak'
            need_reply = True
        elif message == 'coc独角':
            reply_text = 'https://www.cocservice.top/update/0283-Unicorn'
            need_reply = True

        # 攻城器械
        elif message == 'coc攻城战车' or message == 'coc攻城车':
            reply_text = 'https://www.cocservice.top/update/0240-Wall-Wrecker'
            need_reply = True
        elif message == 'coc攻城飞艇' or message == 'coc飞艇':
            reply_text = 'https://www.cocservice.top/update/0241-Battle-Blimp'
            need_reply = True
        elif message == 'coc攻城气球' or message == 'coc打气球':
            reply_text = 'https://www.cocservice.top/update/0242-Stone-Slammer'
            need_reply = True
        elif message == 'coc攻城训练营':
            reply_text = 'https://www.cocservice.top/update/0243-Siege-Barracks'
            need_reply = True
        elif message == 'coc攻城滚木车' or message == 'coc滚木攻城车' or message == 'coc滚木车':
            reply_text = 'https://www.cocservice.top/update/0244-Log-Launcher'
            need_reply = True

        elif message == 'coc城墙':
            reply_text = 'https://www.cocservice.top/update/0300-Walls'
            need_reply = True
        elif message == 'coc加农炮':
            reply_text = 'https://www.cocservice.top/update/0301-Cannon'
            need_reply = True
        elif message == 'coc箭塔':
            reply_text = 'https://www.cocservice.top/update/0302-Archer-Tower'
            need_reply = True
        elif message == 'coc迫击炮':
            reply_text = 'https://www.cocservice.top/update/0303-Mortar'
            need_reply = True
        elif message == 'coc防空火箭':
            reply_text = 'https://www.cocservice.top/update/0304-Air-Defense'
            need_reply = True
        elif message == 'coc法师塔':
            reply_text = 'https://www.cocservice.top/update/0305-Wizard-Tower'
            need_reply = True
        elif message == 'coc空气炮' or message == 'coc吹风机':
            reply_text = 'https://www.cocservice.top/update/0306-Air-Sweeper'
            need_reply = True
        elif message == 'coc特斯拉电磁塔' or message == 'coc电塔' or message == '特斯拉电塔':
            reply_text = 'https://www.cocservice.top/update/0307-Hidden-Tesla'
            need_reply = True
        elif message == 'coc炸弹塔':
            reply_text = 'https://www.cocservice.top/update/0308-Bomb-Tower'
            need_reply = True
        elif message == 'cocx连弩' or message == 'coc连弩':
            reply_text = 'https://www.cocservice.top/update/0309-X-Bow'
            need_reply = True
        elif message == 'coc地狱之塔' or message == 'coc地狱塔':
            reply_text = 'https://www.cocservice.top/update/030a-Inferno-Tower'
            need_reply = True
        elif message == 'coc天鹰火炮':
            reply_text = 'https://www.cocservice.top/update/030b-Eagle-Artillery'
            need_reply = True
        elif message == 'coc投石炮':
            reply_text = 'https://www.cocservice.top/update/030e-Scattershot'
            need_reply = True
        elif message == 'coc隐形炸弹' or message == 'coc小炸弹':
            reply_text = 'https://www.cocservice.top/update/0380-Bomb'
            need_reply = True
        elif message == 'coc隐形弹簧':
            reply_text = 'https://www.cocservice.top/update/0381-Spring-Trap'
            need_reply = True
        elif message == 'coc空中炸弹':
            reply_text = 'https://www.cocservice.top/update/0382-Air-Bomb'
            need_reply = True
        elif message == 'coc巨型炸弹' or message == 'coc大炸弹':
            reply_text = 'https://www.cocservice.top/update/0383-Giant-Bomb'
            need_reply = True
        elif message == 'coc搜空地雷':
            reply_text = 'https://www.cocservice.top/update/0384-Seeking-Air-Mine'
            need_reply = True
        elif message == 'coc骷髅陷阱':
            reply_text = 'https://www.cocservice.top/update/0385-Skeleton-Trap'
            need_reply = True
        elif message == 'coc飓风陷阱':
            reply_text = 'https://www.cocservice.top/update/0386-Tornado-Trap'
            need_reply = True

        elif message == 'coc巨型特斯拉电磁塔':
            reply_text = 'https://www.cocservice.top/update/030c-Giga-Tesla'
            need_reply = True
        elif message == 'coc巨型地狱之塔':
            reply_text = 'https://www.cocservice.top/update/030d-Giga-Inferno'
            need_reply = True
        elif message == 'coc14本巨型地狱之塔':
            reply_text = 'https://www.cocservice.top/update/030f-Giga-Inferno-14'
            need_reply = True
        elif message == 'coc大本营':
            reply_text = 'https://www.cocservice.top/update/0400-Town-Hall'
            need_reply = True
        elif message == 'coc金矿':
            reply_text = 'https://www.cocservice.top/update/0401-Gold-Mine'
            need_reply = True
        elif message == 'coc圣水收集器':
            reply_text = 'https://www.cocservice.top/update/0402-Elixir-Collector'
            need_reply = True
        elif message == 'coc储金罐':
            reply_text = 'https://www.cocservice.top/update/0404-Gold-Storage'
            need_reply = True
        elif message == 'coc圣水瓶':
            reply_text = 'https://www.cocservice.top/update/0405-Elixir-Storage'
            need_reply = True
        elif message == 'coc暗黑重油罐':
            reply_text = 'https://www.cocservice.top/update/0406-Dark-Elixir-Storage'
            need_reply = True
        elif message == 'coc部落城堡':
            reply_text = 'https://www.cocservice.top/update/0407-Clan-Castle'
            need_reply = True
        elif message == 'coc兵营':
            reply_text = 'https://www.cocservice.top/update/0480-Army-Camp'
            need_reply = True
        elif message == 'coc训练营':
            reply_text = 'https://www.cocservice.top/update/0481-Barracks'
            need_reply = True
        elif message == 'coc暗黑训练营':
            reply_text = 'https://www.cocservice.top/update/0482-Dark-Barracks'
            need_reply = True
        elif message == 'coc实验室' or message == 'coc研究所':
            reply_text = 'https://www.cocservice.top/update/0483-Laboratory'
            need_reply = True
        elif message == 'coc法术工厂':
            reply_text = 'https://www.cocservice.top/update/0484-Spell-Factory'
            need_reply = True
        elif message == 'coc暗黑法术工厂':
            reply_text = 'https://www.cocservice.top/update/0485-Dark-Spell-Factory'
            need_reply = True
        elif message == 'coc攻城机器工坊':
            reply_text = 'https://www.cocservice.top/update/0486-Workshop'
            need_reply = True
        elif message == 'coc战宠小屋':
            reply_text = 'https://www.cocservice.top/update/0487-Pet-House'
            need_reply = True
        elif message == 'coc建筑工人小屋':
            reply_text = 'https://www.cocservice.top/update/0500-Builders-Hut'
            need_reply = True
        elif message == 'coc建筑大师小屋':
            reply_text = 'https://www.cocservice.top/update/0501-Master-Builders-Hut'
            need_reply = True

        # 超级部队
        elif message == 'coc超级野蛮人' or message == 'coc小黄毛':
            reply_text = 'https://www.cocservice.top/update/0600-Super-Barbarian'
            need_reply = True
        elif message == 'coc超级弓箭手' or message == 'coc超弓':
            reply_text = 'https://www.cocservice.top/update/0606-Super-Archer'
            need_reply = True
        elif message == 'coc超级巨人' or message == 'coc超胖':
            reply_text = 'https://www.cocservice.top/update/0602-Super-Giant'
            need_reply = True
        elif message == 'coc隐秘哥布林' or message == 'coc超级哥布林' or message == 'coc超哥':
            reply_text = 'https://www.cocservice.top/update/0601-Sneaky-Goblin'
            need_reply = True
        elif message == 'coc超级炸弹人' or message == 'coc超炸':
            reply_text = 'https://www.cocservice.top/update/0603-Super-Wall-Breaker'
            need_reply = True
        elif message == 'coc火箭气球兵':
            reply_text = 'https://www.cocservice.top/update/060b-Rocket-Balloon'
            need_reply = True
        elif message == 'coc超级法师' or message == 'coc超法':
            reply_text = 'https://www.cocservice.top/update/0609-Super-Wizard'
            need_reply = True
        elif message == 'coc地狱飞龙':
            reply_text = 'https://www.cocservice.top/update/0604-Inferno-Dragon'
            need_reply = True
        elif message == 'coc超级瓦基丽武神':
            reply_text = 'https://www.cocservice.top/update/0607-Super-Valkyrie'
            need_reply = True
        elif message == 'coc超级亡灵' or message == 'coc马云' or message == 'coc超级苍蝇':
            reply_text = 'https://www.cocservice.top/update/0608-Super-Minion'
            need_reply = True
        elif message == 'coc超级女巫':
            reply_text = 'https://www.cocservice.top/update/0605-Super-Witch'
            need_reply = True
        elif message == 'coc寒冰猎犬' or message == 'coc冰狗':
            reply_text = 'https://www.cocservice.top/update/060a-Ice-Hound'
            need_reply = True

        # 夜世界
        elif message == 'coc狂暴野蛮人':
            reply_text = 'https://www.cocservice.top/update/1000-Raged-Barbarian'
            need_reply = True
        elif message == 'coc隐秘弓箭手':
            reply_text = 'https://www.cocservice.top/update/1001-Sneaky-Archer'
            need_reply = True
        elif message == 'coc巨人拳击手':
            reply_text = 'https://www.cocservice.top/update/1002-Boxer-Giant'
            need_reply = True
        elif message == 'coc异变亡灵':
            reply_text = 'https://www.cocservice.top/update/1003-Beta-Minion'
            need_reply = True
        elif message == 'coc炸弹兵':
            reply_text = 'https://www.cocservice.top/update/1004-Bomber'
            need_reply = True
        elif message == 'coc夜世界飞龙宝宝':
            reply_text = 'https://www.cocservice.top/update/1005-Baby-Dragon'
            need_reply = True
        elif message == 'coc加农炮战车' or message == 'coc跑车':
            reply_text = 'https://www.cocservice.top/update/1006-Cannon-Cart'
            need_reply = True
        elif message == 'coc暗夜女巫':
            reply_text = 'https://www.cocservice.top/update/1007-Night-Witch'
            need_reply = True
        elif message == 'coc骷髅气球':
            reply_text = 'https://www.cocservice.top/update/1008-Drop-Ship'
            need_reply = True
        elif message == 'coc超级皮卡':
            reply_text = 'https://www.cocservice.top/update/1009-Super-P.E.K.K.A'
            need_reply = True
        elif message == 'coc野猪飞骑':
            reply_text = 'https://www.cocservice.top/update/100a-Hog-Glider'
            need_reply = True
        elif message == 'coc战争机器':
            reply_text = 'https://www.cocservice.top/update/10f0-Battle-Machine'
            need_reply = True

        elif message == 'coc夜世界城墙':
            reply_text = 'https://www.cocservice.top/update/110c-Walls'
            need_reply = True
        elif message == 'coc夜世界加农炮':
            reply_text = 'https://www.cocservice.top/update/1100-Cannon'
            need_reply = True
        elif message == 'coc双管加农炮':
            reply_text = 'https://www.cocservice.top/update/1101-Double-Cannon'
            need_reply = True
        elif message == 'coc夜世界箭塔':
            reply_text = 'https://www.cocservice.top/update/1102-Archer-Tower'
            need_reply = True
        elif message == 'coc夜世界特斯拉电磁塔':
            reply_text = 'https://www.cocservice.top/update/1103-Hidden-Tesla'
            need_reply = True
        elif message == 'coc夜世界防空火炮':
            reply_text = 'https://www.cocservice.top/update/1104-Firecrackers'
            need_reply = True
        elif message == 'coc撼地巨石':
            reply_text = 'https://www.cocservice.top/update/1105-Crusher'
            need_reply = True
        elif message == 'coc熔岩发射器':
            reply_text = 'https://www.cocservice.top/update/110d-Lava-Launcher'
            need_reply = True
        elif message == 'coc夜世界弹射陷阱':
            reply_text = 'https://www.cocservice.top/update/1180-Push-Trap'
            need_reply = True
        elif message == 'coc夜世界隐形弹簧':
            reply_text = 'https://www.cocservice.top/update/1181-Spring-Trap'
            need_reply = True
        elif message == 'coc夜世界地雷':
            reply_text = 'https://www.cocservice.top/update/1182-Mine'
            need_reply = True
        elif message == 'coc夜世界巨型地雷':
            reply_text = 'https://www.cocservice.top/update/1183-Mega-Mine'
            need_reply = True
        elif message == 'coc建筑大师大本营':
            reply_text = 'https://www.cocservice.top/update/1200-Builder-Hall'
            need_reply = True
        elif message == 'coc夜世界金矿':
            reply_text = 'https://www.cocservice.top/update/1201-Gold-Mine'
            need_reply = True
        elif message == 'coc夜世界圣水收集器':
            reply_text = 'https://www.cocservice.top/update/1202-Elixir-Collector'
            need_reply = True
        elif message == 'coc夜世界储金罐':
            reply_text = 'https://www.cocservice.top/update/1203-Gold-Storage'
            need_reply = True
        elif message == 'coc夜世界圣水瓶':
            reply_text = 'https://www.cocservice.top/update/1204-Elixir-Storage'
            need_reply = True
        elif message == 'coc宝石矿井':
            reply_text = 'https://www.cocservice.top/update/1205-Gem-Mine'
            need_reply = True
        elif message == 'coc建筑大师训练营':
            reply_text = 'https://www.cocservice.top/update/1280-Builder-Barracks'
            need_reply = True
        elif message == 'coc夜世界兵营':
            reply_text = 'https://www.cocservice.top/update/1281-Army-Camp'
            need_reply = True
        elif message == 'coc星空实验室':
            reply_text = 'https://www.cocservice.top/update/1282-Star-Laboratory'
            need_reply = True
        elif message == 'coc时光钟楼':
            reply_text = 'https://www.cocservice.top/update/1283-Clock-Tower'
            need_reply = True
        elif message == 'coc奥仔小屋' or message == 'coc奥拓小屋':
            reply_text = 'https://www.cocservice.top/update/1284-O.T.T.O-Hut'
            need_reply = True

        return need_reply, reply_text, reply_image
