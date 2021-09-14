from PySide2.QtWidgets import QApplication,QWidget,QLineEdit
from PySide2.QtWidgets import QLabel,QPushButton
from PySide2.QtGui import QIcon,QFont
from PySide2.QtCore import Qt

import sys
sys.path.append("...")

import time
import pyautogui as pag
import pyperclip
from ctypes import *

# ===========================================================================================
# 相关函数：


# 获取x,y位置像素颜色
def get_color(x, y):
    gdi32 = windll.gdi32
    user32 = windll.user32
    hdc = user32.GetDC(None)  # 获取颜色值
    pixel = gdi32.GetPixel(hdc, x, y)  # 提取RGB值
    r = pixel & 0x0000ff
    g = (pixel & 0x00ff00) >> 8
    b = pixel >> 16
    return [r, g, b]


# HEX转RGB
def hex2rgb(hexcolor):
    '''HEX转RGB

    :param hexcolor: int or str
    :return: Tuple[int, int, int]

    >>> hex2rgb(16777215)
    (255, 255, 255)
    >>> hex2rgb('0xffffff')
    (255, 255, 255)
    '''
    hexcolor = int(hexcolor, base=16) if isinstance(hexcolor, str) else hexcolor
    rgb = ((hexcolor >> 16) & 0xff, (hexcolor >> 8) & 0xff, hexcolor & 0xff)
    return rgb

# RGB转HEX
def rgb2hex(r, g, b):
    color = "#"
    color += str(hex(r)).replace('x','0')[-2:]
    color += str(hex(g)).replace('x','0')[-2:]
    color += str(hex(b)).replace('x','0')[-2:]
    return color

# RGB转HSV
def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    m = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = ((g-b)/m)*60
        else:
            h = ((g-b)/m)*60 + 360
    elif mx == g:
        h = ((b-r)/m)*60 + 120
    elif mx == b:
        h = ((r-g)/m)*60 + 240
    if mx == 0:
        s = 0
    else:
        s = m/mx
    v = mx
    H = h / 2
    S = s * 255.0
    V = v * 255.0
    return (round(H), round(S), round(V))

# ===========================================================================================
# 窗口类：
class Window(QWidget):
    def __init__(self,Width=450,Height=600):
        super().__init__() 
        self.setWindowTitle("getScreenColor")
        self.setWindowFlags(Qt.WindowStaysOnTopHint) 
        self.Width=Width
        self.Height=Height

        # 样式表
        self.SS_bkg_Label="QLabel{background: rgb(220,220,220);color:rgb(62,62,62);border-radius:8px}"
        self.SS_Inf_Label="QPushButton{background: rgb(79,148,204);color:rgb(240,240,240);border-radius:8px}"
        self.SS_Inf_Box="QLineEdit{border-radius:3px;border: 2px solid rgb(149,179,215);color:rgb(92,92,92)}"
        self.SS_Main_Box="QPushButton{background: #FFFFFF;border: 3px solid rgb(150,150,150);border-radius:8px}"
        self.SS_Color_Box="QPushButton{background: #FFFFFF;border: 2px solid rgb(150,150,150);border-radius:3px}"
        self.SS_btn_1="QPushButton{background: rgb(214,219,233);color:rgb(82,82,82)}"
        self.SS_btn_2="QPushButton{background: rgb(225,235,205);color:rgb(82,82,82)}"
        self.SS_btn_3="QPushButton{background: rgb(232,191,190);color:rgb(82,82,82)}"

        # 该类私有变量或属性
        self.defaultColor=['#58827E','#144853','#4C6756','#849E77','#ADBDA3',
                           '#6B1B1E','#A94047','#E05E60','#F8A2AF','#E4CEDB',
                           '#B0A087','#7F877C','#C7C7BB','#D4C7BE','#E3E4DF',
                           '#C63866','#FE676E','#FD8F52','#FFBF73','#FFDCA2',
                           '#7292B8','#769EB8','#B4C5D7','#C5D5EC','#D9E0EA',
                           '#681F71','#7E0D5D','#6E57A5','#B589BE','#C993B7',
                           '#3978A4','#81AAAE','#EBCFC4','#FDB8A8','#E3929B','#7D7294']
        self.curBoxId=0
        self.curColor_RGB=[255,255,255]
        self.curColor_HEX='#FFFFFF'
        self.curColor_HSV=[0,0,255]
        self.storeList=[]
        self.defaultList=[]



        # 框架构造函数调用
        self.setSize()
        self.partition()
        self.setInfBox()
        self.setMainBox()
        self.setBtn()
        self.setIcon()
        self.setColorBox()
        

    # ================================================================================================
    # 颜色框回调函数部分：
    def selectedMain(self):
        tColor_HEX=self.curColor_HEX
        tColor_RGB=hex2rgb('0x'+tColor_HEX[1:])
        tColor_HSV=rgb2hsv(tColor_RGB[0], tColor_RGB[1], tColor_RGB[2])
        pyperclip.copy(str(tColor_RGB)+' '+tColor_HEX+' '+str(tColor_HSV)) 
        print(str(tColor_RGB)+' '+tColor_HEX+' '+str(tColor_HSV))

    def selectedStore(self):
        storeBox=self.sender()
        tColor_HEX=storeBox.property("Color")
        tColor_RGB=hex2rgb('0x'+tColor_HEX[1:])
        tColor_HSV=rgb2hsv(tColor_RGB[0], tColor_RGB[1], tColor_RGB[2])
        pyperclip.copy(str(tColor_RGB)+' '+tColor_HEX+' '+str(tColor_HSV)) 
        print(str(tColor_RGB)+' '+tColor_HEX+' '+str(tColor_HSV))

    def selectedDefault(self):
        defaultBox=self.sender()
        tNum=defaultBox.property("defaultId")
        tColor_HEX=self.defaultColor[tNum]
        tColor_RGB=hex2rgb('0x'+tColor_HEX[1:])
        tColor_HSV=rgb2hsv(tColor_RGB[0], tColor_RGB[1], tColor_RGB[2])
        pyperclip.copy(str(tColor_RGB)+' '+tColor_HEX+' '+str(tColor_HSV)) 
        print(str(tColor_RGB)+' '+tColor_HEX+' '+str(tColor_HSV))
    # ------------------------------------------------------------------------------------------------
    # 颜色信息标签回调
    def copyInf(self):
        infLabel=self.sender()
        infBox=infLabel.property('Children')
        pyperclip.copy(infBox.text())
        print(infBox.text())
    
    # ------------------------------------------------------------------------------------------------
    # 按钮回调函数部分：
    def getColor(self):
        time.sleep(2)
        x,y=pag.position()
        self.curColor_RGB=get_color(x,y)
        self.curColor_HSV=rgb2hsv(self.curColor_RGB[0], self.curColor_RGB[1], self.curColor_RGB[2])
        self.curColor_HEX=rgb2hex(self.curColor_RGB[0], self.curColor_RGB[1], self.curColor_RGB[2]).upper()

        RGB_STR=str(self.curColor_RGB).replace(" ", "")[1:-1]
        HSV_STR=str(self.curColor_HSV).replace(" ", "")[1:-1]
        self.CB1.setText(RGB_STR) 
        self.CB2.setText(self.curColor_HEX)
        self.CB3.setText(HSV_STR) 
        self.mainBox.setStyleSheet("QPushButton{background:"+self.curColor_HEX
        +";border: 3px solid rgb(150,150,150);border-radius:8px}")
    def saveColor(self):
        if self.curBoxId<20:
            tempBox=self.storeList[self.curBoxId]
            tempBox.setProperty("Color",self.curColor_HEX)
            tempBox.setStyleSheet("QPushButton{background:"+self.curColor_HEX
            +";border: 2px solid rgb(150,150,150);border-radius:3px}")
            self.curBoxId+=1
    def deleteColor(self):
        if self.curBoxId>0:
            self.curBoxId-=1
            tempBox=self.storeList[self.curBoxId]
            tempBox.setProperty("Color",'#FFFFFF')
            tempBox.setStyleSheet(self.SS_Color_Box)

    # ================================================================================================
    # 框架构造函数部分：
    def setSize(self):# 调整框架大小
        self.setGeometry(80,80,self.Width,self.Height)
        self.setMaximumSize(self.Width,self.Height)
        self.setMinimumSize(self.Width,self.Height)

    def setIcon(self):# 设置图标
        appIcon=QIcon("ICON.ico")
        self.setWindowIcon(appIcon)

    def partition(self):# 各部分划分
        Width=self.Width
        Height=self.Height
        qf=QFont()
        qf.setBold(True)
        qf.setPointSize(12)
        qf.setFamily("Cambria")   
        # --part1--当前颜色显示框背景-----
        self.bkgLabel1=QLabel(self)
        self.bkgLabel1.setGeometry(0.024*Width,0.015*Height,0.4*Width,0.3*Height)
        self.bkgLabel1.setStyleSheet(self.SS_bkg_Label)
        # --part2--当前颜色信息背景-----
        self.bkgLabel2=QLabel(self)
        self.bkgLabel2.setGeometry(0.448*Width,0.015*Height,0.528*Width,0.3*Height)
        self.bkgLabel2.setStyleSheet("QLabel{background: rgb(235,235,235);border-radius:8px}")
        # --part3--颜色存储库背景-----
        self.bkgLabel3=QLabel(self)
        self.bkgLabel3.setGeometry(0.024*Width,0.41*Height,0.952*Width,0.205*Height)
        self.bkgLabel3.setStyleSheet(self.SS_bkg_Label)
        self.bkgLabel3_title=QLabel(self)
        self.bkgLabel3_title.setGeometry(0.038*Width,0.415*Height,0.4*Width,0.05*Height)
        self.bkgLabel3_title.setStyleSheet(self.SS_bkg_Label)
        self.bkgLabel3_title.setText("Color Library") 
        self.bkgLabel3_title.setFont(qf)
        # --part4--预设颜色库背景-----
        self.bkgLabel4=QLabel(self)
        self.bkgLabel4.setGeometry(0.024*Width,0.63*Height,0.952*Width,0.355*Height)
        self.bkgLabel4.setStyleSheet(self.SS_bkg_Label)
        self.bkgLabel4_title=QLabel(self)
        self.bkgLabel4_title.setGeometry(0.038*Width,0.635*Height,0.8*Width,0.05*Height)
        self.bkgLabel4_title.setStyleSheet(self.SS_bkg_Label)
        self.bkgLabel4_title.setText("Color Library(default)") 
        self.bkgLabel4_title.setFont(qf)


    def setInfBox(self):# 设置信息显示框
        Width=self.Width
        Height=self.Height
        # 字体设置
        qf=QFont()
        qf.setBold(True)
        qf.setPointSize(12)
        qf.setFamily("Cambria")   
        # 绘制颜色信息框
        qf.setPointSize(10)
        self.CB1=QLineEdit(self) 
        self.CB1.setText("255,255,255") 
        self.CB1.move(0.62*Width,0.03*Height)  
        self.CB1.resize(0.35*Width,0.065*Height)
        self.CB1.setFont(qf)
        self.CB1.setStyleSheet(self.SS_Inf_Box)
        #
        self.CB2=QLineEdit(self) 
        self.CB2.setText("#FFFFFF") 
        self.CB2.move(0.62*Width,0.13*Height)  
        self.CB2.resize(0.35*Width,0.065*Height)
        self.CB2.setFont(qf)
        self.CB2.setStyleSheet(self.SS_Inf_Box)
        #
        self.CB3=QLineEdit(self) 
        self.CB3.setText("0,0,255") 
        self.CB3.move(0.62*Width,0.23*Height)  
        self.CB3.resize(0.35*Width,0.065*Height)
        self.CB3.setFont(qf)
        self.CB3.setStyleSheet(self.SS_Inf_Box)
        #
        self.CB1.setFocusPolicy(Qt.NoFocus)
        self.CB2.setFocusPolicy(Qt.NoFocus)
        self.CB3.setFocusPolicy(Qt.NoFocus)
        # 绘制颜色信息标签
        self.CL1=QPushButton(self)
        self.CL1.setGeometry(0.448*Width,0.025*Height,0.14*Width,0.075*Height)
        self.CL1.setStyleSheet(self.SS_Inf_Label)
        self.CL1.setText("RGB")
        self.CL1.setFont(qf)
        self.CL1.setProperty('Children',self.CB1)
        self.CL1.clicked.connect(self.copyInf)
        #
        self.CL2=QPushButton(self)
        self.CL2.setGeometry(0.448*Width,0.125*Height,0.14*Width,0.075*Height)
        self.CL2.setStyleSheet(self.SS_Inf_Label)
        self.CL2.setText("HEX")
        self.CL2.setFont(qf)
        self.CL2.setProperty('Children',self.CB2)
        self.CL2.clicked.connect(self.copyInf)
        #
        self.CL3=QPushButton(self)
        self.CL3.setGeometry(0.448*Width,0.225*Height,0.14*Width,0.075*Height)
        self.CL3.setStyleSheet(self.SS_Inf_Label)
        self.CL3.setText("HSV")
        self.CL3.setFont(qf)
        self.CL3.setProperty('Children',self.CB3)
        self.CL3.clicked.connect(self.copyInf)


    def setMainBox(self):# 设置其他label
        Width=self.Width
        Height=self.Height
        # 左上角当前颜色显示框
        self.mainBox=QPushButton(self)
        self.mainBox.setGeometry(0.04*Width,0.025*Height,0.368*Width,0.28*Height)
        self.mainBox.setStyleSheet(self.SS_Main_Box)
        self.mainBox.clicked.connect(self.selectedMain)

    def setBtn(self):# 设置按钮
        Width=self.Width
        Height=self.Height
        # 按钮字体
        qf=QFont()
        qf.setBold(True)
        qf.setPointSize(10)
        qf.setFamily("Cambria")
        # 获取颜色按钮
        self.bnt1=QPushButton(self)
        self.bnt1.setGeometry(0.024*Width,0.33*Height,0.4*Width,0.06*Height)
        self.bnt1.setStyleSheet(self.SS_btn_1)
        self.bnt1.setText("Get Screen Color")
        self.bnt1.setFont(qf)
        self.bnt1.clicked.connect(self.getColor)
        # 保存颜色按钮
        self.bnt2=QPushButton(self)
        self.bnt2.setGeometry(0.444*Width,0.33*Height,0.26*Width,0.06*Height)
        self.bnt2.setStyleSheet(self.SS_btn_1)
        self.bnt2.setText("Save Color")
        self.bnt2.setFont(qf)
        self.bnt2.clicked.connect(self.saveColor)
        # 删除颜色按钮
        self.bnt3=QPushButton(self)
        self.bnt3.setGeometry(0.724*Width,0.33*Height,0.26*Width,0.06*Height)
        self.bnt3.setStyleSheet(self.SS_btn_3)
        self.bnt3.setText("Delete Last")
        self.bnt3.setFont(qf)
        self.bnt3.clicked.connect(self.deleteColor)

    def setColorBox(self):# 绘制存储颜色及预设颜色框
        Width=self.Width
        Height=self.Height
        # 存储颜色框
        for i in range(0,2):
            for j in range(0,10):
                storeColorBox=QPushButton(self)
                storeColorBox.setGeometry((0.04+0.093*j)*Width,(0.475+0.07*i)*Height,0.08*Width,0.06*Height)
                storeColorBox.setStyleSheet(self.SS_Color_Box)
                storeColorBox.setProperty("storeId",i*10+j)
                storeColorBox.setProperty("Color",'#FFFFFF')
                storeColorBox.clicked.connect(self.selectedStore)
                self.storeList.append(storeColorBox)

        # 预设颜色框
        for i in range(0,4):
            for j in range(0,10):
                if i*10+j<36:
                    defaultColorBox=QPushButton(self)
                    defaultColorBox.setGeometry((0.04+0.093*j)*Width,(0.7+0.07*i)*Height,0.08*Width,0.06*Height)
                    defaultColorBox.setStyleSheet("QPushButton{background: "
                    +self.defaultColor[i*10+j]+";border: 2px solid rgb(150,150,150);border-radius:3px}")
                    defaultColorBox.setProperty("defaultId",i*10+j)
                    defaultColorBox.clicked.connect(self.selectedDefault)
                    self.defaultList.append(storeColorBox)

# ===========================================================================================
# 函数调用：
myapp = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(myapp.exec_())
