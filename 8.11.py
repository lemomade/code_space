import os
from msilib.schema import ListView

from PySide2 import QtCore
from PySide2.QtCore import QUrl, QStringListModel

from PySide2.QtWidgets import *
from PySide2.QtWidgets import QWidget, QApplication
from PySide2.QtCore import *
class myListView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.listview = QListView()
        self.slm = QStringListModel()  # 实例化字符串列表模型
        self.qList = ['1','3','4','34']

        self.slm.setStringList(self.qList)  # 给字符串列表模型对象添加数据-字符串列表

        self.setModel(self.slm)  # 给列表视图设置模型


        self.setAcceptDrops(True)
    def dragEnterEvent(self, event):
        filename = event.mimeData().urls()[0].fileName()  # 只有文件名
        basename, ext = os.path.splitext(filename)  # 文件名和后缀
        ext = ext.upper()
        if (ext == ".JPG"):  # 只接受jpg文件
            event.acceptProposedAction()  # 接受拖放操作
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        filename = event.mimeData().urls()[0].fileName()  # 只有文件名
        basename, ext = os.path.splitext(filename)  # 文件名和后缀
        ext = ext.upper()
        if (ext == ".JPG"):  # 只接受jpg文件
            event.acceptProposedAction()  # 接受拖放操作
        else:
            event.ignore()


    def dropEvent(self, event):
        self.listModel=[]
        filename = event.mimeData().urls()[0].fileName()  # 只有文件名
        basename, ext = os.path.splitext(filename)  # 文件名和后缀
        ext = ext.upper()
        if (ext == ".JPG"):  # 只接受jpg文件
            event.acceptProposedAction()  # 接受拖放操作
        else:
            event.ignore()
        for url in event.mimeData().urls():
            self.qList.append(url.path()[1:])
        # print(self.qList)
        self.slm.setStringList(deleteDuplicatedElementFromList(self.qList))
        for i in range(self.slm.rowCount()):
            indexs=self.slm.index(i)
            self.listModel.append(list(self.slm.itemData(indexs).values())[0])#将listmodel转换成了列表了呢
        print(self.listModel)

    def delete_kw(self):
        index = self.listview.currentIndex()

        print(index.data())








def deleteDuplicatedElementFromList(listA):
    return sorted(set(listA), key = listA.index)


class FolderUI(QWidget):
    def __init__(self):
        super(FolderUI, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('test')
        vbox = QVBoxLayout()
        # camera = self.createCameraComboMenus()
        putIn = self.textIn()
        subtitute = self.textOut()
        listView = myListView()

        self.delete_button = QPushButton("删除")
        self.delete_button.clicked.connect(listView.delete_kw)

        button = QPushButton('PlayBlast')
        # button.clicked.connect(self.setvalue)
        vbox.addLayout(putIn)
        vbox.addLayout(subtitute)
        vbox.addWidget(listView)
        vbox.addWidget(self.delete_button)
        vbox.addWidget(button)
        self.setLayout(vbox)

    def textIn(self):
        hbox = QHBoxLayout()
        Label = QLabel('put in replaced string')
        replacedText = QLineEdit()
        hbox.addWidget(Label)
        hbox.addWidget(replacedText)
        return hbox

    def textOut(self):
        hbox = QHBoxLayout()
        Label = QLabel('subtitute string')
        subtituteText = QLineEdit()
        hbox.addWidget(Label)
        hbox.addWidget(subtituteText)
        return hbox


if __name__ == '__main__':
    app = QApplication([])
    twin = FolderUI()
    twin.show()
    app.exec_()
