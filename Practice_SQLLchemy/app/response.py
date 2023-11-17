from flask import jsonify
from app.strings import success_res,failure_res

def success_response(content):
    response = {
        'status': success_res,
        'status_code': '200',
        'content': content
    }
    return jsonify(response)

def failure_response(statuscode,content):
    response ={
        'status': failure_res,
        'status_code': statuscode,
        'content': content,
    }
    return jsonify(response)

