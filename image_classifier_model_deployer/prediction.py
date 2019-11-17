from PIL import Image
import numpy as np
import json
import os

import tensorflow as tf
from keras.models import load_model

from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory

from collections import OrderedDict

# Settings
STATIC_FOLDER = os.path.join('static', 'images/')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['STATIC_FOLDER'] = STATIC_FOLDER

config = ''
with open('config.json', 'r') as f:
	config = f.read()
	config = json.loads(config)

img_rows = int(config['img_rows'])
img_cols = int(config['img_cols'])
img_channels = int(config['img_channels'])
nclasses = int(config['nclasses'])
model_path = config['model_path']
image_path = ''

def loadlabels():
	with open('labels.txt', 'r') as f:
		labels = f.read()
	labels = labels.split('\n')
	return labels

def createlabelmapping(preds):
	labels = loadlabels()
	lab_pred = dict()
	final_lab_pred = dict()

	for i, j in zip(labels, preds[0]):
		lab_pred[str(i)] = j

	# Sort by predictions
	lab_pred = OrderedDict(sorted(lab_pred.items(), key=lambda x: x[1], reverse=True))
	for x, y in zip(lab_pred.keys(), lab_pred.values()):
		final_lab_pred[x] = y

	return final_lab_pred

def loadmodel():
	return load_model(model_path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process', methods=['GET','POST'])
def predictImage():
	print(image_path)
	if image_path!='':	
		img = Image.open(image_path).resize((img_rows, img_cols))

		if img_channels == 1:
			img = img.convert('L')

		img = np.asarray(img)
		img = img.reshape(1, img_rows, img_cols, img_channels)
		img = img.astype('float32')
		img /= 255

		model = loadmodel()
		print(model.summary())
		   
		predictions = model.predict(img)
		preds = createlabelmapping(predictions)
		print(preds)
		cls = 'Class: ' + list(preds.keys())[0]
		prob = ' Probability: ' + str(list(preds.values())[0])
		prediction = cls + ' , ' + prob

		return render_template('index.html', msg=prediction)
	else:
		return render_template('index.html', msg='Image not uploaded!')


@app.route('/predict', methods=['POST'])
def predict():
	if request.method == 'POST':
		image_path = request.files['file']

		print(image_path)
		img = Image.open(image_path).resize((img_rows, img_cols))

		if img_channels == 1:
			img = img.convert('L')

		img = np.asarray(img)
		img = img.reshape(1, img_rows, img_cols, img_channels)
		img = img.astype('float32')
		img /= 255

		model = loadmodel()
		print(model.summary())
		   
		predictions = model.predict(img)
		preds = createlabelmapping(predictions)
		print(preds)
		return str(preds)
	else:
		return render_template('index.html', msg='Please upload an image!')


@app.route('/index', methods=['GET', 'POST'])
def upload_file():
    fname = app.config['STATIC_FOLDER'] + 'no_image.png'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fname = os.path.join(app.config['STATIC_FOLDER'], filename)
            file.save(fname)
            global image_path
            image_path = fname
            print("Image uploaded!", image_path)
            return render_template('index.html', img=image_path)
    else:
    	return render_template('index.html', img=fname)
    

if __name__ ==  '__main__':
	app.debug = True
	app.run()



