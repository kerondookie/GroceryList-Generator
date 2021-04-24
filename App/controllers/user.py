import json
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask import Flask, request, render_template, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

from App.models import ( User )

def create_user(firstname, lastname, uwi_id, email, gender, dob):
    # newuser = use()
    return 'new user'

