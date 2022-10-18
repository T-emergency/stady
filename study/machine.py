import torch
import base64
import io
import cv2
from PIL import Image
import numpy as np


def is_study(request):
    if request.method == "POST":
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

        img = request.POST.get('imgUpload', '') # base64를 통한 이미지 문자열
        img_str = img.split(',')[1] # 이미지 문자열 추출
        imgdata = base64.b64decode(img_str) # 이미지 문자열 디코딩

        arr = np.fromstring(imgdata, np.uint8) # 디코딩된 문자열을 ndrray로 변환

        img = cv2.imdecode(arr, cv2.IMREAD_ANYCOLOR) # 이미지로 변환
        image = cv2.resize(arr, (img.shape[0], img.shape[1])) # 3차원으로 변경
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # 컬러 변경

        results = model(img) # 모델에 따른 이미지 결과 도출
        result = results.pandas().xyxy[0].to_numpy()
        print(result)
        result = [ item for item in result if item[6] == 'person'] 
        
        if len(result) == 0:
            return False
        return True
    
    return False