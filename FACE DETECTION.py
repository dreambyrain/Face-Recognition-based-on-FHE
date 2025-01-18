from logging import warning

import cv2
import os
import urllib

import urllib.request

#加载训练数据集文件
recognizer = cv2.face.LBPHFaceRecognizer_create()
#加载数据
recognizer.read('trainer/trainer.yml')
#name
names=[]
#警报全局变量
warningtime = 0

#md5 encrypt
def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode("utf-8"))
    return m.hexdigest()

#SMS feedback
statusStr = {
    '0':'Success Sending',
    '-1':'Incomplete Parameters',
    '-2':'服务器空间不支持，请确认支持curl或者fsocket,联系您的空间解决或者更换空间',
    '30':'Password Error',
    '40':'Account do not exist',
    '41':'Insufficient Balance',
    '42':'Invalid Account',
    '43':'Ip address restrict',
    '50':'Sensitive Content'

}

#alarm model
def warning():
    smsapi = "http://api.smsbao.com/"
    #SMS platform account
    user = ''
    #password
    password = md5('')
    #content
    content = '[warning]\nReson: xxx\nAddress: xxx\nTime: xxx'
    #phone number
    phone = ('')

    data = urllib.parse.urlencode({'u':user,'p':password,'m':phone,'c':content})
    send_url = smsapi + 'sms?' +data
    respond = urllib.request.urlopen(send_url)
    the_page = respond.read().decode('utf-8')
    print(statusStr[the_page])


def face_detect_demo(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#change color to gray
    face_detector = cv2.CascadeClassifier('E:/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
    #face = face_detector.detectMultiScale(gray,1.1,5,cv2.CASCADE_SCALE_IMAGE,(100,100),(300,300))
    face=face_detector.detectMultiScale(gray,1.1,5,0,(300,300))
    for x,y,w,h in face:
        cv2.rectangle(img,(x,y),(x+w,y+h),color=(0,0,255),thickness=2)
        cv2.circle(img,center=(x+w//2,y+h//2),radius=w//2,color=(0,255,0),thickness=1)
        #face recognition
        ids,confidence = recognizer.predict(gray[y: y + h ,x : x + w])
        #print('标签id：'，ids,'置信评分：'，confidence)
        if confidence > 80:
            global warningtime
            warningtime += 1
            if warningtime > 100:
                warning()
                warningtime = 0
            cv2.putText(img,'unknow',(x+10,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,0),1)
        else:
            cv2.putText(img,str(names[ids-1]),(x+10,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,0),1)
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)  # 创建可调整窗口
    cv2.resizeWindow('result', 800, 600)  # 设置窗口大小
    cv2.imshow('result',img)
    #print('bug:',ids)

#name sign
def name():
    path = './save file'
    #names = []
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    for imagePath in imagePaths:
       name = str(os.path.split(imagePath)[1].split('.',2)[1])
       names.append(name)

#loading video
cap=cv2.VideoCapture('1.mp4')
name()
while True:
    flag,frame = cap.read()
    if not flag:
        break
    face_detect_demo(frame)
    if ord(' ') == cv2.waitKey(10):
        break
cv2.destroyAllWindows()
cap.release()