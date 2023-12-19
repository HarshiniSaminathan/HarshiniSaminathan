import requests
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/hello", methods=['GET'])
def hello_microservice():
    message = {"message": "Hello from the microservice! This is GeeksForGeeks"}
    return jsonify(message)


result_url = "http://127.0.0.1:5002/check"

def results():
    result = requests.get(result_url)
    return result.json()

@app.route("/resultprint", methods=['GET'])
def result_print():
    result_data = results()
    return jsonify(result_data)


if __name__ == "__main__":
    app.run(port=5000,debug=True)



