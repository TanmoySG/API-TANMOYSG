import json
import shortuuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# CREATE
@app.route('/<api_key>/projects/add', methods = ['POST'])
def add_projects(api_key):
    with open('keys') as key_json:
        keys = json.load(key_json)
        data_json = request.get_json(force = True)
        if api_key in keys['api_keys']:
            _uuid = shortuuid.uuid()
            project_name = data_json['project']
            preview_link = data_json['preview']
            code_link = data_json['codelink']
            code_link = data_json['articlelink']
            description = data_json['description']
            stack = data_json['stack']
            category = data_json['category']
            project = {
                "_uuid": _uuid,
                "project": project_name,
                "preview": preview_link,
                "codelink": code_link,
                "articlelink": code_link,
                "description": description,
                "stack": stack,
                "category": category
            }
            with open('projects_file') as json_file:
                data = json.load(json_file)
                temp = data['projects']

                temp.append(project)

            write_json(data, 'projects_file')

            return 'Data Entered!'
        else:
            return 'Wrong API Key'

# READ
@app.route('/<api_key>/projects/view', methods = ['GET'])
def view_projects(api_key):
    with open('keys') as key_json:
        keys = json.load(key_json)
        if api_key in keys['api_keys']:
            with open('projects_file') as json_file:
                data = json.load(json_file)
                projects = data['projects']
            return jsonify(projects)
        else:
            return 'Wrong API Key'

# UPDATE
@app.route('/<api_key>/projects/update', methods = ['POST'])
def update_projects(api_key):
    with open('keys') as key_json:
        keys = json.load(key_json)
        data_json = request.get_json(force = True)
        if api_key in keys['api_keys']:
            _uuid = data_json['_uuid']
            with open('projects_file') as json_file:
                data = json.load(json_file)
                temp = data['projects']
                if not any(d['_uuid'] == _uuid for d in temp):
                    return 'Data does not exist'
                else:
                    for i in range(len(temp)): 
                        if temp[i]['_uuid'] == _uuid: 
                            temp[i].update(data_json)
                            break
                    write_json(data, 'projects_file')
                    return 'Updated!'
        else:
            return 'Wrong API Key'

# DELETE
@app.route('/<api_key>/projects/delete', methods = ['POST'])
def delete_projects(api_key):
    with open('keys') as key_json:
        keys = json.load(key_json)
        data_json = request.get_json(force = True)
        if api_key in keys['api_keys']:
            _uuid = data_json['_uuid']
            with open('projects_file') as json_file:
                data = json.load(json_file)
                temp = data['projects']

                if not any(d['_uuid'] == _uuid for d in temp):
                    return 'Data does not exist'
                else:
                    for i in range(len(temp)): 
                        if temp[i]['_uuid'] == _uuid: 
                            del temp[i] 
                            break
                    write_json(data, 'projects_file')
                    return 'Deleted!'
        else:
            return 'Wrong API Key'
