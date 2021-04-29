from app import app, socketio
from flask import render_template
from app.model import cartoonize as cartoonify
from flask_socketio import SocketIO, emit
import numpy as np
from cv2 import cv2
import io
import base64
import json

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image')
def image_template():
    return render_template('image.html')

@socketio.on('test_image')
def test(data):
    emit('same_image',data)

@socketio.on('input_image')
def input_image(data):
    print("Image received")
    try:
        heading, encoded_data = data.split(',')
        nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print("Frame convertion done, sent to ml model to cartoonise")
        processed_image = cartoonify.cartoonize(frame)
        print("Image cartoonized")
        _, im_arr = cv2.imencode('.jpg', processed_image)  # im_arr: image in Numpy one-dim array format.
        im_bytes = im_arr.tobytes()
        print("Image sent back")
        emit('processed_image',{ 'frame': im_bytes })
    except:
        emit('error',"Not able to convert the image, try another image")
