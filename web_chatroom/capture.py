import json
from flask import Response, Blueprint
from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
from flask import current_app

EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]
detection_model_path = 'web_chatroom/static/haarcascade_files/haarcascade_frontalface_default.xml'  # opencv的分类器，找出脸位置
emotion_model_path = 'web_chatroom/static/models/_mini_XCEPTION.102-0.66.hdf5'  # 训练好的模型
# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
capture = Blueprint('capture', __name__)


class DataProcess:
    def __init__(self):
        pass

    def getList(self, image):
        # resize: maintains the aspect ratio
        image = imutils.resize(image, width=200)
        # print("image size:", image.shape)
        # bgr->gray
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # detect face position (x,y,w,h)
        faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                flags=cv2.CASCADE_SCALE_IMAGE)
        # print("list:", faces)

        if len(faces) > 0:
            # ROI (region of interest)
            faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # predict via model
            preds = emotion_classifier.predict(roi)  # result list
            # 返回一下脸位置
            # face_restored_pos =[faces[0]/]
            # print(EMOTIONS)
            # print(preds)
            dictionary = dict(zip(EMOTIONS, preds[0].tolist()))
            return True, dictionary, faces
        else:
            return False, {}, []


dataProcess = DataProcess()


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame_byte(self):
        success, image = self.video.read()
        # 将图片转码成jpg
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_frame_pic(self):
        success, image = self.video.read()
        return image


def get_pic(camera):
    while True:
        frame = camera.get_frame_byte()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        # 注意Flask 要求视图函数返回的结果是可调用的
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def get_emo(camera):
    while True:
        res, emotion, face_pos = dataProcess.getList(camera.get_frame_pic())
        if res:
            # print(emotion)
            # print(json.dumps(emotion))
            yield json.dumps(emotion)


@capture.route('/video')  # 这个地址返回视频流响应
def video():
    # 视图函数的返回值会被自动转换为一个响应对象 mimetype控制contentType。
    # 不能传递音频，替换式的相应
    return Response(get_pic(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@capture.route('/emo')  # 这个地址分析情绪
def emo():
    return Response(get_emo(VideoCamera()))
