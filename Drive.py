import argparse
import base64
from datetime import datetime
import os
import shutil
import numpy as np
import socketio
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO
from keras.models import load_model
import utils

sio = socketio.Server()

app = Flask(__name__)

model = None
prev_image_array = None

MAX_SPEED = 25
MIN_SPEED = 10

speed_limit = MAX_SPEED


@sio.on('telemetry')
def telemetry(data):
    if data:
        speed = float(data["speed"])
        image = Image.open(BytesIO(base64.b64decode(data["image"])))
        try:
            image = np.asarray(image)
            image = utils.preprocess(image)
            image = np.array([image])

            steering_angle = float(model.predict(image, batch_size=1))

            # lower the throttle as the speed increases
            # if the speed is above the current speed limit, we are on a downhill.
            # make sure we slow down first and then go back to the original max speed.

            global speed_limit
            if speed > speed_limit:
                speed_limit = MIN_SPEED
            else:
                speed_limit = MAX_SPEED
            throttle = 1.0 - steering_angle**2 - (speed/speed_limit)**2

            print('{} {} {}'.format(steering_angle, throttle, speed))
            send_control(steering_angle, throttle)
        except Exception as e:
            print(e)

    else:

        sio.emit('manual', data={}, skip_sid=True)


@sio.on('connect')
def connect(sid):
    print("connect ", sid)
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__()
        },
        skip_sid=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remote Driving')
    parser.add_argument(
        'model',
        type=str,
        help='Path to model h5 file. Model should be on the same path.'
    )

    args = parser.parse_args()

    model = load_model(args.model)

    app = socketio.Middleware(sio, app)

    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
