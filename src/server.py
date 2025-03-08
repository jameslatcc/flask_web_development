import os
from flask import Flask, request, send_from_directory, redirect, url_for, flash
from flask_restful import Resource
from werkzeug.utils import secure_filename


current_path = os.path.abspath(os.getcwd())
upload_path = os.path.join(current_path, 'uploads')
os.makedirs(upload_path, exist_ok=True)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','iso','mp4'}
server = Flask(__name__)
server.config['upload_path'] = upload_path

def allowed_file(filename):
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@server.route('/uploads/<name>')
def upload_ok(name):
    return "after upload, the file name: {}".format(name)

@server.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(server.config['upload_path'], filename))
        return redirect(url_for('upload_ok', name=filename))
     

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=5000, debug=True)
