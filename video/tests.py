from random import random

from . import client
from .models import Video

url = 'http://127.0.0.1:5000/tutorials'
url_register = 'http://127.0.0.1:5000/register'
url_login = 'http://127.0.0.1:5000/login'
url_profile = 'http://127.0.0.1:5000/profile'


number = int(random() * 1000000)


def test_get():
    token = test_login()
    resp = client.get(url, headers={'Authorization': f'Bearer {token["access_token"]}'})
    print(f'\nresponse: {resp.get_json()}')

    assert resp.status_code == 200


def test_post():
    token = test_login()
    data = {'name': 'Unit Tests',
            'description': 'Pytest tuttorial'
            }

    resp = client.post(url, json=data, headers={'Authorization': f'Bearer {token["access_token"]}'})
    print(f'\nresponse: {resp.get_json()}')

    assert resp.status_code == 200
    assert resp.get_json()['name'] == data['name']


def test_put():
    token = test_login()
    video_id = Video.query.all()[-1].id
    print(f'\nid: {video_id}')
    resp = client.put(f'{url}/{video_id}', json={'name': 'zapel',
                                                 'description': 'fisher'
                                                 },
                      headers={'Authorization': f'Bearer {token["access_token"]}'})

    assert resp.status_code == 200
    assert Video.query.get(video_id).name == 'zapel'


def test_delete():
    token = test_login()
    video_id = Video.query.all()[-1].id
    print(f'\nvideo_id: {video_id}')
    resp = client.delete(f'{url}/{video_id}', headers={'Authorization': f'Bearer {token["access_token"]}'})

    assert resp.status_code == 204
    assert Video.query.get(video_id) is None


def test_register():
    data = {
        'name': f'zapel_{number}',
        'email': f'test_{number}@gmail.com',
        'password': f'test_{number}'
    }
    print(f'\ndata: {data}')

    resp = client.post(url_register, json=data)
    print(f'\nresponse: {resp.get_json()}')
    assert resp.status_code == 200


def test_login():
    data_login = {
        'email': 'test_525014@gmail.com',
        'password': 'test_525014'
    }

    resp = client.post(url_login, json=data_login)
    print(f'resp:{resp.get_json()}')
    assert resp.status_code == 200

    return resp.get_json()


def test_profile():
    token = test_login()
    resp = client.get(url_profile, headers={'Authorization': f'Bearer {token["access_token"]}'})
    print(f'\nresponse: {resp.get_json()}')

    assert resp.status_code == 200
