from flask import request, Flask
from app import app, db
from app.models import User
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()


@app.route('/login', methods=['POST'])
def login_method():
    response = request.get_json()

    email = response['email']
    password = response['password']

    user = User.query.filter_by(email=email).first()
    if user.password_hash == password:
        return str(user.id)
    else:
        return "0"
    # try:
    #     user = User.query.filter_by(email=email).first()
    #     if user.password_hash == password:
    #         return '1'
    #     else:
    #         return '2'
    # finally:
    #     return email







@app.route('/users', methods=['POST'])
def user_methods():
    response = request.get_json()

    username = response['username']
    email = response['email']
    designation = response['designation']
    dob = response['dob']
    password = response['password']

    user = User(username=username, email=email, Designation=designation, DOB=dob, password_hash=password)
    db.session.add(user)
    db.session.commit()

    return '200'
