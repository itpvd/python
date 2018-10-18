from flask import Flask, render_template,url_for,flash,redirect,request
from app import app,db
from app.models.user import User
from flask_login import login_user,logout_user

#--LOGIN function--
#form login
@app.route("/")
@app.route("/formLogin")
def formLogin():
	return render_template('user/login.html',title='login')
#check login
@app.route("/checkLogin", methods=['POST'])
def checkLogin():
      result = request.form
      user = User.findUserByName(result['username'])
      if user and user.password == result['password'] and user.role=='user':
            login_user(user,remember = False)
            return redirect('viewPost')
      elif user and user.password == result['password'] and user.role=='admin':
            login_user(user,remember = False)
            return redirect('listUser')
      else:
            flash('User name or password is incorrect')
            return redirect('formLogin')
#--REGISTER function--
#form register
@app.route("/formRegister")
def formRegister():
	return render_template('user/register.html',title='register')
#check register
@app.route("/checkRegister", methods=['POST'])
def checkRegister():
      result = request.form
      user = User.findUserByName(result['username'])
      if result['password']== result['confilmpass'] and not user  and User.checkLenPass(result['password']):
            user = User(result['username'],result['password'],result['email'],result['gender'],result['birthday'],result['phone'],'user')
            User.createUser(user)
            flash('Account: %s created successfully'%result['username'])
            return render_template("user/register.html")
      else:
            flash(User.alertRegister(result['username'],result['password'],result['confilmpass']))
            return redirect('formRegister')
#Logout
@app.route("/logout")
def logout():
      logout_user()
      return redirect('formLogin')
