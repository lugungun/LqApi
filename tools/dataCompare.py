#  -*-coding:utf8 -*-
import json
from decimal import *


class DataCheck(object):

    def __init__(self):
        pass

    def remove_ex(self, num):
        return num.to_integral() if num == num.to_integral() else num.normalize()

    def dispose(self, retdata_a, dispose_a=None):  # 对小数点的0做处理，例如1.0200=1.02
        retdata_a = str(retdata_a)
        try:
            if type(eval(retdata_a)) == type(float()):
                dispose_a = self.remove_ex(Decimal(str(retdata_a)))
        except:
            pass
        return (retdata_a if dispose_a == None else dispose_a)
    def is_json(self,data):
        """判断字符串能否转化为列表"""

        a = "[{'shareOtd': '2.00', 'shareFrz': 'test'},{'shareOtd': '0.00', 'shareFrz': 'adbv'},]"
        b = "1011re"
        c = '{"loanDate": "2020/05/07", "day": "4", "moneyUseDate": "2020/05/11", "moneyTakeDate": "2020/05/12"}'
        try:
            eval(data)
        except:
            return False
        return True

    def valuecheck(self, type_a, retdata_a, retdata_b, global_match=None,
                   digital=False):  # 检查key和value齐全，支持字典和列表嵌套字典形式；
        # 对两份数据做数据处理转换，兼容字符串类型
        if type(retdata_a) == type(""):
            retdata_a = eval(retdata_a)
        if type(retdata_b) == type(""):
            retdata_b = eval(retdata_b)
        try:
            # 比对的是列表数据(即里面嵌套字典)时
            if type_a == "list":
                for i in range(len(retdata_a)):
                    for y in retdata_a[i]:
                        # 非全局匹配情况
                        if global_match == None:
                            # digital==False不对取值数据做处理，并且对数据类型、列表长度、列表内的字典长度做校验
                            if digital == False and (
                                    retdata_a[i][y] != retdata_b[i][y] or len(retdata_a) != len(retdata_b) or len(
                                    retdata_a[i]) != len(retdata_b[i])):
                                # 成立情况抛出异常
                                raise ValueError("raiseError:type_a==list,digital==True")
                            # digital==True是对数字做处理(例如：4 = 4.0 = "4"= "4.00")；并且对列表长度、列表内的字典长度做校验
                            elif digital == True:
                                count = 0
                                print(type(retdata_a[i][y]))
                                if str(self.dispose(retdata_a[i][y])) != str(self.dispose(retdata_b[i][y])):
                                    #     if self.is_josn(str(retdata_a[i][y])) and  self.is_josn(str(retdata_b[i][y])) :
                                    # print(111)
                                    # self.valuecheck("list",retdata_a[i][y],retdata_b[i][y])
                                    print(111)
                                    raise ValueError("raiseError:type_a==list,digital==False")
                                elif len(retdata_a) != len(retdata_b):
                                    print(len(retdata_a),len(retdata_b))
                                    raise ValueError("raiseError:type_a==list,digital==False")
                                elif len(retdata_a[i]) != len(retdata_b[i]):
                                    print(len(retdata_a[i]),len(retdata_b[i]))
                                    raise ValueError("raiseError:type_a==list,digital==False")




                        # 此块是支持全局匹配，如嵌套多个字典下；只要有一个字段匹配即可
                        else:
                            result_a = False
                            for ii in range(len(retdata_a)):
                                # 只要for循环下全局匹配到一个正确，即为True并退出结束循环
                                if str(self.dispose(retdata_a[i][y])) == str(self.dispose(retdata_b[ii][y])):
                                    result_a = True
                                    break
                            # digital==False不对取值数据做处理，并for循环全局匹配
                            if result_a == False or len(retdata_a) != len(retdata_b):
                                raise ValueError("raiseError:type_a==list,digital==True,global_match")
            # 比对的时字典数据时
            elif type_a == "dict":
                for i in retdata_a:
                    # digital==False不对取值数据做处理，并且对字典长度、value类型做校验
                    if digital == False and (retdata_a[i] != retdata_b[i] or len(retdata_a) != len(retdata_b)):
                        raise ValueError("raiseError:type_a==dict,digital==True")
                    # digital==True对取值数据做处理，并且对字典长度做校验
                    elif digital == True and (
                            str(self.dispose(retdata_a[i])) != str(self.dispose(retdata_b[i])) or len(
                        retdata_a) != len(retdata_b)):
                        raise ValueError("raiseError:type_a==dict,digital==False")
            return True
        except Exception as ex:
            print(ex)
            return False
if __name__ == '__main__':
    dict_a = {"loanDate": "2020/05/07", "day": "4", "moneyUseDate": "2020/05/11", "moneyTakeDate": "2020/05/12"}
    dict_b = {"loanDate": "2020/05/07", "moneyTakeDate": "2020/05/12", "day": "4.00", "moneyUseDate": "2020/05/11"}
    list_a = "[{'shareOtd': '2.00', 'shareFrz': 'test'},{'shareOtd': '0.00', 'shareFrz': 'adbv'},]"
    list_b = [{'shareOtd': 2.0, 'shareFrz': 'test'}, {'shareOtd': "0.00", 'shareFrz': "adbv"}]
    a = DataCheck()
    print(a.is_toJson())
    print(a.valuecheck("dict", dict_a, dict_b, digital=True))
    print(a.valuecheck("list", list_a, list_b, digital=False))
    print(a.valuecheck("list", list_a, list_b, digital=True))
    # pp='[{"PHYSICAL_DATE": "20201216"}, {"PHYSICAL_DATE": 20201217}]'
    # ppp='[{"PHYSICAL_DATE": 20201216}, {"PHYSICAL_DATE": 20201217}]'
    # print(a.valuecheck("list",pp,ppp,digital=True))
    # m=a.valuecheck("list",list_a,list_b,"fortow")
    # print(
    for x in range(len(list_b)):
        for y in list_b[x]:
            print(list_b[x][y])
    pass