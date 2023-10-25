import json
import os
import sys
import winsound

isplaysound=True

def check_is_sound():
    global isplaysound
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
    if "isplaysound" not in data:
        data["isplaysound"]=True
        with open(os.path.join(BASE_PATH, "config.json"), "w") as f:
            # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
            formatted_data = json.dumps(data, indent=4)
            # 将格式化后的 json 字符串写入新的文件
            f.write(formatted_data)
    isplaysound=data["isplaysound"]

def playsound():
    if isplaysound:
        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        sound_file = os.path.join(BASE_PATH, "BeepBox-Song.wav")  # 声音文件的路径
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)

def repair_is_sound(is_play):
    global isplaysound
    isplaysound=is_play
    if is_play:
        print("设置任务结束后播放音频")
    else:
        print("设置任务结束后不播放音频")
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
        data["isplaysound"]=is_play
    with open(os.path.join(BASE_PATH, "config.json"), "w") as f:
        # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
        formatted_data = json.dumps(data, indent=4)
        # 将格式化后的 json 字符串写入新的文件
        f.write(formatted_data)