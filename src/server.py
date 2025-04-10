from flask import Flask, render_template
import os


current_path = os.path.abspath(os.getcwd()+"/src")
server = Flask(__name__)
server.config['upload_path'] = os.path.join(current_path, 'uploads')

if not os.path.exists(server.config['upload_path']):
    os.makedirs(server.config['upload_path'])

@server.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@server.route('/show_files', methods=['GET'])
def show_files():
    files = os.listdir(server.config['upload_path'])  
    return render_template('show_files.html', files=files)

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000, debug=True)