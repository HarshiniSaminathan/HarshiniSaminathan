
import requests
from flask import jsonify
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


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

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password


users = {
    1: User(1, 'user1', 'password1'),
    2: User(2, 'user2', 'password2')
}

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@app.route('/')
def index():
    return jsonify({'message':'Welcome to the home page!'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data=request.get_json()
        required_fields =['username','password']
        for field in required_fields:
            if field not in data:
                return jsonify({'message':f'{field} is missing'})
        username = data['username']
        password = data['password']
        user = next((user for user in users.values() if user.username == username and user.password == password), None)
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        return jsonify({'message': 'Incorrect Password/username'})
    return jsonify({'message':'You have to login'})

@app.route('/dashboard')
@login_required
def dashboard():
    return jsonify({'message':f'Welcome to the home page , {current_user.username}'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=5000,debug=True)
