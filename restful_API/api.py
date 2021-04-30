from flask import Flask, request, jsonify
from model import cartoonize as cartoonify
import numpy as np
from cv2 import cv2
import io
import base64
import json

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/model', methods=['GET'])
def processed_image():
    if 'frame' in request.args:
        data = request.args['frame']
        try:
            nparr = np.fromstring(base64.b64decode(data), np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            print("Frame convertion done, sent to ml model to cartoonise")
            processed_image = cartoonify.cartoonize(frame)
            print("Image cartoonized")
            _, im_arr = cv2.imencode('.jpg', processed_image)  # im_arr: image in Numpy one-dim array format.
            image_string = base64.b64encode(im_arr).decode()
            return jsonify({'frame': image_string }) #im_arr.tostring().hex()}
        except:
            return jsonify({'error':"Not able to convert the image, try another image"})
    else:
        return jsonify({'error':"Select a proper image"})

@app.route('/test',methods=['GET'])
def test():
    if 'frame' in request.args:
        return {'answer':"Works"}
    else:
        return {'answer':"Frame param missing"}


if __name__=='__main__':
    app.run(host='0.0.0.0',port='8080')