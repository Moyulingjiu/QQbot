import random
import time
import re

from plugins import dataManage


def dick_sys(max_range):
    return random.randint(1, max_range)


def attribute_dick1():
    return (dick_sys(6) + dick_sys(6) + dick_sys(6)) * 5


def attribute_dick2():
    return (dick_sys(6) + dick_sys(6) + 6) * 5


# 将字符串转变为属性字典
# 0:追加属性
# 1:修改属性
def str_to_attribute(attribute, string, mode):
    print('attribute:' + str(attribute))
    print('string:' + string)
    print('mode:' + str(mode))
    name = ''
    number = 0
    length = len(string)
    i = 0
    edit_number = 0
    while i < length:
        if string[i].isdigit():
            while string[i].isdigit():
                number = number * 10 + int(string[i])
                i += 1
                if i >= length:
                    break
            if number > 100:
                number = 100
            name = name.strip()
            print(name)
            if len(name) > 0:
                if mode == 0 or (mode == 1 and attribute.__contains__(name)):
                    attribute[name] = number
                    edit_number += 1
            name = ''
            number = 0

        if i >= length:
            break
        name += string[i]
        i += 1

    return attribute, edit_number


# 栈
class Stack:
    def __init__(self):
        self.items = []
        self.length = 0

    # 判断栈是否为空，返回布尔值
    def is_empty(self):
        return self.length == 0

    # 返回栈顶元素
    def top(self):
        return self.items[self.length - 1]

    # 返回栈的大小
    def size(self):
        return self.length

    # 入栈
    def push(self, item):
        self.items.append(item)
        self.length += 1

    # 出栈
    def pop(self):
        if self.length == 0:
            return None
        self.length -= 1
        return self.items.pop()


# 骰子
class Dick:
    def __int__(self):
        self.number = 0
        self.size = 1
        self.sum = 0
        self.dick = []

    def __init__(self, number, size):
        self.number = number
        self.size = size
        if self.number < 0:
            self.number = 0
        if self.size <= 0:
            self.size = 6
        self.sum = 0
        self.dick = []
        self.calculate()

    def calculate(self):
        self.sum = 0
        self.dick = []
        for i in range(self.number):
            tmp = dick_sys(self.size)
            self.dick.append(tmp)
            self.sum += tmp

    def show(self):
        if self.number <= 0:
            return '0'
        if self.number == 1:
            return str(self.dick[0])

        result = '('
        plus_flag = False
        for i in self.dick:
            if plus_flag:
                result += '+'
            else:
                plus_flag = True

            result += str(i)

        result += ')'
        return result

    def show_without_brackets(self):
        if self.number <= 0:
            return '0'
        result = ''
        plus_flag = False
        for i in self.dick:
            if plus_flag:
                result += '+'
            else:
                plus_flag = True

            result += str(i)
        return result


# =====================================
# 计算表达式分析
def filters(string):
    reg = r"[0-9\+\-\*\/\^rd()]+"
    temp = re.fullmatch(reg, string)
    return temp


def power(base, exponent):
    res = 1
    while exponent:
        if exponent & 1:  # 判断当前的最后一位是否为1，如果为1的话，就需要把之前的幂乘到结果中。
            res *= base
        base *= base  # 一直累乘，如果最后一位不是1的话，就不用了把这个值乘到结果中，但是还是要乘。
        exponent = exponent >> 1
    return res


def get_prior(ch):
    if ch == '(':
        return 1
    elif ch == '+' or ch == '-':
        return 2
    elif ch == '*' or ch == '/':
        return 3
    elif ch == '^':
        return 4


# -----------------------
# @author Troiy
# @Date 2021/6/29
# 实现表达式计算
class Expression:
    expression = ''

    def __init__(self, expression):
        self.expression = expression
        self.number = Stack()
        self.operator = Stack()

    def show(self):
        return int(self.handle())

    def calculate(self, operation):
        num3 = 0
        num2 = self.number.pop()
        num1 = self.number.pop()
        if operation == '+':
            num3 = num1 + num2
        elif operation == '-':
            num3 = num1 - num2
        elif operation == '*':
            num3 = num1 * num2
        elif operation == '/':
            num3 = num1 / num2
        elif operation == '^':
            if num2 > 1000:
                raise OverflowError('too large')
            num3 = power(num1, num2)

        self.number.push(num3)

    def handle(self):
        i = 0
        operator_flag = 0
        negate = 1
        bracket_flag = 0
        if filters(self.expression) is None:
            raise ArithmeticError('Non-expression')
        if not self.expression[len(self.expression)-1] == ')' and not '0' <= self.expression[len(self.expression)-1] <= '9':
            raise ArithmeticError('wrong format')
        while i < len(self.expression):
            current = time.time()
            if '0' <= self.expression[i] <= '9':
                j = i + 1
                while j < len(self.expression) and '0' <= self.expression[j] <= '9':
                    j = j + 1
                tmp = int(self.expression[i:j])
                self.number.push(tmp * negate)
                negate = 1
                operator_flag = 0
                i = j
            elif self.expression[i] == '+' or self.expression[i] == '-' or self.expression[i] == '*' or \
                    self.expression[i] == '/' or self.expression[i] == '^':
                if operator_flag < 1 or operator_flag == 1 and self.expression[i] == '-':
                    operator_flag = operator_flag + 1
                    if operator_flag == 1:
                        if self.operator.is_empty():
                            self.operator.push(self.expression[i])
                        else:
                            while not self.operator.is_empty():
                                tmp = self.operator.top()
                                if get_prior(tmp) >= get_prior(self.expression[i]):
                                    self.calculate(tmp)
                                    try:
                                        end = time.time()
                                        if end - current > 1:
                                            raise ArithmeticError("time out")
                                    except ArithmeticError:
                                        print("time out")
                                        raise ArithmeticError("time out")
                                    self.operator.pop()
                                else:
                                    break
                            self.operator.push(self.expression[i])
                    else:
                        if operator_flag == 2:
                            negate = -1
                else:
                    raise ArithmeticError('wrong format')
                i = i + 1
            elif self.expression[i] == 'r':
                try:
                    j = self.expression.index('d', i, len(self.expression))
                    if j != -1:
                        r_str = self.expression[i + 1:j]
                    else:
                        raise ArithmeticError('wrong format')
                except ArithmeticError:
                    print("error")
                    raise ArithmeticError('wrong format')

                d_str = ''
                i = j
                if '0' <= self.expression[i + 1] <= '9':
                    j = i + 1
                    d_str = self.expression[j]
                elif self.expression[i + 1] == '(':
                    bracket_flag = 1
                    j = j+1
                    while bracket_flag > 0:
                        if self.expression[j + 1] == '(':
                            bracket_flag = bracket_flag+1
                        elif self.expression[j+1] == ')':
                            bracket_flag = bracket_flag-1
                        j = j + 1

                    d_str = self.expression[i + 1:j+1]
                dick_expression = Expression(r_str)
                dick_number = dick_expression.handle()
                dick_expression = Expression(d_str)
                dick_size = dick_expression.handle()
                dice = Dick(dick_number, dick_size)
                self.number.push(dice.sum)
                i = j + 1

            elif self.expression[i] == '(':
                self.operator.push(self.expression[i])
                i = i + 1
            elif self.expression[i] == ')':
                while self.operator.top() != '(':
                    tmp = self.operator.top()
                    self.calculate(tmp)
                    try:
                        end = time.time()
                        if end - current > 1:
                            raise ArithmeticError("time out")
                    except ArithmeticError:
                        print("time out")
                        raise ArithmeticError("time out")
                    self.operator.pop()
                self.operator.pop()
                i = i + 1
            else:
                raise ArithmeticError('wrong format')

        while not self.operator.is_empty():
            tmp = self.operator.top()
            self.calculate(tmp)
            try:
                end = time.time()
                if end - current > 1:
                    raise ArithmeticError("time out")
            except ArithmeticError:
                print("time out")
                raise ArithmeticError("time out")
            self.operator.pop()
        return self.number.top()


# 跑团
class TableRolePlayGame:
    attribute = {}
    role = {}

    def __init__(self):
        self.attribute = dataManage.load_obj('self.role')
        self.role = dataManage.load_obj('cocRole')

    # ==========================================================
    # 丢色子

    def rasan(self, group_id, qq):
        if not self.attribute.__contains__(group_id):
            return '意志属性，请使用rd命令手动检验'
        if not self.attribute[group_id].__contains__(qq):
            return '意志属性，请使用rd命令手动检验'

        powe = -1
        if self.attribute[group_id][qq].__contains__('意志'):
            powe = self.attribute[group_id][qq]['意志']
        elif self.attribute[group_id][qq].__contains__('pow'):
            powe = self.attribute[group_id][qq]['pow']

        tmp = dick_sys(100)
        if tmp <= powe:
            return '你扔出来的点数为：' + str(tmp) + '（意志：' + str(powe) + '） 鉴定成功！小柒也在为你祈祷哦~'
        else:
            return '你扔出来的点数为：' + str(tmp) + '（意志：' + str(powe) + '） 鉴定失败！摸摸头，不要哭'

    def sc(self, success, fail_dick_number, fail_dick_size, fail_dick_base, group_id, qq):
        if not self.attribute.__contains__(group_id):
            return '未能找到san值、意志两个属性，请使用rd命令手动检验'
        if not self.attribute[group_id].__contains__(qq):
            return '未能找到san值、意志两个属性，请使用rd命令手动检验'

        san = -1
        powe = -1
        result = '鉴定结果如下：'

        if self.attribute[group_id][qq].__contains__('san'):
            san = self.attribute[group_id][qq]['san']
        elif self.attribute[group_id][qq].__contains__('san值'):
            san = self.attribute[group_id][qq]['san值']
        elif self.attribute[group_id][qq].__contains__('理智'):
            san = self.attribute[group_id][qq]['理智']
        elif self.attribute[group_id][qq].__contains__('理智值'):
            san = self.attribute[group_id][qq]['理智值']

        if self.attribute[group_id][qq].__contains__('意志'):
            powe = self.attribute[group_id][qq]['意志']
        elif self.attribute[group_id][qq].__contains__('pow'):
            powe = self.attribute[group_id][qq]['pow']

        if san == -1 or powe == -1:
            return '未能找到san值、意志两个属性，请使用rd命令手动检验'

        tmp = dick_sys(100)
        if tmp <= powe:
            result = '鉴定成功！'
            san -= success
            if san <= 0:
                san = 0
            result += '\nsan值减少：' + str(success)
            result += '\n目前san值：' + str(san) + '/' + str(powe)
            self.attribute[group_id][qq]['san'] = san
            self.attribute[group_id][qq]['san值'] = san
            self.attribute[group_id][qq]['理智'] = san
            self.attribute[group_id][qq]['理智值'] = san
        else:
            sum = fail_dick_base
            while fail_dick_number > 0:
                fail_dick_number -= 1
                sum += dick_sys(fail_dick_size)
            result = '鉴定失败！'
            san -= sum
            if san <= 0:
                san = 0
            result += '\nsan值减少：' + str(sum)
            result += '\n目前san值：' + str(san) + '/' + str(powe)
            self.attribute[group_id][qq]['san'] = san
            self.attribute[group_id][qq]['san值'] = san
            self.attribute[group_id][qq]['理智'] = san
            self.attribute[group_id][qq]['理智值'] = san
        dataManage.save_obj(self.attribute, 'coc')
        return result

    def sa(self, num, group_id, qq):
        if not self.attribute.__contains__(group_id):
            return '未能找到san值、意志两个属性，请先使用sta指令为你自己添加这个两个属性'
        if not self.attribute[group_id].__contains__(qq):
            return '未能找到san值、意志两个属性，请先使用sta指令为你自己添加这个两个属性'

        san = -1
        powe = -1

        if self.attribute[group_id][qq].__contains__('san'):
            san = self.attribute[group_id][qq]['san']
        elif self.attribute[group_id][qq].__contains__('san值'):
            san = self.attribute[group_id][qq]['san值']
        elif self.attribute[group_id][qq].__contains__('理智'):
            san = self.attribute[group_id][qq]['理智']
        elif self.attribute[group_id][qq].__contains__('理智值'):
            san = self.attribute[group_id][qq]['理智值']

        if self.attribute[group_id][qq].__contains__('意志'):
            powe = self.attribute[group_id][qq]['意志']
        elif self.attribute[group_id][qq].__contains__('pow'):
            powe = self.attribute[group_id][qq]['pow']

        if san == -1 or powe == -1:
            return '未能找到san值、意志两个属性，请先使用sta指令为你自己添加这个两个属性'

        san += num
        if san > powe:
            san = powe
        self.attribute[group_id][qq]['san'] = san
        self.attribute[group_id][qq]['san值'] = san
        self.attribute[group_id][qq]['理智'] = san
        self.attribute[group_id][qq]['理智值'] = san
        return '恢复' + str(num) + 'san值，当前san值：' + str(san) + '/' + str(powe)

    def coc7(self, num):
        result = '你的人物制作：'

        if num <= 0:
            return result
        elif num > 20:
            return '咦？你确定要那么多板子吗？输入一个小于20的数字试试吧~'

        for i in range(num):
            strength = attribute_dick1()
            con = attribute_dick1()
            size = attribute_dick2()
            dex = attribute_dick1()
            appe = attribute_dick1()
            intt = attribute_dick2()
            powe = attribute_dick1()
            edu = attribute_dick2()
            lucky = attribute_dick1()

            result += '\n力量：' + str(strength)
            result += ' 体质：' + str(con)
            result += ' 体型：' + str(size)
            result += ' 敏捷：' + str(dex)
            result += ' 外貌：' + str(appe)
            result += ' 智力：' + str(intt)
            result += ' 意志：' + str(powe)
            result += ' 教育：' + str(edu)
            result += ' 幸运：' + str(lucky)

            result += ' 共计：'
            total = strength + con + size + dex + appe + intt + powe + edu + lucky
            result += str(total) + '/' + str(total + lucky)

        return result

    def rd(self, number, size, times):
        if size > 1000000:
            return '这么多面吗？输一个小点的数字试试吧~'
        if number > 200:
            return '这么多骰子吗？输一个小点的数字试试吧~'

        dick = Dick(number, size)
        if number > 1:
            if times != 1:
                return '你投出的点数为：' + dick.show() + '*' + str(times) + '=' + str(dick.sum * times)
            else:
                return '你投出的点数为：' + dick.show_without_brackets() + '=' + str(dick.sum)
        else:
            if times != 1:
                return '你投出的点数为：' + str(dick.sum * times)
            else:
                return '你投出的点数为：' + str(dick.sum)

    def st(self, attribute, group_id, qq):
        if self.attribute.__contains__(group_id):
            del self.attribute[group_id]
        dataManage.save_obj(self.attribute, 'coc')
        self.sta(attribute, group_id, qq)
        return '覆盖成功！目前有属性个数：' + str(len(self.attribute[group_id][qq]))

    def sta(self, attribute, group_id, qq):
        if not self.attribute.__contains__(group_id):
            self.attribute[group_id] = {}
        if not self.attribute[group_id].__contains__(qq):
            self.attribute[group_id][qq] = {}

        print(1)
        self.attribute[group_id][qq], edit_number = str_to_attribute(self.attribute[group_id][qq], attribute, 0)

        dataManage.save_obj(self.attribute, 'coc')
        return '追加成功！' + '\n追加属性个数：' + str(edit_number) + '\n目前有属性个数：' + str(len(self.attribute[group_id][qq]))

    def stc(self, attribute, group_id, qq):
        if not self.attribute.__contains__(group_id):
            return '不存在该属性'
        if not self.attribute[group_id].__contains__(qq):
            return '不存在该属性'

        self.attribute[group_id][qq], edit_number = str_to_attribute(self.attribute[group_id][qq], attribute, 1)

        dataManage.save_obj(self.attribute, 'coc')
        return '成功修改' + str(edit_number) + '个属性'

    def std(self, attribute, group_id, qq):
        if not self.attribute.__contains__(group_id):
            return '不存在该属性'
        if not self.attribute[group_id].__contains__(qq):
            return '不存在该属性'

        attributeList = attribute.split(' ')
        edit_number = 0
        for i in attributeList:
            i = i.strip()
            if not self.attribute[group_id][qq].__contains__(i):
                continue
            edit_number += 1
            del self.attribute[group_id][qq][i]
        dataManage.save_obj(self.attribute, 'coc')
        return '成功删除' + str(edit_number) + '个属性'

    def clear_all(self, group_id):
        if self.attribute.__contains__(group_id):
            del self.attribute[group_id]
        dataManage.save_obj(self.attribute, 'coc')
        return '清空成功！'

    def clear_single(self, group_id, qq):
        if self.attribute.__contains__(group_id):
            if self.attribute[group_id].__contains__(qq):
                del self.attribute[group_id][qq]
        dataManage.save_obj(self.attribute, 'coc')
        return '清空成功！'

    def show(self, group_id, qq):
        if not self.attribute.__contains__(group_id):
            return '暂无属性'
        if not self.attribute[group_id].__contains__(qq):
            return '暂无属性'
        if len(self.attribute[group_id][qq]) == 0:
            return '暂无属性'

        result = '你的20及以上的属性如下：'
        for key, value in self.attribute[group_id][qq].items():
            if value >= 20:
                result += '\n' + key + '：' + str(value)
        return result

    def show_single(self, name, group_id, qq):
        if not self.attribute.__contains__(group_id):
            return '你没有属性' + name
        if not self.attribute[group_id].__contains__(qq):
            return '你没有属性' + name
        if not self.attribute[group_id][qq].__contains__(name):
            return '你没有属性' + name
        return '属性：' + name + '值：' + str(self.attribute[group_id][qq][name])

    def show_all(self, group_id, qq):
        if not self.attribute.__contains__(group_id):
            return '暂无属性'
        if not self.attribute[group_id].__contains__(qq):
            return '暂无属性'
        if len(self.attribute[group_id][qq]) == 0:
            return '暂无属性'

        result = '你的属性如下：'
        for key, value in self.attribute[group_id][qq].items():
            result += '\n' + key + '：' + str(value)
        return result

    # 鉴定属性
    def ra(self, attribute, group_id, qq):
        if not self.attribute.__contains__(group_id):
            return '不存在该属性'
        if not self.attribute[group_id].__contains__(qq):
            return '不存在该属性'
        if attribute[len(attribute) - 1].isdigit():
            index = len(attribute) - 2
            while index >= 0:
                if not attribute[index].isdigit():
                    break
                index -= 1
            name = ''
            if index == -1:
                name = '[未知属性]'
            else:
                name = attribute[:index + 1]
            number = int(attribute[index + 1:])
            if number > 100:
                number = 100
            elif number < 0:
                number = 0
            dicks = dick_sys(100)
            if dicks < number:
                return '点数：' + str(dicks) + '\n' + name + ':' + str(number) + '\n鉴定成功！'
            else:
                return '点数：' + str(dicks) + '\n' + name + ':' + str(number) + '\n鉴定失败！'

        if not self.attribute[group_id][qq].__contains__(attribute):
            return '不存在该属性'
        dicks = dick_sys(100)
        if dicks <= self.attribute[group_id][qq][attribute]:
            return '点数：' + str(dicks) + '\n' + attribute + ':' + str(
                self.attribute[group_id][qq][attribute]) + '\n鉴定成功！'
        else:
            return '点数：' + str(dicks) + '\n' + attribute + ':' + str(
                self.attribute[group_id][qq][attribute]) + '\n鉴定失败！'

    def export(self, group_id, qq):
        if not self.attribute.__contains__(group_id):
            return '*st '
        if not self.attribute[group_id].__contains__(qq):
            return '*st '
        if len(self.attribute[group_id][qq]) == 0:
            return '*st '

        result = '*st '
        for key, value in self.attribute[group_id][qq].items():
            result += key + str(value)
        return result

    # ====================================
    # 人物模板
    def add_role(self, attribute, group_id, role_name):
        if role_name.isdigit():
            return '人物模板名不能全为数字！'
        if self.role.__contains__(role_name):
            del self.role[role_name]
        self.role[role_name], edit_number = str_to_attribute(self.role[role_name], attribute, 0)

        dataManage.save_obj(self.role, 'cocRole')
        return '人物' + role_name + '已修改'

    def remove_role(self, group_id, role_name):
        if self.role.__contains__(role_name):
            del self.role[role_name]
            dataManage.save_obj(self.role, 'cocRole')
            return '人物' + role_name + '已删除'
        else:
            return '人物' + role_name + '不存在'

    def show_role(self, group_id, role_name):
        if not self.role.__contains__(role_name):
            return '人物' + role_name + '不存在'
        result = '人物' + role_name + '的属性如下：'
        for key, value in self.role[role_name].items():
            result += '\n' + key + '：' + str(value)
        return result

    def show_role_list(self, group_id):
        if len(self.role) == 0:
            return '暂无人物'

        result = '人物列表如下：'
        for key, value in self.role.items():
            result += '\n' + key
        return result

    def copy_role(self, role_name, group_id, qq):
        if not self.attribute.__contains__(group_id):
            self.attribute[group_id] = {}
        if not self.attribute[group_id].__contains__(qq):
            self.attribute[group_id][qq] = {}
        if not self.role.__contains__(role_name):
            return '不存在该人物'

        self.attribute[group_id][qq] = self.role[role_name]
        dataManage.save_obj(self.attribute, 'coc')
        return '已将人物模板' + role_name + '的属性复制给你~'

    def copy_to_role(self, role_name, group_id, qq):
        if not self.attribute.__contains__(group_id):
            return '你目前没有属性，不能复制到人物卡上哦~'
        if not self.attribute[group_id].__contains__(qq):
            return '你目前没有属性，不能复制到人物卡上哦~'

        self.role[role_name] = self.attribute[group_id][qq]
        dataManage.save_obj(self.role, 'cocRole')
