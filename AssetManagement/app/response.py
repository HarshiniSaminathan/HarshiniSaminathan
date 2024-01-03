from flask import jsonify
from app.strings import Strings

def success_response(content):
    response = {
        'status': Strings.success_res,
        'status_code': '200',
        'content': content
    }
    return jsonify(response)

def failure_response(statuscode,content):
    response ={
        'status': Strings.failure_res,
        'status_code': statuscode,
        'content': content,
    }
    return jsonify(response)