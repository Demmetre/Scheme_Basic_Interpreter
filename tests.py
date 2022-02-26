
import sys
from lexer import Lexer_S
from mainGen import Generator

testsDict = {}

# Functions below are for testing
# You can add new tests or try online input




def testsOnlyNums():
    testsDict["5"] = 5
    testsDict["-2.1"] = -2.1
    testsDict["12/2"] = "6"
    testsDict["12/8"] = "3/2"
    testsDict["-19/13"] = "-19/13"
    testsDict["(+ 5 6)"] = 11
    testsDict["(- 9 -6.5)"] = 15.5
    testsDict["(* -9 6)"] = -54
    testsDict["(/ 24 2)"] = 12
    testsDict["(+ 1 2 3 4 5)"] = 15
    testsDict["(- 15 5 4 3 2 1)"] = 0
    testsDict["(* 1 2 3 4)"] = 24
    testsDict["(/ 24 2 2 3)"] = 2
    testsDict["(+ (* 2 5) (/ (- 8 4) 2) 2)"] = 14
    testsDict["'(1 2 3 4)"] = [1 , 2 ,3 ,4]
    testsDict["'((1 2) (6 9) ())"] = [ [1,2] , [6,9], []]

def testConstants():
    testsDict["(define p 5)"] = "success"
    testsDict["p"] = 5
    testsDict["(define s 3.14)"] = "success"
    testsDict["s"] = 3.14
    testsDict["(define a '(1 2 3))"] = "success"
    testsDict["a"] = [1,2,3]


def testLocalLambdasIncNested():
    testsDict["((lambda (x y) (+ x y)) 1 2)"] = 3
    testsDict["((lambda (x y z) (* (+ x y) (/ z y))) 1 2 6)"] = 9
    testsDict["(((lambda (x y) (lambda (x) (* x y))) 5 6) 10)"] = 60
    testsDict["(((lambda (x y) (lambda (x) (* x y))) 5 6) 10 2)"] = None
    testsDict["((lambda (x y) ((lambda (x y) (* x y)) (+ x y) (- y x))) 4 6)"] = 20
    testsDict["((lambda (x y z) (append x (append (cdr y) z)) ) '(1 2 3) '(1 2 3) '(1 2 3) )"] =[ 1, 2, 3, 2, 3, 1, 2, 3]
    testsDict["((lambda (x) (cdr (apply append x))) '((1 2) (3 4) (5 6)))"] = [2, 3, 4, 5, 6]

def testListFuncs():
    testsDict["(cdr '(1 2 3))"] = [2, 3]
    testsDict["(cons 5 '(6 7 8 9))"] = [5, 6, 7, 8, 9]
    testsDict["(append '(1 2 3) '(4 5))"] = [1, 2, 3, 4, 5]
    testsDict["(car '((-1 0) 1 2 3))"] = [-1, 0]
    testsDict["(map (lambda (x) (* 2 x)) '(1 2 3))"] = [2, 4, 6]
    testsDict["(map + '(1 2 3) '(1 2 3) a)"] = [3, 6, 9]
    testsDict["(map (lambda (x y) (append (cdr x) (cdr y))) '((1 2 3) (3 4 5)) '((1 2 3) (3 4 5)))"] = [[2, 3, 2, 3], [4, 5, 4, 5]]
    testsDict["(map (lambda (x) (if(> x 2) 0 x)) '(1 2 3 4))"] = [1, 2, 0, 0]
    testsDict["(append (cons 1 '(2 3)) (cdr '(3 4 5)))"] = [1, 2, 3, 4, 5]
    testsDict["(map (lambda (x) (* 2 x)) (map (lambda (x) (+ x 1)) '(1 2 3)))"] = [4, 6, 8]
    testsDict["(cadr (map (lambda (x) (apply + x)) '((1 2 3 4) (5 6 7 8)) ))"] = 26

def testLocalFuncs():
    testsDict["(eval (+ 6 6))"] = 12
    testsDict["(apply + '(1 2 3 4))"] = 10
    testsDict["(apply append '((1 2) (3 4) (6)))"] = [1, 2, 3, 4, 6]
    testsDict["(null? '())"] = True
    testsDict["(null? '(1 2))"] = False
    testsDict["(null? (cdr '(1)))"] = True
    testsDict["(length '())"] = 0
    testsDict["(length '(1 2 3 (4 5 6)))"] = 4

def testEasyFuncs():
    testsDict["(define (sum x y) (+ x y))"] = "success"
    testsDict["(sum 5 6)"] = 11
    testsDict["(define foo (lambda (x y) (+ (car x) (car y))))"] = "success"
    testsDict["(foo '(2 9 7) '(3 6 4))"] = 5
    testsDict["(define (contains x y) (> (apply + (map (lambda (y) (if (= x y) 1 0)) y)) 0))"] = "success"
    testsDict["(contains 1 '(1 2 3) )"] = True
    testsDict["(contains 0 '(1 2 3 9) )"] = False
    testsDict["(if (contains 9 '(1 2 3 9)) ((lambda (x y z) (* x y z)) 1 2 3) 1)"] = 6
    testsDict["(define (remove lst num temp) (if (= (car lst) num) (append temp (cdr lst)) (remove (cdr lst) num (cons (car lst) temp))))"] = "success"
    testsDict["(remove '(1 2 2 6) 2 '())"] = [1, 2, 6]
    testsDict["(define (getMin lst) (apply min lst))"] = "success"
    testsDict["(getMin '(2 6 1 9 4))"] = 1
    testsDict["(define (sort lst ) (if (null? lst) '() (cons (getMin lst) (sort (remove lst (getMin lst) '() ) ) ) ) )"] = "success"
    testsDict["(sort '())"] = []
    testsDict["(sort '(2 6 5 1 ))"] = [1, 2, 5, 6]
    testsDict["(sort '(9 -6 5 3 5 2 0 ))"] = [-6, 0, 2, 3, 5, 5, 9]
    testsDict["(define (fib n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2)) ) ) )"] = "success"
    testsDict["(fib 6)"] = 8
    testsDict["(fib 9)"] = 34
    testsDict["(define (filterRange lst x y) (map (lambda (z) (if (and (>= z x) (<= z y)) z 0) ) lst) )"] = "success"
    testsDict["(filterRange '(1 2 3 4 5 6 7 ) 2 5)"] = [0, 2, 3, 4, 5, 0, 0]
    testsDict["(define (filter lst) (cond ((null? lst) '()) ((> (car lst ) 0) (cons (car lst) (filter (cdr lst)))) ((filter (cdr lst))) ))"] = "success"
    testsDict["(filter (filterRange '(1 2 3 4 5 6 7 ) 2 5))"] = [2, 3, 4, 5]
    testsDict["(define (reverse lst) (if (null? lst) '() (append (reverse (cdr lst)) (list (car lst)))))"] = "success"
    testsDict["(reverse '(1 2 3 4))"] = [4, 3 , 2 ,1]
    testsDict["(define (pow x y) (if (= y 0) 1 (* x (pow x (- y 1)))))"] = "success"
    testsDict["(pow 2 4)"] = 16
    testsDict["(define (generateToNum x) (if (= x 0) '() (append (generateToNum (- x 1)) (list x))))"] = "success"
    testsDict["(generateToNum 4)"] = [1, 2, 3, 4]
    testsDict["(define (powersOf x y) (map (lambda (z) (pow x z)) (generateToNum y)))"]= "success"
    testsDict["(powersOf 2 10)"] = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    testsDict["(map sum '(1 2 3) '(1 2 3))"] = [2,4,6]
    testsDict["(define (factorial x) (if (= x 0) 1 (* x (factorial (- x 1)))))"] = "success"
    testsDict["(factorial 4)"] = 24
    testsDict["(factorial 5)"] = 120
    testsDict["(define (sumOfDigits n) (if (= n 0) 0 (+ (mod n 10) (sumOfDigits (/ (- n (mod n 10)) 10)))))"] = "success"
    testsDict["(sumOfDigits 1234)"] = 10
    testsDict["(define (tempFunc a b res)(cond ((null? a) res) ((null? b) res) ((= (car a) (car b)) (tempFunc (cdr a) (cdr b) (cons (car a) res))) ((> (car a) (car b) ) (tempFunc a (cdr b) res)) ((tempFunc (cdr a) b res))))"] = "success"
    testsDict["(define (intersect a b) (reverse (tempFunc a b '())))"] = "success"
    testsDict["(tempFunc '(0 1 2 3 6 9) '(1 2 4 6 11) '() )"] = [6, 2, 1 ]
    testsDict["(intersect '(1 2 3 4 5 6) '(0 2 3 5 7))"] = [2, 3, 5]
    testsDict["(intersect '(1 2 2 2) '(1 1 2 2))"] =  [1, 2 , 2]
    testsDict["(intersect '() '(1 1 2 2))"] =  []
    testsDict["(define (generateSubsets lst) (if (null? lst) '(()) (append (generateSubsets (cdr lst)) (map (lambda (x) (cons (car lst) x)) (generateSubsets (cdr lst))))))"] = "success"
    testsDict["(generateSubsets '(1 2 3))"] = [[], [3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]]
    testsDict["(generateSubsets '(1 2))"] = [[], [2], [1], [1, 2]]
    testsDict["(define (ksubset lst k) (cond  ((> k (length lst)) '()) ((= k 0) '(())) ((append (map (lambda (x) (cons (car lst) x)) (ksubset (cdr lst) (- k 1))) (ksubset (cdr lst) k)))))"] = "success"
    testsDict[" (ksubset '(1 2 3 4) 2) "] = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    testsDict["(define (count n lst) (apply + (map (lambda (x) (if (= x n) 1 0)) lst)))"] = "success"
    testsDict["(count 5 '(1 5 3 4 5))"] = 2
    testsDict["(define (set lst) (cond ((null? lst) '()) ((= 1 (count (car lst) lst)) (cons (car lst) (set (cdr lst)))) ( (set (cdr lst)))))"] = "success"
    testsDict["(set '(1 1 1 2 2 2 3 3 5 6 9 9))"] =  [1, 2, 3, 5, 6, 9]
    testsDict["(define (frequency lst) (map (lambda (x) (list x (count x lst))) (set lst)))"] = "success"
    testsDict["(frequency '(1 2 2 2 3 3 9 9 9 ))"] = [[1, 1], [2, 3], [3, 2], [9, 3]]
    testsDict["(define (multi n elem) (if (= n 0) '() (cons elem (multi (- n 1) elem))))"] = "success"
    testsDict["(multi 3 4)"] = [4, 4, 4]
    testsDict["(define (multiply n lst) (apply append (map (lambda (x) (multi n x)) lst)))"] = "success"
    testsDict["(multiply 2 '(1 2 3 4))"] = [1, 1, 2, 2, 3, 3, 4, 4]
    testsDict["(define (closestnode node) (if (null? (cadr node)) (car node) (+ (car node) (apply min (map closestnode (cadr node))))))"] = "success"
    testsDict["(closestnode '(100 ((76 ()) (-28 ()))))"] = 72
    testsDict["(closestnode '(-60 ((-9 ((-2 ((27 ((-28 ()) (76 ()))) (-52 ((76 ()) (-10 ()))))))) (47 ((-97 ((-45 ((58 ()) (32 ()))) (-74 ((-56 ()) (10 ()))))) (-1 ((-27 ((-38 ()) (-13 ()))))))))))"] = -240


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
    print("Testing My_Scheme :)")
    counter = 0
    data = {}
    testsOnlyNums()
    testConstants()
    testLocalLambdasIncNested()
    testListFuncs()
    testLocalFuncs()
    testEasyFuncs()

    # Segment below prints results of the tests
    # In the case of a successful trial it prints SUCCESS !!!, otherwise FAILED!!!

    for x in testsDict :
        counter = counter +1
        if not(checkBraces(x)) :
            continue
        lex = Lexer_S()
        tok=lex.lex(x)
        result = Generator(iter(tok))
        print("Testing: " + x)
        res = result.printResult(data)
        if res == testsDict[x]:
            print("SUCCESS!!!   Got : " + str(res))
        else:
            print("FAILED!!!   Expected : " + str(testsDict[x]) +  "  Got : " + str(res))
            

fun()