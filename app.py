from flask import Flask, render_template, request, redirect, url_for, flash
from flask_monitor import Monitor, ObserverLog
from werkzeug.utils import secure_filename
from PIL import Image
import cv2
import logging
import numpy as np
from backend.face import *

app =  Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    # process incoming files
    if request.method == 'POST':
        if 'file' not in request.files:
            logging.error('no file')
            # TODO: alert user if no file is found
        user_photo = request.files['file']
        logging.error(user_photo.filename)
        if user_photo.filename == '':
            logging.error('No photo selected')
            # TODO: alert user if no file name
            redirect('home.html')
        if user_photo and allowed_file(user_photo.filename):
            filename = secure_filename(user_photo.filename)
            img = Image.open(user_photo)
            img = np.array(img)
            img = analyse_user_face(img)
            if img != None:
                return render_template('result.html', img=img, error='')
        #TODO: handle if return value is None (didn't see a face)

        # TODO: redirect to result
    return render_template('home.html')

_allowed_extensions = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in _allowed_extensions

if __name__ == '__main__':
    app.secret_key = 'randomsecretkey'
    app.debug = True
    app.templates_auto_reload = True
    app.run()