import os as os
import sys as sys
import json 

# 此工具主要統計所有json檔總共標註多少人物
# 使用方式: python calculate_bounding_boxs.py (Auto_Calculate資料夾位置) (匯出位置)
#      EX： python calculate_bounding_boxs.py E:\\Auto_Calculate\\ E:\\Auto_Calculate\\


# 讀取JSON檔
def read_json_file(file):
    with open(file) as f:
        # 回傳json檔資料
        return json.load(f)

def export_json_file(path, fileName, data):
    with open(path + fileName, 'w') as obj:
        # 輸出成JSON並格式化
        json.dump(data, obj, indent=4, separators=(',', ':'))
        print('Done!')

if __name__ == '__main__':
    # export data
    calculates = {}
    total = 0
    # 資料夾位置
    folderPath =  sys.argv[1]
    files = os.listdir(folderPath)
    for file in files:
        # 讀取JSON文件內容
        data = read_json_file(sys.argv[1] + file)
        # 各個JSON文件標註多少
        if 'name' in data: 
            key = data['name']
            calculates[key] = data['total_labels']
            # 將所有JSON文件標註的total加總
            total = total + data['total_labels']
    calculates['total_labels'] = total
    export_json_file(sys.argv[2], 'VoTT_Label_Result.json', calculates)
        