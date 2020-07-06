from PIL import Image
import urllib.request
import ssl
import cv2
import time
import os
from backend.predictor import predict
import math

'''
    Load image from url & save it
'''

context = ssl._create_unverified_context()
face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt2.xml')

def open_url(url: str) -> str:
    # make a directory
    if not os.path.exists('data'):
        os.makedirs('data')

    # open & save image
    image = Image.open(urllib.request.urlopen(url, context=context))
    image = image.convert('RGB') #if an image was blured / in an rgba format
    image_path = './temp.jpg'
    image.save(image_path)

    return image_path

def save_face(image_path: str) -> list:

    # get face location
    img = cv2.imread(image_path, 0)
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.5, minNeighbors=5)

    roi_list = [] # roi = region of interest (i.e the face only)
    index = 1
    for x, y, w, h in faces:
        roi = img[y:y+h, x:x+w] # get only the face region
        roi = cv2.resize(roi, (150, 150))
        curr = time.gmtime()
        label = f'./data/{index}_{curr.tm_min}_{curr.tm_sec}.jpg'
        cv2.imwrite(label, roi)
        roi_list.append(label)
        index += 1
    
    return roi_list

def analyse_user_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    if faces == []:
        return None
    for x, y, w, h in faces:
        roi = gray[y:y+h, x:x+w] # get only the face region
        roi = cv2.resize(roi, (150, 150))
        score = predict(roi)

        # add rectangle and label
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 5)
        img = cv2.putText(img, str(round(score, 1)), (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 5, color=(0,0,0), thickness=2)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

#save_face(url)
#see more https://www.youtube.com/watch?v=QSTnwsZj2yc
# or https://medium.com/better-programming/step-by-step-face-recognition-in-images-ad0ad302058a
