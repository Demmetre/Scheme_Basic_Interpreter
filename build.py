
from tokens import Tokens
from lexer import Lexer_S
import sys
import re
from itertools import chain
from itertools import tee
import copy
import math
ELEMENT= (int,float,str)
NUMBER = (int , float)
class Procedure:


    # This class has almost same logic described in mainGen.py
    # Difference is that, it saves functions and its argumens in map, so it may seem different
    # It recplaces argument names and takes its values 

    def __init__(self,string,names,args,data):
        self.data = data
        self.string = string
        self.names= names
        self.args = args
    

    def next_token(self):
        if self.string.__len__() == 0 :
            return None 
        try:
            temp = self.string[0]
            self.string = self.string[1:]
            return temp
        except StopIteration:
            return None

    def peek(self):
        if self.string.__len__() == 0 :
            return None 
        try:
            temp = self.string[0]
            return temp
        except StopIteration:
            return None


    def getNumber(self,token):
        try :
            return int(token)
        except :
            return float(token)


    def parse_mod(self, data):
        peek= self.peek()
        first = None
        second = None
        if peek.get_type() == "NUMBER" :
            first = self.getNumber(peek.token)
            self.next_token()
        elif peek.get_type() == "IDENTIFIER":
            first = self.args[self.names.get(peek.token)]
            self.next_token()
        elif peek.token == "(":
            self.next_token()
            first = self.parse_expression(data)
        peek = self.peek()
        if peek.get_type() == "NUMBER" :
            second = self.getNumber(peek.token)
            self.next_token()
        elif peek.get_type() == "IDENTIFIER":
            second = self.args[self.names.get(peek.token)]
            self.next_token()
        elif peek.token == "(":
            self.next_token()
            second = self.parse_expression(data)
        if not(isinstance(first,NUMBER)) or not(isinstance(second,NUMBER)):
            return "no matching syntax rule"
        peek = self.peek()
        if peek.token != ")":
            return "no matching syntax rule"
        self.next_token()
        return first%second




    def parse_expression(self,data = None,flag = False):
        if self.names.__len__() != self.args.__len__() :
            print("invalid number of arguments")
            return 
        next_token = self.next_token()
        if next_token == None :
            print("No matching syntax rule")
            return None
        elif next_token.get_type() == "NUMBER" :
            print("invalid type of expression -> " + next_token.token + " is a number")
            return 0
        # list additional functions 
        elif next_token.token == "caar":
            return self.parse_caar()
        elif next_token.token == "cadr":
            return self.parse_cadr()
        elif next_token.token == "cdar":
            return self.parse_cdar()
        elif next_token.token == "cddr":
            return self.parse_cddr()
        elif next_token.token == "caaar":
            return self.parse_caaar()
        elif next_token.token == "caadr":
            return self.parse_caadr()
        elif next_token.token == "cadar":
            return self.parse_cadar()
        elif next_token.token == "cdaar":
            return self.parse_cdaar()
        elif next_token.token == "cddar":
            return self.parse_cddar()
        elif next_token.token == "caddr":
            return self.parse_caddr()
        elif next_token.token == "cdadr":
            return self.parse_cdadr()
        elif next_token.token == "cdddr":
            return self.parse_cdddr()
        
        elif next_token.token  == "mod":
            res = self.parse_mod(self)
            return res 
        elif next_token.token == "list":
            temp = self.getArgs()
            return temp
        elif next_token.token == "cond" :
            res = self.parse_cond()
            return res
        elif next_token.get_type() == "IF":
            return self.parse_if(data,flag)
        elif next_token.get_type() == "PLUS" :
            return self.parseAddition(data,flag)
        elif next_token.get_type() == "MINUS" :
            return self.parseNegattion(data,flag)
        elif next_token.get_type() == "MULTI" :
            return self.parseMulti(data,flag)
        elif next_token.get_type() == "DIVISION" :
            return self.parseDivision(data,flag)
        elif next_token.get_type() == "APPEND" :
            return self.parse_append() 
        elif next_token.get_type() == "CAR" :
            return self.parse_car()
        elif next_token.get_type() == "CONS" :
            return self.parse_cons()
        elif next_token.get_type() == "CDR" :
            return  self.parse_cdr()
        elif next_token.get_type() == "MAP" :
            res=  self.parse_map()
            return res
        elif next_token.get_type() == "IDENTIFIER" :
            if self.data.get(next_token.token,"NONE") == "NONE"  :
                print("No matching syntax rule, no declaration seen for " + next_token.token)
                return
            a = self.getArgs()
            func = self.data[next_token.token]
            r = func(a)
            self.next_token()
            return r
        elif next_token.token == "length" :
            peek = self.peek()
            temp = None
            if peek.get_type() == "IDENTIFIER" :
                temp = self.args[self.names.get(peek.token)]
                self.next_token()
            elif peek.token == "(":
                self.next_token()
                temp = self.parse_expression()
            else:
                print("invalid identifier for function length")
                return 
            if temp == None or type(temp)!= list:
                print("invalid type of argument")
                return 
            self.next_token()
            return len(temp)
        elif next_token.token == "lambda" :
            func = self.parse_lambda()
            return func
        elif next_token.token == "(" :
            self.next_token()
            funct = self.parse_lambda()
            self.next_token()
            peek = self.peek()
            argL = self.getArgs()
            return funct(argL)
        elif next_token.token == "apply" :
            return self.parse_apply()
        elif next_token.token == "null" :
            return self.parse_null()
        elif next_token.token == "and" :
            first ,second = self.relation()
            self.next_token()
            return first and second
        elif next_token.token == "or" :
            first ,second = self.relation()
            self.next_token()
            return first or second
        elif next_token.token == ">" :
            x,y = self.relation()
            self.next_token()
            return x>y
        elif next_token.token == "<" :
            x,y = self.relation()
            self.next_token()
            return x < y
        elif next_token.token == ">=" :
            x,y = self.relation()
            self.next_token()
            return x >= y
        elif next_token.token == "<=" :
            x,y = self.relation()
            self.next_token()
            return x <= y
        elif next_token.token == "=" :
            x,y = self.relation()
            self.next_token()
            return x == y
        return 0

    def parse_caar(self):
        elem = self.parse_car()
        if type(elem)!= list :
            return "invalid argument, expected list"
        return elem[0]

    def parse_cadr(self):
        elem = self.parse_cdr()
        if type(elem)!= list :
            return "invalid argument, expected list"
        return elem[0]

    def parse_cdar(self):
        elem = self.parse_car()
        if type(elem)!= list :
            return "invalid argument, expected list"
        return elem[1:]

    def parse_cddr(self):
        elem = self.parse_cdr()
        if type(elem)!= list :
            return "invalid argument, expected list"
        return elem[1:]

    def parse_caaar(self):
        elem = self.parse_car()
        if type(elem)!= list :
            return "invalid argument, expected list"
        elem = elem[0]
        if type(elem)!= list :
            return "invalid argument, expected list"
        return elem[0]

    def parse_caadr(self):
        elem = self.parse_cdr()
        if type(elem)!= list :
            return "invalid argument, expected list"
        elem = elem[0]
        if type(elem)!= list :
            return "invalid argument, expected list"
        return elem[0]

    def parse_cadar(self):
        elem = self.parse_car()
        if type(elem)!= list :
            return "invalid argument, expected list"
        elem = elem[1:]
        return elem[0]

    def parse_cdaar(self):
        elem = self.parse_car()
        if type(elem)!= list :
            return "invalid argument, expected list"
        elem = elem[0]
        if type(elem)!= list :
            return "invalid argument, expected list"
        return elem[1:]

    def parse_caddr(self):
        elem = self.parse_cdr()
        if type(elem)!= list :
            return "invalid argument, expected list"
        elem = elem[1:]
        return elem[0]


    def parse_cddar(self):
        elem = self.parse_car()
        if type(elem)!= list :
            return "invalid argument, expected list"
        elem = elem[1:]
        return elem[1:]

    def parse_cdadr(self):
        elem = self.parse_cdr()
        if type(elem)!= list :
            return "invalid argument, expected list"
        elem = elem[0]
        if type(elem)!= list :
            return "invalid argument, expected list"
        return elem[1:]

    def parse_cdddr(self):
        elem = self.parse_cdr()
        if type(elem)!= list :
            return "invalid argument, expected list"
        elem = elem[1:]
        return elem[1:]


    def parse_cond(self):
        peek = self.peek()
        while peek.token != ")":
            peek = self.peek()
            if peek.token != "(":
                return "unexpected token"
            self.next_token()
            peek = self.peek()
            if peek.get_type() == "NUMBER" :
                check = self.getNumber(peek.token)
                self.next_token()
                return check
            elif peek.get_type() == "IDENTIFIER" :
                check = self.args[self.names.get(peek.token)]
                self.next_token()
                return check
            if peek.token != "(":
                return "unexpected token"
            self.next_token()
            peek = self.peek()
            # print(peek.token)
            check = self.parse_expression()
            if not(isinstance(check, bool)) :
                return check
            peek = self.peek()
            if check : 
                res = None
                if peek.get_type() == "NUMBER" :
                    res = self.getNumber(peek.token)
                    self.next_token()
                elif peek.get_type() == "IDENTIFIER" :
                    res = self.args[self.names.get(peek.token)]
                    self.next_token()
                elif peek.token == "(" :
                    self.next_token()
                    peek=self.peek()
                    res = self.parse_expression()
                elif peek.token == "'":
                    self.next_token()
                    self.next_token()
                    res = self.par_list()
                peek = self.peek()
                self.next_token()
                peek = self.peek()
                if peek == None :
                    return check
                return res
            else :
                c = 1
                peek = self.peek()
                while (peek.token != ")" or c != 1):
                    if peek.token == "(" :
                        c = c+1
                    elif peek.token == ")":
                        c = c - 1
                    self.next_token()
                    peek = self.peek()
                peek = self.peek()
                self.next_token()
                peek = self.peek()
                if peek == None :
                    return check


    def parse_lambda(self):
        peek = self.peek()
        if peek.token != "(":
            print("invalid character, no matching syntax rule")
            return
        args = {}
        self.next_token()
        peek = self.peek()
        counter = 0
        while peek!= None and peek.token != ")" :
            if type(peek.token) != str:
                return "invalid identifier"
            args[peek.token] = counter
            self.next_token()
            peek= self.peek()
            counter = counter + 1
        if peek.token != ")":
            return "no matching syntax rule"
        self.next_token()
        peek = self.peek()
        if peek == None or peek.token != "(" :
            return "syntax rule"
        self.next_token()
        peek = self.peek()
        foo = []
        counter = 1
        while peek != None :
            check = self.names.get(peek.token,"NONE")
            if check == "NONE" or args.get(peek.token,"NONE") != "NONE":
                foo.append(peek)
            else :
                tok = self.args[self.names.get(peek.token)]
                temptoken = Tokens(str(tok))
                temptoken.get_type()
                foo.append(temptoken)
            if peek.get_type() == "CLOSE_PAREN" :
                counter = counter - 1
                if counter == 0 :
                    break
            if peek.token == "(":
                counter = counter + 1
            self.next_token()
            peek = self.peek()
        if peek.get_type() != "CLOSE_PAREN":
            return "No matching syntax rule"
        def tempFunc(lst):
            proc = Procedure(foo, args, lst, self.data)
            return proc.parse_expression()
        self.next_token()
        peek = self.peek()
        return tempFunc

    def relation(self):
        peek = self.peek()
        first = None
        second = None
        if peek.get_type() == "NUMBER":
            first = self.getNumber(peek.token)
            self.next_token()
        elif peek.get_type() == "IDENTIFIER" :
            try :
                first = self.args[self.names.get(peek.token)]
            except :
                try :
                    first = self.data.get(peek.token)
                except :
                    pass
            self.next_token()
        elif peek.token == "(":
            self.next_token()
            first = self.parse_expression()
            peek = self.peek()
        else :
            return "invalid type of exression"
        if not(isinstance(first,NUMBER)):
            return "number expected , got other"
        peek = self.peek()
        if peek.get_type() == "NUMBER":
            second = self.getNumber(peek.token)
            self.next_token()
        elif peek.get_type() == "IDENTIFIER" :
            try :
                second = self.args[self.names.get(peek.token)]
            except :
                try :
                    second = self.data.get(peek.token)
                except :
                    pass
            self.next_token()
        elif peek.token == "(":
            self.next_token()
            second = self.parse_expression()
        else :
            return "invalid type of exression"
        if not(isinstance(second,NUMBER)):
            return "number expected , got other"
        peek = self.peek()
        return first,second     


    def getArgs(self) :
        res = []
        peek = self.peek()
        while peek!= None and peek.get_type() != "CLOSE_PAREN" :
            if peek.token == "(":
                self.next_token()
                peek = self.peek()
                temp = self.parse_expression()
                res.append(temp)
            elif peek.get_type() == "IDENTIFIER":
                temp = None
                try :
                    temp = self.args[self.names.get(peek.token)]
                except :
                    try :
                        temp = self.data.get(peek.token)
                    except :
                        temp = None
                res.append(temp)
                self.next_token()
            else:
                if peek.token == "'":
                    self.next_token()
                    self.next_token()
                    tmp  = self.par_list()
                    res.append(tmp)
                else:
                    res.append(self.getNumber(peek.token))
                    self.next_token()
            peek = self.peek()
        return res

    def getOp(self,ope,x , y):
        if ope.token == "min":
            return min(x, y)
        if ope.token == "max":
            return max(x, y)
        if ope.token == "+":
            return x + y
        if ope.token == "-":
            return x - y
        if ope.token == "*":
            return x * y
        if ope.token == "/":
            return x / y
        if ope.token == "append":
            if type(x) != list or type (y)!= list:
                return "invalid type of parameter"
            x.extend(y)
            return x
        if ope.get_type() == "IDENTIFIER":
            func = self.data.get(ope.token,"None")
            if func == "None":
                return "invalid function"
            tss = [x ,y]
            return func(tss)
        return "invalid type"

    def parse_apply(self):
        peek = self.peek()
        operator = peek
        self.next_token()
        peek = self.peek()
        lst = None
        if peek.token == "(":
            self.next_token()
            lst = self.parse_expression()
        else :    
            lst = self.getArgs()[0]
        peek = self.peek()
        size =lst.__len__()
        if size == 0 :
            return []
        result = []
        curr =lst[0]
        for index in range(1,size) :
                curr = self.getOp(operator,curr,lst[index])
        self.next_token()
        peek = self.peek()
        return curr

    # Map funtion can take lambda or defined funtion with one or more arguments, but it should be appropriate.
    # It can also take + - * / operators  

    def parse_map(self):
        peek = self.peek()
        func = None
        if peek == None :
            return "syntax rule"
        if peek.get_type() == "IDENTIFIER" :
            func = self.data.get(peek.token,"NONE")
        if func == "NONE" :
            print("warning , no declaration seen for " + peek.token)
            return
        if peek.token == "+":
     
            def tempfn(lst):
                res = 0
                for x in lst :
                    res = res + x
                return res
            func = tempfn
        elif peek.token == "-":
            def tempfn(lst):
                res = lst[0]
                for x in range(1,len(lst)) :
                    res = res - lst[x]
                return res
            func = tempfn
        elif peek.token == "*":
            def tempfn(lst):
                res = 1
                for x in lst :
                    res = res * x
                return res
            func = tempfn
        elif peek.token == "/":
            def tempfn(lst):
                res = lst[0]
                for x in range(1,len(lst)) :
                    res = res / lst[x]
                return res
            func = tempfn

        elif peek.get_type() != "IDENTIFIER" :
            if peek.token != "(":
                print("invalid character, no matching syntax rule")
                return
            self.next_token()
            peek = self.peek()
            if peek.token != "lambda":
                print("invalid character, no matching syntax rule")
                return
            self.next_token()
            peek = self.peek()
            if peek.token != "(":
                print("invalid character, no matching syntax rule")
                return
            args = {}
            self.next_token()
            peek = self.peek()
            counter = 0
            while peek!= None and peek.token != ")" :
                if type(peek.token) != str:
                    return "invalid identifier"
                args[peek.token] = counter
                self.next_token()
                peek= self.peek()
                counter = counter + 1
            if peek.token != ")":
                return "no matching syntax rule"
            self.next_token()
            peek = self.peek()
            if peek == None or peek.token != "(" :
                return "syntax rule"
            self.next_token()
            peek = self.peek()
            foo = []
            counter = 1
            while peek != None :
                check = self.names.get(peek.token,"NONE")
                if check == "NONE" or args.get(peek.token , "NONE") != "NONE":
                    foo.append(peek)
                else :
                    tok = self.args[self.names.get(peek.token)]
                    temptoken =  None
                    if type(tok) != list:
                        temptoken = Tokens(str(tok))
                        temptoken.get_type()
                        foo.append(temptoken)
                    else :
                        temptoken = "'("
                        for tempelem in tok :
                            temptoken = temptoken + str(tempelem)
                        temptoken = temptoken + ")"
                        for elem in temptoken:
                            tempStr = Tokens(elem)
                            tempStr.get_type()
                            foo.append(tempStr)
                if peek.get_type() == "CLOSE_PAREN" :
                    counter = counter - 1
                    if counter == 0 :
                        break
                if peek.token == "(":
                    counter = counter + 1
                self.next_token()
                peek = self.peek()
            if peek.get_type() != "CLOSE_PAREN":
                return "No matching syntax rule"
            def tempFunc(lst):
                proc = Procedure(foo, args, lst, self.data)
                return proc.parse_expression()
            func = tempFunc
            peek = self.peek()
            if peek.token != ")" :
                print("No matching syntax rule")
                return
        
        self.next_token()
        peek = self.peek()
        lst = None
        if(peek.token == ")"):
            self.next_token()
            peek = self.peek()
        if peek.get_type() == "IDENTIFIER":
            lst= self.getArgs()
        elif peek.token == "(":
            lst = self.getArgs()
        else :
            print("invalid identifer")
        size = len(lst[0])
        for tmpList in lst :
            if len(tmpList) != size :
                print("lists must have equal lengths")
                return
        result = []
        for x in range(0,size):
            tempppp = []
            for elem in lst:
                tempppp.append(elem[x])
            result.append(func(tempppp))
        self.next_token()
        return result
        
    
    def parse_if_cond(self, data, flag):
        peek = self.peek()
        first = None
        if peek.get_type() == "NUMBER":
            first = self.getNumber(peek.token)
            self.next_token()
            peek = self.peek()
        elif peek.get_type() == "OPEN_PAREN" :
            self.next_token()
            first = self.parse_expression(data)
            peek = self.peek()
        elif peek.get_type() == "IDENTIFIER" :
            elem = self.args[self.names.get(peek.token)]
            if elem == None :
                print("invalid identifier")
                return
            first = elem
            self.next_token()
            peek = self.peek()
        else:
            print("syntax error")
            return
        return first

    def parse_fullCond(self,data,flag):
        peek = self.peek()
        if peek.token != "(" :
            print("unexpected token, open parenthesis expected")
            return
        self.next_token()
        return self.parse_expression()
        
    def parse_null(self):
        peek = self.peek()
        if peek.token != "?":
            print("syntax rule violation")
            return
        self.next_token()
        peek = self.peek()
        temp = None
        if peek.get_type() == "IDENTIFIER":
            self.next_token()
            temp = self.args[self.names.get(peek.token)]
            self.next_token()
        elif peek.token == "(":
            self.next_token()
            temp = self.parse_expression()
        else:
            print("invalid type of arguments")
            return
        if temp == None :
            print("expected 1 argument , got 0")
            return
        if type(temp) == list and len(temp)== 0 :
            return True
        self.next_token()
        return False


    # Funtion bellow is called with if conditions

    def tmpIf(self):
        peek = self.peek()
        ifbody = None
        if peek.get_type() == "IDENTIFIER" :
            ifbody = self.args[self.names.get(peek.token)]
            self.next_token()
            peek = self.peek()
            temp = peek
        elif peek.get_type() == "NUMBER" :
                ifbody = self.getNumber(peek.token)
                self.next_token()
                peek = self.peek()
        elif peek.token == "'":
            self.next_token()
            self.next_token()
            ifbody = self.par_list()
            peek = self.peek()
        else :
            if peek.token == "(":
                self.next_token()
                peek = self.peek()
                ifbody = self.parse_expression()
                peek = self.peek()
            else:
                print("no matching syntax rule")
                return 0
            peek = self.peek()
        return ifbody

    def parse_if(self,data,flag):

        tempCheck = self.parse_fullCond(data,flag)
        if tempCheck:
            return self.tmpIf()
        else :
            peek = self.peek()
            flag = True
            if peek.token == "(" :
                self.next_token()
                peek = self.peek()
                flag = False
            elif peek.token == "'":
                self.next_token()
                self.next_token()
                peek = self.peek()
                flag = False
            # Skip first return expression
            c = 1
            while (peek.token != ")" or c != 1) and not(flag) :
                if peek.token == "(" :
                    c = c+1
                elif peek.token == ")":
                    c = c - 1
                self.next_token()
                peek = self.peek()
            self.next_token()
            peek = self.peek()
            return self.tmpIf()

    def parse_append(self):

        peek = self.peek()
        if peek == None :

            print("unexpected token")
            return
        ls = []
        # Getting first list
        if peek.token == "(" :
            self.next_token()
            peek = self.peek()
            ls = self.parse_expression()
        elif peek.token == "'" :
            self.next_token()
            self.next_token()
            ls = self.par_list()
        elif peek.get_type() == "IDENTIFIER" :
            elem = self.args[self.names.get(peek.token)]
            if type(elem) != list :
                print("invalid type of element")
                return
            ls = elem
            self.next_token() 
        else :
            print("unexpected token")
            return
        peek = self.peek()
        if peek == None :
            print("unexpected token")
            return
        ls2 = []
        # getting second list
        if peek.token == "(" :
            self.next_token()
            peek = self.peek()
            ls2 = self.parse_expression()
        elif peek.token == "'" :
            self.next_token()
            self.next_token()
            ls2 = self.par_list()
        elif peek.get_type() == "IDENTIFIER" :
            elem = self.args[self.names.get(peek.token)]
            if type(elem) != list :
                print("invalid type of element")
                return
            ls2 = elem
            self.next_token() 
        else :
            print("unexpected token")
            return
        ls.extend(ls2)
        self.next_token()
        return ls

    def parse_cdr(self):
        peek = self.peek()
        if peek == None :
            print("unexpected token")
            return
        ls = []
        if peek.token == "(" :
            self.next_token()
            peek = self.peek()
            ls = self.parse_expression()
        elif peek.token == "'" :
            self.next_token()
            ls = self.par_list()
            ls = ls[0]
        elif peek.get_type() == "IDENTIFIER" :
            elem = self.args[self.names.get(peek.token)]
            if type(elem) != list :
                print("invalid type of element")
                return
            ls = elem
            self.next_token()
            peek = self.peek() 
        else :
            print("unexpected token")
            return
        self.next_token()
        return ls[1:]




    def parse_car(self):
        peek = self.peek()
        if peek == None :
            print("unexpected token")
            return
        ls = []
        if peek.token == "(" :
            self.next_token()
            peek = self.peek()
            ls = self.parse_expression()
        elif peek.token == "'" :
            self.next_token()
            ls = self.par_list()[0]

        elif peek.get_type() == "IDENTIFIER" :
            elem = self.args[self.names.get(peek.token)]
            if type(elem) != list :
                print("invalid type of element")
                return
            ls = elem
            self.next_token()
            self.next_token()
            peek = self.peek()
            return ls[0] 
        else :
            print("unexpected token")
            return   
        res = ls[0]
        return res

    def parse_cons(self):
        peek = self.peek()
        if peek == None : 
            print("unexpected token")
            return
        elem = None
        if peek.token == "(":
            self.next_token()
            peek = self.peek()
            elem = self.parse_expression()
        elif peek.get_type() == "NUMBER":
            elem  = self.getNumber(peek.token)
            self.next_token()
        elif peek.get_type() == "IDENTIFIER" :
            elem  = self.args[self.names.get(peek.token)]
            self.next_token()
        else :
            return
        peek = self.peek()
        if not(isinstance(elem, NUMBER)):
            return
        if peek == None :
            print("unexpected token")
            return
        ls = []
        if peek.token == "(" :
            self.next_token()
            ls = self.parse_expression()
        elif peek.token == "'" :
            self.next_token()
            ls = self.par_list()
            ls = ls[0]
        elif peek.get_type() == "IDENTIFIER" :
            ls = self.args[self.names.get(peek.token)]
            self.next_token() 
        else :
            print("unexpected token")
            return
        
        ls.insert(0, elem)
        self.next_token()
        return ls

    def par_list(self) :
        peek = self.next_token()
        args = []
        if peek == None :
            return "Syntax error"
        
        while peek != None and peek.get_type()!= "CLOSE_PAREN" :
            if peek.get_type () == "OPEN_PAREN" :
                args.append(self.par_list())
            else :
                args.append(self.getNumber(peek.token))
            peek = self.next_token()
        
        return args


    def parseDivision(self,data,p):
        peek = self.peek()
        res = None
        if peek.get_type() == "IDENTIFIER" :
            elem = self.args[self.names.get(peek.token)]
            self.next_token()
            res = elem
        elif peek.token == "(" :
            self.next_token()
            res = self.parse_expression()
        else:
            res = self.getNumber(peek.token)
            self.next_token()
        peek = self.peek()
        temp = 1
        while peek != None and peek.get_type()!="CLOSE_PAREN" :
            if peek.get_type() == "OPEN_PAREN" :
                self.next_token()
                peek = self.peek()
                temp*=self.parse_expression(data,False)
                peek = self.peek()
            elif peek.get_type() == "NUMBER":    
                temp *= self.getNumber(peek.token)
                self.next_token() 
                peek = self.peek()
            elif peek.get_type() == "IDENTIFIER" :
                elem = self.args[self.names.get(peek.token)]
                temp *=  self.getNumber(elem)
                self.next_token() 
                peek = self.peek()
            else :
                print("no matching syntax rule")
                return
        self.next_token()
        return res/temp

    def parseMulti(self,data,p):
        peek = self.peek()
        res = 1
        while peek != None and peek.get_type()!="CLOSE_PAREN" :
            if peek.get_type() == "OPEN_PAREN" :
                self.next_token()
                peek = self.peek()
                res*=self.parse_expression(data,False)
                peek = self.peek()
            elif peek.get_type() == "NUMBER":
                res *= self.getNumber(peek.token)
                self.next_token() 
                peek = self.peek()
            elif peek.get_type() == "IDENTIFIER" :
                elem = self.args[self.names.get(peek.token)]
                res *=  self.getNumber(elem)
                self.next_token() 
                peek = self.peek()
            else :
                print("no matching syntax rule")
                return
        self.next_token()
        return res

    
    def parseNegattion(self,data,p):
        peek = self.peek()
        if peek.get_type() == "IDENTIFIER" :
            elem = self.args[self.names.get(peek.token)]
            res = elem
        elif peek.token == "(" :
            self.next_token()
            res = self.parse_expression()
        else:
            res = self.getNumber(peek.token)
        self.next_token()
        peek = self.peek()
        while peek != None and peek.get_type()!="CLOSE_PAREN" :
            if peek.get_type() == "OPEN_PAREN" :
                self.next_token()
                peek = self.peek()
                res-=self.parse_expression(data,False)
                peek = self.peek()
            elif peek.get_type() == "NUMBER":
                res -= self.getNumber(peek.token)
                self.next_token() 
                peek = self.peek()
            elif peek.get_type() == "IDENTIFIER" :
                elem = self.args[self.names.get(peek.token)]
                res -=  self.getNumber(elem)
                self.next_token() 
                peek = self.peek()
            else :
                print("no matching syntax rule")
                return 0
        self.next_token()
        return res

    def parseAddition(self,data,p):
        t = 0
        peek = self.peek()
        counter = 1
        while peek != None and peek.get_type()!="CLOSE_PAREN" :
            if peek.get_type() == "OPEN_PAREN" :
                counter =  counter + 1
                self.next_token()
                peek = self.peek()
                t+= self.parse_expression(data)
                peek = self.peek()
            elif peek.get_type() == "NUMBER":
                t += self.getNumber(peek.token)
                self.next_token() 
                peek = self.peek()
            elif peek.get_type() == "IDENTIFIER" :
                elem = self.args[self.names.get(peek.token)]
                t +=  self.getNumber(elem)
                self.next_token()
                peek = self.peek() 
            if peek != None and peek.get_type() =="CLOSE_PAREN":
                counter = counter - 1
                if counter != 0:
                    self.next_token()
                    peek = self.peek()
        self.next_token()
        return t
