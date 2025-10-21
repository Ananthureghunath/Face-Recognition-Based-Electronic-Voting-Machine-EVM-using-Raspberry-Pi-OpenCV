import cv2
import numpy as np
from PIL import Image
import os
path = 'data'
recognizer = cv2.face.LBPHFaceRecognizer_create()
file = 'haarcascade_frontalface_default.xml'
detector = cv2.CascadeClassifier(cv2.data.haarcascades +file)
def getImages(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') 
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids
print ("\n Training faces. It will take a few seconds. Wait ...")
faces,ids = getImages(path)
recognizer.train(faces, np.array(ids))
recognizer.write('train/trainer.yml') 
print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))
