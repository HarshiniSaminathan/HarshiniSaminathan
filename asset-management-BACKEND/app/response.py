from flask import jsonify
from app.strings import Strings

def success_response(content):
    responseData = {
        'status': Strings.success_res,
        'status_code': '200',
        'content': content
    }
    return jsonify(responseData)

def failure_response(statuscode,content):
    responseData ={
        'status': Strings.failure_res,
        'status_code': statuscode,
        'content': content,
    }
    return jsonify(responseData)