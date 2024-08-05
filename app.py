import json
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response
import jwt
import datetime
from mock_users import users
import bcrypt
from flask_cors import CORS
# import logging
from functools import wraps
from mock_users import users;

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'mbs'
app.config['SESSION_COOKIE_HTTPONLY'] = True 

# logging.basicConfig(
#     level=logging.DEBUG,   
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[logging.StreamHandler()]  
# )

# add CRUD

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.cookies.get('authToken')
        if not token:
            return redirect(url_for('login'))

        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorator

@app.route('/', methods=["GET"])
@token_required
def home():
    return render_template('home.html')

@app.route('/register', methods=["GET"])
def register():
    return render_template('register.html')


@app.route('/register', methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if username in users:
        return jsonify({"message": "Username already exists"}), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed.decode('utf-8')

    with open('mock_users.py', 'w') as file:
        file.write('users = ')
        json.dump(users, file, indent=4)
    
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    response = jsonify({'message': 'Login successful'})
    response.set_cookie('authToken', token, httponly=False)
    return response

@app.route('/profile', methods=["GET"])
@token_required
def profile():
    return render_template('profile.html')



@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/logout', methods=["POST"])
def logout():
    # session.pop('user_id', None) 
    
    response = make_response(redirect('/login')) 
    
    response.set_cookie('authToken', '', expires=0, path='/')
    
    return response


@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password').encode('utf-8')

    if username in users and bcrypt.checkpw(password, users[username].encode('utf-8')):
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        response = jsonify({'message': 'Login successful'})
        response.set_cookie('authToken', token, httponly=False)
        return response
     
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
