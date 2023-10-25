import os

import sys
import time
from _ctypes import COMError
from datetime import datetime

import photoshop.api as ps
import pythoncom
from photoshop import Session
from PIL import Image


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
