import json
import os
import sys

import qdarktheme
from PyQt5 import QtCore

isnight=False
isopacity=True
def toggle_topmost(window):
    # 切换置顶状态
    if window.windowFlags() & QtCore.Qt.WindowStaysOnTopHint:
        window.setWindowFlags(window.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
    else:
        window.setWindowFlags(window.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
    window.show()

def check_is_night():
    global isnight
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
    isnight=data["isnight"]

def night_theme():
    # 切换夜间模式
    if isnight:
        for i in range(0, 2):
            qdarktheme.setup_theme(
                custom_colors={
                    "[dark]": {
                        "background": "#4d4d4d",
                    }
                }
            )
    else:
        qdarktheme.setup_theme("light")
        qdarktheme.setup_theme("light")
    # qdarktheme.setup_theme()
    # qdarktheme.setup_theme()

def repair_is_night(is_night):
    global isnight
    isnight=is_night
    if isnight:
        print("设置夜间模式")
    else:
        print("设置昼间模式")
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
        data["isnight"]=isnight
    with open(os.path.join(BASE_PATH, "config.json"), "w") as f:
        # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
        formatted_data = json.dumps(data, indent=4)
        # 将格式化后的 json 字符串写入新的文件
        f.write(formatted_data)
    night_theme()

def check_opacity():
    global isopacity
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
    isopacity=data["isopacity"]

def set_opacity(windows):
    # 切换夜间模式
    if isopacity:
        windows.setWindowOpacity(1)
    else:
        windows.setWindowOpacity(0.9)

def repair_is_opacity(is_opacity,windows):
    global isopacity
    isopacity=is_opacity
    if isopacity:
        print("设置不透明")
    else:
        print("设置半透明")
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
        data["isopacity"]=isopacity
    with open(os.path.join(BASE_PATH, "config.json"), "w") as f:
        # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
        formatted_data = json.dumps(data, indent=4)
        # 将格式化后的 json 字符串写入新的文件
        f.write(formatted_data)
    set_opacity(windows)

def all_url_method(current_page, application,small_application=None):
    for i in application:
        i.webui_url.setText(application[current_page].webui_url.text())
    if small_application:
        for i in small_application:
            i.webui_url.setText(small_application[current_page].webui_url.text())
    print("已自动将全部任务的url更改完成")


def all_num_method(current_page, application):
    for i in application:
        i.paint_count.setText(application[current_page].paint_count.text())
    print("已自动将全部任务的张数更改完成")


def all_hd_method(current_page, application,small_application=None):
    for i in application:
        i.is_hd.setChecked(application[current_page].is_hd.isChecked())
        i.hd_weight.setText(application[current_page].hd_weight.text())
    if small_application:
        for i in small_application:
            i.is_hd.setChecked(small_application[current_page].is_hd.isChecked())
            i.hd_weight.setText(small_application[current_page].hd_weight.text())
    print("已自动将全部任务的放大设置更改完成")
