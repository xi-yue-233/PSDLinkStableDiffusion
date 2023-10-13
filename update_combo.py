import json
import os
import sys


def update_preset(application_list):
    #刷新所有tab的预设层
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
        now_preset = data["setting_index"]
        preset_list = data["settings"]
    all_preset_name = []
    for i in preset_list:
        all_preset_name.append(i["name"])
    for i in application_list:
        origin_index=i.preset_combo.currentIndex()
        i.preset_combo.clear()
        i.preset_combo.addItems(all_preset_name)
        i.preset_combo.setCurrentIndex(origin_index)

def upadate_cn_preset(application_list):
    # 刷新所有tab的cn层
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "ControlNet.json"), "r") as f:
        data_control = json.load(f)
    cn_list = []
    cn_list.append("无")
    for i in data_control:
        cn_list.append(i["name"])
    for i in application_list:
        origin_index=i.cn0_preset.currentIndex()
        i.cn0_preset.clear()
        i.cn0_preset.addItems(cn_list)
        i.cn0_preset.setCurrentIndex(origin_index)
        try:
            origin_index=i.cn1_preset.currentIndex()
            i.cn1_preset.clear()
            i.cn1_preset.addItems(cn_list)
            i.cn1_preset.setCurrentIndex(origin_index)

            origin_index=i.cn2_preset.currentIndex()
            i.cn2_preset.clear()
            i.cn2_preset.addItems(cn_list)
            i.cn2_preset.setCurrentIndex(origin_index)

            origin_index=i.cn3_preset.currentIndex()
            i.cn3_preset.clear()
            i.cn3_preset.addItems(cn_list)
            i.cn3_preset.setCurrentIndex(origin_index)
        except:
            pass