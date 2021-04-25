from flask import Blueprint, redirect, render_template, request, jsonify, send_from_directory
import sys
from App.models import db

user_views = Blueprint('user_views', __name__, template_folder='../templates')

from App.models import User

@user_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@user_views.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not User.check_password(user,password):
        print("User not authenticated", file=sys.stderr)
        return render_template('login.html')
    print("User authenticated", file=sys.stderr)
    return render_template('home.html')


@user_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@user_views.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
   # print (email, file=sys.stderr)
   # print (password, file=sys.stderr)
    user = User.query.filter_by(username=name).first()
   
    if user:
        print ("User found", file=sys.stderr)
        return render_template('login.html')
    else:
        print ("User not found", file=sys.stderr)
    
    new_user = User(email=email, username=name)
    User.set_password(new_user, password)
    db.session.add(new_user)
    db.session.commit()

    return render_template('login.html')
    


@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = User.query.all()
    return render_template('users.html', users=users)

@user_views.route('/api/users')
def client_app():
    users = User.query.all()
    if not users:
        return jsonify([])
    users = [user.toDict() for user in users]
    return jsonify(users)

@user_views.route('/static/users')
def static_user_page():
  return send_from_directory('static', 'static-user.html')