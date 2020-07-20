from PIL import Image
import ssl
import sys
import cv2
from .predictor import predict
import math
import numpy as np

# Imports the Google Cloud client library
from google.cloud import vision
from google.protobuf.json_format import MessageToDict

'''
    Load image from url & save it
'''

context = ssl._create_unverified_context()
face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt2.xml')
client = vision.ImageAnnotatorClient()


def distance(pos1: dict, pos2: dict) -> float:
    # sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)
    dis_x = pos2.get('x') - pos1.get('x')
    sqr_x = dis_x * dis_x
    dis_y = pos2.get('y') - pos1.get('y') 
    sqr_y = dis_y * dis_y
    dis_z = pos2.get('z')  - pos1.get('z') 
    sqr_z = dis_z * dis_z

    return math.sqrt(sqr_x + sqr_y + sqr_z)


# given a dict of request
# return a list of corrds and features of each face
def get_features(request: dict):
    response = client.annotate_image(request)
    response = MessageToDict(response)
    faces = response['faceAnnotations']
    list_coords = list()
    list_features = list()
    for face in faces:
        try:
            list_features.append(get_numeric_feature(face['landmarks']))
            list_coords.append(face['fdBoundingPoly']['vertices'])
        except:
            print(response)
            return list()

    return list_coords, list_features


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


# when users submit their picture
# pass it to get_features for analysing
def analyse_user_face(img):
    # the predicton is gonna call read() on img, 
    # which results in it being empty
    img_copy = img 

    b64_img = img.read()
    request = {
        'image': {
            'content': b64_img
        },
        'features': [{
                'type': vision.enums.Feature.Type.FACE_DETECTION
            }]
        }

    # get a list of coordinates & features for each face
    # draw squares and write scores on each face
    list_coord, list_features = get_features(request)
    img = Image.open(img_copy)
    img = np.array(img)

    for i in range(0, len(list_features)):
        score = predict(list_features[i])
        coord = list_coord[i]

        upper_left = [sys.maxsize, sys.maxsize]
        bottom_right = [0, 0]

        # coordinates returned from google vision may not contain
        # both x and y
        # so we have to find it manually
        for c in coord:
            if c.get('x', sys.maxsize) < upper_left[0]:
                upper_left[0] = c['x']
            if c.get('x', 0) > bottom_right[0]:
                bottom_right[0] = c['x']
            if c.get('y', sys.maxsize) < upper_left[1]:
                upper_left[1] = c['y']
            if c.get('y', 0) > bottom_right[1]:
                bottom_right[1] = c['y']

        # TODO: scale font size based on pic size
        img = cv2.rectangle(img, tuple(upper_left), tuple(bottom_right), (255, 255, 255), thickness=10)
        img = cv2.putText(img, str(round(score, 1)), (upper_left[0] + 75, bottom_right[1] + 150), cv2.FONT_HERSHEY_SIMPLEX, 5, color=(255,255,255), thickness=5)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return score, img
