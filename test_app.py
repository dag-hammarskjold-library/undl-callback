import os, pytest, json
from dlx import DB

os.environ['UNDL_CALLBACK_TESTING'] = 'True'
DB.connect('mongomock://localhost')

@pytest.fixture()
def client():
    from app import app
    return app.test_client()
    
def test_callback(client, capsys):
    r = client.post(
        'http://localhost/',
        headers={'Content-Type': 'application/json'}, 
        data=json.dumps({'nonce': json.dumps({'type': 'bib', 'id': 1, 'key': 'test_key'}), 'results': []})
    )
    assert r.status_code == 200
    assert json.loads(r.data) == {'Status': 'Okay'}
    
    # stdout
    stdout = capsys.readouterr().out
    assert json.loads(stdout)['nonce'] == 'hidden'
    assert json.loads(stdout)['record_type'] == 'bib'
    assert json.loads(stdout)['record_id'] == 1
    assert isinstance(json.loads(stdout)['results'], list)

    # db log
    result = DB.handle['undl_callback_log'].find_one({})
    assert result.get('time')
    assert result.get('nonce') == {'type': 'bib', 'id': 1, 'key': 'test_key'}
    assert result.get('record_id') == 1
    assert result.get('record_type') == 'bib'
    
    # invalid key
    r = client.post(
        'http://localhost/',
        headers={'Content-Type': 'application/json'}, 
        data=json.dumps({'nonce': json.dumps({'type': 'bib', 'id': 1, 'key': 'invalid'}), 'results': []})
    )
    assert r.status_code == 200
    assert json.loads(r.data) == {'Status': 'Invalid Key'}
    