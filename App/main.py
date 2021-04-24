import json
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask import Flask, request, render_template, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


''' End Flask Login Functions '''


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = "MYSECRET"
    login_manager.init_app(app)
    db.init_app(app)
    return app


app = create_app()

app.app_context().push()
db.create_all(app=app)
''' End Boilerplate Code '''


@app.route('/', methods=['GET'])
def index():
  form = LogIn()
  return render_template('login.html', form=form)

@app.route('/', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): # respond to form submission
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): # check credentials
        flash('Logged in successfully.') # send message to next page
        login_user(user) # login the user
        return redirect(url_for('todos')) # redirect to main page if login successful
  flash('Invalid credentials')
  return redirect(url_for('index'))


@app.route('/signup', methods=['GET'])
def signup():
  form = SignUp() # create form object
  return render_template('signup.html', form=form) # pass form object to template




@app.route('/signup', methods=['POST'])
def signupAction():
  form = SignUp() # create form object
  if form.validate_on_submit():
    data = request.form # get data from form submission
    newuser = User(username=data['username'], email=data['email']) # create user object
    newuser.set_password(data['password']) # set password
    db.session.add(newuser) # save new user
    db.session.commit()
    flash('Account Created!')# send message
    return redirect(url_for('index'))# redirect to login page
  flash('Error invalid input!')
  return redirect(url_for('signup')) 

@app.route('/todos', methods=['GET'])
@login_required
def todos():
  toggle_id = request.args.get('toggle')
  if toggle_id:
    todo = Todo.query.filter_by(id=toggle_id, userid=current_user.id).first() # retrieve todo
    if todo:
      todo.done = not todo.done # toggle the done state
      db.session.add(todo) # save the todo
      db.session.commit()
  form = AddTodo()
  todos = Todo.query.filter_by(userid=current_user.id).all()
  if todos is None:
      todos = [] # if user has no todos pass an empty list
  return render_template('todo.html', form=form, todos=todos)

@app.route('/todos', methods=['POST'])
@login_required
def todosAction():
  form = AddTodo()
  if form.validate_on_submit():
    data = request.form # get request data
    todo = Todo(text=data['text'], done=False, userid=current_user.id) # create todo object
    db.session.add(todo) # save todo object
    db.session.commit()
    flash('Todo Created!') # send message
    return redirect(url_for('todos')) # redirect
  flash('Invalid data!')
  return redirect(url_for('todos')) # redirect


@app.route('/editTodo/<id>', methods=['POST'])
@login_required
def edit_todo_action(id):
  data = request.form
  if data : # if data exists a form submission occured
    todo = Todo.query.filter_by(userid=current_user.id, id=id).first() # query  todo
    todo.text = data['text'] # update text
    db.session.add(todo) # save todo
    db.session.commit()
    flash('Todo Updated!')
    return redirect(url_for('todos'))
  flash('Invalid data')
  return redirect(url_for('todos'))

@app.route('/editTodo/<id>', methods=['GET'])
@login_required
def edit_todo(id):
  form = AddTodo()
  return render_template('edit.html', id=id, form=form)

'''
0. Assume todo id provided in url and user logged in
1. retrieve todo by id given in url and userid
3. delete the todo object if retrieved
4. flash success and redirect
5. else if not retrieved flash failure and redirect
'''

@app.route('/deleteTodo/<id>', methods=['GET'])
@login_required
def delete_todo(id):
  todo = Todo.query.filter_by(userid=current_user.id, id=id).first() # query  todo
  if todo:
    db.session.delete(todo)
    db.session.commit()
    flash('Todo Deleted!')
    return redirect(url_for('todos'))
  flash('Unauthorized or todo not found')
  return redirect(url_for('todos')) 

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  flash('Logged Out!')
  return redirect(url_for('index')) 

app.run(host='0.0.0.0', port=8080)
