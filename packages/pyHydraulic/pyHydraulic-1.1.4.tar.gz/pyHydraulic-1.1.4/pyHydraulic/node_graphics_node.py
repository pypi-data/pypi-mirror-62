"""
    Author: lee
    Time: 2020-01-06, 14:41
    File: node_graphics_node.py
    Function: 基本元件节点的绘制文件
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math,os
from pyHydraulic.node_node import *
from pyHydraulic.node_edge import Edge

DEBUG = True
# 控件的名称,每一个类型应该独一无二
# NODE_TYPES = ["pressure sensor",
#               "flow meter",
#               "tank",
#               "simple tank",
#               "gauge",
#               "servo valve",
#               "piston dual",
#               "piston right",
#               "piston left",
#               "pump",
#               "filter",
#               "accumulator",
#               "one-way valve",
#               "relief valve",
#               "text"
#               ]
# 所有的节点类的父类



# 自定义元件层级类
class componentsLib():
    NODE_TYPES_DICT = {
        "dynamic components": [{"pump": 100}],
        "executive components": [{"piston dual": 200},
                                 {"piston right": 201},
                                 {"piston left": 201}
                                 ],
        "control components": [{"servo valve": 300},
                               {"one-way valve": 301},
                               {"relief valve": 302}
                               ],
        "auxiliary components": [{"pressure sensor": 400},
                                 {"flow meter": 401},
                                 {"tank": 402},
                                 {"simple tank": 403},
                                 {"gauge": 404},
                                 {"filter": 405},
                                 {"accumulator": 406},
                                 {"picture": 407},
                                 {"text": 408}
                                 ]
    }
    def __int__(self):
        pass

    # 类函数：不需要访问实例变量，但是要访问类变量，静态函数：实例变量和类变量都不需要访问
    # 这里定义为类函数
    # 返回第一层名称的List
    @classmethod
    def getTopList(cls):
        return cls.NODE_TYPES_DICT.keys()

    # 返回第二层名称的List
    @classmethod
    def getSecondList(cls):
        secondComp = []
        toplist = cls.getTopList()
        for topName in toplist:
            secondList = cls.NODE_TYPES_DICT[topName]
            for dict in secondList:
                secondComp += dict.keys()
        return secondComp

    # 通过元件名称找到第一层大类
    @classmethod
    def getTopListByName(cls, Name):
        if Name in cls.getSecondList():
            toplist = cls.getTopList()
            for topname in toplist:
                secondlist = cls.NODE_TYPES_DICT[topname]
                for dict in secondlist:
                    if Name in dict: #如果dict中有Name
                        return topname
        else :
            return None

    # 通过第一层大类返回第二层的集合
    @classmethod
    def getSecondListByName(cls, name):
        toplist = cls.getTopList()
        secondComp = []
        if name in toplist:
            for topname in toplist:
                if topname == name:
                    secondList = cls.NODE_TYPES_DICT[topname]
                    for dict in secondList:
                        secondComp += dict.keys()
                    return secondComp
        else:
            return None

# print(componentsLib.getSecondListByName("auxiliary components"))
# print(componentsLib.getSecondList())
# print(componentsLib.getTopByName("tank"))


class QAbstractGraphicsNode(QGraphicsItem):
    def __init__(self, node):
        super().__init__()
        # 下面是公共的变量放在下面
        self.parent = node # 父容器控件
        self._width = 500  # 这两个属性可以根据具体控件在子类中修改
        self._height = 120

        # 修改选中和不选中的线型
        self._pen_default = QPen(Qt.white)# QPen(QColor("#7F000000"))
        self._pen_default.setWidth(8)
        self._pen_selected = QPen(Qt.green) #QPen(QColor("#FFFFA637"))
        self._pen_selected.setWidth(8)

        # init UI
        self.initUI()
        # 自己被移动表示位
        self.wasMoved = False
        # 下面可以添加一个通用变量
        self._name = self.parent._node_type+ str(self.parent.id) # 每个node有个独一无二的名字
        # 最大值最小值
        self._minValue = 0
        self._maxValue = 100.0
        self._value = 00.0  # 当前值
        self._percent = 0.0  # 占比
        self._text = " "  # 显示的文本数值，不想显示，赋值为空即可
        self._unit = " "  # 显示的文本单位，不想显示，赋值为空即可
        self.textEnable = True  # 是否显示文本开关
        self.textFont = "微软雅黑"
        # 下面存放本node中的socket的信息：包括1.socket位置坐标，2.socket的个数, 默认只有1个socket，在正中间
        self.socketInfo = []  # 默认没有socket信息，就没有socket

        # self.socketInfo = [[QPointF(1 / 2 * self._width, 1 / 2 * self._height), 0]]  # 后面0为socket颜色样式，取值0-5

##################### Properties defined ##################################################
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        value = str(value)
        # 遍历所有node，防止名字重复
        nodes = self.parent.scene.nodes
        for item in nodes:
            if item.grNode.name != self.name: # 排除自己的名字
                continue
                if item.grNode.name == value:
                    baseWidget = self.parent.scene.grScene.views()[0]
                    warningInfo = self.name + ":名字与其他元件重复，请重新修改"
                    self.showTips(warningInfo) # parent是nodeWidget对象
                    # QMessageBox.warning(baseWidget, '名称重复！', warningInfo, QMessageBox.Yes, QMessageBox.Yes)
                    return


        self._name =  value





        self.update()  # 这个会调用下面的paint()函数

    @property
    def id(self):
        return self.parent.id
    @id.setter
    def id(self, idNum):
        self.parent.id = idNum

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        if isinstance(value, int) or isinstance(value, float):
            if (value >= self._minValue) and (value <= self._maxValue):
                self._value = value
                self._percent = (self._value - self.minValue) / (self.maxValue - self.minValue)  # 0-1取值 百分数
                self.update()  # 这个会调用下面的paint()函数
            else:
                baseWidget = self.parent.scene.grScene.views()[0]

                warningInfo = (self.name + ":修改超出范围:%.2f ~ %.2f"%(self.minValue, self.maxValue))
                self.showTips(warningInfo)
                # QMessageBox.warning(baseWidget,'赋值超阈值',warningInfo,QMessageBox.Yes,QMessageBox.Yes)

    @property
    def maxValue(self):
        return self._maxValue
    @maxValue.setter
    def maxValue(self, value):
        if value >= self.value:
            self._maxValue = value
            self._percent = (self.value - self.minValue) / (self.maxValue - self.minValue)  # 0-1取值 百分数
            self.update()  # 这个会调用下面的paint()函数
        else:
            baseWidget = self.parent.scene.grScene.views()[0]
            warningInfo = (self.name + ":当前值必须保证在此范围:%.2f ~ %.2f" % (self.minValue, self.maxValue))
            self.showTips(warningInfo)
            # QMessageBox.warning(baseWidget, '最大赋值超阈值', warningInfo, QMessageBox.Yes, QMessageBox.Yes)


    @property
    def minValue(self):
        return self._minValue
    @minValue.setter
    def minValue(self, value):
        if value<= self.value:
            self._minValue = value
            self._percent = (self.value - self.minValue) / (self.maxValue - self.minValue)  # 0-1取值 百分数
            self.update()  # 这个会调用下面的paint()函数
        else:
            baseWidget = self.parent.scene.grScene.views()[0]
            warningInfo = (self.name + ":当前值必须保证在此范围:%.2f ~ %.2f" % (self.minValue, self.maxValue))
            self.showTips(warningInfo)
            # QMessageBox.warning(baseWidget, '最大赋值超阈值', warningInfo, QMessageBox.Yes, QMessageBox.Yes)

    # 显示文本的内容
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, value):
        if type(value) == str:
            self._text = value
            self.update()
        else:
            if DEBUG:
                raise Exception("必须赋值文本！")


    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, value):
        if isinstance(value, str):  # 判断为字符串形式
            self._unit = value
        else:#
            if DEBUG:
                print("node的单位不能为非字符串形式\n")


    @property
    def pos_x(self):
        return self.scenePos().x()
    @pos_x.setter
    def pos_x(self, value):
        self.setX(value)
        self.wasMoved = True

    @property
    def pos_y(self):
        return self.scenePos().y()
    @pos_y.setter
    def pos_y(self, value):
        self.setY(value)
        self.wasMoved = True

    @property
    def pos_rotation(self):
        return self.rotation()
    @pos_rotation.setter
    def pos_rotation(self, angle):
        # 1.设置旋转中心为操作图元的中心
        self.setTransformOriginPoint(self.boundingRect().center().x(),
                                            self.boundingRect().center().y())
        # 2.每次调用，在原先的旋转角度上，加上新的旋转角度
        self.setRotation(angle)
        # 3.旋转之后将scene中的所有edge更新一遍
        for edge in self.parent.scene.edges:
            edge.updatePositions()
        self.wasMoved = True

    # 获取绝对缩放因子
    @property
    def pos_scale(self):
        return self.scale()
    # 获取绝对缩放因子
    @pos_scale.setter
    def pos_scale(self, absFactor):
        # 1.设置旋转中心为操作图元的中心
        self.setTransformOriginPoint(self.boundingRect().center().x(),
                                     self.boundingRect().center().y())
        # 2.每次调用，在原先的旋转角度上，加上新的旋转角度
        self.setScale(absFactor)
        # 3.旋转之后将scene中的所有edge更新一遍
        self.parent.updateConnectedEdges()
        self.wasMoved = True  # 表示当前node被移动过了，为下面拍照做准备

        # for edge in self.parent.scene.edges:
        #     edge.updatePositions()

    # 层
    @property
    def layer(self):
        return self.zValue()
    # 获取绝对缩放因子
    @layer.setter
    def layer(self, value):
        self.setZValue(value)

    # 设置node的类型，能彻底更改类型,只读
    @property
    def type(self):
        return self.parent._node_type

    # 控件宽度
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._width = value
            self.update()
            for socket in self.parent.sockets:
                socket.updatePos()



        else:
            self.showTips(self.name+"width属性输入不合法")


    # 控件宽度
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._height = value
            self.update()
        else:
            self.showTips(self.name+"height属性输入不合法")

    # @type.setter
    # def type(self, strType):
    #     if strType in componentsLib.getSecondList():
    #         self.parent._node_type = strType
    #         self.parent.grNode = self.parent.create_grNode(strType)
    #     else:
    #         warningInfo = self.name + "元件类型无效！"
    #         self.showTips(warningInfo)



##################### Methods ##################################################
    # 父控件公共的属性
    def getProperty(self):
        dict = {"name": self.name,
                "id": self.id,
                "type":self.type,
                "pos_x": self.pos_x,
                "pos_y": self.pos_y,
                "pos_rotation": self.pos_rotation,
                "pos_scale": self.pos_scale,
                "layer":self.layer,
                "width": self.width,
                "height": self.height,
                }
        return dict

    # 从几层控件之上，显示提示信息
    def showTips(self, message):
        self.parent.scene.grScene.views()[0].parent.showTips(message)  # parent是nodeWidget对象


    # 增量角度
    def rotateDelata(self, deltaAngle):
        self.setRotation(self.pos_rotation + deltaAngle)
        self.parent.updateConnectedEdges()

    # 拖拽node使之移动，触发该事件
    def mouseMoveEvent(self, event):


        super().mouseMoveEvent(event)


        # 鼠标变成十字箭头
        self.setCursor(Qt.SizeAllCursor)
        # optimize me! just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
        self.wasMoved = True # 表示当前node被移动过了，为下面拍照做准备





    # 拖拽node后，释放鼠标, 触发该事件
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        # # If you want to change an item's geometry in any way, you must first call prepareGeometryChange() to allow QGraphicsScene to update its bookkeeping.
        # self.prepareGeometryChange()

        # 鼠标还原成正常箭头
        self.setCursor(Qt.ArrowCursor)
        # 触发历史记录
        if self.wasMoved:
            self.wasMoved = False
            self.parent.scene.history.storeHistory("Node moved", setModified=True)

    # 双击弹出输入框
    def mouseDoubleClickEvent(self, QGraphicsSceneMouseEvent):
        # 第一个参数就是父控件，这里是Qgrahicsview
        class_name = str(type(self))
        # 文字类型
        if class_name.find("GraphicsNode_text") >=0:
            text,ok = QInputDialog.getText(self.node.scene.grScene.views()[0], "修改文字对话框","请输入修改文字",QLineEdit.Normal, self.text)
            if ok:
                self.text = text
        # 数字类型控件
        elif class_name.find("GraphicsNode_flow_meter") >=0 or \
                class_name.find("GraphicsNode_tank") >=0 or \
                class_name.find("GraphicsNode_gauge") >= 0 or \
                class_name.find("GraphicsNode_servo_valve") >= 0 or \
                class_name.find("GraphicsNode_pistion") >=0:
            step = (self.maxValue - self.minValue) / 100.0 #每次拨动的步长
            value,ok = QInputDialog.getDouble(self.parent.scene.grScene.views()[0], "修改当前值对话框", ("修改范围:%.2f / %.2f"%(self.minValue, self.maxValue)), self.value, self.minValue, self.maxValue,  step)
            if ok:
                self.value = value

    # 定义控件的区域
    def boundingRect(self):
        return QRectF(
            -self._width / 2,
            -self._height / 2,
            self._width,
            self._height
        )

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    # 该函数只是在选中的时候，绘制一个框框和原点十字，需要在子类中重写
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None): #自己在子类中重新实现这个函数
        if self.isSelected():
            painter.save()
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)  # 把笔给画家
            # 1.画出整个控件的轮廓
            pen = painter.pen()
            painter.setOpacity(0.5)
            pen.setWidth(1)
            pen.setStyle(Qt.DashDotLine)
            pen.setColor(Qt.red)
            pen.setWidth(4)
            painter.setPen(pen)  # 把笔给画家
            painter.drawLine(-self._width / 5, 0, self._width / 5, 0)
            painter.drawLine(0, -self._height / 10, 0, self._height / 10)
            painter.drawRect(-self._width / 2, -self._height / 2, self._width, self._height)

            painter.restore()


# 1.静止的压力传感器，继承自子上面的node
class GraphicsNode_pressure_sensor(QAbstractGraphicsNode):
    def __init__(self, node=None):
        super().__init__(node)
        self.unit = "MPa"
        # 自己独特的变量，或者对父类变量进行篡改
        self._width = 250  # 整个控件边界的宽度
        self._height = self._width * 3.0 / 2  # 整个控件边界的高度
        # 修改 socket信息
        self.socketInfo = [[QPointF(0, self._height / 2), 2]]


    # 重写node绘制函数，画压力传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)  # 把笔给画家

        # 1.画出整个控件的轮廓
        # painter.drawRect(0, 0, self._width, self._height)

        # 1. 绘制一个圆 QtGui.QPainter.drawEllipse(center, rx, ry)
        r = self._height / 3.0
        painter.drawEllipse(QPoint(0, - self._height / 6), r, r)  #
        # 2.绘制一条竖线,作为支架
        painter.drawLine(0, self._height / 6, 0, self._height / 2)  #
        # 3.绘制叉叉
        painter.drawLine(r * (1 - math.sin(math.pi / 180 * 45)) - self._width / 2, r * (1 - math.cos(math.pi / 180 * 45)) - self._height / 2,
                         r * (1 + math.cos(math.pi / 180 * 45)) - self._width / 2, r * (1 + math.sin(math.pi / 180 * 45)) - self._height / 2)  #
        painter.drawLine(r * (1 - math.sin(math.pi / 180 * 45)) - self._width / 2, r * (1 + math.cos(math.pi / 180 * 45)) - self._height / 2,
                         r * (1 + math.cos(math.pi / 180 * 45)) - self._width / 2, r * (1 - math.sin(math.pi / 180 * 45)) - self._height / 2)  #
        #
        # index =0
        # for socket in self.node.sockets:
        #     self.socketInfo[index][0] = QPointF(socket.grSocket.x(), socket.grSocket.y())

# 2.静止的流量传感器
class GraphicsNode_flow_meter(QAbstractGraphicsNode):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 自己独特的变量，或者对父类变量进行篡改
        self.unit = "mL"
        self._width = 200  # 整个控件边界的宽度
        self._height = self._width * 2  # 整个控件边界的高度

        self.textEnable = True
        # 修改 socket信息
        self.socketInfo = [[QPointF(0, - self._height/2), 2],
                           [QPointF(0, self._height/2), 2]
                           ]

    # 重写node绘制函数，静止的流量传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        # 根据获取的坐标，更新要绘制的路径
        # path = QPainterPath()

        # 画2个竖线
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.drawLine(0, - self._height / 2, 0, - self._height * 1 / 4)
        painter.drawLine(0, self._height * 1 / 4, 0, self._height / 2)
        painter.drawEllipse(QPointF(0, 0), self._height / 4,
                            self._height / 4)
        # 画1个圆上个两个弧形

        painter.drawArc(
            QRect(-self._width * 9 / 10, - self._height * 4/ 24, self._height / 3, self._height / 3),
            -60 * 16, 120 * 16)
        painter.drawArc(QRect(self._width * 2.3 / 10, - self._height * 4 / 24, self._height /3, self._height / 3),
            120 * 16, 120 * 16)
        #  添加文字路径
        # 4.显示文本
        if self.textEnable:
            self._text = str(round(self.value, 1)) + self.unit
            painter.setFont(QFont(self.textFont, self._width / 4, QFont.Medium))  # 第二个参数是字体大小
            painter.drawText(QPointF(0, self._height * 0.45), self._text)


    def getProperty(self):
        commonProperty = super().getProperty()
        dictUnique = \
                {"value":self.value,
                "minValue":self.minValue,
                "maxValue":self.maxValue,
                "unit":self.unit
                }
        commonProperty.update(dictUnique) # 把dictUnique并入commonProperty
        return commonProperty
# 3.tank：液面会动的油箱
class GraphicsNode_tank(QAbstractGraphicsNode):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        # 自己独特的变量，或者对父类变量进行篡改
        self.unit = "cm"
        self._width = 1000  # 整个控件边界的宽度
        self._height = self._width*1 # 整个控件边界的高度

        # 波浪相关的变量
        self._frequency = 0.0015  # 波浪的频率,Hz
        self._amplitude = self._width / 50  # 像素，波浪幅值
        self._phase1 = 0  # 像素，波浪1相位
        self._phase2 = 0  # 像素，波浪2相位
        self._deepth = 0  # 水位高度
        # 修改父类变量
        self.maxValue = 100
        self.minValue = 0
        self.value = 20  # _value为内部变量，此句话意思要调用一下value函数，更新初始状态


        # 定义一个Timer，刷新波浪用的
        # 定时器初始化
        self.timer = QTimer()

        self.t = 0  # 时间
        self.sampleTime = 0.1 # s
        self.timer.setInterval(self.sampleTime * 1000)  # ms
        self.timer.timeout.connect(self.time_out)
        self.timer.start()

        # 修改 socket信息
        self.socketInfo = [[QPointF(0,- self._height /2), 2]]


    # 重写node绘制函数，画压力传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        waterPath1 = QPainterPath()

        # 1.开始画波浪线
        # 第一条波浪路径集合
        waterPath1 = QPainterPath()
        # 第二条波浪路径集合
        waterPath2 = QPainterPath()

        self._deepth = self._percent * self._height * 3 / 4  # 像素单位的深度
        y_deep = self._height - self._deepth - self._amplitude - self._height/2  # 液面的中值坐标
        waterPath1.moveTo(-self._width/2, y_deep)
        waterPath2.moveTo(-self._width / 2, y_deep)

        self._phase1 = self._width / 400 * self.t  # 每次更新相位自动加
        self._phase2 = self._width / 400 * self.t + 2 * math.pi * self._frequency * self._width /5 # 每次更新相位自动加
        # 开始填充波浪
        startDraw = -self._width //2
        endDraw =  self._width // 2
        stepDraw = self._width // 50
        for x_wave in range(startDraw, endDraw, stepDraw):
            y_wave1 = self._amplitude * math.sin(2 * math.pi * self._frequency * x_wave + self._phase1) + y_deep  # 计算波浪点y坐标
            y_wave2 = self._amplitude * math.sin(2 * math.pi * self._frequency * x_wave + self._phase2) + y_deep  # 计算波浪点y坐标

            waterPath1.lineTo(x_wave, y_wave1)
            waterPath2.lineTo(x_wave, y_wave2)

        waterPath1.lineTo(self._width / 2, y_deep)  # 移动到右下角结束点,整体形成一个闭合路径
        waterPath1.lineTo(self._width / 2, self._height / 2)  # 移动到右下角结束点,整体形成一个闭合路径
        waterPath2.lineTo(self._width / 2, y_deep)
        waterPath2.lineTo(self._width / 2, self._height / 2)  # 移动到右下角结束点,整体形成一个闭合路径

        waterPath1.lineTo(-self._width / 2, self._height/2)
        waterPath2.lineTo(-self._width / 2, self._height/2)

        waterPath1.lineTo(-self._width / 2, y_deep)
        waterPath2.lineTo(-self._width / 2, y_deep)

        # 大路径
        bigPath = QPainterPath()
        #后背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#008B8B"))
        # painter.setOpacity(0.3)
        painter.drawPath(waterPath1)

        painter.setBrush(QColor("#40E0D0"))
        painter.setOpacity(0.5)
        painter.drawPath(waterPath2)
         # 2.画出整个tank的轮廓
        painter.setOpacity(1)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)

        painter.drawLine(-self._width/2, - self._height * 1 / 4, -self._width/2, self._height/2)
        painter.drawLine(-self._width/2, self._height/2, self._width/2, self._height/2)
        painter.drawLine(self._width/2, self._height/2, self._width/2, -self._height * 1 / 4)
        # 画出最后的中间管路
        painter.drawLine(0, - self._height/2, 0, self._height * 2 / 5)
        # 4.显示文本
        if self.textEnable:
            # 下面只能用self._text，而不是self.text，否则会导致无限刷新
            self._text = str(round(self.value, 1)) + self.unit + "(" + format(self._percent, '.0%') + ")"
            # painter.setPen(self._pen_default)
            painter.setFont(QFont(self.textFont, self._width / 12, QFont.Medium))  # 第二个参数是字体大小
            # painter.setOpacity(0.6)  # 0：完全透明，1：完全不透明
            # 波浪的总高度，也就深度，不是幅值，从液面顶到油箱底的深度
            painter.drawText(- self._width *3/ 8, self._height * 0.46, self._text)

    def time_out(self):
        self.t += self.sampleTime
        self.update()


        # self.update(QRectF(0, 0,self._width/4,  self._height/4))

        # self.update(QRectF(-self._width/2, - self._height * 1 / 4,self._width/2,  self._height/2))

        #     index +=1
    def getProperty(self):
        commonProperty = super().getProperty()
        dictUnique = \
                {"value":self.value,
                "minValue":self.minValue,
                "maxValue":self.maxValue,
                "unit":self.unit
                }
        commonProperty.update(dictUnique) # 把dictUnique并入commonProperty
        return commonProperty

# 3.simple_tank：静止的简单tank符号
class GraphicsNode_simple_tank(QAbstractGraphicsNode):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 自己独特的变量，或者对父类变量进行篡改
        self.unit = "cm"
        self._width = 250  # 整个控件边界的宽度
        self._height = self._width/2  # 整个控件边界的高度

         # 修改父类变量
        self.maxValue = 100
        self.minValue = 0
        self.value = 50  # _value为内部变量，此句话意思要调用一下value函数，更新初始状态

        self.textEnable = False

        # 修改 socket信息
        self.socketInfo = [[QPointF(0, -self._height/2), 2]]


    # 重写node绘制函数，画压力传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        # self._deepth = self._percent * self._height * 1 / 2  # 像素单位的深度
        # y_deep = self._height - self._deepth - self._amplitude  # 液面的中值坐标
        # path.moveTo(0, y_deep)
        #
        # self._phase1 = self._width / 50 * self.t  # 每次更新相位自动加
        # for x_wave in range(self._width):
        #     y_wave = self._amplitude * math.sin(2 * math.pi * self._frequency * x_wave + self._phase1) + y_deep  # 计算波浪点y坐标
        #     path.lineTo(x_wave, y_wave)
        # path.lineTo(self._width, self._height)
        # path.lineTo(0, self._height)
        # path.lineTo(0, y_deep)
        #
        # painter.setBrush(Qt.darkRed)
        # painter.setOpacity(0.2)
        # painter.drawPath(path)
        # 2.画出整个tank的轮廓
        painter.setOpacity(1)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)

        painter.drawLine(-self._width /2, 0, -self._width /2, self._height/2)
        painter.drawLine(-self._width /2, self._height/2, self._width /2, self._height/2)
        painter.drawLine(self._width/2, self._height/2, self._width/2, 0)
        # 画出最后的中间管路
        painter.drawLine(0, -self._height/2, 0, self._height * 2 / 5)
        # 4.显示文本
        if self.textEnable:
            self._text = str(round(self.value, 1)) + self.unit + "(" + format(self._percent, '.0%') + ")"
            painter.setPen(self._pen_default)
            painter.setFont(QFont(self.textFont, self._width / 10, QFont.Medium))  # 第二个参数是字体大小
            # painter.setOpacity(0.6)  # 0：完全透明，1：完全不透明
            # 波浪的总高度，也就深度，不是幅值，从液面顶到油箱底的深度
            painter.drawText(self._width / 4, self._height * 0.95, self._text)
# 4.Gauge：会转动的仪表盘
class GraphicsNode_gauge(QAbstractGraphicsNode):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 自己独特的变量，或者对父类变量进行篡改
        self.unit = "MPa"
        self._width = 300  # 整个控件边界的宽度
        self._height = self._width*2  # 整个控件边界的高度

        # 与偏转相关的物理量
        self.maxValue = 30
        self.minValue = 0
        self.value = 0  # _value为内部变量，此句话意思要调用一下value函数，更新初始状态

        self._angel = 0  # 偏转的角度：protected
        # 修改 socket信息
        self.socketInfo = [[QPointF(0, self._height/2), 2]]


    # 重写node绘制函数，画压力传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)# 把笔给画家
        # 1.画出整个控件的轮廓
        # painter.drawRect(0, 0, self._width, self._height)

        # 1. 绘制一个圆 QtGui.QPainter.drawEllipse(center, rx, ry)
        r = self._height / 4
        painter.drawEllipse(QPoint(r-self._width / 2, r - self._height / 2), r, r)  #
        # 2.绘制一条竖线,作为支架
        painter.drawLine(0, 0, 0, self._height/2)  #
        # 绘制旋转点
        painter.save()
        painter.setBrush(Qt.black)
        painter.drawEllipse(QPointF(r -self._width / 2, r - self._height / 2), self._width / 40, self._width / 40)
        painter.restore()
        # painter.drawPoint(r -self._width / 2, r - self._height / 2)
        # 3.绘制指针
        painter.save()
        # min-max 对应 0-360°转角
        pen = painter.pen()
        pen.setWidth(8)
        painter.setPen(pen)
        self._angel = self._percent * 360  # 度
        self._angel = 240 / 360 * self._angel + 60  # 只从60-300转换

        painter.drawLine(r * (1 - math.sin(math.pi / 180 * self._angel) * 3 / 5) -self._width / 2,
                         r * (1 + math.cos(math.pi / 180 * self._angel) * 3 / 5) - self._height / 2,
                         r * (1 + math.sin(math.pi / 180 * self._angel) / 5) - self._width / 2,
                         r * (1 - math.cos(math.pi / 180 * self._angel) / 5)- self._height / 2 )  #

        painter.restore()
        # 4.绘制刻盘圆弧
        # （实际单位为1 / 16度），QPainter.drawArc(rect, a（起始角度）, alen（划过的圆角，单位为1/16度）)
        # 画绿色圆弧
        painter.save()
        pen = QPen()
        # painter.setOpacity(0.4)
        pen.setWidth(30)
        pen.setColor(QColor("#7B68EE"))
        painter.setPen(pen)  # 把笔给画家
        painter.drawArc(QRect(r * 1 / 5 -self._width / 2, r * 1 / 5 - self._height / 2, r * 8 / 5, r * 8 / 5), 210 * 16, -180 * 16)  # 绘画角度为30°~(330°)
        # 画红色圆弧
        pen.setWidth(30)
        pen.setColor(QColor("#FF0000"))
        painter.setPen(pen)  # 把笔给画家
        painter.drawArc(QRect(r * 1 / 5 -self._width / 2, r * 1 / 5 - self._height / 2, r * 8 / 5, r * 8 / 5), 30 * 16, -60 * 16)  # 绘画角度为30°~(330°)

        painter.restore()
        # 4.显示文本
        if self.textEnable:
            self._text = str(round(self.value, 1)) + self.unit
            # painter.setPen(self._pen_default)
            painter.setFont(QFont(self.textFont, self._width/6, QFont.Medium))  # 第二个参数是字体大小
            # painter.setOpacity(0.6)  # 0：完全透明，1：完全不透明
            painter.drawText(-self._width*1/4, -self._height*0.3/7, self._text)
        #     index +=1

    def getProperty(self):
        commonProperty = super().getProperty()
        dictUnique = \
                {"value":self.value,
                "minValue":self.minValue,
                "maxValue":self.maxValue,
                "unit":self.unit
                }
        commonProperty.update(dictUnique) # 把dictUnique并入commonProperty
        return commonProperty

# 5.Gauge：伺服阀
class GraphicsNode_servo_valve(QAbstractGraphicsNode):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 自己独特的变量，或者对父类变量进行篡改
        self.node_type = "servo valve"
        self.unit = "mA"
        self._width = 2500  # 整个控件边界的宽度
        self._height = self._width/4  # 整个控件边界的高度
        self._OffsetPix = 0  # 阀芯偏移的像素点
        # 与偏转相关的物理量
        self.maxValue = 100
        self.minValue = -100
        self.value = 0  # _value为内部变量，此句话意思要调用一下value函数，更新初始状态
        # 修改 socket坐标信息
        self.socketInfo = [[QPointF(1 / 20 * self._width, self._height/2), 2],
                           [QPointF(-1 / 20 * self._width, self._height/2), 2],
                           [QPointF(-1 / 20 * self._width, -self._height/2), 2],
                           [QPointF(1 / 20 * self._width, -self._height/2), 2]
                           ]
        # 箭头子类嵌入到本控件中
        self._arrow_left = MyArrowItem(self, QPointF(self._width * -11.5 / 25, self._height * 4.5 / 10), QPointF(self._width * -7.5 / 25, 0))
        self._arrow_left.arrowLength = self._width / 50

        self._arrow_right = MyArrowItem(self, QPointF(self._width * 11.5 / 25, self._height * 4.5 / 10), QPointF(self._width * 7.5 / 25, 0))
        self._arrow_right.arrowLength = self._width / 50

    # 重写node绘制函数，画压力传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        # 根据获取的坐标，更新要绘制的路径

        path = QPainterPath()

        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        # 画2个横线
        painter.save()
        pen = painter.pen()
        pen.setWidth(20)
        painter.setPen(pen)
        path.moveTo(self._width *-1.5 / 5, -self._height/2)
        path.lineTo(self._width * 1.5 / 5,  -self._height/2)
        path.moveTo(self._width * -1.5 / 5, self._height/2)
        path.lineTo(self._width * 1.5 / 5, self._height/2)
        painter.drawPath(path)
        path.clear()
        painter.restore()
        # 添加矩形阀芯，从下面开始就是要整体偏移的绘图
        # 计算出杆和隔离柱整体的像素偏移, 距离正中间偏移为0，左边为负，右为正
        self._OffsetPix = (self._percent - 0.5) * self._width * (2 / 5)

        path.addRect(self._width * -1.5 / 5 + self._OffsetPix, self._height *-4 / 10, self._width * 3 / 5,
                     self._height * 8 / 10)
        # 添加矩形电磁线圈
        path.addRect(-self._width / 2 + self._OffsetPix, self._height * 2 / 10, self._width * 1 / 5, self._height * 2 / 10)
        path.addRect(self._width * 1.5 / 5 + self._OffsetPix, self._height * 2 / 10, self._width * 1 / 5,
                     self._height * 2 / 10)

        # 画线左线圈上的线
        path.moveTo(self._width * -11.5/ 25 + self._OffsetPix, self._height * 4 / 10)
        path.lineTo(self._width * -10.5 / 25 + self._OffsetPix, self._height * 2 / 10)
        path.moveTo(self._width * -8.5 / 25 + self._OffsetPix, self._height * 4 / 10)
        path.lineTo(self._width * -9.5 / 25 + self._OffsetPix, self._height * 2 / 10)
        # 画线右线圈上的线
        path.moveTo(self._width * 8.5 / 25 + self._OffsetPix, self._height * 4 / 10)
        path.lineTo(self._width * 9.5 / 25 + self._OffsetPix, self._height * 2 / 10)
        path.moveTo(self._width * 11.5 / 25 + self._OffsetPix, self._height * 4 / 10)
        path.lineTo(self._width * 10.5 / 25 + self._OffsetPix, self._height * 2 / 10)
        # 画中间的竖线
        path.moveTo(self._width * -0.5 / 5 + self._OffsetPix, self._height * - 4 / 10)
        path.lineTo(self._width * -0.5 / 5 + self._OffsetPix, self._height * 4 / 10)

        path.moveTo(self._width * -1 / 20 + self._OffsetPix, self._height * -4 / 10)
        path.lineTo(self._width * -1 / 20 + self._OffsetPix, self._height * 4 / 10)

        path.moveTo(self._width * 1 / 20 + self._OffsetPix, self._height * -4 / 10)
        path.lineTo(self._width * 1 / 20 + self._OffsetPix, self._height * 4 / 10)

        path.moveTo(self._width * 0.5 / 5 + self._OffsetPix, self._height * -4 / 10)
        path.lineTo(self._width * 0.5 / 5 + self._OffsetPix, self._height * 4 / 10)
        # 中间横线
        path.moveTo(self._width * -1 / 20 + self._OffsetPix, 0)
        path.lineTo(self._width * 1 / 20 + self._OffsetPix, 0)

        # 画左边的竖线
        path.moveTo(self._width * -5 / 20 + self._OffsetPix, self._height * -4 / 10)
        path.lineTo(self._width * -5 / 20 + self._OffsetPix, self._height * 4 / 10)

        path.moveTo(self._width * -3 / 20 + self._OffsetPix, self._height * -4 / 10)
        path.lineTo(self._width * -3 / 20 + self._OffsetPix, self._height * 4 / 10)

        # 画右边的斜线
        path.moveTo(self._width * 3 / 20 + self._OffsetPix, self._height * -4 / 10)
        path.lineTo(self._width * 5 / 20 + self._OffsetPix, self._height * 4 / 10)

        path.moveTo(self._width * 3 / 20 + self._OffsetPix, self._height * 4 / 10)
        path.lineTo(self._width * 5 / 20 + self._OffsetPix, self._height * -4 / 10)

        painter.setBrush(Qt.black)
        painter.drawPath(path)

        # 中间添加两个点.点的直径为3
        path.addEllipse(QPointF(self._width * -1 / 20 + self._OffsetPix, 0), 3, 3)
        path.addEllipse(QPointF(self._width * 1 / 20 + self._OffsetPix, 0), 3, 3)

        # path.setFillRule(Qt.WindingFill)  # 所有闭合曲线全部填充
        # 路径
        painter.setBrush(Qt.darkGreen)
        painter.drawPath(path)

        # 两个箭头移动位置,下面self._arrow_right.update()比较耗时,父控件更新，子空间也默认更新
        self._arrow_left.source = QPointF(self._width * -11.5 / 25 + self._OffsetPix, self._height * 4.5 / 10)
        self._arrow_left.dest = QPointF(self._width * -7.5 / 25 + self._OffsetPix, 0)

        self._arrow_right.source = QPointF(self._width * 11.5 / 25 + self._OffsetPix, self._height * 4.5 / 10)
        self._arrow_right.dest = QPointF(self._width * 7.5 / 25 + self._OffsetPix, 0)


        #  添加文字路径
        # 4.显示文本
        if self.textEnable:
            self._text = str(round(self.value, 1)) + self.unit
            painter.setPen(self._pen_default)
            painter.setFont(QFont(self.textFont, self._width / 20, QFont.Medium))  # 第二个参数是字体大小
            # painter.setOpacity(0.6)  # 0：完全透明，1：完全不透明
            painter.drawText(QPointF(-self._width/2 + self._OffsetPix, 0), self._text)

        #     index +=1

    def getProperty(self):
        commonProperty = super().getProperty()
        dictUnique = \
                {"value":self.value,
                "minValue":self.minValue,
                "maxValue":self.maxValue,
                "unit":self.unit
                }
        commonProperty.update(dictUnique) # 把dictUnique并入commonProperty
        return commonProperty

# 6.piston：会伸缩的液压缸
class GraphicsNode_pistion(QAbstractGraphicsNode):
    # Piston_type_dual = 0  # 对称缸
    # Piston_type_right = 1  # 右出杆缸
    # Piston_type_left = 2  # 左出杆缸

    def __init__(self, parent=None):
        super().__init__(parent)
        # 自己独特的变量，或者对父类变量进行篡改
        self.unit = "cm"
        self._width = 5000  # 整个控件边界的宽度
        self._height = self._width/8  # 整个控件边界的高度
        self._OffsetPix = 0  # 阀芯偏移的像素点


        # 修改 socket信息
        self.socketInfo = [[QPointF(-9 / 40 * self._width, self._height/2), 2], [QPointF(9 / 40 * self._width, self._height/2), 2]]

        # 计算加速度方向的属性，即连续三个缸的位置采样点
        self.x1 = 0
        self.x2 = 0
        self.x3 = 0
        self.acceleration = 0  # 加速度方向默认为0

        # 与偏转相关的物理量
        self.maxValue = 100
        self.minValue = -100
        self.value = 0  # _value为内部变量，此句话意思要调用一下value函数，更新初始状态


    # 做的玩，判断缸加速度方向，加速度向右，返回正，否则返回负
    def jugde_acceleration(self, position):
        self.x1 = self.x2
        self.x2 = self.x3
        self.x3 = position
        acceleration = self.x3 - 2 * self.x2 + self.x1
        return acceleration  # 加速度大于零，即方向向右

    # 重写父类value赋值属性，赋值的时候才更新加速度状态
    @QAbstractGraphicsNode.value.setter
    def value(self, value):
        self.acceleration = self.jugde_acceleration(value)
        super(GraphicsNode_pistion, GraphicsNode_pistion).value.__set__(self, value)

    # 重写node绘制函数，画压力传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        # 更新修改 socket信息
        self.socketInfo = [[QPointF(-9 / 40 * self._width, self._height / 2), 2],
                           [QPointF(9 / 40 * self._width, self._height / 2), 2]]

        pen = QPen()
        pen.setStyle(Qt.DashDotLine)
        pen.setWidth(2)
        pen.setColor(Qt.black)




        # 1.画出整个缸体的轮廓(起始x,起始y,宽，高),缸整体宽度为1/2控件宽度
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)# 把笔给画家
        painter.drawRect(self._width *-1/4, -self._height/2, self._width/2, self._height)
        # 2.画出各个腔室
        pen.setStyle(Qt.NoPen)
        painter.setOpacity(0.6)
        painter.setPen(pen)  # 把笔给画家

        # 计算偏移的像素点和加速度
        self._OffsetPix = (self._percent - 0.5) * self._width * (1 / 2 - 1 / 20)
        # self.acceleration = self.jugde_acceleration(self.value)

        if self.acceleration > 0:  # 表示缸偏右
            # 左腔室轮廓
            painter.setBrush(Qt.red)  # 填充颜色
            painter.drawRect(self._width *(-1/ 4), -self._height / 2, self._width / 4 + self._OffsetPix, self._height)
            # 右腔室轮廓
            painter.setBrush(QColor("#40E0D0"))  # 填充颜色
            painter.drawRect(0 + self._OffsetPix, -self._height / 2, self._width / 4 - self._OffsetPix,
                             self._height)
        elif self.acceleration < 0:  # 表示缸偏左边
            painter.setBrush(QColor("#40E0D0"))  # 填充颜色
            painter.drawRect(self._width * -1 / 4, -self._height/2, self._width / 4 + self._OffsetPix, self._height)
            # 右腔室轮廓
            painter.setBrush(Qt.red)  # 填充颜色
            painter.drawRect(0 + self._OffsetPix, -self._height/2, self._width / 4 - self._OffsetPix,
                             self._height)
        elif self.acceleration == 0:  # 表示缸偏右边
            painter.setBrush(QColor("#40E0D0"))  # 填充颜色
            painter.drawRect(self._width *-1/ 4, -self._height/2, self._width / 4 + self._OffsetPix, self._height)
            # 右腔室轮廓
            painter.setBrush(QColor("#40E0D0"))  # 填充颜色
            painter.drawRect(0 + self._OffsetPix, -self._height/2, self._width / 4 - self._OffsetPix,
                             self._height)

        # painter.drawRect(self._width * 1 / 4, 0, self._width * 2 / 4, self._height)
        # 3.画缸中间的隔离柱，隔离柱厚度取1/20的控件宽度
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)# 把笔给画家
        painter.setBrush(QColor("#886600"))  # 填充颜色
        painter.setOpacity(1)
        painter.drawRect(self._width * - 1 / 80 + self._OffsetPix, - self._height/2, self._width * 2 / 80,
                         self._height)
        # 3.根据缸的类型，画缸左右出杆，中位出杆伸出缸外面长度为1/40控件宽度，杆的上下高度为1/10控件高度
        if self.parent._node_type == "piston dual":  # 对称缸
            # 3.画缸左出杆，中位出杆伸出缸外面长度为1/40控件宽度，杆的上下高度为1/10控件高度
            painter.drawRect(self._width * (-2 / 4 - 1 / 80) + self._OffsetPix, self._height *  - 1 / 20,
                             self._width * 1 / 2, self._height * 1 / 10)
            # 4.画缸右出杆，中位出杆伸出缸外面长度为1/40控件宽度，杆的上下高度为1/10控件高度
            painter.drawRect(self._width * (1 / 80) + self._OffsetPix, self._height * ( -1 / 20),
                             self._width * 1 / 2, self._height * 1 / 10)
        elif self.parent._node_type == "piston right":  # 右出杆
            painter.drawRect(self._width * (1 / 80) + self._OffsetPix, self._height * (- 1 / 20),
                             self._width * 1 / 2, self._height * 1 / 10)
        elif self.parent._node_type == "piston left":  # 左出杆
            painter.drawRect(self._width * (-2 / 4 - 1 / 80) + self._OffsetPix, self._height * (- 1 / 20),
                             self._width * 1 / 2, self._height * 1 / 10)

        # 5.显示文本
        if self.textEnable:
            self._text = str(round(self.value, 1)) + self.unit
            painter.setPen(self._pen_default)
            painter.setFont(QFont(self.textFont, self._width / 20, QFont.Medium))  # 第二个参数是字体大小
            # painter.setOpacity(0.6)  # 0：完全透明，1：完全不透明
            painter.drawText(-self._width/3.8 + self._OffsetPix, -self._width/100, self._text)

    def getProperty(self):
        commonProperty = super().getProperty()
        dictUnique = \
                {"value":self.value,
                "minValue":self.minValue,
                "maxValue":self.maxValue,
                "unit":self.unit
                }
        commonProperty.update(dictUnique) # 把dictUnique并入commonProperty
        return commonProperty


# 7.filter:静止的定量泵
class GraphicsNode_pump(QAbstractGraphicsNode):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 自己独特的变量，或者对父类变量进行篡改
        self.unit = "L/min"
        self._width = 300  # 整个控件边界的宽度
        self._height = self._width * 2  # 整个控件边界的高度
        self.textEnable = False
        # 修改 socket信息
        self.socketInfo = [[QPointF(0, -self._height/2), 2],
                           [QPointF(0, self._height/2), 2]
                           ]

    # 重写node绘制函数，画压力传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        # 根据获取的坐标，更新要绘制的路径


        # 画2个竖线
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.drawLine(0, -self._height/2, 0, self._height * -1 / 4)
        painter.drawLine(0, self._height * 1 / 4, 0, self._height/2)
        painter.drawEllipse(QPointF(0, 0), self._height / 4,
                            self._height / 4)
        # 画1个圆上个1个箭头
        tranglePath = QPainterPath()
        tranglePath.moveTo(0, self._height *-1/ 4)
        tranglePath.lineTo(self._width / 8, self._height *-1/ 8)
        tranglePath.lineTo(-self._width / 8, self._height *-1/ 8)
        tranglePath.lineTo(0, self._height * -1/ 4)
        painter.setBrush(Qt.black)
        painter.drawPath(tranglePath)
        #  添加文字路径
        # 4.显示文本
        if self.textEnable:
            self._text = str(round(self.value, 1)) + self.unit
            painter.setPen(self._pen_default)
            painter.setFont(QFont(self.textFont, self._width / 4, QFont.Medium))  # 第二个参数是字体大小
            # painter.setOpacity(0.6)  # 0：完全透明，1：完全不透明
            painter.drawText(QPointF(self._width * 2 / 3, self._height), self._text)

        #     index +=1

    def getProperty(self):
        commonProperty = super().getProperty()
        dictUnique = \
                {
                "unit":self.unit
                }
        commonProperty.update(dictUnique) # 把dictUnique并入commonProperty
        return commonProperty


# 8.filter:静止的油滤
class GraphicsNode_filter(QAbstractGraphicsNode):
    def __init__(self,parent=None):
        super().__init__(parent)
        # 自己独特的变量，或者对父类变量进行篡改
        self.unit = "L/min"
        self._width = 200  # 整个控件边界的宽度
        self._height = self._width * 1.6  # 整个控件边界的高度
        self.textEnable = False
        # 修改 socket信息
        self.socketInfo = [[QPointF(0, -self._height/2), 2],
                           [QPointF(0, self._height/2), 2]
                           ]

    # 重写node绘制函数，画压力传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        # 根据获取的坐标，更新要绘制的路径


        # 画2个竖线
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.drawLine(0, -self._height/2, 0, self._height * - 1.5 / 5)
        painter.drawLine(0, self._height * 1.5 / 5, 0, self._height/2)
         # 画1个个正方形
        Path = QPainterPath()
        Path.moveTo(0, self._height * -1.5/ 5)
        Path.lineTo(-self._width / 2, 0)
        Path.lineTo(0, self._height * 1.5 / 5)
        Path.lineTo(self._width/2 , 0)
        Path.lineTo(0, self._height *-1.5/ 5)

        painter.setBrush(QColor("#B8860B"))
        painter.drawPath(Path)
        # 画中间虚线
        pen = painter.pen()
        pen.setStyle(Qt.DotLine)
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawLine(-self._width/2, 0, self._width/2, 0)



        # painter.drawArc(
        #     QRect(-self._width * 2 / 5, self._height * 9.2 / 24, self._height / 4, self._height / 4),
        #     -60 * 16, 120 * 16)
        # painter.drawArc(
        #     QRect(self._width * 3.5 / 5, self._height * 9.2 / 24, self._height / 4, self._height / 4),
        #     120 * 16, 120 * 16)

        # 画1个圆，圆心，直径
        # path.addEllipse(QPointF(self._width / 2, self._height / 2), self._height / 6, self._height /6)

        # 画1个圆上个两个弧形
        # path.arcTo(self._width* 8/ 24, self._height *5/ 12, self._height / 4 , self._height / 4, -45, 90)

        # 路径
        # self.setPath(path)
        # painter.setBrush(Qt.lightGray)
        # painter.drawPath(path)

        #  添加文字路径
        # 4.显示文本
        if self.textEnable:
            self._text = str(round(self.value, 1)) + self.unit
            painter.setPen(self._pen_default)
            painter.setFont(QFont(self.textFont, self._width / 4, QFont.Medium))  # 第二个参数是字体大小
            # painter.setOpacity(0.6)  # 0：完全透明，1：完全不透明
            painter.drawText(QPointF(self._width * 0.5 / 3, self._height/2), self._text)
# 9.accumulator:静止的蓄能器
class GraphicsNode_accumulator(QAbstractGraphicsNode):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 自己独特的变量，或者对父类变量进行篡改
        self.unit = "mL"
        self._width = 300  # 整个控件边界的宽度
        self._height = self._width * 2.5  # 整个控件边界的高度
        self.textEnable = False
        # 修改 socket信息
        self.socketInfo = [[QPointF(0, self._height/2), 2]]

    # 重写node绘制函数
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        # 根据获取的坐标，更新要绘制的路径

        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)

        # 画1个个正方形
        radius_corner = self._width/2
        painter.drawRoundedRect(-self._width/2, -self._height/2, self._width, self._height*4/5, radius_corner, radius_corner)  # 后面两个参数为xround – int, yround – int,拐角的圆度
        # 画中间横线
        painter.drawLine(-self._width/2, self._height*-0.5/5, self._width/2, self._height*-0.5/5)
        # 画下面竖线
        painter.drawLine(0, self._height * 1.5/5, 0, self._height/2)
        # 画弹簧
        path = QPainterPath()
        path.moveTo(self._width *-0.5/ 3, self._height* -1.5/5)
        path.lineTo(self._width * 0.5 / 3, self._height/5 + self._height/20 - self._height/2)
        path.lineTo(self._width * -0.5 / 3, self._height / 5 + self._height * 2 / 30 - self._height/2)
        path.lineTo(self._width * 0.5 / 3, self._height / 5 + self._height * 3 / 30 - self._height/2)
        path.lineTo(self._width * -0.5 / 3, self._height / 5 + self._height * 4 / 30 - self._height/2)
        path.lineTo(self._width * 0.5 / 3, self._height / 5 + self._height * 5 / 30 - self._height/2)
        path.lineTo(self._width * -0.5 / 3, self._height / 5 + self._height * 6 / 30 - self._height/2)
        painter.drawPath(path)
        # 4.显示文本
        # if self.textEnable:
        #     self._text = str(round(self.value, 1)) + self.unit
        #     painter.setPen(self._pen_default)
        #     painter.setFont(QFont(self.textFont, self._width / 4, QFont.Medium))  # 第二个参数是字体大小
        #     painter.setOpacity(0.6)  # 0：完全透明，1：完全不透明
        #     painter.drawText(QPointF(self._width * 2 / 3, self._height), self._text)
# 10.one-way valve:静止的单向阀
class GraphicsNode_oneway_valve(QAbstractGraphicsNode):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 自己独特的变量，或者对父类变量进行篡改
        self.unit = "mL"
        self._width = 150  # 整个控件边界的宽度
        self._height = self._width * 2  # 整个控件边界的高度
        # 修改 socket信息
        self.socketInfo = [[QPointF(0, -self._height/2), 2],
                           [QPointF(0, self._height/2), 2]
                           ]

    # 重写node绘制函数，画压力传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        # 画2个竖线和圆
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.drawLine(0, -self._height/2, 0, self._height * (-1 / 4 - 1/20))
        painter.drawLine(0, self._height * (1 / 4 - 1/20), 0, self._height/2)
        painter.drawEllipse(QPointF(0, self._height * ( - 2/20)), self._height / 5,
                            self._height / 5)
        # 画1个圆上个楔形切线直线
        painter.drawLine(-self._width/2,  self._height*( - 1 / 20), 0, self._height * (1 / 4 - 1 / 20))
        painter.drawLine(self._width/2,  self._height*(- 1 / 20), 0, self._height * (1 / 4 - 1 / 20))
        # 4.显示文本
        # if self.textEnable:
        #     self._text = str(round(self.value, 1)) + self.unit
        #     painter.setPen(self._pen_default)
        #     painter.setFont(QFont('Times New Roman', self._width / 4, QFont.Medium))  # 第二个参数是字体大小
        #     painter.setOpacity(0.6)  # 0：完全透明，1：完全不透明
        #     painter.drawText(QPointF(self._width * 2 / 3, self._height), self._text)
# 11.静止的溢流阀
class GraphicsNode_relief_valve(QAbstractGraphicsNode):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 自己独特的变量，或者对父类变量进行篡改
        self.unit = "mL"
        self._width = 500  # 整个控件边界的宽度
        self._height = self._width * 1  # 整个控件边界的高度
        # 修改 socket信息
        self.socketInfo = [[QPointF(1 / 8 * self._width, -self._height/2), 2],
                           [QPointF(1 / 8 * self._width, self._height/2), 2]
                           ]
        # 箭头子类嵌入到本控件中
        self._arrow_left = MyArrowItem(self, QPointF(0, self._height * -2 / 6),
                                       QPointF(0, self._height * 1.8 / 6))
        self._arrow_left.arrowLength = self._width / 20

    # 重写node绘制函数，画压力传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        # 根据获取的坐标，更新要绘制的路径
        path = QPainterPath()

        # 1. 画2个竖线
        pen = self._pen_default if not self.isSelected() else self._pen_selected
        painter.setPen(pen)
        painter.drawLine(self._width * 1 / 8, - self._height/2, self._width * 1 / 8, self._height * -2 / 6)
        painter.drawLine(self._width * 1 / 8, self._height * 2 / 6, self._width * 1 / 8, self._height/2)

        painter.save()
        painter.setBrush(QColor("#886600"))
        painter.drawRect(self._width * (1 / 8 - 2 / 6), self._height * -2 / 6, self._width * 4 / 6, self._height * 4 / 6)
        painter.restore()
        # 2.画弹簧
        # 画弹簧
        path = QPainterPath()
        path.moveTo(self._width * (1 / 8 + 2 / 6), self._height * -2 / 6)
        path.lineTo(self._width * (1 / 8 + 2 / 6 + 1 / 20), 0)
        path.lineTo(self._width * (1 / 8 + 2 / 6 + 2 / 20), self._height * -2 / 6)
        path.lineTo(self._width * (1 / 8 + 2 / 6 + 3 / 20), 0)
        path.lineTo(self._width * (1 / 8 + 2 / 6 + 4 / 20), self._height * -2 / 6)
        path.lineTo(self._width * (1 / 8 + 2 / 6 + 5 / 20), 0)

        painter.drawPath(path)

        # 3.画虚线，下面是拐角的集合
        points = [QPointF(self._width * (1 / 8 - 2 /6), self._height * 1 / 6),
                  QPointF(-self._width/2,self._height * 1 / 6),
                  QPointF(-self._width/2, -self._height/2),
                  QPointF(self._width * -1/8, -self._height/2),
                  QPointF(self._width * 1 / 8, self._height * -2 / 6),
                  ]
        path = QPainterPath(points[0])  # 先到 第一个点
        for point in points:
            path.lineTo(point)
        pen.setStyle(Qt.DotLine)

        painter.setPen(pen)
        painter.drawPath(path)
        pen.setStyle(Qt.SolidLine)  # 还原画笔原有的实线状态，为下一次绘图做准备








        # #  添加文字路径
        # # 4.显示文本
        # if self.textEnable:
        #     self._text = str(round(self.value, 1)) + self.unit
        #     painter.setPen(self._pen_default)
        #     painter.setFont(QFont('Times New Roman', self._width / 4, QFont.Medium))  # 第二个参数是字体大小
        #     painter.setOpacity(0.6)  # 0：完全透明，1：完全不透明
        #     painter.drawText(QPointF(self._width * 2 / 3, self._height), self._text)
# 12.静止的文本
class GraphicsNode_text(QAbstractGraphicsNode):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 自己独特的变量，或者对父类变量进行篡改
        self.text = "Hello world!"
        self._height = 100  # 整个控件边界的高度

        self.textEnable = True









    # 重写node绘制函数，画压力传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):




        pen = self._pen_default if not self.isSelected() else self._pen_selected
        painter.setPen(pen)
        # painter.drawRect(0,0,self._width,self._height)
    #  添加文字路径
        # 4.显示文本
        if self.textEnable:
            # self._text = str(round(self.value, 1)) + self.unit
            painter.setFont(QFont(self.textFont, self._height, QFont.Medium))  # 第二个参数是字体大小
            # painter.setOpacity(0.6)  # 0：完全透明，1：完全不透明
            painter.drawText(QPointF(- self._width/2, self._height/2), self.text)

        self._width = painter.fontMetrics().width(self.text)  # 获取字符串的像素宽度
        super().paint(painter, QStyleOptionGraphicsItem, widget)


    def getProperty(self):
        commonProperty = super().getProperty()
        dictUnique = \
                {
                "text":self.text
                }
        commonProperty.update(dictUnique) # 把dictUnique并入commonProperty
        return commonProperty


# 13.静止的文本
class GraphicsNode_picture(QAbstractGraphicsNode):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 自己独特的变量，或者对父类变量进行篡改
        self.text = "Hello world!"
        self._height = 200  # 整个控件边界的高度
        self._height = 200  # 整个控件边界的高度

        self.textEnable = False
        # 图片信息
        self._picturePath = "./images/icons/南工校徽红底.png"
        self._pixmap = QPixmap()
        self.picturePath = self._picturePath # 加载显示pic




    @property
    def picturePath(self):
        return self._picturePath
    @picturePath.setter
    def picturePath(self,value):
        if os.path.isfile(value):
            self._picturePath = value
            self._pixmap.load(value)
            self._width = self._pixmap.width()  # 获得图片真实尺寸
            self._height = self._pixmap.height()
            self.update()
        else:
            baseWidget = self.node.scene.grScene.views()[0]
            warningInfo = self.name + ":路径文件无效，请重新输入！"
            self.showTips(warningInfo)  # parent是nodeWidget对象






    # 重写node绘制函数，画压力传感器
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # self._width = painter.fontMetrics()._width(self.text)  # 获取字符串的像素宽度

        pen = self._pen_default if not self.isSelected() else self._pen_selected
        painter.setPen(pen)

        painter.drawPixmap(self.boundingRect().toRect(),self._pixmap)

        super().paint(painter, QStyleOptionGraphicsItem, widget)

    #  添加文字路径
        # 4.显示文本
        if self.textEnable:
            self._text = str(round(self.value, 1)) + self.unit
            painter.setFont(QFont(self.textFont, self._height, QFont.Medium))  # 第二个参数是字体大小
            # painter.setOpacity(0.6)  # 0：完全透明，1：完全不透明
            painter.drawText(QPointF(- self._width/2, self._height/2), self.text)



    def getProperty(self):
        commonProperty = super().getProperty()
        dictUnique = \
                {"text":self.text,
                "picturePath":self.picturePath
                }
        commonProperty.update(dictUnique) # 把dictUnique并入commonProperty
        return commonProperty

# 0.箭头，用来嵌入其他控件中, 仅用来在本文件使用



class MyArrowItem(QGraphicsLineItem):
    # source箭头线段起始，dest箭头线段终止
    def __init__(self, parent=None, source=QPointF(0, 0), dest=QPointF(0, 0)):
        super().__init__(parent)
        self.source = source
        self.dest = dest

        self.arrowLength = 20  # 单个箭头的长度
        # 修改选中和不选中的线型
        self._pen_default = QPen(Qt.white)  # QPen(QColor("#7F000000"))
        self._pen_default.setWidth(8)
        self._pen_default.setJoinStyle(Qt.MiterJoin)

        self._pen_selected = QPen(Qt.green)  # QPen(QColor("#FFFFA637"))
        self._pen_selected.setWidth(8)
        self._pen_selected.setJoinStyle(Qt.MiterJoin)




    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):

        self.line = QLineF(self.source, self.dest)
        self.line.setLength(self.line.length() - self.arrowLength)

        # pen = self._pen_default if not self.isSelected() else self._pen_selected

        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)  # 把笔给画家

        # setBrush
        brush = QBrush()
        brush.setColor(Qt.black)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        v = self.line.unitVector()
        v.setLength(self.arrowLength)
        v.translate(QPointF(self.line.dx(), self.line.dy()))

        n = v.normalVector()
        n.setLength(n.length() * 0.5)
        n2 = n.normalVector().normalVector()

        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()

        # 方法1
        painter.drawLine(self.line)
        painter.drawPolygon(p1, p2, p3)
#  *************基本元件节点的绘制文件************** End