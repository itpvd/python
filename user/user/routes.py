from flask import Flask, render_template,url_for,flash,redirect,request
from user import app,db
from user.forms import loginForm,registerForm
from user.models import User
from flask_login import login_user,logout_user

@app.route("/")
@app.route("/login", methods=['GET','POST'])
def login():
	form = loginForm()
	return render_template('login.html',title='login',form = form)

@app.route("/checkLogin", methods=['GET','POST'])
def checkLogin():
      result = request.form
      user = User.query.filter_by(username=result['username']).first()
      if user and user.password == result['password'] and user.role=='user':
            login_user(user,remember = True)
            flash('Hello %s! welecome to website'%result['username'])
            return render_template("news.html",result = result)
      elif user and user.password == result['password'] and user.role=='admin':
            login_user(user,remember = True)
            flash('Hello %s, welecome to website'%result['username'])
            return redirect('listuser')
      else:
            flash('User name or password is incorrect')
            return redirect('login')


@app.route("/register",methods=['GET','POST'])
def register():
	form = registerForm()
	return render_template('register.html',title='register',form = form)
@app.route("/checkRegister", methods=['GET','POST'])
def checkRegister():
      result = request.form
      user = User.query.filter_by(username=result['username']).first()
      if result['password']== result['confilmpass'] and not user:
            user = User(username=result['username'],password=result['password'],role='user')
            db.session.add(user)
            db.session.commit()
            flash('Account: %s created successfully'%result['username'])
            return render_template("register.html")
      else:
            flash('Account: %s created failed'%result['username'])
            return redirect('register')



@app.route("/logout")
def logout():
      logout_user()
      form = loginForm()
      return render_template('login.html',title='login',form = form)


@app.route("/listuser", methods=['GET','POST'])
def listuser():
      result = User.query.all()
      return render_template("admin_user.html",result = result)


@app.route("/deleteuser", methods=['GET','POST'])
def deleteuser():
      id = request.args['id']
      User.query.filter_by(id=id).delete()
      db.session.commit()
      return redirect('listuser')


@app.route("/adduser",methods=['GET','POST'])
def adduser():
      form = registerForm()
      return render_template('admin_user_add.html',form = form)
@app.route("/checkadduser", methods=['GET','POST'])
def checkadduser():
      result = request.form
      if result['password']== result['confilmpass']:
            user = User(username=result['username'],password=result['password'],role=result['role'])
            db.session.add(user)
            db.session.commit()
            return redirect('listuser')
      else:
            return redirect('adduser')



@app.route("/edituser",methods=['GET','POST'])
def edituser():
      id = request.args['id']
      user = User.query.filter_by(id=id).first()
      form = registerForm()
      return render_template('admin_user_update.html',form = form)