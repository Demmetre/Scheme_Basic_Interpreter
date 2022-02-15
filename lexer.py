
import re
import sys
from tokens import Tokens


class Lexer_S:

    def __init__(self,filePath=None):
        self.regString = "\(|\)|[a-zA-Z]\w*|-?\d+\.?\d*|\?|>=|=|<=|>|<|'|\.|\+|\-|/|\*|equal|#t|#f|define|map|lambda|and|or|else|if|eval|append|apply|length|null|cdr|car|cons"
        self.path = filePath
        self.result = []
    def lex(self,text):
        sourceFile = None
        if self.path != None :
            try:
                sourceFile = open(self.path,"r")
            except IOError:
                print("File couldn't be found")
                exit(1)
        else : 
            sourceFile = text
        tempRes = []
        if self.path != None :
            for newLine in sourceFile.readlines():
                tempRes.extend(re.findall(self.regString, newLine))
        else : 
            tempRes.extend(re.findall(self.regString, sourceFile))
        for elem in tempRes:
            last = Tokens(elem)
            last.get_type()
            self.result.append(last)
           
        if self.path != None :
            sourceFile.close()
        
        return self.result