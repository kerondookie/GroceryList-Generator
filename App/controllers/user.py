from flask import redirect, render_template, request, session, url_for

from App.models import ( User )

def create_user(first_name, last_name):
    newuser = User(first_name=first_name, last_name=last_name)
    db.session.add(newuser)
    db.session.commit()