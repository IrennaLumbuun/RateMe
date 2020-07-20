from flask import Flask, render_template, request, redirect, url_for
import cv2
import base64
from backend.face import analyse_user_face

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True
)

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    # process incoming files
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('home.html', error='No file selected')

        user_photo = request.files['file']
        if user_photo.filename == '':
            return render_template('home.html', error='No photo selected')

        valid_extension = allowed_file(user_photo.filename)
        if not valid_extension:
            return render_template('home.html', error='Extension is not valid. Only allow .png, .jpg, and .jpeg')

        if user_photo and valid_extension:
            score, img = analyse_user_face(user_photo)
            print(score)
            if img.size > 0:
                _, buffer = cv2.imencode('.jpeg', img)
                b64 = base64.b64encode(buffer)
                return render_template('result.html', img=b64.decode('utf-8'), score=score)
            else:
                return render_template('home.html', error='Can\'t find a face in the picture')
    return render_template('home.html', error ='')


def allowed_file(filename) -> bool:
    _allowed_extensions = {'pdf', 'png', 'jpg', 'jpeg'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in _allowed_extensions


if __name__ == '__main__':
    app.secret_key = 'randomsecretkey'
    app.run(debug=True)
