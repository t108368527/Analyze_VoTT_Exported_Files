import os as os
import sys as sys
import json 
import re

#此工具為分析VoTT 匯出的JSON檔案 每幀標註多少人物+位置
# 使用方式: python calculate_the_items.py (資料夾位置)
#      EX： python calculate_the_items.py E:\\VoTT_JSON\\

# 建立存放匯出文件的資料夾
def createFolder(path):
    folder = os.path.exists(path)
    if not folder:
        #如果不存在，則建立新目錄
        os.makedirs(path)
        print('-----建立成功-----')

# 讀取JSON檔
def read_json_file(file):
    with open(file) as f:
        # 回傳json檔資料
        return json.load(f)

# 回傳資料夾內所有的資料夾
def check_folder(folders):
    is_folders=[]
    for folder in folders:
        if os.path.isdir(sys.argv[1] + '\\' + folder):
            is_folders.append(folder)
    return is_folders

if __name__ == '__main__':
    folderPath =  sys.argv[1]
    # 建立JSON檔存放位置
    exportPath = './Auto_Calculate'
    createFolder(exportPath)

    folders = os.listdir(folderPath)
    is_folders = check_folder(folders)
    for folder in is_folders:
        # JSON檔資料 dict
        calculates = {}
        calculates['regions']={}
        calculates_item = [];
        # 總共label多少
        totalLabels = 0;
        # 先建立產出JSON檔的name
        # substrName = sys.argv[1].rfind('\\')
        targetName = folder
        calculates['name'] = targetName
        print(targetName)
        # 要讀取的資料夾
        path = sys.argv[1] + folder + '\\vott-json-export'
        
        if os.path.exists(path):
            # 遍歷檔案
            files = os.listdir(path)
            for file in files:
                print(file)
                # 若黨名與資料夾名稱相同則打開
                if(file == calculates['name']+"-export.json"):
                    
                    data = read_json_file(path+'/'+file)
                    keys = list(data['assets'].keys())
                    
                    for key in reversed(keys):
                        bbox=[]
                        b = []
                        # re.sub刪除 '.mp4'
                        index = re.sub(".mp4","",str(data['assets'][key]['asset']['name']))
                        calculates['regions'][index] = {}
                        # 這個frame總共標記多少個人物
                        totalLabels = totalLabels + len(data['assets'][key]['regions'])
                        calculates['regions'][index]['count'] = len(data['assets'][key]['regions'])
                        # bbox
                        if data['assets'][key]['regions'] :
                            for i in range(len(data['assets'][key]['regions'])):
                                b.append([ int(data['assets'][key]['regions'][i]['points'][0]['y']),int(data['assets'][key]['regions'][i]['points'][0]['x']),int(data['assets'][key]['regions'][i]['points'][2]['y']),int(data['assets'][key]['regions'][i]['points'][2]['x'])])
                            calculates['regions'][index]['boundingBox'] = b
                        else:
                            calculates['regions'][index]['boundingBox']=[]

                    calculates['total_labels'] = totalLabels
                    # JSON檔名
                    file = exportPath + '/' + folder + '_auto_calculate_the_items.json'
                    with open(file, 'w') as obj:
                        # 輸出成JSON並格式化
                        json.dump(calculates, obj, indent=4, separators=(',', ':'))