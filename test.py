from math import factorial

class Calculator():
    DEFAULT     = 0
    EQUALITY    = 1
    INEQUALITY  = 2


    @staticmethod
    def calc(str):
        str = str.replace("^", "**")
        str = str.replace("=", "==")
        str = str.replace("<==", "<=")
        str = str.replace(">==", ">=")

        mode = Calculator.DEFAULT
        for char in str:
            if char in ["<", ">", "="]:
                mode = Calculator.INEQUALITY
                break
            elif char in ["+", "-", "/", "*", "^", "!"]:
                mode = Calculator.EQUALITY

        while (str.find("!") != -1):
            findex = str.find("!")
            ans, start, stop = Calculator.replaceFactorial(str[:findex+1], findex)
            str = str.replace(str[start:stop]+"!", "factorial("+ans+")")

        return eval(str), mode


    @staticmethod
    def replaceFactorial(str, findex):
        newStr = ""
        bracket = 0
        pointer = findex-1

        while True:
            char = str[pointer]
            if char == ")":
                bracket += 1
                newStr = char + newStr
                pointer -= 1
            elif char == "(" and bracket > 1:
                bracket -= 1
                newStr = char + newStr
                pointer -= 1
            elif char == "(" and bracket == 1:
                newStr = char + newStr
                pointer -= 1
                break
            elif (char.isdigit()) or (not char.isdigit() and bracket != 0):
                newStr = char + newStr
                pointer -= 1
            else:
                break
        return [newStr, pointer+1, findex]

string = "5!"

ans, mode = Calculator.calc(string)
if mode == Calculator.DEFAULT:
    print(string)
elif mode == Calculator.EQUALITY:
    print(string+" = "+str(ans))
elif mode == Calculator.INEQUALITY:
    print(string+" is "+str(ans))
