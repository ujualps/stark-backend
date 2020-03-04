from flask import request, Flask, jsonify
from app import app, db
from app.models import User, Posts
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()


@app.route('/login', methods=['POST'])
def login_method():
    response = request.get_json()

    email = response['email']
    password = response['password']

    user = User.query.filter_by(email=email).first()
    if user.password_hash == password:
        return_dict = dict()
        return_dict['id'] = user.id
        return jsonify(return_dict)


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


@app.route('/get_user', methods=['POST'])
def get_details():
    response = request.get_json()

    uid = response['userid']
    user = User.query.filter_by(id=uid).first()
    return_dict = dict()
    print(user)
    return_dict['userid'] = user.id
    return_dict['username'] = user.username
    return_dict['designation'] = user.Designation
    return_dict['email'] = user.email
    return_dict['dob'] = user.DOB

    return jsonify(return_dict)


@app.route('/new_post',methods=['POST'])
def new_post():
    response = request.get_json()

    uid = response['userid']
    title = response['title']
    desc = response['desc']
    post = Posts(title=title, description=desc, userid=uid)
    db.session.add(post)
    db.session.commit()
    return '200'


@app.route('/get_all_posts', methods=['GET'])
def get_all_posts():
    posts = Posts.query.all()
    return jsonify([post.serialize for post in posts])


