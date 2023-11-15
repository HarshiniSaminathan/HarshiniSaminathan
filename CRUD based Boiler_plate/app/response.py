from flask import jsonify


def success(message, content):
    data = {'message': message, 'error': 0}
    data['content'] = content
    resp = jsonify(data)
    resp.status_code = 200
    resp.content_type = "application/json"
    return resp

def failure(message, status_code=400):
    data = {'message': message, 'error': 1}
    resp = jsonify(data)
    resp.status_code = status_code
    resp.content_type = "application/json"
    return resp