from app import app, socketio
from flask import render_template
from flask_socketio import SocketIO, emit
import requests
import json
import base64
import numpy as np

api_link = "http://127.0.0.1:8080/model"


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
    
    try:
        heading, encoded_data = data.split(',')
        
        json_dict = {
            'frame': encoded_data
        }
        
        answer = requests.get(url=api_link, params=json_dict)
        answer = answer.json()
    
        if 'frame' in answer:
            decoded = base64.b64decode(answer['frame'])
            im_arr = np.frombuffer(decoded, dtype=np.uint8)
            im_bytes = im_arr.tobytes()
            print("Image sent back")
            emit('processed_image',{ 'frame': im_bytes })
            emit('update', "Image cartoonized successfully")
        elif 'error' in answer:
            emit('update', answer['error'])
        else:
            emit('update', "Currently facing some problems, try again later")
    except:
        emit('update', "Currently facing some problems, try again later")


    
