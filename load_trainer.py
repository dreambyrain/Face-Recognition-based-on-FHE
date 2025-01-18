import cv2

#build LBPH face recognizor

recongnizer = cv2.face.LBPHFaceRecognizer_create()

#load trained model

trainer_path = "/home/yourname/桌面/trainer/trainer.yml"
recongnizer.read(trainer_path)

print("loading success!")