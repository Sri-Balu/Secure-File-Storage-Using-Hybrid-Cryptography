import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
import tools
import divider as dv
import encrypter as enc
import decrypter as dec
import restore as rst
from flask import send_file
import numpy as np
from PIL import Image
from steganography.steganography import Steganography

UPLOAD_FOLDER = './uploads/'
UPLOAD_KEY = './key/'
ALLOWED_EXTENSIONS = set(['pem', 'jpg', 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_KEY'] = UPLOAD_KEY

#port = int(os.getenv('PORT', 8000))

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def string_to_binary(string):
    binary = ''.join(format(ord(char), '08b') for char in str(string))
    return binary

def start_encryption():
	dv.divide()
	tools.empty_folder('uploads')
	enc.encrypter()
	return render_template('success.html')

def start_decryption():
	dec.decrypter()
	tools.empty_folder('key')
	rst.restore()
	return render_template('restore_success.html')

@app.route('/return-key/My_Key.pem')
def return_key():
    # Retrieve the image file
    image_path = './nature.jpg'  
    image = Image.open(image_path)

    # Load the key file
    key_file_path = './key/Key.pem'  # Change this to the path of your key file
    with open(key_file_path, 'rb') as f:
        key = f.read()
        text = key.decode('utf-8')
    path = "./nature.jpg"
    output_path = "./output.jpg"
    Steganography.encode(path, output_path, text)
    # Save the embedded image temporarily
    temp_image_path = 'output.jpg'

    # Send the embedded image file as an attachment
    return send_file(temp_image_path, as_attachment=True, download_name='hidden_image.png')


@app.route('/return-file/')
def return_file():
    list_directory = tools.list_dir('restored_file')
    filename = './restored_file/' + list_directory[0]
    print("****************************************")
    print(list_directory[0])
    print("****************************************")
    return send_file(filename, download_name=list_directory[0], as_attachment=True)


@app.route('/download/')
def downloads():
	return render_template('download.html')

@app.route('/upload')
def call_page_upload():
	return render_template('upload.html')

@app.route('/home')
def back_home():
	tools.empty_folder('key')
	tools.empty_folder('restored_file')
	return render_template('index.html')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def upload_file():
	tools.empty_folder('uploads')
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return 'NO FILE SELECTED'
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
			return start_encryption()
		return 'Invalid File Format !'

@app.route('/download_data', methods=['GET', 'POST'])
def upload_key():
    tools.empty_folder('key')
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, browser may submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 'NO FILE SELECTED'
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_KEY'], filename)
            file.save(filepath)
            # Extract text from the uploaded image
            extracted_text = Steganography.decode(filepath)
            # Save the extracted text to key.pem file
            key_folder = 'key'
            key_filepath = os.path.join(key_folder, 'key.pem')
            with open(key_filepath, 'w') as key_file:
                key_file.write(extracted_text)
            # Optionally, you may want to perform further processing or redirection here
            return start_decryption()
        
        return 'Invalid File Format !'

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, debug=True)