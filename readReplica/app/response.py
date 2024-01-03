from flask import jsonify


def success_response(content):
    response= {
    "status_code" : 200,
    "status":content,
    "success_res": 'Success'
    }
    return jsonify(response)


def failure_response(statusCode,content):
    response= {
    "status_code" : statusCode,
    "status":content,
    "success_res": 'Failure'
    }
    return jsonify(response)