from flask import Flask, render_template, request, send_file
import subprocess
import csv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_scripts():
    script_name = request.form.get('scripts')

    if script_name == "app_clean_active":
        messages, active_links = execute_app_clean_active()
    elif script_name == "sd":
        messages, active_links, csv_filename = execute_sd()
    else:
        messages = ['Invalid script specified']
        active_links = []
        csv_filename = None

    return render_template('index.html', messages=messages, active_links=active_links, csv_filename=csv_filename)

def execute_app_clean_active():
    scripts = ["app", "clean", "active"]
    messages = []
    active_links = []

    for script_name in scripts:
        script_path = f'subfiles/{script_name}.py'

        try:
            subprocess.run(['python', script_path], check=True)
            message = f'Successfully executed {script_name}.py'
            messages.append(message)
        except subprocess.CalledProcessError:
            message = f'Error executing {script_name}.py'
            messages.append(message)

    active_links = read_active_links()
    
    return messages, active_links

def execute_sd():
    script_path = 'subfiles/sd.py'
    messages = []
    active_links = []

    try:
        subprocess.run(['python', script_path], check=True)
        message = 'Successfully executed sd.py'
        messages.append(message)
    except subprocess.CalledProcessError:
        message = 'Error executing sd.py'
        messages.append(message)

    active_links = read_active_links()
    csv_filename = 'onion_page_info.csv'  

    return messages, active_links, csv_filename

def read_active_links():
    active_links = []
    folder_path = 'subfiles/active_links'
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                links = [row[0] for row in reader]
                active_links.extend(links)

    return active_links

@app.route('/download/<filename>')
def download_file(filename):
    folder_path = '/home/deepak/Finalproject/onion_page_info'
    file_path = os.path.join(folder_path, filename)
    
    print(f"Attempting to download file: {file_path}")

    if os.path.exists(file_path):
        print("File exists. Initiating download.")
        return send_file(file_path, as_attachment=True)
    else:
        print("File does not exist.")
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
