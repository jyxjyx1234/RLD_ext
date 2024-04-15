#观察脚本发现文本格式：00 00 00 00 96 00 00 00 人名 00 文本 00，尝试据此进行解析
#仅针对明文rlb文件，根据游戏对应的脚本进行修改
import os

def process_binary_file(file_path):
    search_pattern = bytes([0x00, 0x00, 0x00, 0x00, 0x96, 0x00, 0x00])
    result_list = []

    with open(file_path, 'rb') as file:
        data = file.read()

    start = 0
    while True:
        start = data.find(search_pattern, start)
        if start == -1:
            break

        start += len(search_pattern)+1
        end = data.find(b'\x00', start)
        if end == -1:
            break

        name = data[start:end].decode('shift_jis', errors='ignore')

        start = end + 1
        end = data.find(b'\x00', start)
        if end == -1:
            break

        message = data[start:end].decode('shift_jis', errors='ignore')

        result_list.append({'name': name, 'message': message})

        start = end + 1

    return result_list

# Usage
import json

datanames = os.listdir('.\OriginFile\\rld')#改地址
for dataname in datanames:
    if os.path.splitext(dataname)[1] == '.rld':
        res=process_binary_file('.\OriginFile\\rld\\'+dataname)
        with open('.\OriginFile\\rld_processed\\'+dataname.replace('rld','json'),'w',encoding='utf8') as f:
            json.dump(res,f,ensure_ascii=False, indent=4)