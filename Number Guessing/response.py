from flask import jsonify


def success_response(content):
    response = {
        'status': 'success',
        'status_code': '200',
        'content': content
    }
    return jsonify(response)

def failure_response(content):
    response ={
        'status': 'failure',
        'status_code': '405',
        'content': content,
    }
    return jsonify(response)

