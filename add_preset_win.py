import json
import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QMessageBox
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

import add_controlnet
import add_preset
from sd_tools import open_driver
from update_combo import upadate_cn_preset, update_preset


def add_preset_win(QMainWindow,application_list,small_application=None):
    QMainWindow.add_w = QtWidgets.QWidget()
    QMainWindow.ui_add_w = add_preset.Ui_Form()
    QMainWindow.ui_add_w.setupUi(QMainWindow.add_w)
    QMainWindow.add_w.setWindowTitle("预设设置")
    QMainWindow.add_w.setWindowFlags(QMainWindow.windowFlags())
    QMainWindow.add_w.show()

    # 控制参数、分辨率的输入范围
    QMainWindow.ui_add_w.max_pics.setValidator(QIntValidator(0, 9999999))
    QMainWindow.ui_add_w.max_hd.setValidator(QIntValidator(0, 9999999))
    QMainWindow.ui_add_w.continue1.setValidator(QDoubleValidator(0.0, 9999999.0, 2))
    QMainWindow.ui_add_w.continue2.setValidator(QDoubleValidator(0.0, 9999999.0, 2))

    all_model=[]
    all_sample=[]
    all_sd=[]

    def on_model_Activated():
        QMainWindow.ui_add_w.model_name.setText(QMainWindow.ui_add_w.import_combo.currentText())

    def on_sample_Activated():
        QMainWindow.ui_add_w.sample_method.setText(QMainWindow.ui_add_w.import_combo_2.currentText())

    def on_hd_Activated():
        QMainWindow.ui_add_w.hd_method.setText(QMainWindow.ui_add_w.import_combo_3.currentText())

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
            #找到所有model模型
            model_input = driver.find_element(By.XPATH, f"//*[@id=\"setting_sd_model_checkpoint\"]/label/div/div[1]/div/input")
            model_parent=driver.find_element(By.XPATH, f"//*[@id=\"setting_sd_model_checkpoint\"]/label/div")
            model_now=model_input.get_attribute("value")
            model_input.click()
            all_model.clear()

            ul = model_parent.find_elements(By.TAG_NAME, "li")
            for li in ul:
                data = li.text.replace("✓\n", "")
                all_model.append(data)
            QMainWindow.ui_add_w.model_name.setText(model_now)
            QMainWindow.ui_add_w.import_combo.clear()
            QMainWindow.ui_add_w.import_combo.addItems(all_model)
            QMainWindow.ui_add_w.import_combo.setCurrentIndex(0)

            #找到所有采样器
            try:
                #云端
                sample_parent=driver.find_element(By.XPATH, "//*[@id=\"img2img_sampling\"]/label/div")
                sample_input=driver.find_element(By.XPATH, "//*[@id=\"img2img_sampling\"]/label/div/div[1]/div/input")
                sample_now=sample_input.get_attribute("value")
                sample_input.click()
                all_sample.clear()


                ul = sample_parent.find_elements(By.TAG_NAME, "li")
                for li in ul:
                    data = li.text.replace("✓\n", "")
                    all_sample.append(data)
            except:
                #本地
                element = driver.find_element(By.XPATH, '//*[@id="img2img_sampling"]')
                labels = element.find_elements(By.XPATH, './/label')
                all_sample.clear()
                for label in labels:
                    # 在这里执行你想要的操作
                    all_sample.append(label.text)
                    if label.find_element(By.TAG_NAME,'input').is_selected():
                        sample_now=label.text
            driver.find_element(By.XPATH, "//*[@id=\"img2img_steps\"]/div[2]/div/input").send_keys(Keys.ENTER)
            QMainWindow.ui_add_w.sample_method.setText(sample_now)
            QMainWindow.ui_add_w.import_combo_2.clear()
            QMainWindow.ui_add_w.import_combo_2.addItems(all_sample)
            QMainWindow.ui_add_w.import_combo_2.setCurrentIndex(0)

            #正向提示词
            positive=driver.find_element(By.XPATH, "//*[@id=\"img2img_prompt\"]/label/textarea").get_attribute("value")
            QMainWindow.ui_add_w.positive.setText(positive)
            #负向提示词
            negative=driver.find_element(By.XPATH, "//*[@id=\"img2img_neg_prompt\"]/label/textarea").get_attribute("value")
            QMainWindow.ui_add_w.negative.setText(negative)

            #放大算法
            element_img2img = driver.find_element(By.XPATH, "//*[@id=\"img2img_script_container\"]")
            element_script_list = element_img2img.find_element(By.ID,
                                                               "script_list")
            element = element_script_list.find_element(By.TAG_NAME, "input")
            is_open=True
            #先看sd放大是否打开
            if "None" in element.get_attribute("value"):
                element.clear()
                element.send_keys("SD upscale")
                element.send_keys(Keys.ENTER)
                is_open=False
            hd_use = driver.find_element(By.XPATH, f"//*[@id=\"script_sd_upscale_upscaler_index\"]")
            hd_list = hd_use.find_elements(By.TAG_NAME, "label")
            all_sd.clear()
            for hd_temp in hd_list:
                all_sd.append(hd_temp.text)
                if hd_temp.find_element(By.TAG_NAME,'input').is_selected():
                    sd_now=hd_temp.text
            #如果没有打开要关上
            if not is_open:
                element.clear()
                element.send_keys("None")
                element.send_keys(Keys.ENTER)
            driver.find_element(By.XPATH, "//*[@id=\"img2img_steps\"]/div[2]/div/input").send_keys(Keys.ENTER)
            QMainWindow.ui_add_w.hd_method.setText(sd_now)
            QMainWindow.ui_add_w.import_combo_3.clear()
            QMainWindow.ui_add_w.import_combo_3.addItems(all_sd)
            QMainWindow.ui_add_w.import_combo_3.setCurrentIndex(0)

            QMainWindow.ui_add_w.import_combo.activated.connect(on_model_Activated)
            QMainWindow.ui_add_w.import_combo_2.activated.connect(on_sample_Activated)
            QMainWindow.ui_add_w.import_combo_3.activated.connect(on_hd_Activated)
        else:
            raise ValueError("没找到指定的url页面，请确保webui url页面已经打开")

    def show_message_box(text):
        message_box = QMessageBox(QMainWindow)
        message_box.setIcon(QMessageBox.Information)
        message_box.setText(text)
        message_box.setWindowTitle("提示")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()

    #确认后执行的方法
    def confirm():
        name=QMainWindow.ui_add_w.layer_name.text()
        model=QMainWindow.ui_add_w.model_name.text()
        sample=QMainWindow.ui_add_w.sample_method.text()
        positive=QMainWindow.ui_add_w.positive.text()
        negative=QMainWindow.ui_add_w.negative.text()
        max_pics=QMainWindow.ui_add_w.max_pics.text()
        max_hd=QMainWindow.ui_add_w.max_hd.text()
        continue1=QMainWindow.ui_add_w.continue1.text()
        continue2=QMainWindow.ui_add_w.continue2.text()
        short_key1=QMainWindow.ui_add_w.short_key1.text()
        short_key2=QMainWindow.ui_add_w.short_key2.text()
        short_key3=QMainWindow.ui_add_w.short_key3.text()
        hd_method=QMainWindow.ui_add_w.hd_method.text()
        is_hd=QMainWindow.ui_add_w.is_hd.isChecked()
        is_back_ps=QMainWindow.ui_add_w.is_back_ps.isChecked()

        try:
            BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
            with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
                data = json.load(f)
                setting = data["settings"]
                new_present = {"model": model,
                               "algorithm": hd_method,
                               "continue1": is_hd,
                               "continue2": is_back_ps,
                               "hotkey1": short_key1,
                               "hotkey2": short_key2,
                               "hotkey3": short_key3,
                               "interval1": float(continue2),
                               "interval2": float(continue1),
                               "max_psi1": int(max_pics),
                               "max_psi2": int(max_hd),
                               "name": name,
                               "negative": negative,
                               "positive": positive,
                               "sample": sample
                               }
                setting.append(new_present)
                data["settings"] = setting
            with open(os.path.join(BASE_PATH, "config.json"), "w") as f:
                # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
                formatted_data = json.dumps(data, indent=4)
                # 将格式化后的 json 字符串写入新的文件
                f.write(formatted_data)
            update_preset(application_list)
            if small_application:
                update_preset(small_application)
            show_message_box("修改完成")
            QMainWindow.add_w.destroy()
        except Exception as e:
            show_message_box("修改失败")

    QMainWindow.ui_add_w.check_btn.clicked.connect(
        lambda: confirm())
    QMainWindow.ui_add_w.import_btn.clicked.connect(
        lambda: import_from_page())

    QMainWindow.add_w.show()

def add_cn_preset_win(QMainWindow,application_list,small_application=None):
    QMainWindow.add_cn_w = QtWidgets.QWidget()
    QMainWindow.ui_add_cn_w = add_controlnet.Ui_Form()
    QMainWindow.ui_add_cn_w.setupUi(QMainWindow.add_cn_w)
    QMainWindow.add_cn_w.setWindowTitle("controlnet预设设置")
    QMainWindow.add_cn_w.setWindowFlags(QMainWindow.windowFlags())
    QMainWindow.add_cn_w.show()

    # 控制参数、分辨率的输入范围
    QMainWindow.ui_add_cn_w.layer_name_4.setValidator(QIntValidator(1, 9999999))
    QMainWindow.ui_add_cn_w.layer_name_5.setValidator(QDoubleValidator(0.0, 9999999.0, 2))
    QMainWindow.ui_add_cn_w.layer_name_6.setValidator(QDoubleValidator(0.0, 9999999.0, 2))

    cn_list = []
    cn_show_list = []
    all_pre = []
    all_model = []

    def on_pre_Activated():
        QMainWindow.ui_add_cn_w.layer_name_2.setText(QMainWindow.ui_add_cn_w.import_combo.currentText())

    def on_model_Activated():
        QMainWindow.ui_add_cn_w.layer_name_3.setText(QMainWindow.ui_add_cn_w.import_combo_2.currentText())

    def onActivated():
        now_index = QMainWindow.ui_add_cn_w.controlnet_layer.currentIndex()
        QMainWindow.ui_add_cn_w.checkBox.setChecked(cn_list[now_index]["is_enable"])
        QMainWindow.ui_add_cn_w.checkBox_2.setChecked(cn_list[now_index]["is_perfect_piexl"])
        QMainWindow.ui_add_cn_w.layer_name_2.setText(cn_list[now_index]["preprocessor"])
        QMainWindow.ui_add_cn_w.layer_name_3.setText(cn_list[now_index]["model"])
        QMainWindow.ui_add_cn_w.layer_name_4.setText(cn_list[now_index]["resolution"])
        QMainWindow.ui_add_cn_w.layer_name_5.setText(cn_list[now_index]["param1"])
        QMainWindow.ui_add_cn_w.layer_name_6.setText(cn_list[now_index]["param2"])
        QMainWindow.ui_add_cn_w.import_combo.clear()
        QMainWindow.ui_add_cn_w.import_combo.addItems(all_pre)
        QMainWindow.ui_add_cn_w.import_combo.setCurrentIndex(0)
        QMainWindow.ui_add_cn_w.import_combo.activated.connect(on_pre_Activated)
        QMainWindow.ui_add_cn_w.import_combo_2.clear()
        QMainWindow.ui_add_cn_w.import_combo_2.addItems(all_model)
        QMainWindow.ui_add_cn_w.import_combo_2.setCurrentIndex(0)
        QMainWindow.ui_add_cn_w.import_combo_2.activated.connect(on_model_Activated)

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
            QMainWindow.ui_add_cn_w.controlnet_layer.clear()
            QMainWindow.ui_add_cn_w.controlnet_layer.addItems(cn_show_list)
            QMainWindow.ui_add_cn_w.controlnet_layer.setCurrentIndex(0)
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
        name = QMainWindow.ui_add_cn_w.layer_name.text()
        is_enable = QMainWindow.ui_add_cn_w.checkBox.isChecked()
        is_perfect_piexl = QMainWindow.ui_add_cn_w.checkBox_2.isChecked()
        preprocessor = QMainWindow.ui_add_cn_w.layer_name_2.text()
        model = QMainWindow.ui_add_cn_w.layer_name_3.text()
        resolution = QMainWindow.ui_add_cn_w.layer_name_4.text()
        if resolution != "":
            resolution = int(resolution)
        param1 = QMainWindow.ui_add_cn_w.layer_name_5.text()
        if param1 != "":
            if "." in param1:
                param1 = float(param1)
            else:
                param1 = int(param1)
        param2 = QMainWindow.ui_add_cn_w.layer_name_6.text()
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
                data.append(new_present)
            with open(os.path.join(BASE_PATH, "ControlNet.json"), "w") as f:
                # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
                formatted_data = json.dumps(data, indent=4)
                # 将格式化后的 json 字符串写入新的文件
                f.write(formatted_data)
            upadate_cn_preset(application_list)
            if small_application:
                upadate_cn_preset(small_application)
            show_message_box("增加预设完成")
            # update_all_ctn(notebook=notebook, application_list=application_list)
            QMainWindow.add_cn_w.destroy()
        except Exception as e:
            show_message_box("增加预设失败")

    QMainWindow.ui_add_cn_w.controlnet_layer.activated.connect(onActivated)
    QMainWindow.ui_add_cn_w.pushButton.clicked.connect(
        lambda: save_set())
    QMainWindow.ui_add_cn_w.pushButton_2.clicked.connect(
        lambda: import_from_page())