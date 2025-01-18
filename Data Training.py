import os
import cv2
from PIL import Image
import numpy as np

def getImageAndlabels(path):
    #save face data
    facesSamples=[]
    #save name data
    ids=[]
    #save picture data
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    #load classifier
    face_detector = cv2.CascadeClassifier('E:/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
    #traverse picture of the list
    for imagePath in imagePaths:
        #打开图片，灰度化 PIL有九种不同模式：1，L,P,RGB,RGBA,CMYK,YCbCr,I,F.
        PIL_img = Image.open(imagePath).convert('L')
        #将图像转换为数组，以黑白深浅
        img_numpy = np.array(PIL_img, 'uint8')
        #获取图片人脸特征
        faces = face_detector.detectMultiScale(img_numpy)
        #获取每张图片的id和姓名
        id = int(os.path.split(imagePath)[1].split('.')[0])
        #预防无面容照片
        for x,y,w,h in faces:
            ids.append(id)
            facesSamples.append(img_numpy[y:y+h,x:x+w])
        #打印面部特征和id
    print('id:',id)
    print('fs:',facesSamples)
    return facesSamples,ids


if __name__=='__main__':
    #picture route
    path='./save file'
    #catch graph array and id sign array and name
    faces,ids = getImageAndlabels(path)
    #加载识别器
    recognizer=cv2.face.LBPHFaceRecognizer_create()
    #train
    recognizer.train(faces,np.array(ids))
    #save file
    recognizer.write('trainer/trainer.yml')