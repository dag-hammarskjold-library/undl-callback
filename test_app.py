import os, pytest, json

os.environ['UNDL_CALLBACK_TESTING'] = 'True'

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
    
    stdout = capsys.readouterr().out
    assert json.loads(stdout)['nonce'] == 'hidden'
    assert json.loads(stdout)['record_type'] == 'bib'
    assert json.loads(stdout)['record_id'] == 1
    assert isinstance(json.loads(stdout)['results'], list)
    
    r = client.post(
        'http://localhost/',
        headers={'Content-Type': 'application/json'}, 
        data=json.dumps({'nonce': json.dumps({'type': 'bib', 'id': 1, 'key': 'invalid'}), 'results': []})
    )
    assert r.status_code == 200
    assert json.loads(r.data) == {'Status': 'Invalid Key'}
    