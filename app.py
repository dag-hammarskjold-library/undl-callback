from flask import Flask, request, jsonify
import os, json, boto3

app = Flask(__name__)

if os.environ.get('UNDL_CALLBACK_TESTING'):
    nonce_key = 'test_key'
else:
    ssm_client = boto3.client('ssm')
    nonce_key = ssm_client.get_parameter(Name='undl-callback-nonce')['Parameter']['Value']

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        nonce = json.loads(data['nonce'])
        if nonce['key'] == nonce_key:
            data['nonce'] = 'hidden'
            data['record_type'] = nonce['type']
            data['record_id'] = nonce['id']
            # this gets sent to the logs
            print(json.dumps(data))
            return jsonify({'Status': 'Okay'}), 200
        else:
            return jsonify({'Status': 'Invalid Key'}), 200
    else:
        return jsonify({'Status': 'You have reached the landing page.'}), 200