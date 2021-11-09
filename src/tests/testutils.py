import os
import json


def get(client, url, headers = None):
    response = client.get(url, headers=headers)
    return response.status_code, response.json()

def post(client, url, data, headers = None):
    data = json.dumps(data)
    response = client.post(url, data=data, headers=headers)
    return response.status_code, response.json()

def put(client, url, data, headers = None):
    data = json.dumps(data)
    response = client.put(url, data=data, headers=headers)
    return response.status_code, response.json()

def delete(client, url, headers = None):
    response = client.delete(url, headers=headers)
    return response.status_code, response.json()

def postFiles(client, url, files):

    if isinstance(files, str):
        stream = open(files, 'rb')
        files_data = {'uploads': (os.path.basename(files), stream, 'image/png')}

    elif isinstance(files, list):
        files_data = []
        for path in files:
            stream = open(path, 'rb')
            item = ('uploads', (os.path.basename(path), stream, 'image/png'))
            files_data.append(item)

    response = client.post(url, files=files_data)
    return response.status_code, response.json()

