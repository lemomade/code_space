# -*- coding: utf-8 -*-
from PySide2 import QtGui
from PySide2.QtCore import QUrl
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
import pymel.core as pmc
import maya.mel as mel

class PlayBlastUI(QWidget):
    def __init__(self):
        super(PlayBlastUI, self).__init__()
        self.default_camera = 'camera1'
        self.dic = {'qt': ['H.264', 'H.263'], 'avi': ['none', 'MS-YUV', 'MS-RLE']}
        self.Frame_rate_dic = {'15fps': 'game', '24fps': 'film', '25fps': 'pal', '30fps': 'ntsc', '48fps': 'show'}
        self.initUI()

    def initUI(self):
        self.setWindowTitle('test')
        vbox = QVBoxLayout()
        camera = self.createCameraComboMenus()
        frm = self.createComboFormatMenus()
        code = self.createComboCodeMenus()
        framerate = self.createFramerateComboMenus()
        frameRange = self.createRangetext()
        frameSize = self.createSizetext()
        path = self.createFilePath()
        PlayBlastbutton = QPushButton('PlayBlast')
        PlayBlastbutton.clicked.connect(self.setvalue)

        vbox.addLayout(camera)
        vbox.addLayout(frm)
        vbox.addLayout(code)
        vbox.addLayout(frameRange)
        vbox.addLayout(frameSize)
        vbox.addLayout(framerate)
        vbox.addLayout(path)
        vbox.addWidget(PlayBlastbutton)

        self.setLayout(vbox)

    def createCameraComboMenus(self):
        hbox = QHBoxLayout()
        Label = QLabel('Camera')
        self.cameraComboBox = QComboBox()
    
        allcameras = cmds.ls(type='camera') or []
        cameras_tr = cmds.listRelatives(allcameras, parent=True)
        exclude = ['top', 'side', 'front', 'persp']
        cameras = list(set(cameras_tr) - set(exclude))
    
        if (self.default_camera not in cameras):
            mel.eval('error "默认摄像机不存在，请改名字"')
        else:
            cameras.remove(self.default_camera)
            cameras_a = [self.default_camera]
            camerasa = cameras_a.extend(cameras)
        for camaras in cameras_a:
            self.cameraComboBox.addItem(camaras)
    
        hbox.addWidget(Label)
        hbox.addWidget(self.cameraComboBox)
        return hbox

    def createFramerateComboMenus(self):
        hbox = QHBoxLayout()
        Label = QLabel('Frame Rate')
        self.FramerateComboBox = QComboBox()
        for k, v in self.Frame_rate_dic.items():
            self.FramerateComboBox.addItem(k)
        hbox.addWidget(Label)
        hbox.addWidget(self.FramerateComboBox)
        return hbox

    def createComboFormatMenus(self):
        hbox = QHBoxLayout()
        Label = QLabel('Format')
        self.formatComboBox = QComboBox()
        for k, v in self.dic.items():
            self.formatComboBox.addItem(k)
            self.formatComboBox.currentIndexChanged.connect(self.comboBox_changed)
        hbox.addWidget(Label)
        hbox.addWidget(self.formatComboBox)
        return hbox

    def comboBox_changed(self):
        for k, v in self.dic.items():
            if (k == self.formatComboBox.currentText()):
                self.CodeComboBox.clear()
                for i in v:
                    self.CodeComboBox.addItem(i)

    def createComboCodeMenus(self):
        hbox = QHBoxLayout()
        Label = QLabel('Code')
        self.CodeComboBox = QComboBox()
        for i in self.dic.get('qt'):
            self.CodeComboBox.addItem(i)
        hbox.addWidget(Label)
        hbox.addWidget(self.CodeComboBox)
        return hbox

    def createRangetext(self):
        hbox = QHBoxLayout()
        Label = QLabel('Frame Range')
        hbox.addWidget(Label)
        hbox.addWidget(QLabel('min'))
        self.lineMinEdit = QLineEdit()
        self.lineMinEdit.setText("0")

        self.lineMinEdit.setValidator(QtGui.QIntValidator())
        hbox.addWidget(self.lineMinEdit)
        hbox.addWidget(QLabel('max'))
        self.lineMaxEdit = QLineEdit()
        self.lineMaxEdit.setText("120")
        self.lineMaxEdit.setValidator(QtGui.QIntValidator())
        hbox.addWidget(self.lineMaxEdit)
        return hbox

    def createSizetext(self):
        hbox = QHBoxLayout()
        Label = QLabel('Size')
        hbox.addWidget(Label)
        hbox.addWidget(QLabel('height'))
        self.lineheightEdit = QLineEdit()
        self.lineheightEdit.setText("1080")
        self.lineheightEdit.setValidator(QtGui.QIntValidator())
        hbox.addWidget(self.lineheightEdit)
        hbox.addWidget(QLabel('width'))
        self.linewidthEdit = QLineEdit()
        self.linewidthEdit.setText("1920")
        self.linewidthEdit.setValidator(QtGui.QIntValidator())
        hbox.addWidget(self.linewidthEdit)
        return hbox

    def clicks(self):

        if (self.formatComboBox.currentText() == 'qt'):
            self.fd = QFileDialog.getSaveFileName(self, '选择一个py文件', './', 'mov(*.mov)')[0]
            self.linePathEdit.setText(self.fd)




        elif (self.formatComboBox.currentText() == 'avi'):
            self.fd = QFileDialog.getSaveFileName(self, '选择一个py文件', './', 'avi(*.avi)')[0]
            self.linePathEdit.setText(self.fd)

    def createFilePath(self):
        hbox = QHBoxLayout()
        Label = QLabel('File Path')
        self.linePathEdit = QLineEdit()
        button = QPushButton('find path')
        button.clicked.connect(self.clicks)
        self.lineMinEdit.displayText()

        hbox.addWidget(Label)
        hbox.addWidget(self.linePathEdit)
        hbox.addWidget(button)
        return hbox

    def setvalue(self):
        self.fd = ''
        dicsave = {'f': " ", 'st': 0, 'et': 120, 'fmt': "", 'fr': 24, 'h': 1920, 'w': 1080, 'co': "",'camera': self.default_camera}
        dicsave['f'] = self.linePathEdit.displayText()
        dicsave['st'] = self.lineMinEdit.displayText()
        dicsave['et'] = self.lineMaxEdit.displayText()
        dicsave['h'] = self.lineheightEdit.displayText()
        dicsave['w'] = self.linewidthEdit.displayText()
        dicsave['co'] = self.CodeComboBox.currentText()
        dicsave['fmt'] = self.formatComboBox.currentText()
        dicsave['fr'] = self.Frame_rate_dic.get(self.FramerateComboBox.currentText())
        print(dicsave)
        return dicsave



