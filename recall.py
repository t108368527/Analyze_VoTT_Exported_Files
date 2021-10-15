import os as os
import sys as sys
import json 
import numpy as np
import matplotlib.pyplot as plt

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

def draw_bar(xData, y1Data, y2Data):
    width=0.25
    x1 = xData
    y1 = y1Data
    x2=[p for p in x1]
    y2 = y2Data
    plt.axhline(y=0.5, xmin=0, xmax=50,linestyle='--',color="red")
    plt.text(-5,0.5, 0.5, color="red", ha="left", va="center")
    plt.bar(x1, y1, label='Precision',align ='edge', width=0.35)  #繪製長條圖
    plt.bar(x1, y2, label='Recall',align ='edge', width=-0.35)  #繪製長條圖
    plt.xticks(x1,rotation=90)    #設定 X 軸刻度標籤
    plt.legend()                               #顯示圖例
    plt.title('Precision & Recall')            #設定圖形標題
    plt.xlabel('Drone Video')                         #設定 X 軸標籤
    plt.ylabel('%')          #設定 Y 軸標籤
    # ax = plt.axes()
    # for i, j in zip(y1, y2):
    #     ax.text(j+1, i-0.5, "{}".format(j))
    plt.show()

if __name__ == '__main__':
    # 用法：python recall.py F:\\Drone_Compare_Result F:\\
    # 計算總Precision跟Recall
    folderPath =  sys.argv[1]
    # 建立JSON檔存放位置
    exportPath = sys.argv[2]
    # return data
    calculates = {}
    calculates['result'] = []
    precision = 0
    recall = 0
    xData = []
    y1Data = []
    y2Data = []

    files = os.listdir(folderPath)
    
    for file in files:
        file_data = {}
        file_data['name'] = str(file)[6:9]
        xData.append(file_data['name'])
        # 讀取JSON資料
        content = read_json_file(sys.argv[1] +'\\' +file)
        file_data['Precision'] = content['Precision_Final']
        y1Data.append(file_data['Precision'])
        file_data['Recall'] = content['Recall_Final']
        y2Data.append(file_data['Recall'])
        precision = precision + content['Precision_Final']
        recall = recall + content['Recall_Final']
        calculates['result'].append(file_data)

    draw_bar(xData, y1Data, y2Data)
    calculates['Precision_Final'] = precision / len(files)
    calculates['Recall_Final'] = recall / len(files)
    print(precision / len(files))
    print(recall / len(files))
    # JSON檔名
    file = exportPath + '/' + 'precision_recall_auto_calculate.json'
    with open(file, 'w') as obj:
        # 輸出成JSON並格式化
        json.dump(calculates, obj, indent=4, separators=(',', ':'))