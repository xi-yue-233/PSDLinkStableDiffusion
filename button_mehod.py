import json
import traceback

import pythoncom

from lama_tools import *
from playsound import playsound
from ps_tools import *
from sd_tools import *

import running_variable


class StopException(Exception):
    pass


class All_running_StopException(Exception):
    pass


def import_to_sd(application_list):
    pythoncom.CoInitialize()  # 初始化com环境
    try:
        # 先定位ps
        print("开始执行批量任务")
        if running_variable.all_running:
            ps = start_ps()
            print(f"定位到当前PS")
        else:
            raise All_running_StopException

        # 保存图片
        img_path_list = []
        save_name_list = []
        print("正在保存图片")
        for i in application_list:
            if running_variable.all_running:
                img_path, save_name = export_image_from_ps(ps, i.layer_name.text())
                img_path_list.append(img_path)
                save_name_list.append(save_name)
                time.sleep(0.1)
                print(f"{i.tab_name.text()} 存储图片至:{img_path}")
            else:
                raise All_running_StopException

        # 循环执行任务
        for i in range(len(application_list)):
            try:
                # 打开浏览器
                if running_variable.all_running:
                    print(f"{application_list[i].tab_name.text()} 开始执行")
                    if running_variable.running:
                        driver = open_driver()
                        print(f"{application_list[i].tab_name.text()} 打开浏览器")
                    else:
                        raise StopException

                    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
                    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
                        data = json.load(f)
                        setting = data["settings"][application_list[i].preset_combo.currentIndex()]
                        model = ""
                        if "model" in setting:
                            model = setting["model"]
                        hd_method = setting["algorithm"]
                        is_hd = setting["continue1"]
                        is_back_ps = setting["continue2"]
                        continue1 = float(setting["interval1"])
                        continue2 = float(setting["interval2"])
                        max_pics = int(setting["max_psi1"])
                        max_hd = int(setting["max_psi2"])
                        negative = setting["negative"]
                        positive = setting["positive"]
                        sample = setting["sample"]

                    time.sleep(continue1)
                    add_positive = application_list[i].add_positive_edit.text()
                    add_negative = application_list[i].add_negative_edit.text()
                    if running_variable.running:
                        # 判断是否要执行翻译
                        if application_list[i].is_use_translate.isChecked():
                            time.sleep(continue2)
                            print(f"{application_list[i].tab_name.text()} 执行翻译")
                            if add_positive!="":
                                add_positive = translate(driver, add_positive)
                            if add_negative!="":
                                add_negative = translate(driver, add_negative)
                    else:
                        raise StopException
                    time.sleep(continue2)

                    # 打开weburl
                    if running_variable.running:
                        print(f"{application_list[i].tab_name.text()} 打开webui_url")
                        open_web_url(driver, application_list[i].webui_url.text())
                    else:
                        raise StopException

                    # 检测是否成功打开weburl
                    if running_variable.running:
                        reflesh_page(driver)
                    else:
                        raise StopException

                    # 更改模型
                    if running_variable.running:
                        if model != "":
                            time.sleep(continue2)
                            change_model(driver, model)
                    else:
                        raise StopException
                    time.sleep(continue2)

                    # 转到图生图页面
                    if running_variable.running:
                        change_to_img2img(driver)
                    else:
                        raise StopException
                    time.sleep(continue2)

                    # 设置提示词
                    if running_variable.running:
                        if add_positive != "" and add_negative != "":
                            set_prompt(driver, f"{positive},{add_positive}",
                                       f"{negative},{add_negative}")
                        elif add_positive == "" and add_negative != "":
                            set_prompt(driver, positive, f"{negative},{add_negative}")
                        elif add_positive != "" and add_negative == "":
                            set_prompt(driver, f"{positive},{add_positive}", negative)
                        else:
                            set_prompt(driver, positive, negative)
                    else:
                        raise StopException
                    time.sleep(continue2)

                    # 上传图片
                    if running_variable.running:
                        import_img_sd(driver, img_path_list[i])
                        print(f"{application_list[i].tab_name.text()} 上传图片成功")
                    else:
                        raise StopException
                    time.sleep(continue2)

                    # 设置采样器
                    if running_variable.running:
                        select_sampling_method(driver, sample)
                    else:
                        raise StopException
                    time.sleep(continue2)

                    # 设置输出图片的长宽
                    if running_variable.running:
                        width, height = set_width_height(driver, img_path_list[i], max_pics)
                    else:
                        raise StopException
                    time.sleep(continue2)

                    # 设置图片重绘幅度
                    if running_variable.running:
                        set_strength(driver, application_list[i].paint_weight.text())
                    else:
                        raise StopException
                    time.sleep(continue2)

                    # 设置图片绘制张数
                    if running_variable.running:
                        set_batch_count(driver, application_list[i].paint_count.text())
                    else:
                        raise StopException

                    print(f"{application_list[i].tab_name.text()} 基础设置完成")

                    # 取消controlnet
                    if running_variable.running:
                        time.sleep(continue2)
                        cancel_controlnet(driver)
                    else:
                        raise StopException

                    # 开启controlnet
                    if running_variable.running:
                        time.sleep(continue2)
                        check_control_net_start(driver)
                    else:
                        raise StopException

                    # 设置controlnet
                    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
                    with open(os.path.join(BASE_PATH, "ControlNet.json"), "r") as f:
                        data = json.load(f)
                    for j in range(0, 4):
                        # 如果当前cn层被启用
                        if eval(f"application_list[{i}].cn{j}_preset.currentIndex()"):
                            print(f"{application_list[i].tab_name.text()} 设置ControlNet{j}")
                            time.sleep(continue2)
                            if running_variable.running:
                                setting_cn = data[eval(f"application_list[{i}].cn{j}_preset.currentIndex()") - 1]
                                is_enable = setting_cn["enable"]
                                preprocessor = setting_cn["preprocessor"]
                                cn_model = setting_cn["model"]
                                resolution = setting_cn["resolution"]
                                param1 = setting_cn["param1"]
                                param2 = setting_cn["param2"]
                                is_perfect_piexl = setting_cn["pixel_perfect"]
                                if eval(f"application_list[{i}].cn{j}_layer.text()") != "":
                                    cn_path = export_controlnet_image_from_ps(ps, eval(
                                        f"application_list[{i}].cn{j}_layer.text()"))
                                    set_control_net(driver, str(j), is_enable,
                                                    is_perfect_piexl,
                                                    preprocessor, cn_model, resolution=resolution,
                                                    param1=param1, param2=param2,
                                                    img_path=cn_path)
                                else:
                                    set_control_net(driver, str(j), is_enable,
                                                    is_perfect_piexl,
                                                    preprocessor, cn_model, resolution=resolution,
                                                    param1=param1, param2=param2,
                                                    img_path=None)
                            else:
                                raise StopException

                    # 取消SD放大
                    if running_variable.running:
                        cancel_SD_scale(driver)
                    else:
                        raise StopException

                    # 点击生成
                    print(f"{application_list[i].tab_name.text()} 开始生成")
                    time.sleep(continue2)
                    if running_variable.running:
                        click_generate(driver, save_name_list[i], int(application_list[i].paint_count.text()))
                    else:
                        raise StopException
                    print(f"{application_list[i].tab_name.text()} 生成完成")

                    # SD放大
                    if application_list[i].is_hd.isChecked():
                        if running_variable.running:
                            time.sleep(continue2)
                            is_satisfy_zoom = SD_scale(driver, img_path_list[i], lim_sd_scale=max_hd, width=width,
                                                       height=height,
                                                       model=hd_method)
                        else:
                            raise StopException
                        # 判断是否满足放大条件
                        if is_satisfy_zoom:
                            if running_variable.running:
                                # 取消controlnet
                                time.sleep(continue2)
                                cancel_controlnet(driver)
                            else:
                                raise StopException
                            for j in range(1, int(application_list[i].paint_count.text()) + 1):
                                # 输入原图尺寸以便进行尺寸计算
                                print(f"{application_list[i].tab_name.text()} 正在放大第{j}张图")
                                time.sleep(continue2)
                                # 设置重绘一遍
                                if running_variable.running:
                                    set_batch_count(driver, 1)
                                else:
                                    raise StopException
                                # 设置重绘幅度
                                time.sleep(continue2)
                                if running_variable.running:
                                    set_strength(driver, application_list[i].hd_weight.text())
                                else:
                                    raise StopException
                                # 导入要重绘的图片
                                time.sleep(continue2)
                                if running_variable.running:
                                    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
                                    EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_SD")
                                    import_img_sd(driver, os.path.join(EXPORT_PATH, f"{save_name_list[i]}-{j}.jpg"))
                                else:
                                    raise StopException
                                # 生成并保存图片
                                time.sleep(continue2)
                                if running_variable.running:
                                    SD_upscale_click_generate(driver, f"{save_name_list[i]}-{j}")
                                else:
                                    raise StopException
                                print(
                                    f"{application_list[i].tab_name.text()} 第{j}张图放大完毕,保存为{save_name_list[i]}-{j}.jpg")
                                time.sleep(continue2)
                        else:
                            print("原图未达到需要放大的分辨率，无需放大")
                    # 导回图片
                    # 如果需要自动传回
                    print(f"{application_list[i].tab_name.text()} 正在传回ps文档")
                    time.sleep(continue2)
                    if running_variable.running:
                        import_image_from_sd(app=ps, img_name=save_name_list[i],
                                             count=int(application_list[i].paint_count.text()))
                    else:
                        raise StopException
                    print(f"{application_list[i].tab_name.text()} 传回完毕")
                else:
                    raise All_running_StopException
            except StopException:
                if running_variable.all_running:
                    print("中止当前正在执行的任务，执行下一个任务")
                running_variable.running = True
                continue

                # 执行完后要将执行判断置否
        running_variable.all_running = False
        running_variable.running = False

        # 播放声音
        playsound()

    except All_running_StopException as e:
        print(f"流水线任务中止")
        running_variable.all_running = False
        running_variable.running = False
    except:
        running_variable.all_running = False
        running_variable.running = False
        traceback.print_exc()
        # 播放声音
        playsound()
    finally:
        pythoncom.CoUninitialize()  # 清理com环境


def short_key_import_to_sd(application_list, current_tab):
    try:
        pythoncom.CoInitialize()  # 初始化com环境

        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
            data = json.load(f)
            setting = data["settings"][application_list[current_tab].preset_combo.currentIndex()]
            model = ""
            if "model" in setting:
                model = setting["model"]
            hd_method = setting["algorithm"]
            is_hd = setting["continue1"]
            is_back_ps = setting["continue2"]
            continue1 = float(setting["interval1"])
            continue2 = float(setting["interval2"])
            max_pics = int(setting["max_psi1"])
            max_hd = int(setting["max_psi2"])
            negative = setting["negative"]
            positive = setting["positive"]
            sample = setting["sample"]

        # 先定位ps
        print(f"{application_list[current_tab].tab_name.text()} 开始执行SD运算全流程")
        time.sleep(continue1)
        running_variable.running = True
        if running_variable.running:
            ps = start_ps()
            print(f"{application_list[current_tab].tab_name.text()} 定位到当前PS")
        else:
            raise StopException

        # 保存图片
        if running_variable.running:
            img_path, save_name = short_key_export_image_from_ps(ps)
            print(f"{application_list[current_tab].tab_name.text()} 存储图片至:{img_path}")
        else:
            raise StopException

        # 打开浏览器
        if running_variable.running:
            driver = open_driver()
            print(f"{application_list[current_tab].tab_name.text()} 打开浏览器")
        else:
            raise StopException

        add_positive = application_list[current_tab].add_positive_edit.text()
        add_negative = application_list[current_tab].add_negative_edit.text()
        if running_variable.running:
            # 判断是否要执行翻译
            if application_list[current_tab].is_use_translate.isChecked():
                time.sleep(continue2)
                print(f"{application_list[current_tab].tab_name.text()} 执行翻译")
                if add_positive != "":
                    add_positive = translate(driver, add_positive)
                if add_negative != "":
                    add_negative = translate(driver, add_negative)
        else:
            raise StopException
        time.sleep(continue2)

        # 打开weburl
        if running_variable.running:
            print(f"{application_list[current_tab].tab_name.text()} 打开webui_url")
            open_web_url(driver, application_list[current_tab].webui_url.text())
        else:
            raise StopException

        # 检测是否成功打开weburl
        if running_variable.running:
            reflesh_page(driver)
        else:
            raise StopException

        # 更改模型
        if running_variable.running:
            if "model" != "":
                time.sleep(continue2)
                change_model(driver, model)
        else:
            raise StopException
        time.sleep(continue2)

        # 转到图生图页面
        if running_variable.running:
            change_to_img2img(driver)
        else:
            raise StopException
        time.sleep(continue2)

        # 设置提示词
        if running_variable.running:
            if add_positive != "" and add_negative != "":
                set_prompt(driver, f"{positive},{add_positive}",
                           f"{negative},{add_negative}")
            elif add_positive == "" and add_negative != "":
                set_prompt(driver, positive, f"{negative},{add_negative}")
            elif add_positive != "" and add_negative == "":
                set_prompt(driver, f"{positive},{add_positive}", negative)
            else:
                set_prompt(driver, positive, negative)
        else:
            raise StopException
        time.sleep(continue2)

        # 上传图片
        if running_variable.running:
            import_img_sd(driver, img_path)
        else:
            raise StopException
        time.sleep(continue2)

        # 设置采样器
        if running_variable.running:
            select_sampling_method(driver, sample)
        else:
            raise StopException
        time.sleep(continue2)

        # 设置输出图片的长宽
        if running_variable.running:
            width, height = set_width_height(driver, img_path, max_pics)
        else:
            raise StopException
        time.sleep(continue2)

        # 设置图片重绘幅度
        if running_variable.running:
            set_strength(driver, application_list[current_tab].paint_weight.text())
        else:
            raise StopException
        time.sleep(continue2)

        # 设置图片绘制张数
        if running_variable.running:
            set_batch_count(driver, application_list[current_tab].paint_count.text())
        else:
            raise StopException

        print(f"{application_list[current_tab].tab_name.text()} 基础设置完成")

        # 取消controlnet
        if running_variable.running:
            time.sleep(continue2)
            cancel_controlnet(driver)
        else:
            raise StopException

        # 开启controlnet
        if running_variable.running:
            time.sleep(continue2)
            check_control_net_start(driver)
        else:
            raise StopException

        # 设置controlnet
        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "ControlNet.json"), "r") as f:
            data = json.load(f)
        for j in range(0, 4):
            # 如果当前cn层被启用
            if eval(f"application_list[{current_tab}].cn{j}_preset.currentIndex()"):
                print(f"{application_list[current_tab].tab_name.text()} 设置ControlNet{j}")
                time.sleep(continue2)
                if running_variable.running:
                    setting_cn = data[eval(f"application_list[{current_tab}].cn{j}_preset.currentIndex()") - 1]
                    is_enable = setting_cn["enable"]
                    preprocessor = setting_cn["preprocessor"]
                    cn_model = setting_cn["model"]
                    resolution = setting_cn["resolution"]
                    param1 = setting_cn["param1"]
                    param2 = setting_cn["param2"]
                    is_perfect_piexl = setting_cn["pixel_perfect"]
                    if eval(f"application_list[{current_tab}].cn{j}_layer.text()") != "":
                        cn_path = export_controlnet_image_from_ps(ps, eval(
                            f"application_list[{current_tab}].cn{j}_layer.text()"))
                        set_control_net(driver, str(j), is_enable,
                                        is_perfect_piexl,
                                        preprocessor, cn_model, resolution=resolution,
                                        param1=param1, param2=param2,
                                        img_path=cn_path)
                    else:
                        set_control_net(driver, str(j), is_enable,
                                        is_perfect_piexl,
                                        preprocessor, cn_model, resolution=resolution,
                                        param1=param1, param2=param2,
                                        img_path=None)
                else:
                    raise StopException

        # 取消SD放大
        if running_variable.running:
            cancel_SD_scale(driver)
        else:
            raise StopException

        # 点击生成
        if is_hd:
            print(f"{application_list[current_tab].tab_name.text()} 开始生成")
            time.sleep(continue2)
            if running_variable.running:
                click_generate(driver, save_name, int(application_list[current_tab].paint_count.text()))
            else:
                raise StopException
            print(f"{application_list[current_tab].tab_name.text()} 生成完成")

            # SD放大
            if application_list[current_tab].is_hd.isChecked():
                if running_variable.running:
                    time.sleep(continue2)
                    is_satisfy_zoom = SD_scale(driver, img_path, lim_sd_scale=max_hd, width=width,
                                               height=height,
                                               model=hd_method)
                else:
                    raise StopException
                # 判断是否满足放大条件
                if is_satisfy_zoom:
                    if running_variable.running:
                        # 取消controlnet
                        time.sleep(continue2)
                        cancel_controlnet(driver)
                    else:
                        raise StopException
                    for j in range(1, int(application_list[current_tab].paint_count.text()) + 1):
                        # 输入原图尺寸以便进行尺寸计算
                        print(f"{application_list[current_tab].tab_name.text()} 正在放大第{j}张图")
                        time.sleep(continue2)
                        # 设置重绘一遍
                        if running_variable.running:
                            set_batch_count(driver, 1)
                        else:
                            raise StopException
                        # 设置重绘幅度
                        time.sleep(continue2)
                        if running_variable.running:
                            set_strength(driver, application_list[current_tab].hd_weight.text())
                        else:
                            raise StopException
                        # 导入要重绘的图片
                        time.sleep(continue2)
                        if running_variable.running:
                            BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
                            EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_SD")
                            import_img_sd(driver, os.path.join(EXPORT_PATH, f"{save_name}-{j}.jpg"))
                        else:
                            raise StopException
                        # 生成并保存图片
                        time.sleep(continue2)
                        if running_variable.running:
                            SD_upscale_click_generate(driver, f"{save_name}-{j}")
                        else:
                            raise StopException
                        print(f"{application_list[current_tab].tab_name.text()} 第{j}张图放大完毕,保存为{save_name}-{j}.jpg")
                        time.sleep(continue2)
                else:
                    print("原图未达到需要放大的分辨率，无需放大")
            # 导回图片
            # 如果需要自动传回
            if is_back_ps:
                print(f"{application_list[current_tab].tab_name.text()} 正在传回ps文档")
                if running_variable.running:
                    short_key_import_image_from_sd(app=ps, img_name=save_name,
                                                   count=int(application_list[current_tab].paint_count.text()))
                else:
                    raise StopException
                print(f"{application_list[current_tab].tab_name.text()} 传回完毕")

        # 执行完后要将执行判断置否
        running_variable.running = False

        # 播放声音
        playsound()
    except StopException as e:
        print(f"{application_list[current_tab].tab_name.text()} 任务中止")
        running_variable.running = False
    except:
        running_variable.running = False
        # 播放声音
        playsound()
        traceback.print_exc()
    finally:
        pythoncom.CoUninitialize()  # 清理com环境


def begin_caculate(application_list, current_tab):
    try:
        pythoncom.CoInitialize()  # 初始化com环境

        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
            data = json.load(f)
            setting = data["settings"][application_list[current_tab].preset_combo.currentIndex()]
            model = ""
            if "model" in setting:
                model = setting["model"]
            hd_method = setting["algorithm"]
            is_hd = setting["continue1"]
            is_back_ps = setting["continue2"]
            continue1 = float(setting["interval1"])
            continue2 = float(setting["interval2"])
            max_pics = int(setting["max_psi1"])
            max_hd = int(setting["max_psi2"])
            negative = setting["negative"]
            positive = setting["positive"]
            sample = setting["sample"]

        # 先定位ps
        print(f"{application_list[current_tab].tab_name.text()} 开始执行SD页面开始运算任务")
        time.sleep(continue1)
        running_variable.running = True
        if running_variable.running:
            ps = start_ps()
            print(f"{application_list[current_tab].tab_name.text()} 定位到当前PS")
        else:
            raise StopException

        # 打开浏览器
        if running_variable.running:
            driver = open_driver()
            print(f"{application_list[current_tab].tab_name.text()} 打开浏览器")
        else:
            raise StopException

        # 打开weburl
        if running_variable.running:
            print(f"{application_list[current_tab].tab_name.text()} 打开webui_url")
            open_web_url(driver, application_list[current_tab].webui_url.text())
        else:
            raise StopException

        time.sleep(continue2)

        # 检测是否成功打开weburl
        if running_variable.running:
            reflesh_page(driver)
        else:
            raise StopException

        time.sleep(continue2)

        # 点击生成
        print(f"{application_list[current_tab].tab_name.text()} 开始生成")
        time.sleep(continue2)
        if running_variable.running:
            click_generate(driver, application_list[current_tab].layer_name.text(),
                           int(application_list[current_tab].paint_count.text()))
        else:
            raise StopException
        print(f"{application_list[current_tab].tab_name.text()} 生成完成")

        now = datetime.now()
        now_long = int(now.timestamp())
        save_name = f"{application_list[current_tab].layer_name.text()}-{now_long}"

        # 下载网页上的图片
        if running_variable.running:
            print(f"{application_list[current_tab].tab_name.text()} 正在下载网页图片")
            num = save_img_from_sd(driver, save_name)
        else:
            raise StopException

        # 导回图片
        print(f"{application_list[current_tab].tab_name.text()} 正在传回ps文档")
        if running_variable.running:
            short_key_import_image_from_sd(app=ps, img_name=save_name, count=num)
        else:
            raise StopException
        print(f"{application_list[current_tab].tab_name.text()} 传回完毕")

        # 执行完后要将执行判断置否
        running_variable.running = False

        # 播放声音
        playsound()
    except StopException as e:
        print(f"{application_list[current_tab].tab_name.text()} 任务中止")
        running_variable.running = False
    except:
        running_variable.running = False
        # 播放声音
        playsound()
        traceback.print_exc()
    finally:
        pythoncom.CoUninitialize()  # 清理com环境


def back_ps(application_list, current_tab):
    try:
        pythoncom.CoInitialize()  # 初始化com环境

        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
            data = json.load(f)
            setting = data["settings"][application_list[current_tab].preset_combo.currentIndex()]
            model = ""
            if "model" in setting:
                model = setting["model"]
            hd_method = setting["algorithm"]
            is_hd = setting["continue1"]
            is_back_ps = setting["continue2"]
            continue1 = float(setting["interval1"])
            continue2 = float(setting["interval2"])
            max_pics = int(setting["max_psi1"])
            max_hd = int(setting["max_psi2"])
            negative = setting["negative"]
            positive = setting["positive"]
            sample = setting["sample"]

        # 先定位ps
        print(f"{application_list[current_tab].tab_name.text()} 开始执行传回ps任务")
        time.sleep(continue1)
        if running_variable.running:
            ps = start_ps()
            print(f"{application_list[current_tab].tab_name.text()} 定位到当前PS")
        else:
            raise StopException
        time.sleep(continue2)

        # 打开浏览器
        if running_variable.running:
            driver = open_driver()
            print(f"{application_list[current_tab].tab_name.text()} 打开浏览器")
        else:
            raise StopException

        time.sleep(continue2)

        # 打开weburl
        if running_variable.running:
            print(f"{application_list[current_tab].tab_name.text()} 打开webui_url")
            open_web_url(driver, application_list[current_tab].webui_url.text())
        else:
            raise StopException

        time.sleep(continue2)

        # 检测是否成功打开weburl
        if running_variable.running:
            reflesh_page(driver)
        else:
            raise StopException

        # 下载网页上的图片
        if running_variable.running:
            print(f"{application_list[current_tab].tab_name.text()} 正在下载网页图片")
            num = save_img_from_sd(driver, f"{application_list[current_tab].layer_name.text()}")
        else:
            raise StopException

        # 导回图片
        print(f"{application_list[current_tab].tab_name.text()} 正在传回ps文档")
        time.sleep(continue2)
        if running_variable.running:
            try:
                short_key_import_image_from_sd(app=ps, img_name=application_list[current_tab].layer_name.text(),
                                               count=num)
            except:
                pass
        else:
            raise StopException
        print(f"{application_list[current_tab].tab_name.text()} 传回完毕")

        # 执行完后要将执行判断置否
        running_variable.running = False

        # 播放声音
        playsound()
    except StopException as e:
        print(f"{application_list[current_tab].tab_name.text()} 任务中止")
        running_variable.running = False
    except:
        running_variable.running = False
        traceback.print_exc()
        # 播放声音
        playsound()
    finally:
        pythoncom.CoUninitialize()  # 清理com环境


def only_import(application_list, current_tab):
    try:
        pythoncom.CoInitialize()  # 初始化com环境

        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
            data = json.load(f)
            setting = data["settings"][application_list[current_tab].preset_combo.currentIndex()]
            model = ""
            if "model" in setting:
                model = setting["model"]
            hd_method = setting["algorithm"]
            is_hd = setting["continue1"]
            is_back_ps = setting["continue2"]
            continue1 = float(setting["interval1"])
            continue2 = float(setting["interval2"])
            max_pics = int(setting["max_psi1"])
            max_hd = int(setting["max_psi2"])
            negative = setting["negative"]
            positive = setting["positive"]
            sample = setting["sample"]

        # 先定位ps
        print(f"{application_list[current_tab].tab_name.text()} 开始执行仅导入任务（不更改提示词）")
        time.sleep(continue1)
        if running_variable.running:
            ps = start_ps()
            print(f"{application_list[current_tab].tab_name.text()} 定位到当前PS")
        else:
            raise StopException
        time.sleep(continue2)

        # 保存图片
        if running_variable.running:
            img_path, save_name = short_key_export_image_from_ps(ps)
            print(f"{application_list[current_tab].tab_name.text()} 存储图片至:{img_path}")
        else:
            raise StopException
        time.sleep(continue2)

        # 打开浏览器
        if running_variable.running:
            driver = open_driver()
            print(f"{application_list[current_tab].tab_name.text()} 打开浏览器")
        else:
            raise StopException

        time.sleep(continue2)

        # 打开weburl
        if running_variable.running:
            print(f"{application_list[current_tab].tab_name.text()} 打开webui_url")
            open_web_url(driver, application_list[current_tab].webui_url.text())
        else:
            raise StopException

        # 检测是否成功打开weburl
        if running_variable.running:
            reflesh_page(driver)
        else:
            raise StopException

        # 更改模型
        if running_variable.running:
            if "model" != "":
                time.sleep(continue2)
                change_model(driver, model)
        else:
            raise StopException
        time.sleep(continue2)

        # 转到图生图页面
        if running_variable.running:
            change_to_img2img(driver)
        else:
            raise StopException
        time.sleep(continue2)

        # 上传图片
        if running_variable.running:
            import_img_sd(driver, img_path)
        else:
            raise StopException
        time.sleep(continue2)

        # 设置采样器
        if running_variable.running:
            select_sampling_method(driver, sample)
        else:
            raise StopException
        time.sleep(continue2)

        # 设置输出图片的长宽
        if running_variable.running:
            width, height = set_width_height(driver, img_path, max_pics)
        else:
            raise StopException
        time.sleep(continue2)

        # 设置图片重绘幅度
        if running_variable.running:
            set_strength(driver, application_list[current_tab].paint_weight.text())
        else:
            raise StopException
        time.sleep(continue2)

        # 设置图片绘制张数
        if running_variable.running:
            set_batch_count(driver, application_list[current_tab].paint_count.text())
        else:
            raise StopException

        print(f"{application_list[current_tab].tab_name.text()} 基础设置完成")

        # 取消controlnet
        if running_variable.running:
            time.sleep(continue2)
            cancel_controlnet(driver)
        else:
            raise StopException

        # 开启controlnet
        if running_variable.running:
            time.sleep(continue2)
            check_control_net_start(driver)
        else:
            raise StopException

        # 设置controlnet
        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "ControlNet.json"), "r") as f:
            data = json.load(f)
        for j in range(0, 4):
            # 如果当前cn层被启用
            if eval(f"application_list[{current_tab}].cn{j}_preset.currentIndex()"):
                print(f"{application_list[current_tab].tab_name.text()} 设置ControlNet{j}")
                time.sleep(continue2)
                if running_variable.running:
                    setting_cn = data[eval(f"application_list[{current_tab}].cn{j}_preset.currentIndex()") - 1]
                    is_enable = setting_cn["enable"]
                    preprocessor = setting_cn["preprocessor"]
                    cn_model = setting_cn["model"]
                    resolution = setting_cn["resolution"]
                    param1 = setting_cn["param1"]
                    param2 = setting_cn["param2"]
                    is_perfect_piexl = setting_cn["pixel_perfect"]
                    if eval(f"application_list[{current_tab}].cn{j}_layer.text()") != "":
                        cn_path = export_controlnet_image_from_ps(ps, eval(
                            f"application_list[{current_tab}].cn{j}_layer.text()"))
                        set_control_net(driver, str(j), is_enable,
                                        is_perfect_piexl,
                                        preprocessor, cn_model, resolution=resolution,
                                        param1=param1, param2=param2,
                                        img_path=cn_path)
                    else:
                        set_control_net(driver, str(j), is_enable,
                                        is_perfect_piexl,
                                        preprocessor, cn_model, resolution=resolution,
                                        param1=param1, param2=param2,
                                        img_path=None)
                else:
                    raise StopException

        # 取消SD放大
        if running_variable.running:
            cancel_SD_scale(driver)
        else:
            raise StopException

        print(f"{application_list[current_tab].tab_name.text()} 设置完成")

        # 执行完后要将执行判断置否
        running_variable.running = False

        # 播放声音
        playsound()
    except StopException as e:
        print(f"{application_list[current_tab].tab_name.text()} 任务中止")
        running_variable.running = False
    except:
        running_variable.running = False
        traceback.print_exc()
        # 播放声音
        playsound()
    finally:
        pythoncom.CoUninitialize()  # 清理com环境


def only_import_and_generate(application_list, current_tab):
    try:
        pythoncom.CoInitialize()  # 初始化com环境

        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
            data = json.load(f)
            setting = data["settings"][application_list[current_tab].preset_combo.currentIndex()]
            model = ""
            if "model" in setting:
                model = setting["model"]
            hd_method = setting["algorithm"]
            is_hd = setting["continue1"]
            is_back_ps = setting["continue2"]
            continue1 = float(setting["interval1"])
            continue2 = float(setting["interval2"])
            max_pics = int(setting["max_psi1"])
            max_hd = int(setting["max_psi2"])
            negative = setting["negative"]
            positive = setting["positive"]
            sample = setting["sample"]

        # 先定位ps
        print(f"{application_list[current_tab].tab_name.text()} 开始执行仅导入并生成任务（不更改提示词）")
        time.sleep(continue1)
        if running_variable.running:
            ps = start_ps()
            print(f"{application_list[current_tab].tab_name.text()} 定位到当前PS")
        else:
            raise StopException
        time.sleep(continue1)

        # 保存图片
        if running_variable.running:
            img_path, save_name = short_key_export_image_from_ps(ps)
            print(f"{application_list[current_tab].tab_name.text()} 存储图片至:{img_path}")
        else:
            raise StopException
        time.sleep(continue2)

        # 打开浏览器
        if running_variable.running:
            driver = open_driver()
            print(f"{application_list[current_tab].tab_name.text()} 打开浏览器")
        else:
            raise StopException

        time.sleep(continue2)

        # 打开weburl
        if running_variable.running:
            print(f"{application_list[current_tab].tab_name.text()} 打开webui_url")
            open_web_url(driver, application_list[current_tab].webui_url.text())
        else:
            raise StopException

        # 检测是否成功打开weburl
        if running_variable.running:
            reflesh_page(driver)
        else:
            raise StopException

        # 更改模型
        if running_variable.running:
            if "model" != "":
                time.sleep(continue2)
                change_model(driver, model)
        else:
            raise StopException
        time.sleep(continue2)

        # 转到图生图页面
        if running_variable.running:
            change_to_img2img(driver)
        else:
            raise StopException
        time.sleep(continue2)

        # 上传图片
        if running_variable.running:
            import_img_sd(driver, img_path)
        else:
            raise StopException
        time.sleep(continue2)

        # 设置采样器
        if running_variable.running:
            select_sampling_method(driver, sample)
        else:
            raise StopException
        time.sleep(continue2)

        # 设置输出图片的长宽
        if running_variable.running:
            width, height = set_width_height(driver, img_path, max_pics)
        else:
            raise StopException
        time.sleep(continue2)

        # 设置图片重绘幅度
        if running_variable.running:
            set_strength(driver, application_list[current_tab].paint_weight.text())
        else:
            raise StopException
        time.sleep(continue2)

        # 设置图片绘制张数
        if running_variable.running:
            set_batch_count(driver, application_list[current_tab].paint_count.text())
        else:
            raise StopException

        print(f"{application_list[current_tab].tab_name.text()} 基础设置完成")

        # 取消controlnet
        if running_variable.running:
            time.sleep(continue2)
            cancel_controlnet(driver)
        else:
            raise StopException

        # 设置controlnet
        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "ControlNet.json"), "r") as f:
            data = json.load(f)
        for j in range(0, 4):
            # 如果当前cn层被启用
            if eval(f"application_list[{current_tab}].cn{j}_preset.currentIndex()"):
                print(f"{application_list[current_tab].tab_name.text()} 设置ControlNet{j}")
                time.sleep(continue2)
                if running_variable.running:
                    setting_cn = data[eval(f"application_list[{current_tab}].cn{j}_preset.currentIndex()") - 1]
                    is_enable = setting_cn["enable"]
                    preprocessor = setting_cn["preprocessor"]
                    cn_model = setting_cn["model"]
                    resolution = setting_cn["resolution"]
                    param1 = setting_cn["param1"]
                    param2 = setting_cn["param2"]
                    is_perfect_piexl = setting_cn["pixel_perfect"]
                    if eval(f"application_list[{current_tab}].cn{j}_layer.text()") != "":
                        cn_path = export_controlnet_image_from_ps(ps, eval(
                            f"application_list[{current_tab}].cn{j}_layer.text()"))
                        set_control_net(driver, str(j), is_enable,
                                        is_perfect_piexl,
                                        preprocessor, cn_model, resolution=resolution,
                                        param1=param1, param2=param2,
                                        img_path=cn_path)
                    else:
                        set_control_net(driver, str(j), is_enable,
                                        is_perfect_piexl,
                                        preprocessor, cn_model, resolution=resolution,
                                        param1=param1, param2=param2,
                                        img_path=None)
                else:
                    raise StopException

        # 取消SD放大
        if running_variable.running:
            cancel_SD_scale(driver)
        else:
            raise StopException

        # 点击生成
        if is_hd:
            print(f"{application_list[current_tab].tab_name.text()} 开始生成")
            time.sleep(continue2)
            if running_variable.running:
                click_generate(driver, save_name, int(application_list[current_tab].paint_count.text()))
            else:
                raise StopException
            print(f"{application_list[current_tab].tab_name.text()} 生成完成")

            # SD放大
            if application_list[current_tab].is_hd.isChecked():
                if running_variable.running:
                    time.sleep(continue2)
                    is_satisfy_zoom = SD_scale(driver, img_path, lim_sd_scale=max_hd, width=width,
                                               height=height,
                                               model=hd_method)
                else:
                    raise StopException
                # 判断是否满足放大条件
                if is_satisfy_zoom:
                    if running_variable.running:
                        # 取消controlnet
                        time.sleep(continue2)
                        cancel_controlnet(driver)
                    else:
                        raise StopException
                    for j in range(1, int(application_list[current_tab].paint_count.text()) + 1):
                        # 输入原图尺寸以便进行尺寸计算
                        print(f"{application_list[current_tab].tab_name.text()} 正在放大第{j}张图")
                        time.sleep(continue2)
                        # 设置重绘一遍
                        if running_variable.running:
                            set_batch_count(driver, 1)
                        else:
                            raise StopException
                        # 设置重绘幅度
                        time.sleep(continue2)
                        if running_variable.running:
                            set_strength(driver, application_list[current_tab].hd_weight.text())
                        else:
                            raise StopException
                        # 导入要重绘的图片
                        time.sleep(continue2)
                        if running_variable.running:
                            BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
                            EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_SD")
                            import_img_sd(driver, os.path.join(EXPORT_PATH, f"{save_name}-{j}.jpg"))
                        else:
                            raise StopException
                        # 生成并保存图片
                        time.sleep(continue2)
                        if running_variable.running:
                            SD_upscale_click_generate(driver, f"{save_name}-{j}")
                        else:
                            raise StopException
                        print(f"{application_list[current_tab].tab_name.text()} 第{j}张图放大完毕,保存为{save_name}-{j}.jpg")
                        time.sleep(continue2)
                else:
                    print("原图未达到需要放大的分辨率，无需放大")
            # 导回图片
            # 如果需要自动传回
            if is_back_ps:
                print(f"{application_list[current_tab].tab_name.text()} 正在传回ps文档")
                if running_variable.running:
                    short_key_import_image_from_sd(app=ps, img_name=save_name,
                                                   count=int(application_list[current_tab].paint_count.text()))
                else:
                    raise StopException
                print(f"{application_list[current_tab].tab_name.text()} 传回完毕")

        # 执行完后要将执行判断置否
        running_variable.running = False

        # 播放声音
        playsound()
    except StopException as e:
        print(f"{application_list[current_tab].tab_name.text()} 任务中止")
        running_variable.running = False
    except:
        running_variable.running = False
        # 播放声音
        playsound()
        traceback.print_exc()
    finally:
        pythoncom.CoUninitialize()  # 清理com环境


def hd_back_ps(application_list, current_tab):
    try:
        pythoncom.CoInitialize()  # 初始化com环境

        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
            data = json.load(f)
            setting = data["settings"][application_list[current_tab].preset_combo.currentIndex()]
            model = ""
            if "model" in setting:
                model = setting["model"]
            hd_method = setting["algorithm"]
            is_hd = setting["continue1"]
            is_back_ps = setting["continue2"]
            continue1 = float(setting["interval1"])
            continue2 = float(setting["interval2"])
            max_pics = int(setting["max_psi1"])
            max_hd = int(setting["max_psi2"])
            negative = setting["negative"]
            positive = setting["positive"]
            sample = setting["sample"]

        # 先定位ps
        print(f"{application_list[current_tab].tab_name.text()} 开始执行传回ps任务")
        time.sleep(continue1)
        if running_variable.running:
            ps = start_ps()
            print(f"{application_list[current_tab].tab_name.text()} 定位到当前PS")
        else:
            raise StopException
        time.sleep(continue2)

        # 打开浏览器
        if running_variable.running:
            driver = open_driver()
            print(f"{application_list[current_tab].tab_name.text()} 打开浏览器")
        else:
            raise StopException

        time.sleep(continue2)

        # 打开weburl
        if running_variable.running:
            print(f"{application_list[current_tab].tab_name.text()} 打开webui_url")
            open_web_url(driver, application_list[current_tab].webui_url.text())
        else:
            raise StopException

        time.sleep(continue2)

        # 检测是否成功打开weburl
        if running_variable.running:
            reflesh_page(driver)
        else:
            raise StopException

        # 下载网页上的图片
        if running_variable.running:
            print(f"{application_list[current_tab].tab_name.text()} 正在下载网页图片")
            num = save_img_from_sd(driver, f"{application_list[current_tab].layer_name.text()}")
        else:
            raise StopException

        if running_variable.running:
            # 取消controlnet
            time.sleep(continue2)
            cancel_controlnet(driver)
        else:
            raise StopException
        back_SD_scale(driver, hd_method)
        for j in range(1, int(application_list[current_tab].paint_count.text()) + 1):
            # 输入原图尺寸以便进行尺寸计算
            print(f"{application_list[current_tab].tab_name.text()} 正在放大第{j}张图")
            time.sleep(continue2)
            # 设置重绘一遍
            if running_variable.running:
                set_batch_count(driver, 1)
            else:
                raise StopException
            # 设置重绘幅度
            time.sleep(continue2)
            if running_variable.running:
                set_strength(driver, application_list[current_tab].hd_weight.text())
            else:
                raise StopException
            # 导入要重绘的图片
            time.sleep(continue2)
            if running_variable.running:
                BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
                EXPORT_PATH = os.path.join(BASE_PATH, "EXPORT_SD")
                import_img_sd(driver,
                              os.path.join(EXPORT_PATH, f"{application_list[current_tab].layer_name.text()}-{j}.jpg"))
            else:
                raise StopException
            # 生成并保存图片
            time.sleep(continue2)
            if running_variable.running:
                SD_upscale_click_generate(driver, f"{application_list[current_tab].layer_name.text()}-{j}")
            else:
                raise StopException
            print(
                f"{application_list[current_tab].tab_name.text()} 第{j}张图放大完毕,保存为{application_list[current_tab].layer_name.text()}-{j}.jpg")
            time.sleep(continue2)

        # 导回图片
        print(f"{application_list[current_tab].tab_name.text()} 正在传回ps文档")
        time.sleep(continue2)
        if running_variable.running:
            try:
                short_key_import_image_from_sd(app=ps, img_name=application_list[current_tab].layer_name.text(),
                                               count=num)
            except:
                pass
        else:
            raise StopException
        print(f"{application_list[current_tab].tab_name.text()} 传回完毕")

        # 执行完后要将执行判断置否
        running_variable.running = False

        # 播放声音
        playsound()
    except StopException as e:
        print(f"{application_list[current_tab].tab_name.text()} 任务中止")
        running_variable.running = False
    except:
        running_variable.running = False
        traceback.print_exc()
        # 播放声音
        playsound()
    finally:
        pythoncom.CoUninitialize()  # 清理com环境


def lama_upload(application_list, current_tab):
    try:
        pythoncom.CoInitialize()  # 初始化com环境

        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
            data = json.load(f)
            setting = data["settings"][application_list[current_tab].preset_combo.currentIndex()]
            model = ""
            if "model" in setting:
                model = setting["model"]
            hd_method = setting["algorithm"]
            is_hd = setting["continue1"]
            is_back_ps = setting["continue2"]
            continue1 = float(setting["interval1"])
            continue2 = float(setting["interval2"])
            max_pics = int(setting["max_psi1"])
            max_hd = int(setting["max_psi2"])
            negative = setting["negative"]
            positive = setting["positive"]
            sample = setting["sample"]

        # 上传lama图片
        print(f"{application_list[current_tab].tab_name.text()} 开始执行上传Lama图片")
        time.sleep(continue1)
        running_variable.running = True
        if running_variable.running:
            ps = start_ps()
            print(f"{application_list[current_tab].tab_name.text()} 定位到当前PS")
        else:
            raise StopException

        time.sleep(continue2)
        # 打开浏览器
        if running_variable.running:
            driver = open_driver()
            print(f"{application_list[current_tab].tab_name.text()} 打开浏览器")
        else:
            raise StopException

        time.sleep(continue2)
        if running_variable.running:
            upload_img_to_lama(ps, driver, application_list[current_tab].lama_url.text(),application_list[current_tab].layer_name.text())
            print(f"{application_list[current_tab].tab_name.text()} 上传Lama图片成功")
        else:
            raise StopException

        # 执行完后要将执行判断置否
        running_variable.running = False

        # 播放声音
        playsound()
    except StopException as e:
        print(f"{application_list[current_tab].tab_name.text()} 任务中止")
        running_variable.running = False
    except:
        running_variable.running = False
        # 播放声音
        playsound()
        traceback.print_exc()
    finally:
        pythoncom.CoUninitialize()  # 清理com环境

def lama_download(application_list, current_tab):
    try:
        pythoncom.CoInitialize()  # 初始化com环境

        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
            data = json.load(f)
            setting = data["settings"][application_list[current_tab].preset_combo.currentIndex()]
            model = ""
            if "model" in setting:
                model = setting["model"]
            hd_method = setting["algorithm"]
            is_hd = setting["continue1"]
            is_back_ps = setting["continue2"]
            continue1 = float(setting["interval1"])
            continue2 = float(setting["interval2"])
            max_pics = int(setting["max_psi1"])
            max_hd = int(setting["max_psi2"])
            negative = setting["negative"]
            positive = setting["positive"]
            sample = setting["sample"]

        # 上传lama图片
        print(f"{application_list[current_tab].tab_name.text()} 开始执行传回Lama图片")
        time.sleep(continue1)
        running_variable.running = True
        if running_variable.running:
            ps = start_ps()
            print(f"{application_list[current_tab].tab_name.text()} 定位到当前PS")
        else:
            raise StopException

        time.sleep(continue2)
        # 打开浏览器
        if running_variable.running:
            driver = open_driver()
            print(f"{application_list[current_tab].tab_name.text()} 打开浏览器")
        else:
            raise StopException

        time.sleep(continue2)
        if running_variable.running:
            download_img_from_lama(ps, driver, application_list[current_tab].lama_url.text(),application_list[current_tab].layer_name.text())
            print(f"{application_list[current_tab].tab_name.text()} 传回Lama图片成功")
        else:
            raise StopException

        # 执行完后要将执行判断置否
        running_variable.running = False

        # 播放声音
        playsound()
    except StopException as e:
        print(f"{application_list[current_tab].tab_name.text()} 任务中止")
        running_variable.running = False
    except:
        running_variable.running = False
        # 播放声音
        playsound()
        traceback.print_exc()
    finally:
        pythoncom.CoUninitialize()  # 清理com环境