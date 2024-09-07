from flask import Flask, render_template, jsonify, request
import requests
import datetime
import sys
import os
import json
import time


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_src_dir = os.path.abspath(os.path.join(current_dir, os.pardir, 'src/'))
sys.path.append(parent_src_dir)
from commander import Commander

commander = Commander()

app = Flask(__name__)

# URL of the image server
IMAGE_SERVER_URL = 'http://127.0.0.1:5000'
TC_DICT = {
'get_timestamp': 1,
'set_height': 3,
'set_mode': 2,
'set_target_velocity': 4,
'start_forward': 5,
'stop_forward': 6,
'stop_turn': 9,
'start_turn': 8,
'tm_enable': 7,
'get_git_version': 10,
'take_photo': 11,
}


# Define a route to display images
@app.route('/')
def index():
    allTC =getAllTC()
    print(allTC)
    #statusTito=checkTitoStatus()
    statusTito=False
    statusServer=checkServerImages()
    image_timestamps=[]
    server_url=''
    if statusServer:
        # Fetch the list of images from the image server
        response = requests.get(f'{IMAGE_SERVER_URL}/list_images')
        image_files = response.json()

        # Sort the image files based on timestamp (assuming the timestamp is in the file name)
        image_files.sort(key=lambda x: x.split('.')[0], reverse=True)
        # Pass only the timestamps to the template
        image_timestamps = [image.split('.')[0].replace('image_', '') for image in image_files]
        server_url=IMAGE_SERVER_URL
    return render_template('index copy.html', image_files=image_timestamps, server_url=server_url,tc=allTC,statusTito=statusTito,statusServer=statusServer)



def getAllTC():
    json_All_TC = {}
    for name, id in TC_DICT.items():
        tc = commander.getTelecommand(id)
        tc = {
            "id": tc.operation,
            "help": tc.help,
            "inputs": tc.input,
            "help_input": tc.help_input,
            "Telecommand num Inputs": tc.num_inputs
        }
        json_All_TC[name] = tc 
    return json_All_TC

def get_TC(id):
    tc = commander.getTelecommand(id)
    return {
        "id": tc.operation,
        "help": tc.help,
        "inputs": tc.input,
        "help_input": tc.help_input,
        "Telecommand num Inputs": tc.num_inputs
    }

@app.route('/test/<int:id>', methods=['GET'])
def get_TC(id):
    tc=commander.getTelecommand(id)
    return jsonify({tc.name: {
        "id":tc.operation ,
        "help": tc.help,
        "inputs": tc.input,
        "help_input": tc.help_input,
        "Telecommand num Inputs": tc.num_inputs
    }})
@app.route('/send_TC', methods=['POST'])
def send_TC():
    data = request.json
    id=TC_DICT[data['idTC'].replace('button-', '')]
    tc=commander.getTelecommand(id)
    inputs={}
    tc.loadInputArguments(inputs)
    commander.send_message(tc,1)
    response=commander.send_message(tc,2)
    return jsonify({"result": {
        "Telecommand Name": tc.name,
        "Telecommand Help": tc.help,
        "Telecommand Input Help": tc.help_input,
        "Telecommand num Inputs": tc.num_inputs
    }})

@app.route('/executeTC', methods=['POST'])
def execute_tc():
    data = request.get_json()
    input_id = data.get('input_id')
    input_value = data.get('input_value')
    button_id = data.get('button_id')
    time.sleep(2) 
    print(f"Received data - Input ID: {input_id}, Input Value: {input_value}")

    return jsonify({'status': 'success', 'message': f"Received input {input_value} from {input_id} triggered by {button_id}."})


@app.template_filter('timestamp_to_date')
def timestamp_to_date(timestamp):
    timestamp = int(timestamp.split('.')[0])
    return datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S %d-%m-%y ')

def checkTitoStatus():
    tc=commander.getTelecommand(TC_DICT['get_timestamp'])
    tc.loadInputArguments("")
    response=commander.send_message(tc,2)
    if response:
        return True
    return False
def checkServerImages():
    try:
        response = requests.get(IMAGE_SERVER_URL+"/list_images", timeout=1)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
