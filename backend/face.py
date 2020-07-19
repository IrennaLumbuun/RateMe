from PIL import Image
import urllib.request
import ssl
import cv2
import time
import os
import io
from predictor import predict
import math

import importlib
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToDict

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
        label = f'./data/{index}_{curr.tm_hour}_{curr.tm_min}_{curr.tm_sec}.jpg'
        cv2.imwrite(label, roi)
        roi_list.append(label)
        index += 1
    
    return roi_list

def analyse_user_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    if faces == []:
        return []
    #TODO: return a list of faces and their respective scores inistead
    for x, y, w, h in faces:
        roi = gray[y:y+h, x:x+w] # get only the face region
        roi = cv2.resize(roi, (150, 150))
        score = predict(roi)

        # add rectangle and label
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), thickness=10)
        img = cv2.putText(img, str(round(score, 1)), (x + 75, y + h + 150), cv2.FONT_HERSHEY_SIMPLEX, 5, color=(255,255,255), thickness=5)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img, score

client = vision.ImageAnnotatorClient()


def distance(pos1: dict, pos2: dict):
    # sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)
    dis_x = pos2.get('x') - pos1.get('x')
    sqr_x = dis_x * dis_x
    dis_y = pos2.get('y') - pos1.get('y') 
    sqr_y = dis_y * dis_y
    dis_z = pos2.get('z')  - pos1.get('z') 
    sqr_z = dis_z * dis_z

    return math.sqrt(sqr_x + sqr_y + sqr_z)


def get_features(image_url: str) -> list:
    request = {
        'image': {
            'source': {
                'image_uri': image_url
                },
            },
        }
    response = client.annotate_image(request)
    response = MessageToDict(response)
    
    # assume there's only 1 face per picture
    # faceAnnotations always return a list of face
    # take the first one only
    try:
        landmarks = response['faceAnnotations'][0]['landmarks']
    except:
        return list()
    
    return get_numeric_feature(landmarks)


def get_numeric_feature(landmarks: list) -> list:
    pos = dict()
    index = 1
    for el in landmarks:
        pos[el.get('type', '').lower()] = el['position']
        index += 1

    to_write = list()
    
    # ratio of left eye to mid & right eye to mid
    left_eye_to_mid = distance(pos['left_eye'], pos['midpoint_between_eyes'])
    right_eye_to_mid = distance(pos['right_eye'], pos['midpoint_between_eyes'])
    to_write.append(left_eye_to_mid / right_eye_to_mid)

    # ratio of distance between eyes & face width at eyes
    distance_between_eyes = distance(pos['left_eye'], pos['right_eye'])
    face_width_at_eye = distance(pos['right_eye_right_corner'], pos['left_eye_left_corner'])
    to_write.append(distance_between_eyes / face_width_at_eye)

    # ratio of left eyebrow length and right eyebrow length
    left_eyebrow_length = distance(pos['left_of_left_eyebrow'], pos['right_of_left_eyebrow'])
    right_eyebrow_length = distance(pos['left_of_right_eyebrow'], pos['right_of_right_eyebrow'])
    to_write.append(left_eyebrow_length / right_eyebrow_length)

    # ratio between face width at eyes and face width at ear
    face_width_at_ear = distance(pos['left_ear_tragion'], pos['right_ear_tragion'])
    to_write.append(face_width_at_eye / face_width_at_ear)

    # distance nose to forehead glabella / distance chin to forehead glabella
    nose_to_forehead = distance(pos['nose_tip'], pos['forehead_glabella'])
    chin_to_forehead = distance(pos['chin_gnathion'], pos['forehead_glabella'])
    to_write.append(nose_to_forehead / chin_to_forehead)

    # lip height / lip width
    lip_height = distance(pos['upper_lip'], pos['lower_lip'])
    lip_width = distance(pos['mouth_left'], pos['mouth_right'])
    to_write.append(lip_height / lip_width)

    # nose width / lip width
    nose_width = distance(pos['nose_bottom_left'], pos['nose_bottom_right'])
    to_write.append(nose_width / lip_width)

    return to_write


#save_face(url)
#see more https://www.youtube.com/watch?v=QSTnwsZj2yc
# or https://medium.com/better-programming/step-by-step-face-recognition-in-images-ad0ad302058a
