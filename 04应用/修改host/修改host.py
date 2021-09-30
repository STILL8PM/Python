import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def add(addStr):
    with open("C:\Windows\System32\drivers\etc\hosts", "a+") as f:
            f.write(addStr+"\n")
    print(addStr+"\thava add")
    input("please press enter exit")

def edit():
    lineNum=1
    with open("C:\Windows\System32\drivers\etc\hosts", "r") as f:
        linesList=f.readlines()
    for i in linesList:
        print(str(lineNum)+" "+i,end="")
        lineNum =lineNum+1
    lineNumber=int(input("please enter lineNumber:"))
    if(linesList[lineNumber-1].startswith("#")):
        linesList[lineNumber-1]=linesList[lineNumber-1].replace("#","",1)
    else:
        linesList[lineNumber-1]="#"+linesList[lineNumber-1]
    with open("C:\Windows\System32\drivers\etc\hosts", "a+") as f:
        f.truncate(0)
        f.writelines(linesList)
    input("please press enter exit")

def show():
    lineNum = 1
    with open("C:\Windows\System32\drivers\etc\hosts", "r") as f:
        linesList = f.readlines()
    for i in linesList:
        print(str(lineNum) + " " + i, end="")
        lineNum = lineNum + 1
    input("please press enter exit")
if __name__ == '__main__':
    if is_admin():
        print("Hosts编辑器\nAuthor:一条coding\nData:2021-08-21\nVersion:0.0.1")
        operateType = input("查看hosts：1\n编辑hosts：2\n新增hosts：3")
        if (operateType == "1"):
            show()
        if (operateType == "2"):
            edit()
        if (operateType == "3"):
            addStr=input("please type your content:")
            add(addStr)
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
input()