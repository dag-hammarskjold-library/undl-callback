from datetime import datetime
import os, json, boto3
from time import timezone
from flask import Flask, request, jsonify
from dlx import DB

app = Flask(__name__)

if os.environ.get('UNDL_CALLBACK_TESTING'):
    nonce_key = 'test_key'
    db_connect = 'mongomock://localhost'
else:
    ssm_client = boto3.client('ssm')
    nonce_key = ssm_client.get_parameter(Name='undl-callback-nonce')['Parameter']['Value']
    db_connect = ssm_client.get_parameter(Name='prodISSU-admin-connect-string')['Parameter']['Value']

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        nonce = json.loads(data['nonce'])
        
        if nonce['key'] == nonce_key:
            data['record_type'] = nonce['type']
            data['record_id'] = nonce['id']

            # print to stdout for capture in Cloudwatch logs
            data['nonce'] = 'hidden' # Cloudwatch log data can appear on public dashboards
            print(json.dumps(data))

            # log in db
            data['time'] = datetime.now()
            data['nonce'] = nonce
            DB.handle['undl_callback_log'].insert_one(data)

            return jsonify({'Status': 'Okay'}), 200
        else:
            return jsonify({'Status': 'Invalid Key'}), 200
    else:
        return jsonify({'Status': 'You have reached the landing page.'}), 200