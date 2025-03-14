from flask import Flask, render_template
import os


current_path = os.path.abspath(os.getcwd()+"/src")
upload_path = os.path.join(current_path, 'uploads')
os.makedirs(upload_path, exist_ok=True)
server = Flask(__name__)
server.config['upload_path'] = upload_path

@server.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000, debug=True)