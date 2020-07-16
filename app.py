from flask import Flask, request, jsonify
import json
import boto3

ssm_client = boto3.client('ssm')
nonce_key = ssm_client.get_parameter(Name='undl-callback-nonce')['Parameter']['Value']

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        json_return = request.get_json()
        nonce = json.loads(json_return['nonce'])
        if nonce['key'] == nonce_key:
            print(json_return)
            return jsonify({'Status': 'Okay'}), 200
        else:
            return jsonify({'Status': 'Invalid Key'}), 200
    else:
        return jsonify({'Status': 'You have reached the landing page.'}), 200