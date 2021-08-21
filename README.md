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


###### tags: `tool`, `Windows10`, `VoTT`


