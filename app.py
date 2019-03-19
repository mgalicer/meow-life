import sys
import os
import csv
import pickle
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

input_path = './uploads/cats'
img2vec = Img2Vec()
pics = {}

def create_pickle():
    with open('vectors.pkl', 'wb') as output:
        for file in os.listdir(input_path):
            filename = os.fsdecode(file)
            img = Image.open(os.path.join(input_path, filename))
            vec = img2vec.get_vec(img)


def create_csv():
    with open('vectors.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        for file in os.listdir(input_path):
            filename = os.fsdecode(file)
            img = Image.open(os.path.join(input_path, filename))
            vec = img2vec.get_vec(img)
            print(vec)
            filewriter.writerow([filename, vec])

def create_file_dict():
    with open('vectors.pkl', 'wb') as output:
        i = 0;
        for file in os.listdir(input_path):
            print(i)
            filename = os.fsdecode(file)
            img = Image.open(os.path.join(input_path, filename))
            vec = img2vec.get_vec(img)
            pics[filename] = vec
        pickle.dump(pics, output, pickle.HIGHEST_PROTOCOL)

def get_image_vector(filename):
    pil_image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    vec = img2vec.get_vec(pil_image)
    return vec

def find_similar_cat(user_image):
    most_similar = 0
    image_name = ""
    for key in list(pics.keys()):
        similarity = cosine_similarity(user_image.reshape((1, -1)), pics[key].reshape((1, -1)))[0][0]
        if similarity > most_similar:
            most_similar = similarity
            image_name = key 
    return image_name

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
        user_image = get_image_vector(filename)
        return find_similar_cat(user_image)

if __name__ == "__main__":
    create_file_dict()
    app.run()
