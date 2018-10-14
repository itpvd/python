from flask import Flask, render_template,url_for,flash,redirect,request
from app import app,db
from app.models.user import User
from flask_login import login_user,logout_user,current_user


#--USER MANAGER function--
#show list user
@app.route("/listUser")
def listUser():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          allrecord = User.listAllUser()
          page = request.args.get('page', 1, type=int)
          result = User.numberUserPerPage(page,2)
          return render_template("admin/admin_user_list.html",result = result,allrecord=allrecord)
#delete user 
@app.route("/deleteUser", methods=['GET'])
def deleteUser():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          id = request.args['id']
          User.deleteUser(id)
          return redirect('listUser')
#show form add user
@app.route("/formAddUser")
def formAddUser():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          return render_template('admin/admin_user_add.html')
#create new user
@app.route("/addUser", methods=['POST'])
def addUser():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          result = request.form
          if result['password']== result['confilmpass'] and not user  and User.checkLenPass(result['password']):
                user = User(result['username'],result['password'],result['role'])
                User.createUser(user)
                return redirect('listUser')
          else:
                return redirect('formAddUser')
#show form edit user
@app.route("/formEditUser", methods=['GET'])
def formEditUser():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          id = request.args['id']
          user = User.findUserById(id)
          return render_template('admin/admin_user_update.html',user=user)
#update user in database
@app.route("/updateUser",methods=['POST'])
def updateUser():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          result = request.form
          id = result['id']
          user = User(result['username'],result['password'],result['role'])
          User.updateUser(id,user)
          return redirect('listUser')
#show form change Password
@app.route("/formChangePassword", methods=['GET'])
def formChangePassword():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          id = current_user.id
          user = User.findUserById(id)
          return render_template('user/change_password.html',user=user)
#change Password
@app.route("/changePassword",methods=['POST'])
def changePassword():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          result = request.form
          if result['passwordold']==current_user.password and result['password'] == result['passwordcf']:
              id = current_user.id
              user = User(current_user.username,result['password'],current_user.role)
              User.updateUser(id,user)
              return redirect('viewPost')
          else:
              return redirect('formChangePassword')
