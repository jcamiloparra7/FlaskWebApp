from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", text="Testing", boolean=True)


@auth.route('/logout')
def logout():
    return render_template("extended_base.html",
                           title="Log out",
                           content="This is the log out menu")


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters',
                  category='error')
        elif password1 != password2:
            flash('Password dont match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email,
                            first_name=first_name,
                            password=generate_password_hash(password1,
                                                            method='sha256'))

            db.session.add(new_user)
            
            try:
                db.session.commit()
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
            
            except:
                db.session.rollback()
                flash('Email already exists!', category='error')


    return render_template("sign_up.html")
