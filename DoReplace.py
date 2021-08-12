from PySide2.QtWidgets import QMessageBox


class DoReplace(object):
    def do_Replace(self, dic_text, list_path):
        replacedText = dic_text['replacedText']
        replacingText = dic_text['replacingText']
        if len(list_path) == 0:
            QMessageBox.warning(self,"温馨提示","还没拉文件",QMessageBox.Yes)
        elif replacedText == '' or replacingText == '':
            QMessageBox.warning(self, "温馨提示", "什么都还没输入", QMessageBox.Yes)
        else:
            for lv in list_path:
                file_data = ""
                with open(r'{}'.format(lv), mode='r') as old_file:
                    check = False
                    for line in old_file:
                        if 'createNode' in line:
                            check = True
                        if 'ftn' in line and check:
                            x = line.split("/")
                            for i in x:
                                if i == replacedText:
                                    x[x.index(i)] = replacingText
                                else:
                                    pass
                            xx = '/'.join(x)
                            line = line.replace(line, xx)
                            check = False
                        file_data += line
                    old_file.close()
                with open(r'{}'.format(lv), mode='w') as new_file:
                    new_file.write(file_data)
                    new_file.close()
            QMessageBox.information(self, "成功！", "已经替换完成", QMessageBox.Yes, QMessageBox.Yes)
