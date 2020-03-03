from flask import request, Flask
from app import app, db
from app.models import User


@app.route('/users', methods=['GET', 'POST'])
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
