from plugins import dataManage

botBaseInformation = {}

def loadFile():
    global botBaseInformation
    botBaseInformation = dataManage.load_obj('baseInformation')

def saveFile():
    global botBaseInformation
    dataManage.save_obj(botBaseInformation, 'baseInformation')

loadFile()
print('当前版本：' + botBaseInformation['baseInformation']['version'])
string = input('请输入版本信息：')
botBaseInformation['baseInformation']['version'] = string
saveFile()
print('修改成功！')
