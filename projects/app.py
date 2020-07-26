import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def write_json(data, filename='projects.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


@app.route('/<api_key>/projects/add', methods = ['POST'])
def add_projects(api_key):
    with open('keys_file') as key_json:
        keys = json.load(key_json)
        data_json = request.get_json(force = True)
        if api_key in keys['api_keys']:
            project_name = data_json['project']
            preview_link = data_json['preview']
            code_link = data_json['codelink']
            code_link = data_json['articlelink']
            description = data_json['description']
            stack = data_json['stack']
            category = data_json['category']
            project = {
                "project": project_name,
                "preview": preview_link,
                "codelink": code_link,
                "articlelink": code_link,
                "description": description,
                "stack": stack,
                "category": category
            }
            with open('projects.json') as json_file:
                data = json.load(json_file)
                temp = data['projects']

                temp.append(project)

            write_json(data)

            return 'Data Entered!'
        else:
            return 'Wrong API Key'

@app.route('/<api_key>/projects/view', methods = ['GET'])
def view_projects(api_key):
    with open('keys_file') as key_json:
        keys = json.load(key_json)
        if api_key in keys['api_keys']:
            with open('projects.json') as json_file:
                data = json.load(json_file)
                projects = data['projects']
            return jsonify(projects)
        else:
            return 'Wrong API Key'
