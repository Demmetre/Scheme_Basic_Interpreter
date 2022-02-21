
import math
import re
import sys
from itertools import chain, tee
import operator as op
from lexer import Lexer_S
from build import Procedure
from tokens import Tokens

NUMBER = (int,float)

lexicon = {
    "CAR" : lambda x : x[0],
    "CDR" : lambda x : x[1:],
    "CONS" : lambda x,y : list(y).insert(0,x),
    "APPEND" : lambda x,y : list(y).extend(list(x))
}

class Generator:

    def __init__(self,it):
        self.it = it 
    

    def next_token(self):
        try:
            temp = next(self.it)
            return temp
        except StopIteration:
            return None

    def peek(self):
        try:
            temp = self.next_token()
            self.it = iter(list(chain([temp], self.it)))
            return temp
        except StopIteration:
            return None


    # returns list of arguments, when the function is called

    def getArgs(self,data) :
        res = []
        peek = self.peek()
        while peek!= None and peek.get_type() != "CLOSE_PAREN" :
            if peek.token == "(":
                self.next_token()
                temp = self.parse_expression(data)
                self.next_token()
                res.append(temp)
            elif peek.get_type() == "IDENTIFIER":
                temp = data.get(peek.token,"NONE")
                if temp == "NONE" :
                    print("warning, no declaration seen for" + peek.token)
                    return
                res.append(temp[0])
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
    

    
    def parse_expression(self,data,flag = True):
        next_token = self.next_token()
        if next_token == None :
            return "No matching syntax rule"
        if next_token.get_type() == "NUMBER" :
            return "invalid type of expression -> " + next_token.token + " is a number"
        elif next_token.token == "cond":
            res = self.parse_cond(data)
            self.next_token()
            return res
        elif next_token.get_type() == "IDENTIFIER" :
            if data.get(next_token.token,"NONE") == "NONE"  :
                return "No matching syntax rule, no declaration seen for " + next_token.token
            args = self.getArgs(data)
            func = data[next_token.token]
            tempRes = func(args)
            return tempRes
        elif next_token.get_type() == "DEFINE" :
            peek =  self.peek()
            if peek == None or peek.get_type() == "NUMBER":
                return "No matching syntax rule"
            elif peek.get_type() == "IDENTIFIER":
                name = self.next_token()
                p = self.peek()
                if p == None :
                    return "No matching syntax rule" 
                if p.get_type() == "NUMBER" :
                    self.next_token()
                    tem = self.peek()
                    if tem == None or tem.get_type() != "CLOSE_PAREN" :
                        return "No matching syntax rule"
                    else :
                        self.next_token()
                        if self.peek() != None :
                            return "No matching syntax rule"
                        else:
                            data[name.token] = self.getNumber(p.token)
                            return "success"
                elif  p.get_type() == "QUOTE":
                    self.next_token()
                    data[name.token] = self.par_list()
                    return "success"
                elif p.get_type() == "OPEN_PAREN":
                    self.next_token()
                    p = self.peek()
                    if p.token=="lambda":
                        self.parse_lambda_func(name.token, data)
                        return "success"
                    else :
                        return "no matching syntax rule"
                else:
                    return "No matching syntax rule "
            elif peek.get_type() == "OPEN_PAREN" :
                self.parseFunctionDefine(data)
                return "success"
            else:    
                return "No matching syntax rule "
            return  0
        elif next_token.get_type() == "OPEN_PAREN" :
            peek = self.peek()
            if peek.token == "(" :
                func = self.parse_expression(data)
                self.next_token()
                peek = self.peek()
                args = self.getArgs(data)
                return func(args)
            if peek.token != "lambda":
                return "invalid identifier"
            tempfunc = self.parse_lambda_func("name", data,False)
            peek = self.peek()
            if peek.token != ")":
                return "no matching syntax rule"
            self.next_token()
            peek = self.peek()
            arglst= self.getArgs(data)
            return tempfunc(arglst)
        elif next_token.get_type() == "PLUS" :
            ress = self.parseAddition(data,(flag))
            return ress
        elif next_token.get_type() == "MINUS" :
            ress = self.parseNegattion(data,(flag))
            return ress
        elif next_token.get_type() == "MULTI" :
            ress =  self.parseMulti(data,(flag))
            return ress
        elif next_token.get_type() == "DIVISION" :
            ress =  self.parseDivision(data,(flag))
            return ress
        elif next_token.get_type() == "CAR" :
            res =  self.parse_car(data)
            return res
        elif next_token.get_type() == "CONS" :
            res =  self.parse_cons(data)
            return res
        elif next_token.get_type() == "CDR" :
            res =  self.parse_cdr(data)
            return res
        elif next_token.get_type() == "APPEND" :
            res=  self.parse_append(data) 
            return res
        elif next_token.get_type() == "MAP" :
            res=  self.parse_map(data) 
            return res
        elif next_token.token == "null":
            return self.parse_null(data)    
        elif next_token.token == "length":
            pl = self.peek()
            temp = self.printResult(data,True)
            if temp == None or type(temp) != list:
                return "invalid parameter"
            return len(temp)
        elif next_token.token == "apply" :
            res =  self.parse_apply(data)
            return res
        elif next_token.token == "eval":
            lst = []
            peek = self.next_token()
            while peek != None :
                lst.append(peek)
                peek=self.next_token()
            lst.pop()
            self.it = iter(lst)
            return self.printResult(data)
        elif next_token.token == "and" :
            first = self.printResult(data)
            second = self.printResult(data)
            return first and second
        elif next_token.token == "or" :
            first = self.printResult(data)
            second = self.printResult(data)
            return first or second
        elif next_token.token == ">" :
            x,y = self.relation(data)
            return x>y
        elif next_token.token == "<" :
            x,y = self.relation(data)
            return x < y
        elif next_token.token == ">=" :
            x,y = self.relation(data)
            return x >= y
        elif next_token.token == "<=" :
            x,y = self.relation(data)
            return x <= y
        elif next_token.token == "=" :
            x,y = self.relation(data)
            return x == y
        elif next_token.token == "if" :
            check = self.printResult(data)
            peek = self.peek()
            x=None
            if peek.get_type() == "NUMBER" :
                x = self.getNumber(peek.token)
                self.next_token()
            else :
                x = self.printResult(data)
            peek = self.peek()
            if peek.get_type() == "NUMBER" :
                y = self.getNumber(peek.token)
                self.next_token()
            else :
                y = self.printResult(data)
            if check :
                return x
            return y  
        return 0

    def parse_cond(self,data):
        peek = self.peek()
        while peek.token != ")":
            peek = self.peek()
            if peek.token != "(":
                return "unexpected token"
            self.next_token()
            peek = self.peek()
            if peek.get_type() == "NUMBER" :
                check = self.getNumber(peek.token)
                return check
            elif peek.get_type() == "IDENTIFIER" :
                check = data.get(peek.token)
                return check
            if peek.token != "(":
                return "unexpected token"
            self.next_token()
            check = self.parse_expression(data)
            self.next_token()
            peek = self.peek()
            res = None
            if peek.get_type() == "NUMBER" :
                res = self.getNumber(peek.token)
            elif peek.get_type() == "IDENTIFIER" :
                res = data.get(peek.token)
            elif peek.token == "(" :
                self.next_token()
                res = self.parse_expression(data)
            self.next_token()
            self.next_token()
            peek = self.peek()
            if res == None:
                return check
            if check :
                return res

    def relation(self,data):
        peek = self.peek()
        first = None
        second = None
        if peek.get_type() == "NUMBER":
            first = self.getNumber(peek.token)
            self.next_token()
        elif peek.get_type() == "IDENTIFIER" :
            first = data[peek.token]
            self.next_token()
        elif peek.token == "(":
            self.next_token()
            first = self.parse_expression(data)
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
            second = data[peek.token]
            self.next_token()
        elif peek.token == "(":
            self.next_token()
            second = self.parse_expression(data)
        else :
            return "invalid type of exression"
        if not(isinstance(second,NUMBER)):
            return "number expected , got other"
        return first,second     


    def getOp(self,ope,x , y,data):
        if ope.token == "min" :
            return min(x, y)
        if ope.token == "max":
            return max(x,y)
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
            func = data.get(ope.token,"None")
            if func == "None":
                return "invalid function"
            tss = [x ,y]
            return func(tss)
        return "invalid type"
            
    def parse_apply(self,data):
        peek = self.peek()
        operator = peek
        self.next_token()
        lst = self.printResult(data,True)
        size =lst.__len__()
        if size == 0 :
            return None
        result = []
        curr = lst[0]
        for index in range(1,size ) :
            curr = self.getOp(operator,curr,lst[index],data)
        return curr

    def parse_null(self,data):
        peek = self.peek()
        if peek.token != "?":
            return "unexcpected character"
        self.next_token()
        peek = self.peek()
        temp = None
        if peek.token == "'":
            self.next_token()
            temp = self.par_list()[0]
        elif peek.token == "(":
            self.next_token()
            temp = self.parse_expression(data,False)
        elif peek.get_type() == "NUMBER" :
            temp = self.getNumber(peek.token)
            self.next_token()
            peek = self.peek()
            if peek == None or peek.token != ")":
                return "syntax error"
        else:
            return "invalid type of arguments"
        if temp == None :
            return "expected 1 argument , got 0"
        if type(temp) == list and len(temp)== 0 :
            return True
        return False

    def parse_map(self,data):
        peek = self.peek()
        args = []
        result = []
        tempfunc = None
        if peek == None :
            return "unexpected token"
        if peek.get_type() ==  "IDENTIFIER" :
            func  = data[peek.token]
            if func == None :
                return "warning, no declaration seen for" + peek.token
            self.next_token()
            args = self.getArgs(data)
            tempfunc = func
        elif peek.token == "+":
            self.next_token()
            args = self.getArgs(data)
            def tempfn(lst):
                res = 0
                for x in lst :
                    res = res + x
                return res
            tempfunc = tempfn
        elif peek.token == "-":
            self.next_token()
            args = self.getArgs(data)
            def tempfn(lst):
                res = lst[0]
                for x in range(1,len(lst)) :
                    res = res - lst[x]
                return res
            tempfunc = tempfn
        elif peek.token == "*":
            self.next_token()
            args = self.getArgs(data)
            def tempfn(lst):
                res = 1
                for x in lst :
                    res = res * x
                return res
            tempfunc = tempfn
        elif peek.token == "/":
            self.next_token()
            args = self.getArgs(data)
            def tempfn(lst):
                res = lst[0]
                for x in range(1,len(lst)) :
                    res = res / lst[x]
                return res
            tempfunc = tempfn              
        else :
            self.next_token()
            peek = self.peek()
            if  peek.get_type() == "LAMBDA" :
                tempfunc = self.parse_lambda_func("random",data,False)
                peek = self.peek()
                if peek.token != ")":
                    return "no matching syntax rule"
                # self.next_token()
                peek = self.peek()
                if peek.token != ")":
                    return "no matching syntax rule"
                self.next_token()
                peek = self.peek()
                args = self.getArgs(data)

        size = len(args[0])
        for tmpList in args :
            if len(tmpList) != size :
                print("lists must have equal lengths")
                return
        for x in range(0,size):
            tempppp = []
            for elem in args:
                tempppp.append(elem[x])
            result.append(tempfunc(tempppp))
        return result
            
        

    def parse_append(self,data):
        peek = self.peek()
        if peek == None :
            return "unexpected token"
        ls = []
        if peek.token == "(" :
            self.next_token()
            peek = self.peek()
            ls = self.parse_expression(data)
        elif peek.get_type() == "IDENTIFIER" :
            t  = data.get(peek.token,"NONE")
            if t == "NONE" or type(t) != list :
                return "can not make a car operation"
            ls = t[0]
            self.next_token()
        elif peek.token == "'" :
            self.next_token()
            self.next_token()
            ls = self.par_list()
        
        else :
            return "unexpected token"
        peek = self.peek()
        if peek == None :
            return "unexpected token"
        ls2 = []
        if peek.token == "(" :
            self.next_token()
            peek = self.peek()
            ls2 = self.parse_expression(data)
        elif peek.token == "'" :
            self.next_token()
            self.next_token()
            ls2 = self.par_list()
        elif peek.get_type() == "IDENTIFIER" :
            t  = data.get(peek.token,"NONE")
            if t == "NONE" or type(t) != list :
                return "can not make a car operation"
            ls2 = t[0]
            self.next_token()
        else :
            return "unexpected token"
        ls.extend(ls2)
        return ls

    def parse_cdr(self,data):
        peek = self.peek()
        if peek == None :
            return "unexpected token"
        ls = []
        if peek.token == "(" :
            self.next_token()
            peek = self.peek()
            ls = self.parse_expression(data)
        elif peek.token == "'" :
            self.next_token()
            ls = self.par_list()
            ls = ls[0]
        elif peek.get_type() == "IDENTIFIER" :
            t  = data.get(peek.token,"NONE")
            if t == "NONE" or type(t) != list :
                return "can not make a car operation"
            ls = t[0]
            self.next_token()
        else :
            return "unexpected token"
        self.next_token()
        return ls[1:]



    def parse_car(self,data):
        peek = self.peek()
        if peek == None :
            return "unexpected token"
        ls = []
        if peek.token == "(" :
            self.next_token()
            ls = self.parse_expression(data,False)
        elif peek.token == "'" :
            self.next_token()
            ls = self.par_list()[0]
        elif peek.get_type() == "IDENTIFIER" :
            t  = data.get(peek.token,"NONE")[0]
            if t == "NONE" or type(t) != list :
                return "can not make a car operation"
            ls = t
            self.next_token()
            self.next_token()
        else :
            return "unexpected token"
            
        res = ls[0]
        return res

    def getNumber(self,token):
        try :
            return int(token)
        except :
            try:
                return float(token)
            except:
                return token

    def parse_cons(self,data):
        peek = self.peek()
        elem =None
        if peek == None : 
            return "unexpected token"
        elif peek.token == "(":
            self.next_token()
            elem = self.parse_expression(data)
        elif peek.get_type() == "IDENTIFIER" :
            elem = data.get(peek.token,"NONE")
        elif peek.get_type() == "NUMBER":
            elem  = self.getNumber(peek.token)
        else :
            return "number expected,got list"
        
        self.next_token() 
        peek = self.peek()
        if peek == None :
            return "unexpected token"
        ls = []
        if peek.token == "(" :
            self.next_token()
            peek = self.peek()
            ls = self.parse_expression(data)
        elif peek.token == "'" :
            self.next_token()
            ls = self.par_list()
            ls = ls[0]
        elif peek.get_type() == "IDENTIFIER" :
            temp = data.get(peek.token,"NONE")
            if temp == "NONE" or type(temp)!=list:
                return "no matching arguments, list expected"
            ls = temp[0]
            self.next_token()
        else :
            return "unexpected token"
        ls.insert(0, elem) 
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


    def parse_lambda_func(self, name, funcs,flag = True):
        self.next_token()
        peek = self.peek()
        if peek == None or peek.get_type() != "OPEN_PAREN" :
            return "syntax rule"
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
            foo.append(peek)
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
            proc = Procedure(foo, args, lst,funcs)
            return proc.parse_expression()
        self.next_token()
        if flag :
            funcs[name] = tempFunc
        else:
            return tempFunc

        
    def parseFunctionDefine(self,funcs):
        self.next_token()
        name = self.next_token().token
        argList = {}
        counter = 0
        peek = self.peek()
        while peek != None and peek.get_type() != "CLOSE_PAREN":
            argList[peek.token] = counter
            counter = counter + 1
            self.next_token()
            peek = self.peek()
        self.next_token()
        peek = self.next_token()
        if peek ==  None or peek.get_type() != "OPEN_PAREN" :
            return "No matching syntax rule"
        peek = self.peek()
        foo = []
        counter = 1
        while peek != None :
            foo.append(peek)
            if peek.get_type() == "CLOSE_PAREN" :
                counter = counter - 1
                if counter == 0 :
                    break
            if peek.token == "(":
                counter = counter + 1
            self.next_token()
            peek = self.peek() 
        if peek != None and peek.get_type() != "CLOSE_PAREN":
            return "No matching syntax rule"
        def tempFunc(lst):
            proc = Procedure(foo, argList, lst,funcs)
            return proc.parse_expression()
        funcs[name] = tempFunc
      


    def parseDivision(self,data,p):
        peek = self.peek()
        if peek.get_type() == "IDENTIFIER":
            temp = data.get(peek.token,"NONE")
            if temp == "NONE" or not(isinstance(temp, NUMBER)):
                return "syntax error, no declaraion"
            res = temp
        elif peek.get_type() == "OPEN_PAREN":
            self.next_token()
            res = self.parse_expression(data)
        elif peek.get_type()== "NUMBER":
            res = self.getNumber(peek.token)
        self.next_token()
        peek = self.peek()
        temp = 1
        while peek != None and peek.get_type()!="CLOSE_PAREN" :
            if peek.get_type() == "OPEN_PAREN" :
                self.next_token()
                peek = self.peek()
                temp*=self.parse_expression(data,True)
                self.next_token()
                peek = self.peek()
            elif peek.get_type() == "NUMBER":    
                temp *= self.getNumber(peek.token)
                self.next_token() 
                peek = self.peek()
            elif peek.get_type() == "IDENTIFIER":
                tem = data.get(peek.token,"NONE")
                if temp == "NONE" or not(isinstance(temp, NUMBER)):
                    return "syntax error, no declaraion"
                temp*= tem
                self.next_token()
                peek = self.peek()
            else :
                return "no matching syntax rule"
        return res/temp

    def parseMulti(self,data,p):
        peek = self.peek()
        res = 1
        while peek != None and peek.get_type()!="CLOSE_PAREN" :
            if peek.get_type() == "OPEN_PAREN" :
                self.next_token()
                peek = self.peek()
                res*=self.parse_expression(data,True)
                self.next_token()
                peek = self.peek()
            elif peek.get_type() == "NUMBER":
                res *= self.getNumber(peek.token)
                self.next_token() 
                peek = self.peek()
            elif peek.get_type() == "IDENTIFIER":
                temp = data.get(peek.token,"NONE")
                if temp == "NONE" or not(isinstance(temp, NUMBER)):
                    return "syntax error, no declaraion"
                res*= temp
                self.next_token()
                peek = self.peek()
            else :
                return "no matching syntax rule"
        return res

    
    def parseNegattion(self,data,p):
        peek = self.peek()
        if peek.get_type() == "IDENTIFIER":
            temp = data.get(peek.token,"NONE")
            if temp == "NONE" or not(isinstance(temp, NUMBER)):
                return "syntax error, no declaraion"
            res = temp
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
                res-=self.parse_expression(data,True)
                self.next_token()
                peek = self.peek()
            elif peek.get_type() == "NUMBER":
                res -= self.getNumber(peek.token)
                self.next_token() 
                peek = self.peek()
            elif peek.get_type() == "IDENTIFIER":
                temp = data.get(peek.token,"NONE")
                if temp == "NONE" or not(isinstance(temp, NUMBER)):
                    return "syntax error, no declaraion"
                res-= temp
                self.next_token()
                peek = self.peek()
            else :
                return "no matching syntax rule"
        return res



    def parseAddition(self,data,p):
        t = 0
        peek = self.peek()
        while peek != None and peek.get_type()!="CLOSE_PAREN" :
            if peek.get_type() == "OPEN_PAREN" :
                self.next_token()
                peek = self.peek()
                t+=self.parse_expression(data,True)
                self.next_token()
                peek = self.peek()
            elif peek.get_type() == "NUMBER":
                t += self.getNumber(peek.token)
                self.next_token() 
                peek = self.peek()
            elif peek.get_type() == "IDENTIFIER":
                temp = data.get(peek.token,"NONE")
                if temp == "NONE" or not(isinstance(temp, NUMBER)):
                    return "syntax error, no declaraion"
                t+= temp
                self.next_token()
                peek = self.peek()
            if peek != None and peek.get_type() =="CLOSE_PAREN" :
                self.next_token()
                peek = self.peek()

        return t
        


    def printResult(self,funcNums,flag = False):
        current = self.next_token()
        if current == None :
            return
        peek = self.peek()
        if current.get_type() == "NUMBER" :
            if peek == None :
                return current.token
            else :
                if peek.get_type() == "DIVISION" :
                    self.next_token()
                    peekk = self.peek()
                    if peekk == None : 
                        return "warning - no declaration seen for : " + current.token + "/" 
                    if peekk.get_type() != "NUMBER" :
                        return "warning - no declaration seen for : " + current.token + "/"+ peekk.token
                        
                    self.next_token()
                    cu = self.next_token()
                    if cu != None :
                        return "warning - no declaration seen for : " + cu.token
                    a = self.getNumber(current.token)
                    b = self.getNumber(peekk.token)
                    t = math.gcd(a, b)
                    if(t == b) :
                        return str(int(a/t))
                    else  : 
                        return str(int(a/t)) + "/" + str(int(b/t))
                else :
                    return "no matching syntax rule"
        elif current.get_type() == "QUOTE" :
            if peek == None:
                return "invalid dispatch character '"
            elif peek.get_type() == "OPEN_PAREN":
                self.next_token()
                result = self.par_list()
                return result
            else :
                t = self.next_token()
                c = self.peek()
                if c != None :
                    return "warning - no declaration seen for " + c.token   
        elif current.get_type() == "IDENTIFIER" :
            temp  = funcNums.get(current.token,"NONE")
            if temp == "NONE" :
                return "warning - no declaration seen for " + current.token
            t = funcNums.get(current.token)
            if isinstance(t, NUMBER) :
                return t
            elif type(t[0]) == list  :
                return t[0]
            else:
                return "<procedure " + current.token+">"
        elif current.get_type() == "OPEN_PAREN":
            rees = self.parse_expression(funcNums,flag)
            self.next_token()
            return rees
        elif current.get_type() == "FALSE":
            return "#f"
        elif current.get_type() == "TRUE":
            return "#t"
        else:
            if current.token == '*':
                return "<procedure *>"
            elif current.token == '+':
                return "<procedure +>"
            elif current.token == '-' :
                return "<procedure ->"
            elif current.token == '/' :
                return "<procedure />"
            else:
                return "warning - no declaration seen for " + current.token
        
        return 0
