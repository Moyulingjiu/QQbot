import requests        #导入requests包
from bs4 import BeautifulSoup

def getHot():
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    strhtml = requests.get(url)        #Get方式获取网页数据
    soup = BeautifulSoup(strhtml.text,'html.parser')

    data = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > a')

    result = ''
    for index in range(0, 7):
        i = data[index]
        link = i.get('href')
        contain = i.get_text()
        if index != 0:
            result +=  '\n' + str(index) + ':' + contain
        else:
            result += '微博置顶:' + contain

    return result

if __name__ == '__main__':
    print(getHot())