import os
# from werkzeug.datastructures import FileStorage
import json


def get(client, url, headers = None):
    response = client.get(url, headers=headers)
    return response.status_code, response.json()

def post(client, url, data, headers = None):
    response = client.post(url, data=data, content_type='application/json', headers=headers)
    return response.status_code, json.loads(response.data.decode('utf-8'))

def put(client, url, data, headers = None):
    response = client.put(url, data=data, content_type='application/json', headers=headers)
    return response.status_code, json.loads(response.data.decode('utf-8'))

def delete(client, url, headers = None):
    response = client.delete(url, headers=headers)
    return response.status_code, json.loads(response.data.decode('utf-8'))

# def postMultipartForm(client, url, one_or_multi_files_path, headers = None):

#     if isinstance(one_or_multi_files_path, str):
#         the_file = FileStorage(
#             stream=open(one_or_multi_files_path, 'rb'),
#             filename=os.path.basename(os.path.normpath(one_or_multi_files_path))
#         )
#         data = { 'file': [the_file] }

#     if isinstance(one_or_multi_files_path, list):
#         data = { 'file': [] }
#         for path in one_or_multi_files_path:

#             the_file = FileStorage(
#                 stream=open(path, 'rb'),
#                 filename=os.path.basename(os.path.normpath(path))
#             )
#             data['file'].append(the_file)

#     response = client.post(url, content_type='multipart/form-data', data=data, headers=headers)
#     return response.status_code, json.loads(response.data.decode('utf-8'))

# def getHTML(client, url):
#     response = client.get(url)
#     return response.status_code, response.data
