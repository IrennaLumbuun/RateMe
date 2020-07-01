import face_recognition
from PIL import Image, ImageDraw

image_path = '../../Downloads/photo.jpg'
image = face_recognition.load_image_file(image_path)

# get arrays of locations of each faces
# [top, right, bottom, left]
face_location = face_recognition.face_location(image)

print(face_location)

# image matching

# encode image
known_image = face_recognition.face_encodings(image)[0]
# result = face_recognition.compare_faces([known_image], unknown_image)
# true if same,false otherwise

# poll faces
for face in face_location:
    top, right, bottom, left = face
    face_image = image[top:bottom, left:right]

    pil_image = Image.fromarray(face_image)
    # pil_image.show()
    # pil_image.save(f'{top}.jpg')

#draw on faces
face_encodings  = face_recognition.face_encodings(image, face_location)
# convert to pil
pil = Image.fromarray(image)
draw = ImageDraw.Draw(pil)

#see more https://www.youtube.com/watch?v=QSTnwsZj2yc