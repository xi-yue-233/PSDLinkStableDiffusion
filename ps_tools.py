import os
import sys
import time
import re
from _ctypes import COMError
from datetime import datetime

import photoshop.api as ps
import pythoncom
from photoshop import Session
from PIL import Image
import json
from importlib import reload
import requests
import hashlib
import uuid

#翻译
reload(sys)

# 读取配置文件
def load_config():
    try:
        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        config_path = os.path.join(BASE_PATH, "config.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("错误：找不到config.json文件，请确保配置文件存在")
        sys.exit(1)
    except json.JSONDecodeError:
        print("错误：config.json格式不正确")
        sys.exit(1)

config = load_config()
YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = config['youdao']['app_key']
APP_SECRET = config['youdao']['app_secret']
VOCAB_ID = config['youdao']['vocab_id']


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def translate_api(text):
    # 构建请求
    data = {}
    q = text
    
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    data['vocabId'] = VOCAB_ID

    response = requests.post(YOUDAO_URL, data=data)
    contentType = response.headers['Content-Type']
    return response.json().get("translation")[0]


#加权
def update_first_word(text):
    # 检查文本中使用的分隔符是英文逗号还是中文逗号
    if '，' in text:
        delimiter = '，'
    else:
        delimiter = ','

    # 按照相应的分隔符分割文本
    words = text.split(delimiter)

    # 检查第一个单词是否已经是（单词:数字）或(单词:数字)的形式
    first_word = words[0].strip()

    # 匹配全角括号或半角括号的形式
    match_full = re.match(r'^\（([^：]+)：(\d+\.\d+)\）$', first_word)  # 全角括号
    match_full_half = re.match(r'^\（([^：]+):(\d+\.\d+)\）$', first_word)  # 全角括号
    match_half = re.match(r'^\(([^:]+):(\d+\.\d+)\)$', first_word)  # 半角括号

    if match_full:
        # 如果是全角括号的形式，提取单词和数字，并将数字加0.1
        word = match_full.group(1)
        number = float(match_full.group(2)) + 0.1
        new_first_word = f"?({word}:{number:.1f})"
    elif match_full_half:
        # 如果是半角括号的形式，提取单词和数字，并将数字加0.1
        word = match_full_half.group(1)
        number = float(match_full_half.group(2)) + 0.1
        new_first_word = f"({word}:{number:.1f})"
    elif match_half:
        # 如果是半角括号的形式，提取单词和数字，并将数字加0.1
        word = match_half.group(1)
        number = float(match_half.group(2)) + 0.1
        new_first_word = f"({word}:{number:.1f})"
    else:
        # 如果不是这种形式，将其转换为（单词:0.1）的形式，使用全角括号
        new_first_word = f"({first_word}:0.1)"

    # 将更新后的第一个单词放回文本中
    words[0] = new_first_word
    # 重新组合文本，使用原来的分隔符
    updated_text = delimiter.join(words)

    return updated_text

# 定位ps
def start_ps():
    app = ps.Application()
    return app

#执行动作
def execute_action(action_name,group_name):
    pythoncom.CoInitialize()  # 初始化com环境
    try:
        with Session() as ps:
            desc69=ps.ActionDescriptor
            ref22=ps.ActionReference
            idactn=ps.app.charIDToTypeID('Actn')
            ref22.putName(idactn,action_name)
            ref22.putName(ps.app.charIDToTypeID("ASet"),group_name)
            desc69.putReference(ps.app.charIDToTypeID("null"),ref22)
            try:
                ps.app.executeAction(ps.app.charIDToTypeID("Ply "),desc69,ps.DialogModes.DisplayNoDialogs)
            except COMError:
                BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
                os.system('chcp 65001')
                os.system(f"cd {BASE_PATH} && start PSDLink动作.atn")
                print("发现未导入动作，导入动作")
                time.sleep(1.5)
                ps.app.executeAction(ps.app.charIDToTypeID("Ply "), desc69, ps.DialogModes.DisplayNoDialogs)
    finally:
        pythoncom.CoInitialize()  # 初始化com环境

# 自动匹配ps文档和tabs文档名
def auto_doc_name(application,small_application=None):
    app = start_ps()
    documents = app.documents
    doc_name = []
    doc_small = []
    for document in documents:
        if document.name.startswith("AI导出"):
            doc_name.append(document.name)
            doc_small.append(document.name)
    for i in application:
        i.layer_name.setText(doc_name[0].replace(".psd", "").replace(".psb", ""))
        if len(doc_name) > 1:
            doc_name.pop(0)
    if small_application:
        for i in small_application:
            i.layer_name.setText(doc_small[0].replace(".psd", "").replace(".psb", ""))
            if len(doc_small) > 1:
                doc_small.pop(0)
    print("已自动将全部任务的文档名命名完成")


# 导出当前ps图片
def export_image_from_ps(app, document_name):
    now = datetime.now()
    now_long = int(now.timestamp())
    documents = app.documents
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_PS")
    options = ps.JPEGSaveOptions()
    options.quality = 5
    options.embedColorProfile = True
    if not os.path.exists(EXPORT_PATH):
        os.mkdir(EXPORT_PATH)
    # 循环查找指定的文档名
    for document in documents:
        if document_name == document.name[0:len(document_name)]:
            document.saveAs(os.path.join(EXPORT_PATH, document_name + f"-{now_long}.jpg"), options)
            return os.path.join(EXPORT_PATH, document_name + f"-{now_long}.jpg"), document_name + f"-{now_long}"
    # 如果没找到指定文档，则默认以当前文档导出
    app.activeDocument.saveAs(os.path.join(EXPORT_PATH, app.activeDocument.name + f"-{now_long}.jpg"), options)
    return os.path.join(EXPORT_PATH,
                        app.activeDocument.name + f"-{now_long}.jpg"), app.activeDocument.name + f"-{now_long}"


# 以当前激活图层导出当前ps图片
def short_key_export_image_from_ps(app):
    now = datetime.now()
    now_long = int(now.timestamp())
    documents = app.documents
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_PS")
    options = ps.JPEGSaveOptions()
    options.quality = 5
    options.embedColorProfile = True
    if not os.path.exists(EXPORT_PATH):
        os.mkdir(EXPORT_PATH)
    app.activeDocument.saveAs(os.path.join(EXPORT_PATH, app.activeDocument.name + f"-{now_long}.jpg"), options)
    return os.path.join(EXPORT_PATH,
                        app.activeDocument.name + f"-{now_long}.jpg"), app.activeDocument.name + f"-{now_long}"


# 从sd导回图片
def import_image_from_sd(app, img_name, count):
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_SD")
    documents = app.documents
    document_name = img_name.split("-")[0]
    # 循环查找指定的文档名
    for document in documents:
        if document_name == document.name[0:len(document_name)]:
            # 获取文档的宽度和高度
            doc_width = document.width
            doc_height = document.height
            for i in range(1, count + 1):
                # 打开你要导入的图片
                img_path = os.path.join(EXPORT_PATH, f"{img_name}-{i}.jpg")
                img = Image.open(img_path)
                # 调整图片的宽度和高度，使它们与文档相同
                img = img.resize((int(doc_width), int(doc_height)))
                # 保存图片为一个临时文件
                img.save(f"{img_name}-{i}.jpg")
                # 打开的psd文件
                with Session(document.path) as ps:
                    desc = ps.ActionDescriptor
                    # 要打开的图像
                    desc.putPath(ps.app.charIDToTypeID("null"), os.path.join(BASE_PATH, f"{img_name}-{i}.jpg"))
                    ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)
                # 将临时文件放置到图层中
                os.remove(f"{img_name}-{i}.jpg")
            return
    # 如果没找到，以当前激活的文档导入
    # 获取文档的宽度和高度
    doc_width = app.activeDocument.width
    doc_height = app.activeDocument.height
    for i in range(1, count + 1):
        # 打开你要导入的图片
        img_path = os.path.join(EXPORT_PATH, f"{img_name}-{i}.jpg")
        img = Image.open(img_path)
        # 调整图片的宽度和高度，使它们与文档相同
        img = img.resize((int(doc_width), int(doc_height)))
        # 保存图片为一个临时文件
        img.save(f"{img_name}-{i}.jpg")
        # 打开的psd文件
        with Session(app.activeDocument.path) as ps:
            desc = ps.ActionDescriptor
            # 要打开的图像
            desc.putPath(ps.app.charIDToTypeID("null"), os.path.join(BASE_PATH, f"{img_name}-{i}.jpg"))
            ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)
        # 将临时文件放置到图层中
        os.remove(f"{img_name}-{i}.jpg")


# 以当前激活图层从sd导回图片
def short_key_import_image_from_sd(app, img_name, count):
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_SD")
    # 获取文档的宽度和高度
    doc_width = app.activeDocument.width
    doc_height = app.activeDocument.height
    for i in range(1, count + 1):
        # 打开你要导入的图片
        img_path = os.path.join(EXPORT_PATH, f"{img_name}-{i}.jpg")
        img = Image.open(img_path)
        # 调整图片的宽度和高度，使它们与文档相同
        img = img.resize((int(doc_width), int(doc_height)))
        # 保存图片为一个临时文件
        img.save(f"{img_name}-{i}.jpg")
        # 打开的psd文件
        with Session(app.activeDocument.path) as ps:
            desc = ps.ActionDescriptor
            # 要打开的图像
            desc.putPath(ps.app.charIDToTypeID("null"), os.path.join(BASE_PATH, f"{img_name}-{i}.jpg"))
            ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)
        os.remove(f"{img_name}-{i}.jpg")


# 导出当前controlnet图片
def export_controlnet_image_from_ps(app, document_name):
    now = datetime.now()
    now_long = int(now.timestamp())
    documents = app.documents
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_PS")
    options = ps.JPEGSaveOptions()
    options.quality = 5
    options.embedColorProfile = True
    if not os.path.exists(EXPORT_PATH):
        os.mkdir(EXPORT_PATH)
    # 循环查找指定的文档名
    for document in documents:
        if document_name == document.name[0:len(document_name)]:
            document.saveAs(os.path.join(EXPORT_PATH, document_name + f"-{now_long}" + "-controlnet.jpg"), options)
            return os.path.join(EXPORT_PATH, document_name + f"-{now_long}" + "-controlnet.jpg")
    # 如果没找到指定文档，则默认以当前文档导出
    app.activeDocument.saveAs(os.path.join(EXPORT_PATH, app.activeDocument.name + f"-{now_long}.jpg"), options)
    return os.path.join(EXPORT_PATH, app.activeDocument.name + f"-{now_long}" + "-controlnet.jpg")

# app = start_ps()
# import_image_from_sd(app, "AI导出10-1693718908.jpg")

def update_prompt_text(preset_combo, positive_textEdit, negative_textEdit):
    """
    根据预设下拉框的选择更新提示词文本框
    """
    config = load_config()
    current_index = preset_combo.currentIndex()
    
    if current_index >= 0 and current_index < len(config['settings']):
        selected_preset = config['settings'][current_index]
        positive_textEdit.setPlainText(selected_preset['positive'])
        negative_textEdit.setPlainText(selected_preset['negative'])
