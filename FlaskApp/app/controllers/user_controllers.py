from flask import Flask, render_template,url_for,flash,redirect,request
from app import app,db,mail
from app.models.user import User
from flask_login import login_user,logout_user,current_user
from flask_mail import Mail, Message
from random import *

#--USER MANAGER function--
#show list user
@app.route("/listUser")
def listUser():
      if current_user.is_authenticated==False or current_user.role!='admin':
         return redirect('formLogin')
      else:
          allrecord = User.listAllUser()
          page = request.args.get('page', 1, type=int)
          result = User.numberUserPerPage(page,10)
          return render_template("admin/admin_user_list.html",result = result,allrecord=allrecord)
#delete user 
@app.route("/deleteUser", methods=['GET'])
def deleteUser():
      if current_user.is_authenticated==False or current_user.role!='admin':
          return redirect('formLogin')
      else:
          id = request.args['id']
          User.deleteUser(id)
          return redirect('listUser')
#show form add user
@app.route("/formAddUser")
def formAddUser():
      if current_user.is_authenticated==False or current_user.role!='admin':
          return redirect('formLogin')
      else:
          return render_template('admin/admin_user_add.html')
#create new user
@app.route("/addUser", methods=['POST'])
def addUser():
      if current_user.is_authenticated==False or current_user.role!='admin':
          return redirect('formLogin')
      else:
          result = request.form
          if User.userExists(result['username'])==False  and User.checkLenPass(result['password']):
                user = User(result['username'],result['password'],result['email'],result['gender'],result['birthday'],result['phone'],result['role'])
                User.createUser(user)
                flash('Create user is successfull')
                return redirect('formAddUser')
          else: 
                flash(User.alertRegister(result['username'],result['password'],result['password']))
                return redirect('formAddUser')
#show form edit user
@app.route("/formEditUser", methods=['GET'])
def formEditUser():
      if current_user.is_authenticated==False or current_user.role!='admin':
          return redirect('formLogin')
      else:
          id = request.args['id']
          user = User.findUserById(id)
          return render_template('admin/admin_user_update.html',user=user)
#update user in database
@app.route("/updateUser",methods=['POST'])
def updateUser():
      if current_user.is_authenticated==False or current_user.role!='admin':
          return redirect('formLogin')
      else:
          result = request.form
          id = result['id']
          if User.checkLenPass(result['password']):
              user = User(result['username'],result['password'],result['email'],result['gender'],result['birthday'],result['phone'],result['role'])
              User.updateUser(id,user)
              flash('Update user is successfull')
              return redirect(url_for('formEditUser',id=id))
          else:
              flash('Password of at least 8 characters, including char and numbers, at least 1 capital letter')
              return redirect(url_for('formEditUser',id=id))
#show form change Password
@app.route("/formChangePassword", methods=['GET'])
def formChangePassword():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          return render_template('user/change_password.html')
#change Password
@app.route("/changePassword",methods=['POST'])
def changePassword():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          result = request.form
          if result['passwordold']==current_user.password and result['password'] == result['passwordcf'] and User.checkLenPass(result['password']):
              id = current_user.id
              user = User(current_user.username,result['password'],current_user.email,current_user.gender,current_user.birthday,current_user.phone,current_user.role)
              User.updateUser(id,user)
              flash('Change password successfull')
              return redirect('formChangePassword')
          else:
              flash(User.alertChangePassword(current_user.password,result['passwordold'],result['password'],result['passwordcf']))
              return redirect('formChangePassword')
#show form change Profile
@app.route("/formChangeProfile", methods=['GET'])
def formChangeProfile():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          id = current_user.id
          user = User.findUserById(id)
          return render_template('user/change_profile.html',user=user)
#change Profile
@app.route("/changeProfile",methods=['POST'])
def changeProfile():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          result = request.form
          id = current_user.id
          user = User(current_user.username,current_user.password,result['email'],result['gender'],result['birthday'],result['phone'],current_user.role)
          User.updateUser(id,user)
          flash('Change profile successfull')
          return redirect('formChangeProfile')
#show form foget password
@app.route("/formForgetPassword", methods=['GET'])
def formForgetPassword():
          return render_template('user/foget_password.html')
#send mail
@app.route("/sendEmail",methods=['POST'])
def senEmail():
      result = request.form
      user = User.findUserByName(result['username'])
      if user and user.email==result['email']:
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
  