from flask import Flask, render_template, request, redirect, url_for, jsonify
import subprocess
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

@server.route('/uploads', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filepath = os.path.join(server.config['upload_path'], file.filename)
        file.save(filepath)
        return redirect(url_for('show_files'))
    return jsonify({"error": "No file uploaded!"}), 400

@server.route('/create_vm', methods=['POST'])
def create_vm():
    data = request.get_json()
    vm_name = data.get('vm_name')
    iso_path = data.get('iso_path')

    if not vm_name or not iso_path:
        return jsonify({"error": "VM name and ISO path are required!"}), 400

    vhd_path = f"C:\\Users\\hhunt\\Downloads\\vm\\{vm_name}.vhdx"
    memory_bytes = 2 * 1024 ** 3
    vhd_size_bytes = 20 * 1024 ** 3
    switch_name = "internal"

    # Ensure directory exists
    os.makedirs(os.path.dirname(vhd_path), exist_ok=True)

    print("iso_path:", iso_path)

    # PowerShell script
    ps_script = f'''
    New-VM -Name "{vm_name}" `
           -MemoryStartupBytes {memory_bytes} `
           -Generation 2 `
           -NewVHDPath "{vhd_path}" `
           -NewVHDSizeBytes {vhd_size_bytes} `
           -SwitchName "{switch_name}" | Out-Null 
    
    Add-VMDvdDrive -VMName "{vm_name}" -ControllerNumber 0 -ControllerLocation 1

    Set-VMProcessor -VMName "{vm_name}" -Count 2
    Set-VMDvdDrive -VMName "{vm_name}" -Path "{iso_path}"

    $dvd = Get-VMDvdDrive -VMName "{vm_name}"
    Set-VMFirmware -VMName "{vm_name}" -FirstBootDevice $dvd -EnableSecureBoot Off

    Start-VM -Name "{vm_name}"
    '''

    try:
        subprocess.run(["powershell", "-Command", ps_script], check=True)
        return jsonify({'status': 'VM created and powered on'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Failed to create VM: {str(e)}'}), 500

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

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000, debug=True)