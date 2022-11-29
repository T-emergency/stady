import torch
import base64
import cv2
import numpy as np


def is_study(request):
    if request.method == "POST":
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

        img = request.POST.get('imgUpload', '')
        img_str = img.split(',')[1]
        imgdata = base64.b64decode(img_str)

        arr = np.fromstring(imgdata, np.uint8)

        img = cv2.imdecode(arr, cv2.IMREAD_ANYCOLOR)


        results = model(img)
        result = results.pandas().xyxy[0].to_numpy()
        print(result)
        result = [ item for item in result if item[6] == 'person'] 
        
        if len(result) == 0:
            return False
        return True
    
    return False