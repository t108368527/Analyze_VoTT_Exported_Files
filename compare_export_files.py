import os as os
import sys as sys
import json 
import cv2
import math

# def loadFile(path):
def drawBbox(picName, folderName,vottBbox):
    # vottBbox = 陣列
    # FIXME:若替換Model 需修改
    path = 'C:\\Model_Output_Image\\' + folderName + '_compare_img'
    folder = os.path.exists(path)
    #FIXME: 照片輸出位置 若改別Model 這邊要改
    print('C:\\Model_Output_Image\\'+folderName+'\\'+ picName)
    img = cv2.imread('F:\\Model_Output_Image\\'+folderName+'\\'+ picName +'.jpg')
    if img is not None:
        for v in vottBbox:
            # bbox
            cv2.rectangle(img, (v[1], v[0]), (v[3], v[2]), (0, 0, 255), 3)
            # VoTT
            cv2.putText(img, 'VoTT', (v[1]-15, v[2]+29), cv2.FONT_HERSHEY_COMPLEX_SMALL,2, (0, 0, 255),2 )
        if not folder:
            #如果不存在，則建立新目錄
            os.makedirs(path)
            print('-----建立成功-----')
            cv2.imwrite(os.path.join(path , picName +'_compare.jpg'), img)

        else:
            #如果目錄已存在，則不建立
            cv2.imwrite(os.path.join(path , picName +'_compare.jpg'), img)
    
def getLast(vottJson,maskRcnnJson):
    vottLastSecond  = 0
    maskRcnnLastSecond = 0;
    for v in range(len(vottJson['regions'])):
        if vottLastSecond < vottJson['regions'][v]['timestamp'] and vottJson['regions'][v]['timestamp']:
            vottLastSecond = vottJson['regions'][v]['timestamp']
    for mr in range(len(maskRcnnJson['regions'])):
        if maskRcnnLastSecond < maskRcnnJson['regions'][mr]['timestamp'] and maskRcnnJson['regions'][mr]['timestamp']:
            maskRcnnLastSecond = maskRcnnJson['regions'][mr]['timestamp']

    if maskRcnnLastSecond > vottLastSecond:
        return maskRcnnLastSecond
    else:
        return vottLastSecond

def calculateIoU(VoTT_bbox, MR_bbox):
    VoTT_bbox = [int(x) for x in VoTT_bbox]
    MR_bbox = [int(x) for x in MR_bbox]

    xA = max(VoTT_bbox[0], MR_bbox[0])
    yA = max(VoTT_bbox[1], MR_bbox[1])
    xB = min(VoTT_bbox[2], MR_bbox[2])
    yB = min(VoTT_bbox[3], MR_bbox[3])

    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    VoTTArea = (VoTT_bbox[2] - VoTT_bbox[0] + 1) * (VoTT_bbox[3] - VoTT_bbox[1] + 1)
    MRArea = (MR_bbox[2] - MR_bbox[0] + 1) * (MR_bbox[3] - MR_bbox[1] + 1)
    
    iou = interArea / float(VoTTArea + MRArea - interArea)

    return iou

def calculateCIoU(VoTT_bbox, Compare_bbox):
    # calculate area of each box
    width_1 = VoTT_bbox[3] - VoTT_bbox[1]
    height_1 = VoTT_bbox[2] - VoTT_bbox[0]
    area_1 = width_1 * height_1

    width_2 = Compare_bbox[3] - Compare_bbox[1]
    height_2 = Compare_bbox[2] - Compare_bbox[0]
    area_2 = width_2 * height_2

    # calculate center point of each box
    center_x1 = (VoTT_bbox[3] - VoTT_bbox[1]) / 2
    center_y1 = (VoTT_bbox[2] - VoTT_bbox[0]) / 2
    center_x2 = (Compare_bbox[3] - Compare_bbox[1]) / 2
    center_y2 = (Compare_bbox[2] - Compare_bbox[0]) / 2

    # calculate square of center point distance
    p2 = (center_x2 - center_x1) ** 2 + (center_y2 - center_y1) ** 2

    # calculate square of the diagonal length
    width_c = max(VoTT_bbox[3], Compare_bbox[3]) - min(VoTT_bbox[1], Compare_bbox[1])
    height_c = max(VoTT_bbox[2], Compare_bbox[2]) - min(VoTT_bbox[0], Compare_bbox[0])
    c2 = width_c ** 2 + height_c ** 2

    # find the edge of intersect box
    left = max(VoTT_bbox[1], Compare_bbox[1])
    top = max(VoTT_bbox[0], Compare_bbox[0])
    bottom = min(VoTT_bbox[2], Compare_bbox[2])
    right = min(VoTT_bbox[3], Compare_bbox[3])

    # calculate the intersect area
    area_intersection = (right - left) * (bottom - top)

    # calculate the union area
    area_union = area_1 + area_2 - area_intersection

    # calculate iou
    if area_union == 0:
        iou = 0
    else:
        iou = float(area_intersection) / area_union

    # calculate v
    if height_2 == 0 or height_1 == 0:
        arctan = 0
    else:
        arctan = math.atan(float(width_2) / height_2) - math.atan(float(width_1) / height_1)
    v = (4.0 / math.pi ** 2) * (arctan ** 2)

    # calculate alpha
    alpha = float(v) / (1 - iou + v)

    # calculate ciou(iou - p2 / c2 - alpha * v)
    ciou = iou - float(p2) / c2 - alpha * v

    return ciou

def compareResult(vottJson, maskRcnnJson):
    # 總共比對多少幀
    timestampCount = 0;
    # Total Precision
    totalPrecision = 0;
    # Total Recall
    totalRecall = 0;
    # 6FPS
    timestamp_fps = [0, 0.166667, 0.333333, 0.5, 0.666667, 0.833333]
    # 秒數
    time = 0
    count = 0
    tmp = 0
    # 比對結果
    result = {}
    result['result'] = []
    # 比較vott MasKRcnn最後一幀 取得最後一秒
    second = getLast(vottJson,maskRcnnJson)
    print(second)
    # 主要以VoTT為主
    for vott in vottJson['regions']:
        # 比對兩者
        IoU_result = {}
        IoU_result['name'] = vott['name']
        IoU_result['VoTT'] = vott['count']
        # 若MaskRCNN此幀沒有偵測到人物 一樣要紀錄
        detection = False
        # 被比較者為MaskRCNN
        for mask in maskRcnnJson['regions']:
            
            # 當兩者在這時間點都有時 則去比對
            if vott['timestamp'] == mask['timestamp']:
                detection = True
                # 畫圖
                print(vott['name'])
                if storageBbox == 'True':
                    drawBbox(vott['name'], vottJson['name'], vott['boundingBox'])
                # Model 共標記 #FIXME: 照片輸出位置 若改別Model 這邊要改
                IoU_result['Model'] = mask['count']
                # 計算IOU
                bbox_count = 0
                catch = False
                for vott_bbox in vott['boundingBox']:
                    if catch == False:
                        item = 0
                    while item < mask['count']:
                        if loss.lower() == 'ciou':
                            iou_number = calculateCIoU(vott_bbox, mask['boundingBox'][item])
                        elif loss.lower() == 'iou':
                            iou_number = calculateIoU(vott_bbox, mask['boundingBox'][item])
                            
                        # 若數值>0.5則判斷有抓到
                        if iou_number > 0.2:
                            # print(iou_number)
                            catch = True
                            bbox_count = bbox_count + 1
                            break
                        item = item + 1

                IoU_result['TP'] = bbox_count # VoTT 跟 MaskRCNN偵測的框有重疊
                IoU_result['FP'] = mask['count'] - bbox_count # MaskRCNN 有框到 但VoTT沒有 (偵測錯誤)
                IoU_result['FN'] = vott['count'] - bbox_count # VoTT有框到 但MaskRCNN沒有 (無偵測到)
                print('TP:'+str(IoU_result['TP']) )
                print('FP:'+str(IoU_result['FP']) )
                print('FN:'+str(IoU_result['FN']) )
                IoU_result['Precision'] = IoU_result['TP'] / (IoU_result['TP'] + IoU_result['FP'] )
                # 由於MaskRCNN可能會把一票人 框成一個 因此FP可能會呈負數，如Drone_027 t=6.166667
                if IoU_result['Precision'] > 1.0:
                    IoU_result['Precision'] = 1.0

                if (IoU_result['TP'] + IoU_result['FN'] ) != 0:
                    IoU_result['Recall'] = IoU_result['TP'] / (IoU_result['TP'] + IoU_result['FN'] )
                else:
                    IoU_result['Recall'] = 1.0

                if IoU_result['Recall'] > 1.0:
                    IoU_result['Recall'] = 1.0
                totalPrecision = totalPrecision + IoU_result['Precision']
                totalRecall = totalRecall + IoU_result['Recall']
                result['result'].append(IoU_result)
                break

        if detection == False:
            #FIXME: 若改別Model 這邊要改 
            IoU_result['Model'] = 0 # MaskRCNN沒有偵測到人物
            IoU_result['TP'] = 0
            IoU_result['FP'] = 0
            IoU_result['Precision'] = 0
            IoU_result['Recall'] = 0
            totalPrecision = totalPrecision + IoU_result['Precision']
            totalRecall = totalRecall + IoU_result['Recall']
            result['result'].append(IoU_result)

    result['Precision_Final'] = round(totalPrecision / len(vottJson['regions']),2)
    result['Recall_Final'] = round( totalRecall / len(vottJson['regions']),2)
    return result

def read_json_file(file):
    with open(file) as f:
        # 回傳json檔資料
        return json.load(f)

if __name__ == '__main__':
    # > python compare_export_files.py E:\\Auto_Calculate\\Drone_003_auto_calculate_the_items.json E:\\Mask_RCNN\\samples\\Drone_003.json F:\\MaskRCNN_Compare_Image CIoU False
    # > python compare_export_files.py E:\\Auto_Calculate\\Drone_019_auto_calculate_the_items.json F:\\Yolov3_Calculate\\Drone_019.json F:\\MaskRCNN_Compare_Image IoU True
    # 執行時輸入兩個要比較的JSON檔案位置
    
    storageBbox = sys.argv[5] # 是否要存照片
    loss = sys.argv[4] # 損失函數
    imagePath = sys.argv[3] # 圖片位置
    filePath_1 = sys.argv[1] # VoTT
    filePath_2 = sys.argv[2] # MaskRCNN / YoloV4 / YoloV3
    vottJson = read_json_file(filePath_1)
    maskRcnnJson = read_json_file(filePath_2)
    finalResult = compareResult(vottJson, maskRcnnJson)
    
    print(finalResult)
    # FIXME:若替換Model 需修改
    path = '.\\'
    # JSON檔名
    # FIXME: 若替換損失函數 這邊需改名稱
    file = path + vottJson['name'] + '_' + loss  + 'model_compare_result.json'
    with open(file, 'w', encoding='utf8') as obj:
    #     # 輸出成JSON並格式化
        json.dump(finalResult, obj, indent=4, separators=(',', ':'), ensure_ascii=False)

    # 2021-08-24 
    # 儲存兩者此frame各標記多少
    # 計算IOU MaskRCNN / HumanMade
    # 修正MASKRCNN的標註數量 