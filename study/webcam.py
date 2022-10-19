from imp import load_module
from django.shortcuts import render, redirect
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import torch
# webcam = cv2.VideoCapture(0)

# if not webcam.isOpened():
#     print('웹캠 실행 할 수 없음')
#     exit()
    
# while webcam.isOpened():
#     status, frame = webcam.read()
    
#     if status:
#         cv2.imshow('test',frame)
        
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
    
# webcam.release()
# cv2.destroyAllWindows()


class VideoCamera(object):
    def __init__(self):
        self.model = self.load_model()
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()


    def get_frame(self):
        image = self.frame
        result= self.model(image)
        
        for i in result.crop(save=False):
            if 'person' in i['label']:
                xmin, ymin, xmax, ymax = map(lambda x: int(x.item()), i['box'])
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 255, 255), 10)
                cv2.waitKey(25)
    
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            
    
    def load_model(self):
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        return model
    
    def save(self):
        print('VideoCamera().save()')
        return cv2.imwrite(f'media/log/log.png',self.frame )

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def detectme(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass

    
def frame_save(request):
    VideoCamera().save()
    return redirect('/')
    # if cv2.VideoCapture.isOpened():
    #     VideoCamera().save()
    #     return redirect('/')
    # else:
    #     print('카메라가 연결되지 않았습니다')
    #     return redirect('/')