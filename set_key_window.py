import json
import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

import set_key


def open_key_preset(QMainWindow):
    QMainWindow.key_w = QtWidgets.QWidget()
    QMainWindow.ui_key_w = set_key.Ui_Form()
    QMainWindow.ui_key_w.setupUi(QMainWindow.key_w)
    QMainWindow.key_w.setWindowTitle("快捷键设置")
    QMainWindow.key_w.setWindowFlags(QMainWindow.windowFlags())

    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
        if "gaopin_key" not in data:
            data["gaopin_key"]="shift+f4"
        if "dipin_key" not in data:
            data["dipin_key"]="shift+f3"
        if "lama_export" not in data:
            data["lama_export"] = "ctrl+shift+f3"
        if "lama_import" not in data:
            data["lama_import"] = "ctrl+shift+f4"
        if "yingdiao" not in data:
            data["yingdiao"] = "ctrl+shift+d"
        if "baohe" not in data:
            data["baohe"] = "ctrl+shift+f"
    with open(os.path.join(BASE_PATH, "config.json"), "w") as f:
        # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
        formatted_data = json.dumps(data, indent=4)
        # 将格式化后的 json 字符串写入新的文件
        f.write(formatted_data)

    QMainWindow.ui_key_w.gaopin.setText(data["gaopin_key"])
    QMainWindow.ui_key_w.dipin.setText(data["dipin_key"])
    QMainWindow.ui_key_w.lama_export.setText(data["lama_export"])
    QMainWindow.ui_key_w.lama_import.setText(data["lama_import"])
    QMainWindow.ui_key_w.yingdiao.setText(data["yingdiao"])
    QMainWindow.ui_key_w.baohe.setText(data["baohe"])

    def show_message_box(text):
        message_box = QMessageBox(QMainWindow)
        message_box.setIcon(QMessageBox.Information)
        message_box.setText(text)
        message_box.setWindowTitle("提示")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()

    def check_btn():
        try:
            data["gaopin_key"]=QMainWindow.ui_key_w.gaopin.text()
            data["dipin_key"]=QMainWindow.ui_key_w.dipin.text()
            data["lama_export"]=QMainWindow.ui_key_w.lama_export.text()
            data["lama_import"]=QMainWindow.ui_key_w.lama_import.text()
            data["yingdiao"]=QMainWindow.ui_key_w.yingdiao.text()
            data["baohe"]=QMainWindow.ui_key_w.baohe.text()

            with open(os.path.join(BASE_PATH, "config.json"), "w") as f:
                # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
                formatted_data = json.dumps(data, indent=4)
                # 将格式化后的 json 字符串写入新的文件
                f.write(formatted_data)

            show_message_box("修改完成")
            QMainWindow.block_all_short_key()
            QMainWindow.key_w.destroy()
        except Exception as e:
            show_message_box("修改失败")

    QMainWindow.ui_key_w.check_btn.clicked.connect(
        lambda: check_btn())


    QMainWindow.key_w.show()