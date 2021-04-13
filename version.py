from plugins import dataManage

botBaseInformation = {}

def loadFile():
    global botBaseInformation
    botBaseInformation = dataManage.load_obj('baseInformation')

def saveFile():
    global botBaseInformation
    dataManage.save_obj(botBaseInformation, 'baseInformation')

string = input('请输入版本信息：')
loadFile()
botBaseInformation['baseInformation']['version'] = string
saveFile()
print('修改成功！')
