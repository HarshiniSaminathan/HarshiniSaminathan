import requests


def make_api_call(url, method="GET", headers=None, params=None, data=None):
    """
    Makes an API call using the provided parameters.

    :param url: The URL of the API endpoint to call.
    :param method: (optional) The HTTP method to use for the request (e.g. "GET", "POST", etc.).
    :param headers: (optional) A dictionary of headers to include in the request.
    :param params: (optional) A dictionary of URL parameters to include in the request.
    :param data: (optional) The data to send in the request body.
    :return: The response from the API call, including the status code in the JSON response.
    """
    supported_methods = ["GET", "POST", "PUT", "DELETE"]
    if method not in supported_methods:
        raise ValueError(f"Unsupported HTTP method: {method}")
    try:
        response = requests.request(method, url, headers=headers, params=params, json=data)
        if response.status_code == 200:
            response.raise_for_status()
            json_response = response.json()
            json_response["status_code"] = response.status_code
            return json_response
        else:
            json_response = {}
            json_response['status_code'] = 400
            return json_response
    except requests.exceptions.RequestException as e:
        raise ValueError(f"API call failed: {e}")


def get_headers(api_key=None):
    """
    Returns a dictionary of headers to be used in API calls.

    :param api_key: (optional) The API key to include in the headers.
    :return: A dictionary of headers.
    """
    headers = {}

    if api_key:
        headers['Authorization'] = f"Bearer {api_key}"

    headers['Content-Type'] = 'application/json'

    return headers

def parse_response(response):
    """
    Parses the response from an API call into a Python object.

    :param response: The response from the API call.
    :return: The parsed response as a Python object.
    """
    return response.json()

def handle_error(response):
    """
    Handles errors that occur during an API call.

    :param response: The error response from the API call.
    :return: An exception or error message.
    """
    error_message = response.json().get("error_message")

    if error_message:
        raise Exception(error_message)
    else:
        response.raise_for_status()

def retry_call(api_call_func, *args, **kwargs):
    """
    Retries an API call if it fails due to network or server errors.

    :param api_call_func: The function to call.
    :param args: (optional) The positional arguments to pass to the function.
    :param kwargs: (optional) The keyword arguments to pass to the function.
    :return: The response from the API call.
    """
    num_retries = 3
    retry_delay = 1

    for retry_count in range(num_retries):
        try:
            response = api_call_func(*args, **kwargs)
            return response
        except requests.exceptions.RequestException:
            if retry_count == num_retries - 1:
                raise
            else:
                time.sleep(retry_delay)
                retry_delay *= 2

