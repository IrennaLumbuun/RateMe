import face_recognition
from PIL import Image, ImageDraw
import urllib.request
import ssl


'''
    Load image from url & save it
'''

context = ssl._create_unverified_context()
url = 'https://preview.redd.it/0jzy2kgbhb851.jpg?width=640&crop=smart&auto=webp&s=3d9e423ba3cf5bb8c2c842b52245c63c8ff29901'

def get_face(url: str) -> list:
    image = Image.open(urllib.request.urlopen(url, context=context))
    # TODO: save this in cloud database
    image_path = 'test.jpg'
    image.save(image_path)

    # get face location
    image = face_recognition.load_image_file(image_path)
    face_location = face_recognition.face_locations(image)
    print(face_location)

    '''
        Poll face from image & save it
    '''
    top, right, bottom, left = face_location[0]
    face_image = image[top:bottom, left:right]
    polled_image = Image.fromarray(face_image)

    # TODO: save this in cloud database
    polled_image_path = 'polled_test.jpg'
    polled_image.save(polled_image_path)

    polled_image = face_recognition.load_image_file(polled_image_path)
    face_encodings  = face_recognition.face_encodings(polled_image)
    
    return face_encodings[0]

#see more https://www.youtube.com/watch?v=QSTnwsZj2yc
# or https://medium.com/better-programming/step-by-step-face-recognition-in-images-ad0ad302058a

