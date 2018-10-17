from flask import Flask, render_template,url_for,flash,redirect,request
from app import app,db
from app.models.post import Post
from flask_login import login_user,logout_user,current_user

#--POST MANAGER function--
#show list all post
@app.route("/listPost")
def listPost():
      if current_user.is_authenticated==False or current_user.role!='admin':
          return redirect('formLogin')
      else:
          allrecord = Post.listAllPost()
          page = request.args.get('page', 1, type=int)
          result = Post.numberPostPerPage(page,10)
          return render_template("admin/admin_post_list.html",result = result, allrecord=allrecord)
#delete post
@app.route("/deletePost", methods=['GET'])
def deletePost():
      if current_user.is_authenticated==False or current_user.role!='admin':
          return redirect('formLogin')
      else:
          id = request.args['id']
          Post.deletePost(id)
          return redirect('listPost')
#show form add post
@app.route("/formAddPost")
def formAddPost():
      if current_user.is_authenticated==False or current_user.role!='admin':
          return redirect('formLogin')
      else:
          return render_template('admin/admin_post_add.html')
#create new post
@app.route("/addPost", methods=['POST'])
def addPost():
      if current_user.is_authenticated==False or current_user.role!='admin':
          return redirect('formLogin')
      else:
          result = request.form
          if result['title']!='' and result['content']!='':
              post = Post(result['title'],result['content'])
              Post.createPost(post)
              return redirect('listPost')
          else:
              return redirect('formAddPost')
#show form edit post
@app.route("/formEditPost",methods=['GET'])
def formEditPost():
      if current_user.is_authenticated==False or current_user.role!='admin':
          return redirect('formLogin')
      else:
          id = request.args['id']
          post = Post.findPostById(id)
          return render_template('admin/admin_post_update.html',post=post)
#update post in database
@app.route("/updatePost",methods=['POST'])
def updatePost():
      if current_user.is_authenticated==False or current_user.role!='admin':
          return redirect('formLogin')
      else:
          result = request.form
          id = result['id']
          post = Post(result['title'],result['content'])
          Post.updatePost(id,post)
          return redirect('listPost')

#POST VIEW function
#show list all post
@app.route("/viewPost")
def viewPost():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          result = Post.listAllPost()
          page = request.args.get('page', 1, type=int)
          result = Post.numberPostPerPage(page,5)
          return render_template("user/post_list.html",result = result)
#show detail post
@app.route("/detailPost")
def detailPost():
      if current_user.is_authenticated==False:
          return redirect('formLogin')
      else:
          id = request.args['id']
          result = Post.findPostById(id)
          return render_template("user/post_detail.html",result = result)
