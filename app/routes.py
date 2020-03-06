from flask import request, Flask, jsonify
from app import app, db
from app.models import User, Posts
from flask_httpauth import HTTPBasicAuth
import re

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


@app.route('/new_post', methods=['POST'])
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
    lst = [post.serialize for post in posts]
    lst.reverse()
    return jsonify(lst)


@app.route('/get_posts_by_user', methods=['POST'])
def get_all_posts_by_user():
    response = request.get_json()
    userid = response['userid']

    posts = Posts.query.filter_by(userid=userid)
    lst = [post.serialize for post in posts]
    lst.reverse()
    return jsonify(lst)


@app.route('/search_posts', methods=['POST'])
def search_post():
    response = request.get_json()
    search_text = response['text']

    posts = Posts.query.filter(Posts.title.contains(search_text))
    # posts = Posts.query.filter(re.search(search_text, Posts.title, re.IGNORECASE) is not None)
    lst = [post.serialize for post in posts]

    posts = Posts.query.filter(Posts.description.contains(search_text))
    lst.extend([post.serialize for post in posts])

    # lst = list(set(lst))
    seen_titles = set()
    new_lst = []
    for obj in lst:
        if obj['id'] not in seen_titles:
            new_lst.append(obj)
            seen_titles.add(obj['id'])

    new_lst.reverse()
    return jsonify(new_lst)
