import ctypes
import os
import subprocess

import sys
import time

import requests
from PIL import Image
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import running_variable


def execute_cmd(cmd):
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)

    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE
    )
    proc.stdin.close()
    proc.wait()
    result = proc.stdout.read().decode('gbk')  # 注意你电脑cmd的输出编码（中文是gbk）
    proc.stdout.close()
    return result


def open_driver():
    result = execute_cmd('netstat -aon|findstr "9222"').split("\r\n")
    # 先检测chrome在不在运行
    chrome_running = False
    if "LISTENING" in result[0]:
        chrome_running = True
    # 设置Chrome选项
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    DATA_PATH = os.path.join(BASE_PATH, "chrome\Data")
    CHROME_PATH = os.path.join(BASE_PATH, "chrome\App")
    DRIVE_PATH = os.path.join(BASE_PATH, "chromedriver.exe")
    options = Options()
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('lang=zh_CN.UTF-8')
    options.binary_location = os.path.join(CHROME_PATH, "chrome.exe")
    # options.binary_location = "F:\\PsDlink2.0.1\\PsDlink2.0.1\\chrome\\App\\chrome.exe"
    chrome_driver = DRIVE_PATH
    # 如果在运行，则直接用当前driver
    if chrome_running:
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:9222")
        # chrome_driver = os.path.join(BASE_PATH, "chromedriver.exe")
        service = Service(chrome_driver)
        service.creation_flags = subprocess.CREATE_NO_WINDOW
        driver = webdriver.Chrome(service=service, options=options)
    # 如果不在运行，则打开浏览器
    else:
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:9222")
        os.system('chcp 65001')
        os.system(f"cd {CHROME_PATH} && .\\chrome.exe --remote-debugging-port=9222 --user-data-dir={DATA_PATH}")
        service = Service(chrome_driver)
        service.creation_flags = subprocess.CREATE_NO_WINDOW
        driver = webdriver.Chrome(service=service, options=options)
    # 在运行的话，检测当前网页
    return driver


def translate(driver, translate_str):
    found = False
    url = "https://fanyi.baidu.com/"
    for handle in driver.window_handles:
        # 切换到该标签页
        driver.switch_to.window(handle)
        # 检查网址是否相符
        if url in driver.current_url:
            # 找到相符的标签页，在标签页进行执行
            print(url)
            print(driver.current_url)
            url = f"https://fanyi.baidu.com/mtpe-individual/multimodal?query={translate_str}&lang=zh2en&ext_channel=Aldtype#/"
            driver.get(url)
            break
    # 如果没有找到相符的标签页，打开一个新的标签页
    if not found:
        # 打开新标签页
        driver.execute_script('window.open()')
        # 切换到新标签页
        driver.switch_to.window(driver.window_handles[-1])
        # 加载网址并执行操作
        url = f"https://fanyi.baidu.com/mtpe-individual/multimodal?query={translate_str}&lang=zh2en&ext_channel=Aldtype#/"
        driver.get(url)
        # do something
    time.sleep(3)
    output_box = driver.find_element(By.XPATH, "//*[@id=\"trans-selection\"]/div/span")
    result = output_box.text
    print(result)
    return result


def open_web_url(driver, url):
    # 标志位，表示是否找到相符的标签页
    found = False
    # 遍历所有标签页
    for handle in driver.window_handles:
        # 切换到该标签页
        driver.switch_to.window(handle)
        # 检查网址是否相符
        if url in driver.current_url:
            # 找到相符的标签页，在标签页进行执行
            return driver
            break
    # 如果没有找到相符的标签页，打开一个新的标签页
    if not found:
        # 打开新标签页
        driver.execute_script('window.open()')
        # 切换到新标签页
        driver.switch_to.window(driver.window_handles[-1])
        # 加载网址并执行操作
        driver.get(url)
    return driver


def reflesh_page(driver):
    # 检测webui是否加载出来
    while True:
        # 如果碰到页面加载出来就跳出
        try:
            driver.find_element(By.XPATH, "//*[@id=\"setting_sd_model_checkpoint\"]/label/div/div[1]/div/input")
            break
        except NoSuchElementException:
            try:
                driver.find_element(By.XPATH, "//*[@id=\"component-3955\"]/div[2]/div/div[1]/div/input")
                break
            except:
                pass
        # 如果中止检测位为False，不运行了也跳出
        if not running_variable.running:
            break


def change_model(driver, model_name):
    # 找到模型
    try:
        driver.find_element(By.XPATH,
                            "//*[@id=\"setting_sd_model_checkpoint\"]/label/div/div[1]/div/input").click()
        driver.find_element(By.XPATH,
                            "//*[@id=\"setting_sd_model_checkpoint\"]/label/div/div[1]/div/input").send_keys(
            model_name)
        driver.find_element(By.XPATH,
                            "//*[@id=\"setting_sd_model_checkpoint\"]/label/div/div[1]/div/input").send_keys(Keys.ENTER)
    except NoSuchElementException:
        driver.find_element(By.XPATH,
                            "//*[@id=\"component-3955\"]/div[2]/div/div[1]/div/input").click()
        driver.find_element(By.XPATH,
                            "//*[@id=\"component-3955\"]/div[2]/div/div[1]/div/input").send_keys(
            model_name)
        driver.find_element(By.XPATH,
                            "//*[@id=\"component-3955\"]/div[2]/div/div[1]/div/input").send_keys(Keys.ENTER)


def change_to_img2img(driver):
    # 进入图生图
    try:
        driver.find_element(By.XPATH, "//*[@id=\"tab_img2img-button\"]").click()
    except NoSuchElementException:
        driver.find_element(By.XPATH, "//*[@id=\"tabs\"]/div[1]/button[2]").click()


def set_prompt(driver, positive, negative):
    # 设置提示词
    driver.find_element(By.XPATH, "//*[@id=\"img2img_prompt\"]/label/textarea").clear()
    driver.find_element(By.XPATH, "//*[@id=\"img2img_prompt\"]/label/textarea").send_keys(positive)
    driver.find_element(By.XPATH, "//*[@id=\"img2img_neg_prompt\"]/label/textarea").clear()
    driver.find_element(By.XPATH, "//*[@id=\"img2img_neg_prompt\"]/label/textarea").send_keys(negative)


def import_img_sd(driver, img_path):
    # 导入图片
    try:
        driver.find_element(By.XPATH, "//*[@id=\"img2img_image\"]/div[3]/div/input").send_keys(img_path)
    except NoSuchElementException:
        parent_element = driver.find_element(By.XPATH, "//*[@id='img2img_image']")
        # 在父元素下查找input元素，类型为file
        input_element = parent_element.find_element(By.XPATH, ".//input[@type='file']")
        input_element.send_keys(img_path)


def select_sampling_method(driver, sampling_method):
    # 更改采样器
    try:
        driver.find_element(By.XPATH, "//*[@id=\"img2img_sampling\"]/label/div/div[1]/div/input").clear()
        driver.find_element(By.XPATH, "//*[@id=\"img2img_sampling\"]/label/div/div[1]/div/input").send_keys(
            sampling_method)
        driver.find_element(By.XPATH, "//*[@id=\"img2img_sampling\"]/label/div/div[1]/div/input").send_keys(Keys.ENTER)
    except NoSuchElementException:
        try:
            driver.find_element(By.XPATH, "//*[@id=\"img2img_sampling\"]/div[2]/div/div[1]/div/input").clear()
            driver.find_element(By.XPATH, "//*[@id=\"img2img_sampling\"]/div[2]/div/div[1]/div/input").send_keys(
                sampling_method)
            driver.find_element(By.XPATH, "//*[@id=\"img2img_sampling\"]/div[2]/div/div[1]/div/input").send_keys(
                Keys.ENTER)
        except NoSuchElementException:
            element = driver.find_element(By.XPATH, '//*[@id="img2img_sampling"]')
            labels = element.find_elements(By.XPATH, './/label')
            for label in labels:
                # 在这里执行你想要的操作
                if sampling_method == label.text:
                    label.find_element(By.XPATH, './/input').click()


def set_width_height(driver, img_path, lim_size):
    # 设置输出图片的长和宽
    img = Image.open(img_path)
    width, height = img.size
    max_size = max(width, height)
    min_size = min(width, height)
    if max_size > lim_size:
        min_size = int(lim_size * min_size / max_size)
        max_size = lim_size
    if width > height:
        width = max_size
        height = min_size
    else:
        height = max_size
        width = min_size
    driver.find_element(By.XPATH, "//*[@id=\"img2img_height\"]/div[2]/div/input").clear()
    driver.find_element(By.XPATH, "//*[@id=\"img2img_height\"]/div[2]/div/input").send_keys(height)
    driver.find_element(By.XPATH, "//*[@id=\"img2img_width\"]/div[2]/div/input").clear()
    driver.find_element(By.XPATH, "//*[@id=\"img2img_width\"]/div[2]/div/input").send_keys(width)
    return width, height


def set_strength(driver, value):
    # 设置重绘幅度
    driver.find_element(By.XPATH, "//*[@id=\"img2img_denoising_strength\"]/div[2]/div/input").clear()
    driver.find_element(By.XPATH, "//*[@id=\"img2img_denoising_strength\"]/div[2]/div/input").send_keys(value)


def set_batch_count(driver, batch_count):
    # 设置生成次数
    driver.find_element(By.XPATH, "//*[@id=\"img2img_batch_count\"]/div[2]/div/input").clear()
    driver.find_element(By.XPATH, "//*[@id=\"img2img_batch_count\"]/div[2]/div/input").send_keys(batch_count)


def check_control_net_start(driver):
    # 检测controlnet是否开启,没有打开就打开
    try:
        input_btn = driver.find_element(By.XPATH,
                                        f"//*[@id=\"img2img_controlnet_ControlNet-0_controlnet_enable_checkbox\"]/label/input")
        input_btn.click()
        input_btn.click()
    except:
        try:
            driver.find_element(By.XPATH, "//*[@id=\"img2img_controlnet\"]").click()
        except NoSuchElementException:
            driver.find_element(By.XPATH, "//*[@id=\"controlnet\"]/button").click()
        while True:
            try:
                try:
                    driver.find_element(By.XPATH, "//*[@id=\"img2img_controlnet_tabs\"]/div[1]/button[1]").click()
                except NoSuchElementException:
                    driver.find_element(By.XPATH, "//*[@id=\"input-accordion-5\"]/button").click()
                break
            except:
                continue


def set_control_net(driver, controlnet_id, is_enable, is_perfect_pixel, preprocessor, model, resolution=None,
                    param1=None, param2=None,
                    img_path=None):
    # 设置controlnet
    # 先进入第几个controlnet
    try:
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_tabs\"]/div[1]/button[{str(int(controlnet_id) + 1)}]").click()
    except NoSuchElementException:
        if driver.find_element(By.XPATH,
                                f"//*[@id=\"input-accordion-{str(int(controlnet_id) + 5)}\"]").get_attribute('class')=='block gradio-accordion input-accordion svelte-12cmxck padded':
                driver.find_element(By.XPATH,
                                f"//*[@id=\"input-accordion-{str(int(controlnet_id) + 5)}\"]/button").click()
    # 把已经导入的图取消掉
    try:
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_input_image\"]/div[3]/div/div[2]/button[3]").click()
    except:
        try:
            check = driver.find_element(By.XPATH,
                                        f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_same_img2img_checkbox\"]/label/input").is_selected()
            if check:
                driver.find_element(By.XPATH,
                                    f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_input_image\"]/div[3]/div[1]/div[2]/button[3]").click()
        except:
            pass
    # 是否启用
    if is_enable:
        enable_element = driver.find_element(By.XPATH,
                                             f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_enable_checkbox\"]/label/input")
        check = enable_element.is_selected()
        if not check:
            enable_element.click()
    else:
        enable_element = driver.find_element(By.XPATH,
                                             f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_enable_checkbox\"]/label/input")
        check = enable_element.is_selected()
        if check:
            enable_element.click()
    # 是否开启完美像素
    if is_perfect_pixel:
        perfect_pixel = driver.find_element(By.XPATH,
                                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_pixel_perfect_checkbox\"]/label/input")
        check = perfect_pixel.is_selected()
        if not check:
            perfect_pixel.click()
    else:
        perfect_pixel = driver.find_element(By.XPATH,
                                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_pixel_perfect_checkbox\"]/label/input")
        check = perfect_pixel.is_selected()
        if check:
            perfect_pixel.click()
    # 设置预处理器
    try:
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_preprocessor_dropdown\"]/label/div/div[1]/div/input").clear()
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_preprocessor_dropdown\"]/label/div/div[1]/div/input").send_keys(
            preprocessor)
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_preprocessor_dropdown\"]/label/div/div[1]/div/input").send_keys(
            Keys.ENTER)
    except NoSuchElementException:
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_preprocessor_dropdown\"]/div[2]/div/div[1]/div/input").clear()

        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_preprocessor_dropdown\"]/div[2]/div/div[1]/div/input").send_keys(
            preprocessor)
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_preprocessor_dropdown\"]/div[2]/div/div[1]/div/input").send_keys(
            Keys.ENTER)
    # 设置controlnet模型
    try:
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_model_dropdown\"]/label/div/div[1]/div/input").clear()
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_model_dropdown\"]/label/div/div[1]/div/input").send_keys(
            model)
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_model_dropdown\"]/label/div/div[1]/div/input").send_keys(
            Keys.ENTER)
    except NoSuchElementException:
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_model_dropdown\"]/div[2]/div/div[1]/div/input").clear()
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_model_dropdown\"]/div[2]/div/div[1]/div/input").send_keys(
            model)
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_model_dropdown\"]/div[2]/div/div[1]/div/input").send_keys(
            Keys.ENTER)
    # 设置参数
    if resolution and resolution != "":
        try:
            driver.find_element(By.XPATH,
                                f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_preprocessor_resolution_slider\"]/div[2]/div/input").clear()
            driver.find_element(By.XPATH,
                                f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_preprocessor_resolution_slider\"]/div[2]/div/input").send_keys(
                resolution)
        except:
            pass
    if param1 and param1 != "":
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_threshold_A_slider\"]/div[2]/div/input").clear()
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_threshold_A_slider\"]/div[2]/div/input").send_keys(
            param1)
    if param2 and param2 != "":
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_threshold_B_slider\"]/div[2]/div/input").clear()
        driver.find_element(By.XPATH,
                            f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_threshold_B_slider\"]/div[2]/div/input").send_keys(
            param2)
    # 是否导入了参考图
    if img_path and img_path != "":
        try:
            driver.find_element(By.XPATH,
                                f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_input_image\"]/div[3]/div/input").send_keys(
                img_path)
            driver.find_element(By.XPATH,
                                f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_trigger_preprocessor\"]").click()
        except:
            driver.find_element(By.XPATH,
                                f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_input_image\"]/div[3]/div[1]/input").send_keys(
                img_path)
            driver.find_element(By.XPATH,
                                f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_trigger_preprocessor\"]").click()


def test_sd(driver):
    # element = driver.find_element(By.XPATH,
    #                                        "/html/body/gradio-app/div/div/div[1]/div/div/div[2]/div[3]/div/div[2]/div[2]/div/div/div[1]/div[13]/div/div[5]/div/label/div/div[1]/div/input")
    element_img2img = driver.find_element(By.XPATH, "//*[@id=\"img2img_script_container\"]")
    element_script_list = element_img2img.find_element(By.ID,
                                                       "script_list")
    element = element_script_list.find_element(By.TAG_NAME, "input")
    element.clear()
    element.send_keys("None")
    element.send_keys(Keys.ENTER)


def cancel_controlnet(driver):
    try:
        try:
            for controlnet_id in range(0,2):
                if driver.find_element(By.XPATH,
                                    f" //*[@id=\"input-accordion-{controlnet_id+5}-visible-checkbox\"]").is_selected():
                    driver.find_element(By.XPATH,
                                        f" //*[@id=\"input-accordion-{controlnet_id + 5}-visible-checkbox\"]").click()
        except NoSuchElementException:
            driver.find_element(By.XPATH,
                                    f"//*[@id=\"img2img_controlnet_ControlNet-0_controlnet_enable_checkbox\"]/label/input")
            # 如果开启了，就把启动按钮全部取消
            for controlnet_id in range(0, 4):
                driver.find_element(By.XPATH,
                                    f"//*[@id=\"img2img_controlnet_tabs\"]/div[1]/button[{controlnet_id + 1}]").click()
                enable_element = driver.find_element(By.XPATH,
                                                     f"//*[@id=\"img2img_controlnet_ControlNet-{controlnet_id}_controlnet_enable_checkbox\"]/label/input")
                check = enable_element.is_selected()
                if check:
                    enable_element.click()
            driver.find_element(By.XPATH,
                                f"//*[@id=\"img2img_controlnet_tabs\"]/div[1]/button[1]").click()
    except:
         # 未开启就什么都不做
            pass


def SD_scale(driver, img_path, lim_sd_scale, width, height, model):
    # 计算缩放比例
    img = Image.open(img_path)
    origin_width, origin_height = img.size
    # 先判断是否需要放大
    if max(origin_width, origin_height) > lim_sd_scale:
        # SD放大
        element_img2img = driver.find_element(By.XPATH, "//*[@id=\"img2img_script_container\"]")
        element_script_list = element_img2img.find_element(By.ID,
                                                           "script_list")
        element = element_script_list.find_element(By.TAG_NAME, "input")
        element.clear()
        element.send_keys("SD upscale")
        element.send_keys(Keys.ENTER)
        # 使用模型
        time.sleep(1)
        model_use = driver.find_element(By.XPATH, f"//*[@id=\"script_sd_upscale_upscaler_index\"]")
        model_list = model_use.find_elements(By.TAG_NAME, "label")
        time.sleep(1)
        for model_temp in model_list:
            if model_temp.text == model:
                model_temp.click()
                break
        # 计算放大倍数,四舍五入保留整数
        time.sleep(3)
        need_zoom = round(max(origin_width / width, origin_height / height))
        driver.find_element(By.XPATH, f"//*[@id=\"script_sd_upscale_scale_factor\"]/div[2]/div/input").clear()
        driver.find_element(By.XPATH, f"//*[@id=\"script_sd_upscale_scale_factor\"]/div[2]/div/input").send_keys(
            need_zoom)
        return True
    else:
        return False


def back_SD_scale(driver, model):
    # 计算缩放比例
    # SD放大
    element_img2img = driver.find_element(By.XPATH, "//*[@id=\"img2img_script_container\"]")
    element_script_list = element_img2img.find_element(By.ID,
                                                       "script_list")
    element = element_script_list.find_element(By.TAG_NAME, "input")
    element.clear()
    element.send_keys("SD upscale")
    element.send_keys(Keys.ENTER)
    # 使用模型
    time.sleep(1)
    model_use = driver.find_element(By.XPATH, f"//*[@id=\"script_sd_upscale_upscaler_index\"]")
    model_list = model_use.find_elements(By.TAG_NAME, "label")
    time.sleep(1)
    for model_temp in model_list:
        if model_temp.text == model:
            model_temp.click()
            break
    # 计算放大倍数,四舍五入保留整数
    driver.find_element(By.XPATH, f"//*[@id=\"script_sd_upscale_scale_factor\"]/div[2]/div/input").clear()
    driver.find_element(By.XPATH, f"//*[@id=\"script_sd_upscale_scale_factor\"]/div[2]/div/input").send_keys(
        "4")


def cancel_SD_scale(driver):
    # 取消sd放大
    element_img2img = driver.find_element(By.XPATH, "//*[@id=\"img2img_script_container\"]")
    element_script_list = element_img2img.find_element(By.ID,
                                                       "script_list")
    element = element_script_list.find_element(By.TAG_NAME, "input")
    element.clear()
    element.send_keys("None")
    element.send_keys(Keys.ENTER)


def click_generate(driver, img_name, generate_count):
    # 点击生成，并保存图片
    driver.find_element(By.XPATH, f"//*[@id=\"img2img_generate\"]").click()
    check = driver.find_element(By.XPATH, f"//*[@id=\"img2img_interrupt\"]")
    # 等待生成,检测中止按钮是否存在
    while (check.get_attribute("style") == "display: block;"):
        if running_variable.running:
            time.sleep(1)
        else:
            return
    img_bus = driver.find_element(By.XPATH, f"//*[@id=\"img2img_gallery\"]/div[2]")
    img_btn_list = img_bus.find_elements(By.TAG_NAME, "button")
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_SD")
    if not os.path.exists(EXPORT_PATH):
        os.mkdir(EXPORT_PATH)
    if generate_count == 1:
        # 获取图片资源
        try:
            src = img_btn_list[0].find_element(By.XPATH,
                                               "//*[@id=\"img2img_gallery\"]/div[2]/div/button/img").get_attribute(
                "src")
        except:
            src = img_btn_list[0].find_element(By.XPATH,
                                               "//*[@id=\"img2img_gallery\"]/div[2]/div[2]/button[1]/img").get_attribute(
                "src")
        # 发送请求，获取图片的二进制数据
        response = requests.get(src)
        # 打开一个文件，以二进制写入模式
        with open(os.path.join(EXPORT_PATH, f"{img_name}-1.jpg"), "wb") as f:
            # 写入图片数据
            f.write(response.content)
    else:
        for i in range(1, generate_count + 1):
            # 获取图片资源
            src = img_btn_list[i].find_element(By.XPATH,
                                               f"//*[@id=\"img2img_gallery\"]/div[2]/div/button[{i + 1}]/img").get_attribute(
                "src")
            # 发送请求，获取图片的二进制数据
            response = requests.get(src)
            # 打开一个文件，以二进制写入模式
            with open(os.path.join(EXPORT_PATH, f"{img_name}-{i}.jpg"), "wb") as f:
                # 写入图片数据
                f.write(response.content)


def save_img_from_sd(driver, img_name):
    # 保存weburl上的图像
    img_bus = driver.find_element(By.XPATH, f"//*[@id=\"img2img_gallery\"]/div[2]")
    img_btn_list = img_bus.find_elements(By.TAG_NAME, "button")
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_SD")
    if not os.path.exists(EXPORT_PATH):
        os.mkdir(EXPORT_PATH)
    generate_count = driver.find_element(By.XPATH, "//*[@id=\"img2img_batch_count\"]/div[2]/div/input").get_attribute(
        "value")
    if int(generate_count) == 1:
        # 获取图片资源
        try:
            src = img_btn_list[0].find_element(By.XPATH,
                                               "//*[@id=\"img2img_gallery\"]/div[2]/div/button/img").get_attribute(
                "src")
        except:
            src = img_btn_list[0].find_element(By.XPATH,
                                               "//*[@id=\"img2img_gallery\"]/div[2]/div[2]/button/img").get_attribute(
                "src")
        # 发送请求，获取图片的二进制数据
        response = requests.get(src)
        # 打开一个文件，以二进制写入模式
        with open(os.path.join(EXPORT_PATH, f"{img_name}-1.jpg"), "wb") as f:
            # 写入图片数据
            f.write(response.content)
        return 1
    else:
        for i in range(1, int(generate_count) + 1):
            # 获取图片资源
            src = img_btn_list[i].find_element(By.XPATH,
                                               f"//*[@id=\"img2img_gallery\"]/div[2]/div/button[{i + 1}]/img").get_attribute(
                "src")
            # 发送请求，获取图片的二进制数据
            response = requests.get(src)
            # 打开一个文件，以二进制写入模式
            with open(os.path.join(EXPORT_PATH, f"{img_name}-{i}.jpg"), "wb") as f:
                # 写入图片数据
                f.write(response.content)
        return int(generate_count)


def SD_upscale_click_generate(driver, img_name):
    # SD放大点击生成，并保存图片
    driver.find_element(By.XPATH, f"//*[@id=\"img2img_generate\"]").click()
    check = driver.find_element(By.XPATH, f"//*[@id=\"img2img_interrupt\"]")
    # 等待生成,检测中止按钮是否存在
    while (check.get_attribute("style") == "display: block;"):
        if running_variable.running:
            time.sleep(1)
        else:
            return
    img_bus = driver.find_element(By.XPATH, f"//*[@id=\"img2img_gallery\"]/div[2]")
    img_btn_list = img_bus.find_elements(By.TAG_NAME, "button")
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_SD")
    if not os.path.exists(EXPORT_PATH):
        os.mkdir(EXPORT_PATH)
        # 获取图片资源
    src = img_btn_list[0].find_element(By.XPATH,
                                       "//*[@id=\"img2img_gallery\"]/div[2]/div/button/img").get_attribute("src")
    # 发送请求，获取图片的二进制数据
    response = requests.get(src)
    # 打开一个文件，以二进制写入模式
    with open(os.path.join(EXPORT_PATH, f"{img_name}.jpg"), "wb") as f:
        # 写入图片数据
        f.write(response.content)

# app = start_ps()
# driver = open_driver()
# open_web_url(driver, "http://127.0.0.1:7860/?__theme=dark")
# # cancel_SD_scale(driver)
# # select_sampling_method(driver,"LMS")
# # open_web_url(driver, "http://region-3.seetacloud.com:23590/?__theme=dark")
# # time.sleep(3)
# #open_web_url(driver, "http://region-3.seetacloud.com:28018/?__theme=dark")
# # check_control_net_start(driver)
# change_to_img2img(driver)
# set_control_net(driver, "0", True, True, preprocessor="normal_midas", model="control_canny-fp16 [e3fe7712]",
#                 param1="0.2", param2=None)
# SD_scale(driver,"F:\客单\空空\9DEE0F152B72A8B05818F19EAD635CC5.jpg",700,604,700,"R-ESRGAN 4x+")
# click_generate(driver)
# cancel_controlnet(driver)
# cancel_SD_scale(driver)
