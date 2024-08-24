from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


from flask import Flask, request, jsonify
import os.path
import subprocess
import cv2
import util
import datetime

app = Flask(__name__)

db_dir = './db'
if not os.path.exists(db_dir):
    os.mkdir(db_dir)

log_path = './log.txt'


@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if 'image_data' not in data:
            return jsonify({'error': 'Image data not provided'}), 400

        # Process image data and perform face recognition
        unknown_img_path = './.tmp.jpg'
        with open(unknown_img_path, 'wb') as f:
            f.write(data['image_data'])

        output = str(subprocess.check_output(['face_recognition', db_dir, unknown_img_path]))
        name = output.split(',')[1][:-5]

        if name in ['unknown_person', 'no_persons_found']:
            return jsonify({'message': 'Unknown User. Please register first or try again'}), 401
        else:
            with open(log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
            return jsonify({'message': 'Welcome back, {}!'.format(name)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if 'image_data' not in data or 'username' not in data:
            return jsonify({'error': 'Image data or username not provided'}), 400

        # Save image data to the database
        name = data['username']
        img_data = data['image_data']
        img_path = os.path.join(db_dir, '{}.jpg'.format(name))

        with open(img_path, 'wb') as f:
            f.write(img_data)

        return jsonify({'message': 'User registered successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
