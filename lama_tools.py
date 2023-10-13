import os
import sys
from base64 import b64decode
from datetime import datetime

from photoshop import Session
from selenium.webdriver.common.by import By

import photoshop.api as ps


def upload_img_to_lama(app,driver,url,img_name):
    now = datetime.now()
    now_long = int(now.timestamp())
    documents = app.documents
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_PS")
    options = ps.JPEGSaveOptions()
    options.quality = 12
    options.embedColorProfile = True
    img_path=os.path.join(EXPORT_PATH, img_name + f"-{now_long}.jpg")
    app.activeDocument.saveAs(img_path, options)
    if not os.path.exists(EXPORT_PATH):
        os.mkdir(EXPORT_PATH)
    found = False
    # 遍历所有标签页
    for handle in driver.window_handles:
        # 切换到该标签页
        driver.switch_to.window(handle)
        # 检查网址是否相符
        if url in driver.current_url:
            # 找到相符的标签页，执行操作
            found = True
            break
    if not found:
        driver.get(url)
    driver.find_element(By.XPATH, "/html/body/div/div/header/div[1]/label/div/input").send_keys(img_path)

def download_img_from_lama(app,driver,url,img_name):
    found = False
    # 遍历所有标签页
    for handle in driver.window_handles:
        # 切换到该标签页
        driver.switch_to.window(handle)
        # 检查网址是否相符
        if url in driver.current_url:
            # 找到相符的标签页，执行操作
            found = True
            break
    if not found:
        driver.get(url)
    # 执行JavaScript代码以获取canvas元素的内容
    js = "return document.querySelector('#root > div > div.editor-container > div.react-transform-wrapper.transform-component-module_wrapper__1_Fgj > div > div.editor-canvas-container > canvas').toDataURL('image/png').split(',')[1];"
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_LAMA")
    if not os.path.exists(EXPORT_PATH):
        os.mkdir(EXPORT_PATH)
    canvas_base64 = driver.execute_script(js)
    # 将base64编码的字符串转换为bytes类型
    canvas_bytes = b64decode(canvas_base64)
    # 将bytes类型的数据保存为PNG文件
    now = datetime.now()
    now_long = int(now.timestamp())
    with open(os.path.join(EXPORT_PATH, f"{img_name}-{now_long}.png"), "wb") as f:
        f.write(canvas_bytes)
    # 打开你要导入的图片
    img_path=os.path.join(EXPORT_PATH, img_name + f"-{now_long}.png")
    # 打开的psd文件
    with Session(app.activeDocument.path) as ps:
        desc = ps.ActionDescriptor
        # 要打开的图像
        desc.putPath(ps.app.charIDToTypeID("null"), img_path)
        ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)


# driver=open_driver()
# # upload_img_to_lama(driver,"http://127.0.0.1:8080/","F:\Psdlink_qtpy\EXPORT_PS\AI导出.psb-1696997104.jpg")
# download_img_from_lama(driver,"http://127.0.0.1:8080/","AI导出")