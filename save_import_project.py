import json
import os
import pickle
import shutil
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt5.QtWidgets import QFileDialog

import tab_window
from ps_tools import auto_doc_name
from set_cn_preset import set_cn_win
from setting_preset import open_set_preset
from tool_bar_method import all_url_method, all_num_method, all_hd_method
from update_combo import update_preset, upadate_cn_preset


def save_project(Main_w, application_list):
    save_data = []
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
    with open(os.path.join(BASE_PATH, "ControlNet.json"), "r") as f:
        data_cn = json.load(f)
    for i in application_list:
        item_data = {}
        item_data["tab_name"]= i.tab_name.text()
        item_data["layer_name"]=i.layer_name.text()

        setting = data["settings"][i.preset_combo.currentIndex()]
        model = ""
        if "model" in setting:
            model = setting["model"]
        hd_method = setting["algorithm"]
        is_hd = setting["continue1"]
        is_back_ps = setting["continue2"]
        hotkey1 = setting["hotkey1"]
        hotkey2 = setting["hotkey2"]
        hotkey3 = setting["hotkey3"]
        continue1 = float(setting["interval1"])
        continue2 = float(setting["interval2"])
        max_pics = int(setting["max_psi1"])
        max_hd = int(setting["max_psi2"])
        negative = setting["negative"]
        positive = setting["positive"]
        sample = setting["sample"]
        name = setting["name"]

        item_data["model"]=model
        item_data["hd_method"]=hd_method
        item_data["continue1"]=is_hd
        item_data["continue2"]=is_back_ps
        item_data["hotkey1"]=hotkey1
        item_data["hotkey2"]=hotkey2
        item_data["hotkey3"]=hotkey3
        item_data["interval1"]=continue1
        item_data["interval2"]=continue2
        item_data["max_pics"]=max_pics
        item_data["max_hd"]=max_hd
        item_data["negative"]=negative
        item_data["positive"]=positive
        item_data["sample"]=sample
        item_data["name"]=name

        item_data["add_positive"] = i.add_positive_edit.text()
        item_data["add_negative"] = i.add_negative_edit.text()
        item_data["is_use_translate"] = i.is_use_translate.isChecked()
        item_data["paint_weight"] = i.paint_weight.text()
        item_data["paint_count"] = i.paint_count.text()
        item_data["webui_url"] = i.webui_url.text()
        item_data["is_hd"] = i.is_hd.isChecked()
        item_data["hd_weight"] = i.hd_weight.text()

        if i.cn0_preset.currentIndex():
            item_data["cn0_enable"] = True
            cn0_preset = {"enable": data_cn[i.cn0_preset.currentIndex()-1]["enable"],
                          "name": data_cn[i.cn0_preset.currentIndex()-1]["name"],
                          "preprocessor": data_cn[i.cn0_preset.currentIndex()-1]["preprocessor"],
                          "model": data_cn[i.cn0_preset.currentIndex()-1]["model"],
                          "resolution": data_cn[i.cn0_preset.currentIndex()-1]["resolution"],
                          "param1": data_cn[i.cn0_preset.currentIndex()-1]["param1"],
                          "param2": data_cn[i.cn0_preset.currentIndex()-1]["param2"],
                          "pixel_perfect": data_cn[i.cn0_preset.currentIndex()-1]["pixel_perfect"],
                          }
            item_data["cn0_preset"] = cn0_preset
            item_data["cn0_layer"] = i.cn0_layer.text()
        else:
            item_data["cn0_enable"] = False

        if i.cn1_preset.currentIndex():
            item_data["cn1_enable"] = True
            cn1_preset = {"enable": data_cn[i.cn1_preset.currentIndex()-1]["enable"],
                          "name": data_cn[i.cn1_preset.currentIndex()-1]["name"],
                          "preprocessor": data_cn[i.cn1_preset.currentIndex()-1]["preprocessor"],
                          "model": data_cn[i.cn1_preset.currentIndex()-1]["model"],
                          "resolution": data_cn[i.cn1_preset.currentIndex()-1]["resolution"],
                          "param1": data_cn[i.cn1_preset.currentIndex()-1]["param1"],
                          "param2": data_cn[i.cn1_preset.currentIndex()-1]["param2"],
                          "pixel_perfect": data_cn[i.cn1_preset.currentIndex()-1]["pixel_perfect"],
                          }
            item_data["cn1_preset"] = cn1_preset
            item_data["cn1_layer"] = i.cn1_layer.text()
        else:
            item_data["cn1_enable"] = False

        if i.cn2_preset.currentIndex():
            item_data["cn2_enable"] = True
            cn2_preset = {"enable": data_cn[i.cn2_preset.currentIndex()-1]["enable"],
                          "name": data_cn[i.cn2_preset.currentIndex()-1]["name"],
                          "preprocessor": data_cn[i.cn2_preset.currentIndex()-1]["preprocessor"],
                          "model": data_cn[i.cn2_preset.currentIndex()-1]["model"],
                          "resolution": data_cn[i.cn2_preset.currentIndex()-1]["resolution"],
                          "param1": data_cn[i.cn2_preset.currentIndex()-1]["param1"],
                          "param2": data_cn[i.cn2_preset.currentIndex()-1]["param2"],
                          "pixel_perfect": data_cn[i.cn2_preset.currentIndex()-1]["pixel_perfect"],
                          }
            item_data["cn2_preset"] = cn2_preset
            item_data["cn2_layer"] = i.cn2_layer.text()
        else:
            item_data["cn2_enable"] = False

        if i.cn3_preset.currentIndex():
            item_data["cn3_enable"] = True
            cn3_preset = {"enable": data_cn[i.cn3_preset.currentIndex()-1]["enable"],
                          "name": data_cn[i.cn3_preset.currentIndex()-1]["name"],
                          "preprocessor": data_cn[i.cn3_preset.currentIndex()-1]["preprocessor"],
                          "model": data_cn[i.cn3_preset.currentIndex()-1]["model"],
                          "resolution": data_cn[i.cn3_preset.currentIndex()-1]["resolution"],
                          "param1": data_cn[i.cn3_preset.currentIndex()-1]["param1"],
                          "param2": data_cn[i.cn3_preset.currentIndex()-1]["param2"],
                          "pixel_perfect": data_cn[i.cn3_preset.currentIndex()-1]["pixel_perfect"],
                          }
            item_data["cn3_preset"] = cn3_preset
            item_data["cn3_layer"] = i.cn3_layer.text()
        else:
            item_data["cn3_enable"] = False

        item_data["lama_url"] = i.lama_url.text()

        save_data.append(item_data)

    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    PROJECT_PATH = os.path.join(BASE_PATH, "PROJECT_SAVED")
    if not os.path.exists(PROJECT_PATH):
        os.mkdir(PROJECT_PATH)
    # 将map数据保存成pickle格式的文件
    # 临时文件
    TEMP_PATH = os.path.join(BASE_PATH, "new project.xydoc")
    with open(TEMP_PATH, "wb") as f:
        pickle.dump(save_data, f)
    # 弹出保存文件对话框，返回用户选择的路径和名称
    save_path, _ = QFileDialog.getSaveFileName(parent=Main_w, caption="保存工程", directory=PROJECT_PATH,
                                               filter="PsdLink Pro工程 (*.xydoc)")
    # 如果用户选择了路径和名称，就复制或移动pickle文件到该路径
    if save_path:
        shutil.copy(TEMP_PATH, save_path)
        os.remove(TEMP_PATH)
        print(f"保存工程完成,保存了{len(save_data)}个项目,保存为{save_path}")
    else:
        os.remove(TEMP_PATH)


def save_project_self(Main_w, application_list, current_index):
    save_data = []

    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
    with open(os.path.join(BASE_PATH, "ControlNet.json"), "r") as f:
        data_cn = json.load(f)

    item_data = {}
    item_data["tab_name"] = application_list[current_index].tab_name.text()
    item_data["layer_name"] = application_list[current_index].layer_name.text()

    setting = data["settings"][application_list[current_index].preset_combo.currentIndex()]
    model = ""
    if "model" in setting:
        model = setting["model"]
    hd_method = setting["algorithm"]
    is_hd = setting["continue1"]
    is_back_ps = setting["continue2"]
    hotkey1 = setting["hotkey1"]
    hotkey2 = setting["hotkey2"]
    hotkey3 = setting["hotkey3"]
    continue1 = float(setting["interval1"])
    continue2 = float(setting["interval2"])
    max_pics = int(setting["max_psi1"])
    max_hd = int(setting["max_psi2"])
    negative = setting["negative"]
    positive = setting["positive"]
    sample = setting["sample"]
    name = setting["name"]

    item_data["model"] = model
    item_data["hd_method"] = hd_method
    item_data["continue1"] = is_hd
    item_data["continue2"] = is_back_ps
    item_data["hotkey1"] = hotkey1
    item_data["hotkey2"] = hotkey2
    item_data["hotkey3"] = hotkey3
    item_data["interval1"] = continue1
    item_data["interval2"] = continue2
    item_data["max_pics"] = max_pics
    item_data["max_hd"] = max_hd
    item_data["negative"] = negative
    item_data["positive"] = positive
    item_data["sample"] = sample
    item_data["name"] = name

    item_data["add_positive"] = application_list[current_index].add_positive_edit.text()
    item_data["add_negative"] = application_list[current_index].add_negative_edit.text()
    item_data["is_use_translate"] = application_list[current_index].is_use_translate.isChecked()
    item_data["paint_weight"] = application_list[current_index].paint_weight.text()
    item_data["paint_count"] = application_list[current_index].paint_count.text()
    item_data["webui_url"] = application_list[current_index].webui_url.text()
    item_data["is_hd"] = application_list[current_index].is_hd.isChecked()
    item_data["hd_weight"] = application_list[current_index].hd_weight.text()

    if application_list[current_index].cn0_preset.currentIndex():
        item_data["cn0_enable"] = True
        cn0_preset = {"enable": data_cn[application_list[current_index].cn0_preset.currentIndex()-1]["enable"],
                      "name": data_cn[application_list[current_index].cn0_preset.currentIndex()-1]["name"],
                      "preprocessor": data_cn[application_list[current_index].cn0_preset.currentIndex()-1][
                          "preprocessor"],
                      "model": data_cn[application_list[current_index].cn0_preset.currentIndex()-1]["model"],
                      "resolution": data_cn[application_list[current_index].cn0_preset.currentIndex()-1]["resolution"],
                      "param1": data_cn[application_list[current_index].cn0_preset.currentIndex()-1]["param1"],
                      "param2": data_cn[application_list[current_index].cn0_preset.currentIndex()-1]["param2"],
                      "pixel_perfect": data_cn[application_list[current_index].cn0_preset.currentIndex()-1][
                          "pixel_perfect"],
                      }
        item_data["cn0_preset"] = cn0_preset
        item_data["cn0_layer"] = application_list[current_index].cn0_layer.text()
    else:
        item_data["cn0_enable"] = False

    if application_list[current_index].cn1_preset.currentIndex():
        item_data["cn1_enable"] = True
        cn1_preset = {"enable": data_cn[application_list[current_index].cn1_preset.currentIndex()-1]["enable"],
                      "name": data_cn[application_list[current_index].cn1_preset.currentIndex()-1]["name"],
                      "preprocessor": data_cn[application_list[current_index].cn1_preset.currentIndex()-1][
                          "preprocessor"],
                      "model": data_cn[application_list[current_index].cn1_preset.currentIndex()-1]["model"],
                      "resolution": data_cn[application_list[current_index].cn1_preset.currentIndex()-1]["resolution"],
                      "param1": data_cn[application_list[current_index].cn1_preset.currentIndex()-1]["param1"],
                      "param2": data_cn[application_list[current_index].cn1_preset.currentIndex()-1]["param2"],
                      "pixel_perfect": data_cn[application_list[current_index].cn1_preset.currentIndex()-1][
                          "pixel_perfect"],
                      }
        item_data["cn1_preset"] = cn1_preset
        item_data["cn1_layer"] = application_list[current_index].cn1_layer.text()
    else:
        item_data["cn1_enable"] = False

    if application_list[current_index].cn2_preset.currentIndex():
        item_data["cn2_enable"] = True
        cn2_preset = {"enable": data_cn[application_list[current_index].cn2_preset.currentIndex()-1]["enable"],
                      "name": data_cn[application_list[current_index].cn2_preset.currentIndex()-1]["name"],
                      "preprocessor": data_cn[application_list[current_index].cn2_preset.currentIndex()-1][
                          "preprocessor"],
                      "model": data_cn[application_list[current_index].cn2_preset.currentIndex()-1]["model"],
                      "resolution": data_cn[application_list[current_index].cn2_preset.currentIndex()-1]["resolution"],
                      "param1": data_cn[application_list[current_index].cn2_preset.currentIndex()-1]["param1"],
                      "param2": data_cn[application_list[current_index].cn2_preset.currentIndex()-1]["param2"],
                      "pixel_perfect": data_cn[application_list[current_index].cn2_preset.currentIndex()-1][
                          "pixel_perfect"],
                      }
        item_data["cn2_preset"] = cn2_preset
        item_data["cn2_layer"] = application_list[current_index].cn2_layer.text()
    else:
        item_data["cn2_enable"] = False

    if application_list[current_index].cn3_preset.currentIndex():
        item_data["cn3_enable"] = True
        cn3_preset = {"enable": data_cn[application_list[current_index].cn3_preset.currentIndex()-1]["enable"],
                      "name": data_cn[application_list[current_index].cn3_preset.currentIndex()-1]["name"],
                      "preprocessor": data_cn[application_list[current_index].cn3_preset.currentIndex()-1][
                          "preprocessor"],
                      "model": data_cn[application_list[current_index].cn3_preset.currentIndex()-1]["model"],
                      "resolution": data_cn[application_list[current_index].cn3_preset.currentIndex()-1]["resolution"],
                      "param1": data_cn[application_list[current_index].cn3_preset.currentIndex()-1]["param1"],
                      "param2": data_cn[application_list[current_index].cn3_preset.currentIndex()-1]["param2"],
                      "pixel_perfect": data_cn[application_list[current_index].cn3_preset.currentIndex()-1][
                          "pixel_perfect"],
                      }
        item_data["cn3_preset"] = cn3_preset
        item_data["cn3_layer"] = application_list[current_index].cn3_layer.text()
    else:
        item_data["cn3_enable"] = False

    item_data["lama_url"] = application_list[current_index].lama_url.text()

    save_data.append(item_data)

    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    PROJECT_PATH = os.path.join(BASE_PATH, "PROJECT_SAVED")
    if not os.path.exists(PROJECT_PATH):
        os.mkdir(PROJECT_PATH)
    # 将map数据保存成pickle格式的文件
    # 临时文件
    TEMP_PATH = os.path.join(BASE_PATH, "new project.xydoc")
    with open(TEMP_PATH, "wb") as f:
        pickle.dump(save_data, f)
    # 弹出保存文件对话框，返回用户选择的路径和名称
    save_path, _ = QFileDialog.getSaveFileName(parent=Main_w, caption="保存工程", directory=PROJECT_PATH,
                                               filter="PsdLink Pro工程 (*.xydoc)")
    # 如果用户选择了路径和名称，就复制或移动pickle文件到该路径
    if save_path:
        shutil.copy(TEMP_PATH, save_path)
        os.remove(TEMP_PATH)
        print(f"保存工程完成,保存了{len(save_data)}个项目,保存为{save_path}")
    else:
        os.remove(TEMP_PATH)

def tabs_bind(Main_w,ui_tab_w,application_list):
    # 对于每个tab执行的方法
    # 更改标签名
    ui_tab_w.rename_tab.clicked.connect(
        lambda: Main_w.rename_tab(application_list))
    ui_tab_w.tab_name.returnPressed.connect(lambda: Main_w.rename_tab(application_list))
    # 读取config.json文件,更改预设的列表
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
        now_preset = data["setting_index"]
        preset_list = data["settings"]
    all_preset_name = []
    for i in preset_list:
        all_preset_name.append(i["name"])
    ui_tab_w.preset_combo.clear()
    ui_tab_w.preset_combo.addItems(all_preset_name)
    ui_tab_w.preset_combo.setCurrentIndex(now_preset)

    # 更改重绘幅度
    ui_tab_w.paint_weight.setText(data["am"])

    # 更改张数
    ui_tab_w.paint_count.setText(data["ct"])

    # 更改weburl
    ui_tab_w.webui_url.setText(data["url"])

    # 更改autodlid
    if "autodl" in data:
        ui_tab_w.autodl_id.setText(data["autodl"])

    # 启用高清放大
    ui_tab_w.is_hd.setChecked(data["hd"])

    # 更改低清放大幅度
    ui_tab_w.hd_weight.setText(data["hdam"])

    # 更改controlnet
    with open(os.path.join(BASE_PATH, "ControlNet.json"), "r") as f:
        data_control = json.load(f)
    cn_list = []
    cn_list.append("无")
    for i in data_control:
        cn_list.append(i["name"])
    ui_tab_w.cn0_preset.clear()
    ui_tab_w.cn1_preset.clear()
    ui_tab_w.cn2_preset.clear()
    ui_tab_w.cn3_preset.clear()
    ui_tab_w.cn0_preset.addItems(cn_list)
    ui_tab_w.cn1_preset.addItems(cn_list)
    ui_tab_w.cn2_preset.addItems(cn_list)
    ui_tab_w.cn3_preset.addItems(cn_list)
    ui_tab_w.cn0_preset.setCurrentIndex(data["control_index"])
    ui_tab_w.cn1_preset.setCurrentIndex(0)
    ui_tab_w.cn2_preset.setCurrentIndex(0)
    ui_tab_w.cn3_preset.setCurrentIndex(0)

    # 连接tab上的预设设置按钮
    ui_tab_w.set_preset.clicked.connect(
        lambda: open_set_preset(Main_w, ui_tab_w.preset_combo.currentIndex(), application_list))

    # 连接设置预设按钮
    ui_tab_w.cn0_preset_set_btn.clicked.connect(
        lambda: set_cn_win(Main_w, ui_tab_w.cn0_preset.currentIndex(), application_list))
    ui_tab_w.cn1_preset_set_btn.clicked.connect(
        lambda: set_cn_win(Main_w, ui_tab_w.cn1_preset.currentIndex(), application_list))
    ui_tab_w.cn2_preset_set_btn.clicked.connect(
        lambda: set_cn_win(Main_w, ui_tab_w.cn2_preset.currentIndex(), application_list))
    ui_tab_w.cn3_preset_set_btn.clicked.connect(
        lambda: set_cn_win(Main_w, ui_tab_w.cn3_preset.currentIndex(), application_list))

    # 控制重绘幅度和张数的输入范围
    ui_tab_w.paint_count.setValidator(QIntValidator(1, 9999999))
    reg = QRegularExpression('^0\.(0[1-9]|[1-9]\d?)$|^1\.00$')
    validator = QRegularExpressionValidator()
    validator.setRegularExpression(reg)
    ui_tab_w.paint_weight.setValidator(validator)

    # 自动匹配文件名
    ui_tab_w.auto_layer_name.clicked.connect(lambda: auto_doc_name(application_list))
    # 全应用该url和id
    ui_tab_w.all_url_btn.clicked.connect(
        lambda: all_url_method(Main_w.ui.tabWidget.currentIndex(), application_list))
    ui_tab_w.all_hd_btn.clicked.connect(
        lambda: all_hd_method(Main_w.ui.tabWidget.currentIndex(), application_list))
    ui_tab_w.all_num_btn.clicked.connect(
        lambda: all_num_method(Main_w.ui.tabWidget.currentIndex(), application_list))

    # 运算按钮
    ui_tab_w.import_sd_btn.clicked.connect(
        lambda: Main_w.short_key_import_sd())
    ui_tab_w.start_cal_btn.clicked.connect(
        lambda: Main_w.start_caculate())
    ui_tab_w.only_import_btn.clicked.connect(
        lambda: Main_w.only_import())
    ui_tab_w.only_import_start.clicked.connect(
        lambda: Main_w.only_import_start())
    ui_tab_w.back_ps_btn.clicked.connect(
        lambda: Main_w.import_back_ps())
    ui_tab_w.hd_btn.clicked.connect(
        lambda: Main_w.hd_back_ps_btn())
    ui_tab_w.stop_project_btn.clicked.connect(
        lambda: Main_w.stop())
    ui_tab_w.lama_import.clicked.connect(
        lambda: Main_w.Lama_export())
    ui_tab_w.lama_export.clicked.connect(
        lambda: Main_w.Lama_import())

    # 存档
    ui_tab_w.export_project_btn.clicked.connect(
        lambda: save_project_self(Main_w,application_list,Main_w.ui.tabWidget.currentIndex()))


def import_project(Main_w, application_list):
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data_preset = json.load(f)
    with open(os.path.join(BASE_PATH, "ControlNet.json"), "r") as f:
        data_cn = json.load(f)
    PROJECT_PATH = os.path.join(BASE_PATH, "PROJECT_SAVED")
    if not os.path.exists(PROJECT_PATH):
        os.mkdir(PROJECT_PATH)
    file_name, _ = QFileDialog.getOpenFileName(parent=Main_w, caption='读取工程', directory=PROJECT_PATH,
                                               filter="PsdLink Pro工程 (*.xydoc)")
    try:
        with open(file_name, 'rb') as f:
            data = pickle.load(f)

            for i in data:
                tab_w = QtWidgets.QWidget()
                ui_tab_w = tab_window.Ui_Form()
                ui_tab_w.setupUi(tab_w)
                tabs_bind(Main_w, ui_tab_w, application_list)
                application_list.append(ui_tab_w)
                ui_tab_w.tab_name.setText(i["tab_name"])
                ui_tab_w.layer_name.setText(i["layer_name"])

                preset_setting = data_preset["settings"]
                # 检测这个预设是否在config.json里面
                is_found_preset = False
                for j in range(len(preset_setting)):
                    score = 0
                    model = ""
                    if "model" in preset_setting[j]:
                        model = preset_setting[j]["model"]
                    hd_method = preset_setting[j]["algorithm"]
                    is_hd = preset_setting[j]["continue1"]
                    is_back_ps = preset_setting[j]["continue2"]
                    hotkey1 = preset_setting[j]["hotkey1"]
                    hotkey2 = preset_setting[j]["hotkey2"]
                    hotkey3 = preset_setting[j]["hotkey3"]
                    continue1 = float(preset_setting[j]["interval1"])
                    continue2 = float(preset_setting[j]["interval2"])
                    max_pics = int(preset_setting[j]["max_psi1"])
                    max_hd = int(preset_setting[j]["max_psi2"])
                    name = preset_setting[j]["name"]
                    negative = preset_setting[j]["negative"]
                    positive = preset_setting[j]["positive"]
                    sample = preset_setting[j]["sample"]

                    if i["model"] == model:
                        score += 1
                    if i["hd_method"] == hd_method:
                        score += 1
                    if i["continue1"] == is_hd:
                        score += 1
                    if i["continue2"] == is_back_ps:
                        score += 1
                    if i["hotkey1"] == hotkey1:
                        score += 1
                    if i["hotkey2"] == hotkey2:
                        score += 1
                    if i["hotkey3"] == hotkey3:
                        score += 1
                    if i["interval1"] == continue1:
                        score += 1
                    if i["interval2"] == continue2:
                        score += 1
                    if i["max_pics"] == max_pics:
                        score += 1
                    if i["max_hd"] == max_hd:
                        score += 1
                    if i["name"] == name:
                        score += 1
                    if i["negative"] == negative:
                        score += 1
                    if i["positive"] == positive:
                        score += 1
                    if i["sample"] == sample:
                        score += 1

                    if score == 15:
                        is_found_preset = True
                        ui_tab_w.preset_combo.setCurrentIndex(j)
                # 不在就增加
                if not is_found_preset:
                    new_present = {"model": i["model"],
                                   "algorithm": i["hd_method"],
                                   "continue1": i["continue1"],
                                   "continue2": i["continue2"],
                                   "hotkey1": i["hotkey1"],
                                   "hotkey2": i["hotkey2"],
                                   "hotkey3": i["hotkey3"],
                                   "interval1": i["interval1"],
                                   "interval2": i["interval2"],
                                   "max_psi1": i["max_pics"],
                                   "max_psi2": i["max_hd"],
                                   "name": i["name"],
                                   "negative": i["negative"],
                                   "positive": i["positive"],
                                   "sample": i["sample"]
                                   }
                    preset_setting.append(new_present)
                    data_preset["settings"] = preset_setting
                    with open(os.path.join(BASE_PATH, "config.json"), "w") as f:
                        # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
                        formatted_data = json.dumps(data_preset, indent=4)
                        # 将格式化后的 json 字符串写入新的文件
                        f.write(formatted_data)
                    update_preset(application_list)
                    ui_tab_w.preset_combo.setCurrentIndex(ui_tab_w.preset_combo.count()-1)

                ui_tab_w.add_positive_edit.setText(i["add_positive"])
                ui_tab_w.add_negative_edit.setText(i["add_negative"])
                ui_tab_w.is_use_translate.setChecked(i["is_use_translate"])
                ui_tab_w.paint_weight.setText(i["paint_weight"])
                ui_tab_w.paint_count.setText(i["paint_count"])
                ui_tab_w.webui_url.setText(i["webui_url"])
                ui_tab_w.is_hd.setChecked(i["is_hd"])
                ui_tab_w.hd_weight.setText(i["hd_weight"])

                if i["cn0_enable"]:
                    is_found_preset = False
                    for j in range(len(data_cn)):
                        score = 0
                        enable = data_cn[j]["enable"]
                        name = data_cn[j]["name"]
                        preprocessor = data_cn[j]["preprocessor"]
                        model = data_cn[j]["model"]
                        resolution = data_cn[j]["resolution"]
                        param1 = data_cn[j]["param1"]
                        param2 = data_cn[j]["param2"]
                        pixel_perfect = data_cn[j]["pixel_perfect"]

                        if enable == i["cn0_preset"]["enable"]:
                            score += 1
                        if name == i["cn0_preset"]["name"]:
                            score += 1
                        if preprocessor == i["cn0_preset"]["preprocessor"]:
                            score += 1
                        if model == i["cn0_preset"]["model"]:
                            score += 1
                        if resolution == i["cn0_preset"]["resolution"]:
                            score += 1
                        if param1 == i["cn0_preset"]["param1"]:
                            score += 1
                        if param2 == i["cn0_preset"]["param2"]:
                            score += 1
                        if pixel_perfect == i["cn0_preset"]["pixel_perfect"]:
                            score += 1

                        if score == 8:
                            is_found_preset = True
                            ui_tab_w.cn0_preset.setCurrentIndex(j+1)

                    if not is_found_preset:
                        new_present = {"enable": i["cn0_preset"]["enable"],
                                       "name": i["cn0_preset"]["name"],
                                       "preprocessor": i["cn0_preset"]["preprocessor"],
                                       "model": i["cn0_preset"]["model"],
                                       "resolution": i["cn0_preset"]["resolution"],
                                       "param1": i["cn0_preset"]["param1"],
                                       "param2": i["cn0_preset"]["param2"],
                                       "pixel_perfect": i["cn0_preset"]["pixel_perfect"]
                                       }
                        data_cn.append(new_present)
                        with open(os.path.join(BASE_PATH, "ControlNet.json"), "w") as f:
                            # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
                            formatted_data = json.dumps(data_cn, indent=4)
                            # 将格式化后的 json 字符串写入新的文件
                            f.write(formatted_data)
                        upadate_cn_preset(application_list)
                        ui_tab_w.cn0_preset.setCurrentIndex(ui_tab_w.cn0_preset.count()-1)
                else:
                    ui_tab_w.cn0_preset.setCurrentIndex(0)

                if i["cn1_enable"]:
                    is_found_preset = False
                    for j in range(len(data_cn)):
                        score = 0
                        enable = data_cn[j]["enable"]
                        name = data_cn[j]["name"]
                        preprocessor = data_cn[j]["preprocessor"]
                        model = data_cn[j]["model"]
                        resolution = data_cn[j]["resolution"]
                        param1 = data_cn[j]["param1"]
                        param2 = data_cn[j]["param2"]
                        pixel_perfect = data_cn[j]["pixel_perfect"]

                        if enable == i["cn1_preset"]["enable"]:
                            score += 1
                        if name == i["cn1_preset"]["name"]:
                            score += 1
                        if preprocessor == i["cn1_preset"]["preprocessor"]:
                            score += 1
                        if model == i["cn1_preset"]["model"]:
                            score += 1
                        if resolution == i["cn1_preset"]["resolution"]:
                            score += 1
                        if param1 == i["cn1_preset"]["param1"]:
                            score += 1
                        if param2 == i["cn1_preset"]["param2"]:
                            score += 1
                        if pixel_perfect == i["cn1_preset"]["pixel_perfect"]:
                            score += 1

                        if score == 8:
                            is_found_preset = True
                            ui_tab_w.cn1_preset.setCurrentIndex(j+1)

                    if not is_found_preset:
                        new_present = {"enable": i["cn1_preset"]["enable"],
                                       "name": i["cn1_preset"]["name"],
                                       "preprocessor": i["cn1_preset"]["preprocessor"],
                                       "model": i["cn1_preset"]["model"],
                                       "resolution": i["cn1_preset"]["resolution"],
                                       "param1": i["cn1_preset"]["param1"],
                                       "param2": i["cn1_preset"]["param2"],
                                       "pixel_perfect": i["cn1_preset"]["pixel_perfect"]
                                       }
                        data_cn.append(new_present)
                        with open(os.path.join(BASE_PATH, "ControlNet.json"), "w") as f:
                            # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
                            formatted_data = json.dumps(data_cn, indent=4)
                            # 将格式化后的 json 字符串写入新的文件
                            f.write(formatted_data)
                        upadate_cn_preset(application_list)
                        ui_tab_w.cn1_preset.setCurrentIndex(ui_tab_w.cn1_preset.count()-1)
                else:
                    ui_tab_w.cn1_preset.setCurrentIndex(0)

                if i["cn2_enable"]:
                    is_found_preset = False
                    for j in range(len(data_cn)):
                        score = 0
                        enable = data_cn[j]["enable"]
                        name = data_cn[j]["name"]
                        preprocessor = data_cn[j]["preprocessor"]
                        model = data_cn[j]["model"]
                        resolution = data_cn[j]["resolution"]
                        param1 = data_cn[j]["param1"]
                        param2 = data_cn[j]["param2"]
                        pixel_perfect = data_cn[j]["pixel_perfect"]

                        if enable == i["cn2_preset"]["enable"]:
                            score += 1
                        if name == i["cn2_preset"]["name"]:
                            score += 1
                        if preprocessor == i["cn2_preset"]["preprocessor"]:
                            score += 1
                        if model == i["cn2_preset"]["model"]:
                            score += 1
                        if resolution == i["cn2_preset"]["resolution"]:
                            score += 1
                        if param1 == i["cn2_preset"]["param1"]:
                            score += 1
                        if param2 == i["cn2_preset"]["param2"]:
                            score += 1
                        if pixel_perfect == i["cn2_preset"]["pixel_perfect"]:
                            score += 1

                        if score == 8:
                            is_found_preset = True
                            ui_tab_w.cn2_preset.setCurrentIndex(j+1)

                    if not is_found_preset:
                        new_present = {"enable": i["cn2_preset"]["enable"],
                                       "name": i["cn2_preset"]["name"],
                                       "preprocessor": i["cn2_preset"]["preprocessor"],
                                       "model": i["cn2_preset"]["model"],
                                       "resolution": i["cn2_preset"]["resolution"],
                                       "param1": i["cn2_preset"]["param1"],
                                       "param2": i["cn2_preset"]["param2"],
                                       "pixel_perfect": i["cn2_preset"]["pixel_perfect"]
                                       }
                        data_cn.append(new_present)
                        with open(os.path.join(BASE_PATH, "ControlNet.json"), "w") as f:
                            # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
                            formatted_data = json.dumps(data_cn, indent=4)
                            # 将格式化后的 json 字符串写入新的文件
                            f.write(formatted_data)
                        upadate_cn_preset(application_list)
                        ui_tab_w.cn2_preset.setCurrentIndex(ui_tab_w.cn2_preset.count()-1)
                else:
                    ui_tab_w.cn2_preset.setCurrentIndex(0)

                if i["cn3_enable"]:
                    is_found_preset = False
                    for j in range(len(data_cn)):
                        score = 0
                        enable = data_cn[j]["enable"]
                        name = data_cn[j]["name"]
                        preprocessor = data_cn[j]["preprocessor"]
                        model = data_cn[j]["model"]
                        resolution = data_cn[j]["resolution"]
                        param1 = data_cn[j]["param1"]
                        param2 = data_cn[j]["param2"]
                        pixel_perfect = data_cn[j]["pixel_perfect"]

                        if enable == i["cn3_preset"]["enable"]:
                            score += 1
                        if name == i["cn3_preset"]["name"]:
                            score += 1
                        if preprocessor == i["cn3_preset"]["preprocessor"]:
                            score += 1
                        if model == i["cn3_preset"]["model"]:
                            score += 1
                        if resolution == i["cn3_preset"]["resolution"]:
                            score += 1
                        if param1 == i["cn3_preset"]["param1"]:
                            score += 1
                        if param2 == i["cn3_preset"]["param2"]:
                            score += 1
                        if pixel_perfect == i["cn3_preset"]["pixel_perfect"]:
                            score += 1

                        if score == 8:
                            is_found_preset = True
                            ui_tab_w.cn3_preset.setCurrentIndex(j+1)

                    if not is_found_preset:
                        new_present = {"enable": i["cn3_preset"]["enable"],
                                       "name": i["cn3_preset"]["name"],
                                       "preprocessor": i["cn3_preset"]["preprocessor"],
                                       "model": i["cn3_preset"]["model"],
                                       "resolution": i["cn3_preset"]["resolution"],
                                       "param1": i["cn3_preset"]["param1"],
                                       "param2": i["cn3_preset"]["param2"],
                                       "pixel_perfect": i["cn3_preset"]["pixel_perfect"]
                                       }
                        data_cn.append(new_present)
                        with open(os.path.join(BASE_PATH, "ControlNet.json"), "w") as f:
                            # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
                            formatted_data = json.dumps(data_cn, indent=4)
                            # 将格式化后的 json 字符串写入新的文件
                            f.write(formatted_data)
                        upadate_cn_preset(application_list)
                        ui_tab_w.cn3_preset.setCurrentIndex(ui_tab_w.cn3_preset.count()-1)
                else:
                    ui_tab_w.cn3_preset.setCurrentIndex(0)
                ui_tab_w.lama_url.setText(i["lama_url"])
                Main_w.add_tab(ui_tab_w,tab_w)
    except FileNotFoundError:
        data = None
