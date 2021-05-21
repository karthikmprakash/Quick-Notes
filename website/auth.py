from flask import Blueprint, render_template, request, flash, redirect, url_for # URLs or Routes inside 
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, login_required, logout_user, current_user   

auth=Blueprint('auth',__name__) #easy to call the variable same 

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # to check if the user exists
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in Succesfuly',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password',category='error')
        else:
            flash('email does not exist',category='error')

    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user=User.query.filter_by(email=email).first()
        if user:
            flash('User already exists!',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters',category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters',category='error')
        elif password1 != password2:
            flash('password\'s dont match',category='error')
        elif len(password1) < 7 :
            flash('Passsword is too short, it must be atleast seven characters',category='error')
        else:
            new_user=User(email=email,first_name=firstName,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created!',category='success')
            return redirect(url_for('views.home'))

           

    return render_template("sign_up.html",user=current_user)