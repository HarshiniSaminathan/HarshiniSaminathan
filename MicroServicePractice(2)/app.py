import random

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/generate", methods=['GET'])
def generate_random_number():
    random_number = random.randint(1, 1000)
    return jsonify({"random_number": random_number})

if __name__ == "__main__":
    app.run(port=5001,debug=True)


