import face_recognition

image_path = '../../Downloads/photo.jpg'
image = face_recognition.load_image_file(image_path)

# get arrays of locations of each faces
# [top, right, bottom, left]
face_location = face_recognition.face_location(image)

print(face_location)