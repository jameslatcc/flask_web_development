from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import os


current_path = os.path.abspath(os.getcwd()+"/src")
server = Flask(__name__)
server.config['upload_path'] = os.path.join(current_path, 'uploads')
socketio = SocketIO(server)

if not os.path.exists(server.config['upload_path']):
    os.makedirs(server.config['upload_path'])

@server.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@server.route('/show_files', methods=['GET','POST'])
def show_files():
    files = os.listdir(server.config['upload_path'])  
    return render_template('show_files.html', files=files)

@server.route('/uploads', methods=['GET','POST'])
def upload_file():
    file = request.files['file']
    if file:
        filepath = os.path.join(server.config['upload_path'], file.filename)
        file.save(filepath)
        return redirect(url_for('show_files'))
    return jsonify({"error": "No file uploaded!"}), 400

@server.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    filepath = os.path.join(server.config['upload_path'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        if os.path.exists(filepath):
            return jsonify({"error": "File deletion failed!"}), 500
        return jsonify({"message": f"File '{filename}' deleted successfully!"}), 200
    else:
        return jsonify({"error": "File not found!"}), 404

@socketio.on('progress')
def handle_progress(data):
    # Emit progress updates to the client
    emit('progress_update', data)

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000, debug=True)