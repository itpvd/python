from flask import Flask, render_template,url_for,flash,redirect,request
from app import app,db
from app.models.models import User,Post
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
      user = User.query.filter_by(username=result['username']).first()
      if user and user.password == result['password'] and user.role=='user':
            login_user(user,remember = False)
            flash('Hello %s! welecome to website'%result['username'])
            return redirect('viewPost')
      elif user and user.password == result['password'] and user.role=='admin':
            login_user(user,remember = False)
            flash('Hello %s, welecome to website'%result['username'])
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
      user = User.query.filter_by(username=result['username']).first()
      if result['password']== result['confilmpass'] and not user:
            user = User(result['username'],result['password'],'user')
            db.session.add(user)
            db.session.commit()
            flash('Account: %s created successfully'%result['username'])
            return render_template("user/register.html")
      else:
            flash('Account: %s created failed'%result['username'])
            return redirect('formRegister')
#Logout
@app.route("/logout")
def logout():
      logout_user()
      return redirect('formLogin')


#--USER MANAGER function--
#show list user
@app.route("/listUser")
def listUser():
      allrecord = User.query.all()
      page = request.args.get('page', 1, type=int)
      result = User.query.paginate(page=page, per_page=10)
      return render_template("admin/admin_user_list.html",result = result,allrecord=allrecord)
#delete user 
@app.route("/deleteUser", methods=['GET'])
def deleteUser():
      id = request.args['id']
      User.query.filter_by(id=id).delete()
      db.session.commit()
      return redirect('listUser')
#show form add user
@app.route("/formAddUser")
def formAddUser():
      return render_template('admin/admin_user_add.html')
#create new user
@app.route("/addUser", methods=['POST'])
def addUser():
      result = request.form
      if result['password']== result['confilmpass']:
            user = User(result['username'],result['password'],result['role'])
            db.session.add(user)
            db.session.commit()
            return redirect('listUser')
      else:
            return redirect('formAddUser')
#show form edit user
@app.route("/formEditUser", methods=['GET'])
def formEditUser():
      id = request.args['id']
      user = User.query.filter_by(id=id).first()
      return render_template('admin/admin_user_update.html',user=user)
#update user in database
@app.route("/updateUser",methods=['POST'])
def updateUser():
      result = request.form
      id = result['id']
      user = User.query.filter_by(id=id).first()
      user.username = result['username']
      user.password = result['password']
      user.role = result['role']
      db.session.commit()
      return redirect('listUser')


#--POST MANAGER function--
#show list all post
@app.route("/listPost")
def listPost():
      allrecord = Post.query.all()
      page = request.args.get('page', 1, type=int)
      result = Post.query.paginate(page=page, per_page=10)
      return render_template("admin/admin_post_list.html",result = result, allrecord=allrecord)
#delete post
@app.route("/deletePost", methods=['GET'])
def deletePost():
      id = request.args['id']
      Post.query.filter_by(id=id).delete()
      db.session.commit()
      return redirect('listPost')
#show form add post
@app.route("/formAddPost")
def formAddPost():
      return render_template('admin/admin_post_add.html')
#create new post
@app.route("/addPost", methods=['POST'])
def addPost():
      result = request.form
      if result['title']!='' and result['content']!='':
            post = Post(result['title'],result['content'])
            db.session.add(post)
            db.session.commit()
            return redirect('listPost')
      else:
            return redirect('formAddPost')
#show form edit post
@app.route("/formEditPost",methods=['GET'])
def formEditPost():
      id = request.args['id']
      post = Post.query.filter_by(id=id).first()
      return render_template('admin/admin_post_update.html',post=post)
#update post in database
@app.route("/updatePost",methods=['POST'])
def updatePost():
      result = request.form
      id = result['id']
      post = Post.query.filter_by(id=id).first()
      post.title = result['title']
      post.content = result['content']
      db.session.commit()
      return redirect('listPost')

#POST VIEW function
#show list all post
@app.route("/viewPost")
def viewPost():
      result = Post.query.all()
      page = request.args.get('page', 1, type=int)
      result = Post.query.paginate(page=page, per_page=5)
      return render_template("user/post_list.html",result = result)
#show detail post
@app.route("/detailPost")
def detailPost():
      id = request.args['id']
      result = Post.query.filter_by(id=id).first()
      return render_template("user/post_detail.html",result = result)
