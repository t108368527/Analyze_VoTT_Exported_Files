---
title: '工具介紹'
disqus: hackmd
---

[TOC]
## 工具介紹

## 1. calculate_the_items.py

此工具是將所有Vott匯出的結果進行統計分析

### 使用方式

python calculate_the_items.py (資料夾位置) (匯出位置)

```python calculate_the_items.py E:\\VoTT_JSON\\  E:\\Auto_Calculate```

將所有VoTT匯出的結果放進第一個參數位置 (範例為E:\\VoTT_JSON\\)
![](https://i.imgur.com/zJJgQPA.png)


工具在分析後會將結果匯出成JSON格式放置第二個參數位置 (範例為E:\\Auto_Calculate)
並將其命名為 VoTT_JSON的子資料夾名稱 + _auto_calculate_the_items
![](https://i.imgur.com/p9VjQph.png)

### 分析結果
包含每幀標註多少人物+位置

![](https://i.imgur.com/0asWjjf.png)



## 2. calculate_bounding_boxs.py

此工具主要統計上方工具匯出的各個JSON檔各標註多少人物總共標註多少人物

### 使用方式

python calculate_bounding_boxs.py (Auto_Calculate資料夾位置) (匯出位置)

```python calculate_bounding_boxs.py E:\\Auto_Calculate\\ E:\\Auto_Calculate\\```


第一個參數為所有VoTT匯出檔案的分析結果資料夾位置

![](https://i.imgur.com/p9VjQph.png)

第二個參數則是要放置匯出文件的資料夾位置
並將其命名為 VoTT_Label_Result

### 分析結果
包含每份檔案總共多少人物+所有檔案總共標記多少人物

![](https://i.imgur.com/SgSPLBj.png)


## 2. compare_export_files.py

此工具主要是分析VoTT與其他模型輸出的JSON檔
並計算出Precision及Recall

### 使用方式

python compare_export_files.py (Auto_Calculate資料夾位置中某部影片的JSON檔) (模型輸出的JSON檔位置) (模型輸出的圖檔位置) (損失函數 可輸入CIoU/IoU) (是否要存照片)

```python compare_export_files.py E:\\Auto_Calculate\\Drone_003_auto_calculate_the_items.json F:\\MaskRCNN_Calculate\\Drone_003.json F:\\MaskRCNN_Compare_Image CIoU False```

第一個參數為所有VoTT匯出檔案的分析結果資料夾位置
![](https://i.imgur.com/p9VjQph.png)

第二個參數為模型輸出的JSON檔位置
![](https://i.imgur.com/0KxF4VH.png)

第三個參數為模型輸出的圖檔位置
![](https://i.imgur.com/9KDT24A.png)

第四個參數為選擇損失函數為CIoU或是IoU

第五個參數為是否要將VoTT的標註框放上模型輸出的圖檔上
(若為True則會放上，這部分會影響計算速度)

### 分析結果
包含每幀模型與VoTT各標註多少以及TP、FP、FN、Precision以及Recall
![](https://i.imgur.com/NJjyam5.png)

並將其結果輸出成JSON檔，放置此程式同一層的位置


## 2. recall.py

此工具主要是將compare_export_files.py輸出的一整包JSON文件統整併輸出成圖表

### 使用方式

python recall.py (JSON文件位置) (輸出文件位置)

```python recall.py F:\\MaskRCNN_Compare_Results F:\\```

第一個參數為compare_export_files.py匯出檔案位置
![](https://i.imgur.com/kc1jK0s.png)

第二個參數為統整後要儲存文件的位置

### 分析結果
包含每個文件(影片)最後統整的Precision以及Recall
![](https://i.imgur.com/uWjop3T.png)

以及輸出圖檔
![](https://i.imgur.com/ZPgupxp.jpg)

###### tags: `tool`, `Windows10`, `VoTT`, `MaskRCNN`, `YOLOv3`, `YOLOv4`