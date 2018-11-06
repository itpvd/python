from flask import Flask, render_template,url_for,flash,redirect,request,json
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
@app.route("/login", methods=['POST'])
def login():
    try:
        input = request.form
        user = User.findUserByName(input['username'])
        if user and user.password == input['password'] and user.role=='user':
            login_user(user)
            return json.dumps({'status':'login_user'});
        elif user and user.password == input['password'] and user.role=='admin':
            login_user(user)
            return json.dumps({'status':'login_admin'});
        else:
            flash('User name or password is incorrect')
            return json.dumps({'status':'login_failed'});
    except Exception as exception:
        return json.dumps({'status':'exception','error':type(exception).__name__});

#--REGISTER function--
#form register
@app.route("/formRegister")
def formRegister():
    return render_template('user/register.html',title='register')
#check register
@app.route("/register", methods=['POST'])
def register():
    try:
        input = request.form
        user = User.findUserByName(input['username'])
        if not user  and input['password']== input['confirmpass'] and  User.checkLenPass(input['password']):
            user = User(input['username'],input['password'],input['email'],input['gender'],input['birthday'],input['phone'],'user')
            User.createUser(user)
            flash('Account: %s created successfully'%user.username)
            return json.dumps({'status':'register_successful'});
        else:
            flash(User.alertRegister(input['username'],input['password'],input['confirmpass']))
            return json.dumps({'status':'register_failed'});
    except Exception as exception:
        return json.dumps({'status':'exception','error':type(exception).__name__});
        
#Logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect('formLogin')
