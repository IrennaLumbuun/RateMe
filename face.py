from PIL import Image, ImageDraw
import urllib.request
import ssl
import cv2
import time
import os

'''
    Load image from url & save it
'''

context = ssl._create_unverified_context()
url = 'https://preview.redd.it/l2o5vkkf8k851.jpg?width=640&crop=smart&auto=webp&s=6f0f279f2ee32da5218946078c537a68dc579864'
face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt2.xml')

def save_face(url: str) -> list:
    # make a directory
    if not os.path.exists('data'):
        os.makedirs('data')

    # open & save image
    image = Image.open(urllib.request.urlopen(url, context=context))
    image_path = './temp.jpg'
    image.save(image_path)

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

#save_face(url)
#see more https://www.youtube.com/watch?v=QSTnwsZj2yc
# or https://medium.com/better-programming/step-by-step-face-recognition-in-images-ad0ad302058a
