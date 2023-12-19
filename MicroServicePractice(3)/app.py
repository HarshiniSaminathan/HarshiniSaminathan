from flask import Flask, jsonify
import requests

app = Flask(__name__)

random_microservice_url = "http://127.0.0.1:5001/generate"
simple_string_url ="http://127.0.0.1:5000/hello"


def call_random_microservice():
    response = requests.get(random_microservice_url)
    return response.json().get("random_number")

def call_string():
    string = requests.get(simple_string_url)
    return string.json().get("message")


@app.route("/check", methods=['GET'])
def check_even_odd():
    random_number = call_random_microservice()
    defined_string = call_string()
    result = "even" if random_number % 2 == 0 else "odd"
    return jsonify({
        "random_number": random_number,
        "result": result,
        "String": defined_string,
        "success": True
    })


if __name__ == "__main__":
    app.run(port=5002,debug=True)
