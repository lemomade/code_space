import os
import proc1
from PySide2.QtCore import (Qt,
                            QResource)
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QWidget,
                               QLabel,
                               QLineEdit,
                               QPushButton,
                               QVBoxLayout,
                               QHBoxLayout,
                               QMessageBox,
                               QFileDialog)


class UI(QWidget):
    QResource.registerResource('resource.rcc')

    def __init__(self):
        super(UI, self).__init__()
        self.setObjectName("shotcutNumGenWgt")
        win_icon = QIcon(":/icon/logo")
        self.setWindowIcon(win_icon)
        self.setWindowTitle(u"幻马镜头号生成器 V2102")
        self.setFixedSize(350, 120)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self._init_ui()

    def _init_ui(self):
        # - File Browser Label.
        file_label = QLabel(self)
        file_label.setObjectName("fileBrowserLabel")
        # - File Browser Line Edit.
        self.file_text_line = QLineEdit(self)
        self.file_text_line.setObjectName("fileBrowserLine")

        replace_label = QLabel(self)
        replace_label.setObjectName("replaceBrowserLabel")

        self.replace_text_line = QLineEdit(self)
        self.replace_text_line.setObjectName("replaceLine")

        # - File Browser Button.
        file_browser_btn = QPushButton(self)
        file_browser_btn.setObjectName("fileBrowserButton")
        # - Run Button
        run_btn = QPushButton(self)
        run_btn.setObjectName("runButton")
        # - Set Layout.
        layout = QVBoxLayout(self)
        layout.setObjectName("mainLayout")
        file_layout = QHBoxLayout(self)
        file_layout.setObjectName("fileBrowserLayout")
        replace_Text_layout = QHBoxLayout(self)
        replace_Text_layout.setObjectName("replaceLayout")
        line_layout = QHBoxLayout(self)
        line_layout.setObjectName("lineEditLayout")
        line_layout.setSpacing(0)
        line_layout.setMargin(0)
        line_layout.setContentsMargins(0, 0, 0, 0)
        line_layout.addStretch()
        self.file_text_line.setLayout(line_layout)
        layout.addLayout(replace_Text_layout)
        layout.addLayout(file_layout)
        # - Add Items In Layout.
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_text_line)

        replace_Text_layout.addWidget(replace_label)
        replace_Text_layout.addWidget(self.replace_text_line)
        # file_layout.addWidget(file_browser_btn)
        line_layout.addWidget(file_browser_btn)
        layout.addWidget(run_btn)
        # - Set Main Layout.
        self.setLayout(layout)

        # - Config Label.
        file_label.setText(u"XML文件")
        replace_label.setText(u"更换字符")
        # - Config Line Edit.
        self.file_text_line.setPlaceholderText(u"XML文件路径")
        self.file_text_line.setFixedHeight(26)
        # self.file_text_line.setDragEnabled(True)

        # - Config File Browser Button.
        file_browser_btn.setText(u"浏览")
        height = self.file_text_line.height()
        file_browser_btn.setFixedSize(height*3, height)
        file_browser_btn.setCursor(Qt.ArrowCursor)
        file_browser_btn.released.connect(self.file_browser)
        # - Set Line Edit Text Margins
        text_margins = self.file_text_line.textMargins()
        self.file_text_line.setTextMargins(text_margins.left(),
                                      text_margins.top(),
                                      file_browser_btn.width(),
                                      text_margins.bottom())
        # - Config Run Button
        run_btn.setText(u"生成镜号")
        run_btn.released.connect(self.run_proc)

    def file_browser(self):
        file_name, _ = QFileDialog.getOpenFileName(self,
                                                   u"选择文件",
                                                   os.environ['USERPROFILE'],
                                                   u"XML 文件(*.xml)")
        self.file_text_line.setText(file_name)

    def dialog(self, message_type=None, message=None):
        dlg_type = ""
        dlg_title = ""
        if message_type == "error":
            dlg_type = QMessageBox.Critical
            dlg_title = u"错误"
        elif message_type == "done":
            dlg_type = QMessageBox.Information
            dlg_title = u"完成"

        dlg = QMessageBox(self)
        dlg.setWindowTitle(dlg_title)
        dlg.setText(message)
        dlg.setIcon(dlg_type)
        dlg.exec_()

    @property
    def line_text(self):
        return self.file_text_line.text()

    @property
    def replace_text(self):
        return self.replace_text_line.text()

    def file_exists(self):
        return os.path.exists(self.line_text)

    def file_ext(self):
        _, ext_name = os.path.splitext(self.line_text)
        if ext_name.lstrip('.').lower() == 'xml':
            return True
        else:
            return False

    def run_proc(self):
        if self.file_exists() and self.file_ext():
            out_put_file = proc1.run(self.line_text,self.replace_text)
            if os.path.exists(out_put_file):
                self.dialog("done", u"完成!")
            else:
                self.dialog("error", u"生成文件失败")
        elif not self.file_exists():
            self.dialog("error", u"文件不存在!")
        elif not self.file_ext():
            self.dialog("error", u"所选文件不是 XML 文件!")
