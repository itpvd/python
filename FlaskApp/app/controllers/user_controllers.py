from flask import Flask, render_template,url_for,flash,redirect,request
from app import app,db,mail
from app.models.user import User
from flask_login import login_user,logout_user,current_user
from random import *
from functools import wraps

#function check authen admin
def login_required_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated==False or current_user.role!='admin':
            flash("You need to login first")
            return redirect(url_for('formLogin')) 
        else:
            try:
                return f(*args, **kwargs)
            except Exception as exception:
                return render_template('error/admin_error.html',error=type(exception).__name__)
    return wrap
#function check authen user
def login_required_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated==False:
            flash("You need to login first")
            return redirect(url_for('formLogin')) 
        else:
            try:
                return f(*args, **kwargs)
            except Exception as exception:
                return render_template('error/user_error.html',error=type(exception).__name__)
    return wrap
                           
#--USER MANAGER function--
#show list user
@app.route("/listUser")
@login_required_admin
def listUser():
    allRecord = User.listAllUser()
    page = request.args.get('page', 1, type=int)
    listUser = User.numberUserPerPage(page,10)
    return render_template("admin/admin_user_list.html",listUser = listUser,allRecord=allRecord)
#delete user 
@app.route("/deleteUser", methods=['GET'])
@login_required_admin
def deleteUser():
    id = request.args['id']
    User.deleteUser(id)
    return redirect('listUser')
#show form add user
@app.route("/formAddUser")
@login_required_admin
def formAddUser():
    return render_template('admin/admin_user_add.html')
#create new user
@app.route("/addUser", methods=['POST'])
@login_required_admin
def addUser():
    input = request.form
    if User.userExists(input['username'])==False  and User.checkLenPass(input['password']):
        user = User(input['username'],input['password'],input['email'],input['gender'],input['birthday'],input['phone'],input['role'])
        user.createUser()
        flash('Create user is successfull')
        return redirect('formAddUser')
    else: 
        flash(User.alertRegister(input['username'],input['password'],input['password']))
        return redirect('formAddUser')
#show form edit user
@app.route("/formEditUser", methods=['GET'])
@login_required_admin
def formEditUser():
    id = request.args['id']
    user = User.findUserById(id)
    return render_template('admin/admin_user_update.html',user=user)
#update user in database
@app.route("/updateUser",methods=['POST'])
@login_required_admin
def updateUser():
    input = request.form
    id = input['id']
    if User.checkLenPass(input['password']):
        user = User(input['username'],input['password'],input['email'],input['gender'],input['birthday'],input['phone'],input['role'])
        user.updateUser(id)
        flash('Update user is successfull')
        return redirect(url_for('formEditUser',id=id))
    else:
        flash('Password of at least 8 characters, including char and numbers, at least 1 capital letter')
        return redirect(url_for('formEditUser',id=id))
#show form change Password
@app.route("/formChangePassword", methods=['GET'])
@login_required_user
def formChangePassword():
    return render_template('user/change_password.html')
#change Password
@app.route("/changePassword",methods=['POST'])
@login_required_user
def changePassword():
    input = request.form
    if input['passwordold']==current_user.password and input['password'] == input['passwordcf'] and User.checkLenPass(input['password']):
        id = current_user.id
        user = User(current_user.username,input['password'],current_user.email,current_user.gender,current_user.birthday,current_user.phone,current_user.role)
        user.updateUser(id)
        flash('Change password successfull')
        return redirect('formChangePassword')
    else:
        flash(User.alertChangePassword(current_user.password,input['passwordold'],input['password'],input['passwordcf']))
        return redirect('formChangePassword')
#show form change Profile
@app.route("/formChangeProfile", methods=['GET'])
@login_required_user
def formChangeProfile():
    id = current_user.id
    user = User.findUserById(id)
    return render_template('user/change_profile.html',user=user)
@app.route("/changeProfile",methods=['POST'])
@login_required_user
def changeProfile():
    input = request.form
    id = current_user.id
    user = User(current_user.username,current_user.password,input['email'],input['gender'],input['birthday'],input['phone'],current_user.role)
    user.updateUser(id)
    flash('Change profile successfull')
    return redirect('formChangeProfile')
#show form foget password
@app.route("/formForgetPassword", methods=['GET'])
def formForgetPassword():
    return render_template('user/foget_password.html')
#send mail
@app.route("/sendEmail",methods=['POST'])
def senEmail():
    input = request.form
    user = User.findUserByName(input['username'])
    if user and user.email==input['email']:
        msg = Message(subject="Hello %s, Flask app reset password"%user.username,
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["%s"%user.email],
                      body="hi %s, new password:%s,thank you."%(user.username,user.password))
        mail.send(msg)
        flash('The password has been sent to your email')
        return redirect('formLogin')
    else:
        flash('User name or email wrong')
        return redirect('formForgetPassword')
