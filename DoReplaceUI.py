import os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import DoReplace


def deleteDuplicatedElementFromList(d_list):
    return sorted(set(d_list), key=d_list.index)


class MyListView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.slm = QStringListModel()  # 实例化字符串列表模型
        self.qList = []
        self.slm.setStringList(self.qList)  # 给字符串列表模型对象添加数据-字符串列表
        self.setModel(self.slm)  # 给列表视图设置模型
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        filename = event.mimeData().urls()[0].fileName()  # 只有文件名
        basename, ext = os.path.splitext(filename)  # 文件名和后缀
        ext = ext.upper()
        if ext == ".MA":  # 只接受jpg文件
            event.acceptProposedAction()  # 接受拖放操作
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        filename = event.mimeData().urls()[0].fileName()  # 只有文件名
        basename, ext = os.path.splitext(filename)  # 文件名和后缀
        ext = ext.upper()
        if ext == ".MA":  # 只接受jpg文件
            event.acceptProposedAction()  # 接受拖放操作
        else:
            event.ignore()

    def dropEvent(self, event):
        self.listModel = []
        filename = event.mimeData().urls()[0].fileName()  # 只有文件名
        basename, ext = os.path.splitext(filename)  # 文件名和后缀
        ext = ext.upper()
        if ext == ".MA":  # 只接受ma文件
            event.acceptProposedAction()  # 接受拖放操作
        else:
            event.ignore()
        for url in event.mimeData().urls():
            self.qList.append(url.path()[1:])
            self.qList = deleteDuplicatedElementFromList(self.qList)
        print(self.qList)
        self.slm.setStringList(self.qList)
        for i in range(self.slm.rowCount()):
            indexes = self.slm.index(i)
            self.listModel.append(list(self.slm.itemData(indexes).values())[0])  # 将listmodel转换成了列表了呢

    def delete_kw(self):
        index = self.currentIndex()
        print(index.row())
        self.slm.removeRow(index.row())
        self.qList.pop(index.row())


class FolderUI(QWidget):
    def __init__(self):
        super(FolderUI, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('改名字的工具')
        vbox = QVBoxLayout()
        putIn = self.textIn()
        subtitute = self.textOut()
        self.listView = MyListView()
        self.String_dic = {'replacedText': '', 'replacingText': ''}
        self.delete_button = QPushButton("删除")
        self.delete_button.clicked.connect(self.listView.delete_kw)
        button = QPushButton('改名啦')
        button.clicked.connect(self.msg)
        vbox.addLayout(putIn)
        vbox.addLayout(subtitute)
        vbox.addWidget(self.listView)
        vbox.addWidget(self.delete_button)
        vbox.addWidget(button)
        self.setLayout(vbox)

    def msg(self):
        reply = QMessageBox.warning(self, "温馨提示", "是否将{0}改成{1}？".format(self.String_dic['replacedText'],
                                                                        self.String_dic['replacingText']),
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            DoReplace.DoReplace.do_Replace(None, self.getdic(), self.listView.qList)

    def textIn(self):
        hbox = QHBoxLayout()
        Label = QLabel('需要更改的字符')
        self.replacedText = QLineEdit()
        self.replacedText.textChanged.connect(self.SetReplacingText)
        hbox.addWidget(Label)
        hbox.addWidget(self.replacedText)
        return hbox

    def textOut(self):
        hbox = QHBoxLayout()
        Label = QLabel('拿来替换的字符')
        self.replacingText = QLineEdit()
        self.replacingText.textChanged.connect(self.SetReplacingText)
        hbox.addWidget(Label)
        hbox.addWidget(self.replacingText)
        return hbox

    def SetReplacingText(self):
        self.String_dic['replacedText'] = self.replacedText.displayText()
        self.String_dic['replacingText'] = self.replacingText.displayText()

    def getdic(self):
        return self.String_dic


if __name__ == '__main__':
    app = QApplication([])
    twin = FolderUI()
    twin.show()
    app.exec_()
