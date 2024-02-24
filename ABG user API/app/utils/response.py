from flask import jsonify


def error_response(status_code, message):
    response = {
        "status": "error",
        "message": message,
        "pagination": None
    }
    return jsonify(response), status_code


def success_response(status_code, data, message=None, pagination=None):
    response = {
        "status_code": status_code,
        "status": "success",
        "data": data,
        "pagination": {
            "total": pagination['total'],
            "pages": pagination['pages'],
            "page": pagination['page'],
            "per_page": pagination['per_page']
        } if pagination else None
    }
    if message:
        response["message"] = message
    return jsonify(response), status_code


def create_download_response(data, filename):
    """
    Helper function to create a file download response
    :param data: The data to include in the file
    :param filename: The filename for the downloaded file
    :return: File download response
    """
    response = make_response(data)
    response.headers.set('Content-Disposition', 'attachment', filename=filename)
    return response


def create_html_response(html):
    """
    Helper function to create an HTML response
    :param html: The HTML to include in the response
    :return: HTML response
    """
    return make_response(html)