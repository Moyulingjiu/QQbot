
import linecache

def step(index, total):
    index += 1
    if index > total:
        index = 1
    return index

def getVocabulary4(number):
    if number > 20:
        return '贪心可不是好事哦~请输入一个小于等于20的数字'
    lineNumber = 1
    with open('data/vocabulary-4-index.txt', 'r+', encoding='utf-8') as f:
        lineNumber = int(f.readline())

    totalNumber = int(linecache.getline(r'data/vocabulary-4.txt', 1))
    reply = ''
    for i in range(0, number):
        reply += linecache.getline(r'data/vocabulary-4.txt', lineNumber + 1)
        lineNumber = step(lineNumber, totalNumber)
    
    print('lineNumber：', lineNumber)

    with open('data/vocabulary-4-index.txt', 'w+', encoding='utf-8') as f:
        f.write(str(lineNumber))

    return reply[:-1]
        
def getVocabulary6(number):
    if number > 20:
        return '贪心可不是好事哦~请输入一个小于等于20的数字'
    lineNumber = 1
    with open('data/vocabulary-6-index.txt', 'r+', encoding='utf-8') as f:
        lineNumber = int(f.readline())

    totalNumber = int(linecache.getline(r'data/vocabulary-6.txt', 1))
    reply = ''
    for i in range(0, number):
        reply += linecache.getline(r'data/vocabulary-6.txt', lineNumber + 1)
        lineNumber = step(lineNumber, totalNumber)

    with open('data/vocabulary-6-index.txt', 'w+', encoding='utf-8') as f:
        f.write(str(lineNumber))
    return reply[:-1]