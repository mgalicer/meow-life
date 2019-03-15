import sys
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from img_to_vec import Img2Vec
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

sys.path.append("..") # Adds higher directory to python modules path.

input_path = './test_images'
img2vec = Img2Vec()

def get_image_vector(filename):
    pil_image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    vec = img2vec.get_vec(pil_image)
    return vec

def compare_image_vectors(vector1, vector2):
    cosine_similarity(pics[pic_name].reshape((1, -1)), pics[key].reshape((1, -1)))[0][0]

def allowed_file(fileName):
    return '.' in fileName and \
            fileName.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods = ["GET"])
def hello():
    return "Hello World!"

@app.route('/classify', methods = ['POST'])
def classify():
    if 'file' not in request.files:
        return 'No file part'
    image = request.files['file']
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        # Do the part where we pass the file to the model
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        get_image_vector(filename)
    return "classifying image"

if __name__ == "__main__":
    app.run()
