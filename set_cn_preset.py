import json
import os
import sys
import traceback

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QMessageBox
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

import set_controlnet
from sd_tools import open_driver
from update_combo import upadate_cn_preset


def set_cn_win(QMainWindow, current_index, application_list,small_application=None):
    QMainWindow.set_cn_w = QtWidgets.QWidget()
    QMainWindow.ui_set_w = set_controlnet.Ui_Form()
    QMainWindow.ui_set_w.setupUi(QMainWindow.set_cn_w)
    QMainWindow.set_cn_w.setWindowTitle("预设设置")
    QMainWindow.set_cn_w.setWindowFlags(QMainWindow.windowFlags())
    QMainWindow.set_cn_w.show()

    # 控制参数、分辨率的输入范围
    QMainWindow.ui_set_w.layer_name_4.setValidator(QIntValidator(0, 9999999))
    QMainWindow.ui_set_w.layer_name_5.setValidator(QDoubleValidator(0.0, 9999999.0, 2))
    QMainWindow.ui_set_w.layer_name_6.setValidator(QDoubleValidator(0.0, 9999999.0, 2))

    # 设置当前预设页面
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "ControlNet.json"), "r") as f:
        preset_list = json.load(f)
    all_preset_name = []
    for i in preset_list:
        all_preset_name.append(i["name"])
    QMainWindow.ui_set_w.preset_combo.addItems(all_preset_name)
    QMainWindow.ui_set_w.preset_combo.setCurrentIndex(current_index - 1)

    def preset_combo_Activated():
        QMainWindow.ui_set_w.layer_name.setText(
            preset_list[QMainWindow.ui_set_w.preset_combo.currentIndex()]["name"])
        QMainWindow.ui_set_w.layer_name_2.setText(
            preset_list[QMainWindow.ui_set_w.preset_combo.currentIndex()]["preprocessor"])
        QMainWindow.ui_set_w.layer_name_3.setText(
            preset_list[QMainWindow.ui_set_w.preset_combo.currentIndex()]["model"])
        QMainWindow.ui_set_w.layer_name_4.setText(
            str(preset_list[QMainWindow.ui_set_w.preset_combo.currentIndex()]["resolution"]))
        QMainWindow.ui_set_w.layer_name_5.setText(
            str(preset_list[QMainWindow.ui_set_w.preset_combo.currentIndex()]["param1"]))
        QMainWindow.ui_set_w.layer_name_6.setText(
            str(preset_list[QMainWindow.ui_set_w.preset_combo.currentIndex()]["param2"]))
        QMainWindow.ui_set_w.checkBox.setChecked(
            preset_list[QMainWindow.ui_set_w.preset_combo.currentIndex()]["enable"])
        QMainWindow.ui_set_w.checkBox_2.setChecked(
            preset_list[QMainWindow.ui_set_w.preset_combo.currentIndex()]["pixel_perfect"])

    preset_combo_Activated()
    QMainWindow.ui_set_w.preset_combo.activated.connect(preset_combo_Activated)

    cn_list = []
    cn_show_list = []
    all_pre = []
    all_model = []

    def on_pre_Activated():
        QMainWindow.ui_set_w.layer_name_2.setText(QMainWindow.ui_set_w.import_combo.currentText())

    def on_model_Activated():
        QMainWindow.ui_set_w.layer_name_3.setText(QMainWindow.ui_set_w.import_combo_2.currentText())

    def onActivated():
        now_index = QMainWindow.ui_set_w.controlnet_layer.currentIndex()
        QMainWindow.ui_set_w.checkBox.setChecked(cn_list[now_index]["is_enable"])
        QMainWindow.ui_set_w.checkBox_2.setChecked(cn_list[now_index]["is_perfect_piexl"])
        QMainWindow.ui_set_w.layer_name_2.setText(cn_list[now_index]["preprocessor"])
        QMainWindow.ui_set_w.layer_name_3.setText(cn_list[now_index]["model"])
        QMainWindow.ui_set_w.layer_name_4.setText(cn_list[now_index]["resolution"])
        QMainWindow.ui_set_w.layer_name_5.setText(cn_list[now_index]["param1"])
        QMainWindow.ui_set_w.layer_name_6.setText(cn_list[now_index]["param2"])
        QMainWindow.ui_set_w.import_combo.clear()
        QMainWindow.ui_set_w.import_combo.addItems(all_pre)
        QMainWindow.ui_set_w.import_combo.setCurrentIndex(0)
        QMainWindow.ui_set_w.import_combo.activated.connect(on_pre_Activated)
        QMainWindow.ui_set_w.import_combo_2.clear()
        QMainWindow.ui_set_w.import_combo_2.addItems(all_model)
        QMainWindow.ui_set_w.import_combo_2.setCurrentIndex(0)
        QMainWindow.ui_set_w.import_combo_2.activated.connect(on_model_Activated)

    def import_from_page():
        # 先定位url
        driver = open_driver()
        url = application_list[QMainWindow.ui.tabWidget.currentIndex()].webui_url.text()
        found = False
        for handle in driver.window_handles:
            # 切换到该标签页
            driver.switch_to.window(handle)
            # 检查网址是否相符
            if url in driver.current_url:
                # 找到相符的标签页，在标签页进行执行
                found = True
                break
        # 找到了标签页，在标签页运行.
        if found:
            # 找到全部controlnet按钮
            button_tabs = driver.find_element(By.XPATH, f"//*[@id=\"img2img_controlnet_tabs\"]/div[1]")
            cn_num = button_tabs.find_elements(By.TAG_NAME, "button")
            cn_list.clear()
            cn_show_list.clear()

            # 预处理器列表
            preprocessor = driver.find_element(By.XPATH,
                                               f"//*[@id=\"img2img_controlnet_ControlNet-0_controlnet_preprocessor_dropdown\"]/label/div")
            preprocessor.click()
            all_pre.clear()
            ul = preprocessor.find_elements(By.TAG_NAME, "li")
            for li in ul:
                data = li.text.replace("✓\n", "")
                all_pre.append(data)
            driver.find_element(By.XPATH,
                                f"//*[@id=\"img2img_controlnet_ControlNet-0_controlnet_preprocessor_dropdown\"]/label/div/div[1]/div/input").send_keys(
                Keys.ENTER)

            # 模型列表
            model = driver.find_element(By.XPATH,
                                        f"//*[@id=\"img2img_controlnet_ControlNet-0_controlnet_model_dropdown\"]/label/div")
            model.click()
            all_model.clear()
            ul = model.find_elements(By.TAG_NAME, "li")
            for li in ul:
                data = li.text.replace("✓\n", "")
                all_model.append(data)
            driver.find_element(By.XPATH,
                                f"//*[@id=\"img2img_controlnet_ControlNet-0_controlnet_model_dropdown\"]/label/div/div[1]/div/input").send_keys(
                Keys.ENTER)

            for i in range(len(cn_num)):
                cn_show_list.append(f"controlnet-{i}")
                cn_map = {}
                driver.find_element(By.XPATH, f"//*[@id=\"img2img_controlnet_tabs\"]/div[1]/button[{i + 1}]").click()
                # 找到是否启用
                cn_map["is_enable"] = driver.find_element(By.XPATH,
                                                          f"//*[@id=\"img2img_controlnet_ControlNet-{i}_controlnet_enable_checkbox\"]/label/input").is_selected()
                # 找到是否完美像素
                cn_map["is_perfect_piexl"] = driver.find_element(By.XPATH,
                                                                 f"//*[@id=\"img2img_controlnet_ControlNet-{i}_controlnet_pixel_perfect_checkbox\"]/label/input").is_selected()
                # 找到预处理器
                cn_map["preprocessor"] = driver.find_element(By.XPATH,
                                                             f"//*[@id=\"img2img_controlnet_ControlNet-{i}_controlnet_preprocessor_dropdown\"]/label/div/div[1]/div/input").get_attribute(
                    "value")
                # 找到controlnet模型
                cn_map["model"] = driver.find_element(By.XPATH,
                                                      f"//*[@id=\"img2img_controlnet_ControlNet-{i}_controlnet_model_dropdown\"]/label/div/div[1]/div/input").get_attribute(
                    "value")
                # 找到参数
                try:
                    cn_map["resolution"] = driver.find_element(By.XPATH,
                                                               f"//*[@id=\"img2img_controlnet_ControlNet-{i}_controlnet_preprocessor_resolution_slider\"]/div[2]/div/input").get_attribute(
                        "value")
                except:
                    cn_map["resolution"] = ""
                try:
                    cn_map["param1"] = driver.find_element(By.XPATH,
                                                           f"//*[@id=\"img2img_controlnet_ControlNet-{i}_controlnet_threshold_A_slider\"]/div[2]/div/input").get_attribute(
                        "value")
                except:
                    cn_map["param1"] = ""
                try:
                    cn_map["param2"] = driver.find_element(By.XPATH,
                                                           f"//*[@id=\"img2img_controlnet_ControlNet-{i}_controlnet_threshold_B_slider\"]/div[2]/div/input").get_attribute(
                        "value")
                except:
                    cn_map["param2"] = ""
                cn_list.append(cn_map)
            driver.find_element(By.XPATH, f"//*[@id=\"img2img_controlnet_tabs\"]/div[1]/button[1]").click()
            QMainWindow.ui_set_w.controlnet_layer.clear()
            QMainWindow.ui_set_w.controlnet_layer.addItems(cn_show_list)
            QMainWindow.ui_set_w.controlnet_layer.setCurrentIndex(0)
            onActivated()
        else:
            raise ValueError("没找到指定的url页面，请确保webui url页面已经打开")

    def show_message_box(text):
        message_box = QMessageBox(QMainWindow)
        message_box.setIcon(QMessageBox.Information)
        message_box.setText(text)
        message_box.setWindowTitle("提示")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()

    def save_set():
        now_index = QMainWindow.ui_set_w.preset_combo.currentIndex()
        name = QMainWindow.ui_set_w.layer_name.text()
        is_enable = QMainWindow.ui_set_w.checkBox.isChecked()
        is_perfect_piexl = QMainWindow.ui_set_w.checkBox_2.isChecked()
        preprocessor = QMainWindow.ui_set_w.layer_name_2.text()
        model = QMainWindow.ui_set_w.layer_name_3.text()
        resolution = QMainWindow.ui_set_w.layer_name_4.text()
        if resolution != "":
            resolution = int(resolution)
        param1 = QMainWindow.ui_set_w.layer_name_5.text()
        if param1 != "":
            if "." in param1:
                param1 = float(param1)
            else:
                param1 = int(param1)
        param2 = QMainWindow.ui_set_w.layer_name_6.text()
        if param2 != "":
            if "." in param2:
                param2 = float(param2)
            else:
                param2 = int(param2)
        try:
            BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
            with open(os.path.join(BASE_PATH, "ControlNet.json"), "r") as f:
                data = json.load(f)
                new_present = {"enable": is_enable,
                               "name": name,
                               "preprocessor": preprocessor,
                               "model": model,
                               "resolution": resolution,
                               "param1": param1,
                               "param2": param2,
                               "pixel_perfect": is_perfect_piexl,
                               }
                data[now_index] = new_present
            with open(os.path.join(BASE_PATH, "ControlNet.json"), "w") as f:
                # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
                formatted_data = json.dumps(data, indent=4)
                # 将格式化后的 json 字符串写入新的文件
                f.write(formatted_data)
            upadate_cn_preset(application_list)
            if small_application:
                upadate_cn_preset(small_application)
            show_message_box("修改完成")
            # update_all_ctn(notebook=notebook, application_list=application_list)
            QMainWindow.set_cn_w.destroy()
        except Exception as e:
            traceback.print_exc()
            show_message_box("修改失败")

    QMainWindow.ui_set_w.controlnet_layer.activated.connect(onActivated)
    QMainWindow.ui_set_w.pushButton.clicked.connect(
        lambda: save_set())
    QMainWindow.ui_set_w.pushButton_2.clicked.connect(
        lambda: import_from_page())
