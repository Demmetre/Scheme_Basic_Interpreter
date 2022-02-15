
import re

class Tokens:

    def __init__(self,token):
        self.type = "NONE"
        self.token = token
        self.tok_types = {
            "(": "OPEN_PAREN",
            ")": "CLOSE_PAREN",
            "define":"DEFINE",
            "map":"MAP",
            "lambda" : "LAMBDA",
            "+" : "PLUS",
            "." : "DOT",
            "-" : "MINUS",
            "?" : "QUEST",
            "*" : "MULTI",
            "/" : "DIVISION",
            ">" : "GREATER",
            "<" : "LESS",
            "#f" : "FALSE",
            "#t" : "TRUE",
            "=" : "EQUAL",
            ">=" : "GR_OR_EQUAL",
            "<=" : "LESS_OR_EQUAL",
            "if" : "IF",
            "else" : "ELSE",
            "or" : "OR",
            "and" : "AND",
            "'" : "QUOTE",
            "apply" : "APPLY",
            "eval" : "EVAL",
            "length" : "LENGTH",
            "null" : "NULL",
            "car" : "CAR",
            "append" : "APPEND",
            "cdr" : "CDR",
            "cons" : "CONS",
            "equal" : "EQUAL",
        }
    def get_type(self):
        temp = re.search('-?\d+\.?\d*', self.token)
        if temp != None:
            self.type = "NUMBER"
            return self.type
        self.type = self.tok_types.get(self.token,"UNKNOWN")
        if self.type != "UNKNOWN":
            return self.type
        temp = re.search('[a-zA-Z]\w*', self.token)
        if temp != None:
            self.type = "IDENTIFIER"
            return self.type