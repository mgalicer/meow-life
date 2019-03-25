import sys
import os
import pickle
from flask import Flask, flash, request, redirect, url_for, send_file
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

# loads the python dictionary from the .pkl file
def load_file_dict():    
    infile = open('vectors.pkl', 'rb')
    image_dict = pickle.load(infile)
    infile.close()
    return image_dict

# write the image vectors as dictionary to a .pkl file 
def create_file_dict():
    with open('vectors.pkl', 'wb') as output:
        i = 0;
        for file in os.listdir(input_path):
            i = i + 1
            print(i)
            filename = os.fsdecode(file)
            img = Image.open(os.path.join(input_path, filename))
            vec = img2vec.get_vec(img)
            pics[filename] = vec
        pickle.dump(pics, output, pickle.HIGHEST_PROTOCOL)

# get the vector for a single image
def get_image_vector(filename):
    pil_image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    vec = img2vec.get_vec(pil_image)
    return vec

# loop through the vector dictionary, finding the most similar image according to cosine similarity
def find_similar_cat(user_image):
    most_similar = 0
    image_name = ""
    for key in list(pics.keys()):
        similarity = cosine_similarity(user_image.reshape((1, -1)), pics[key].reshape((1, -1)))[0][0]
        if similarity > most_similar:
            most_similar = similarity
            image_name = key 
    return image_name

# check if file name is allowed 
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
	# convert the image to a vector and find the most similar cat photo
        user_image = get_image_vector(filename)
        similar_cat_image = find_similar_cat(user_image)
        return send_file(input_path + '/'+ similar_cat_image)

if __name__ == "__main__":
    pics = load_file_dict()
    app.run()
