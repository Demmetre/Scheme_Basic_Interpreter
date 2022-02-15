
import sys
from lexer import Lexer_S
from mainGen import Generator

def printLex(tok):
    for tok in tok:
        print(tok.token + " " + " type : " + tok.get_type())


def tokenize(chars: str) -> list:
    temp = "'"
    result = chars
    if temp[0] == chars[0]:
        x = chars[1:chars.__len__()]
        result = "(quote"+x+")"
    return result.replace('(', ' ( ').replace(')', ' ) ').split()

def checkBraces(s):
    temp = tokenize(s)
    stack = []
    counter = len(temp) 
    for i in temp:
        if i == '(':
            stack.append(i)
        elif i == ')':
            curr = stack.pop()
            if curr != '(':
                print("syntax error")
                return False
        counter = counter - 1
        if stack.__len__() == 0 and counter != 0:
            print("syntax error")
            return False
    if stack.__len__() != 0:
        print("syntax error")
        return False
    return True 

def fun():
    print("Welcome to scheme,(ctrl+D) to exit")
    counter = 0
    data = {}
    while True:
        counter = counter +1
        s = input('Line ' +str(counter) + ' in My_Scheme : ')
        if not(checkBraces(s)) :
            continue
        lex = Lexer_S()
        tok=lex.lex(s)
        result = Generator(iter(tok))
        res = result.printResult(data)
        if res != "success" :
            print(res)
            

fun()












