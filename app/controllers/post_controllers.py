from flask import Flask, render_template,url_for,flash,redirect,request,json
from app import app,db
from app.models.post import Post
from flask_login import login_user,logout_user,current_user
from functools import wraps

#function check authen admin
def login_required_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated==False or current_user.role!='admin':
            flash("You need to login first")
            return json.dumps({'status':'not_authenticated'});
        else:
            try:
                return f(*args, **kwargs)
            except Exception as exception:
                return json.dumps({'status':'exception','error':type(exception).__name__});
    return wrap
#function check authen user
def login_required_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated==False:
            flash("You need to login first")
            return json.dumps({'status':'not_authenticated'});
        else:
            try:
                return f(*args, **kwargs)
            except Exception as exception:
                return json.dumps({'status':'exception','error':type(exception).__name__});
    return wrap

#--POST MANAGER function--
#show list all post
@app.route("/showListPost")
@login_required_admin
def showListPost():
    return render_template('admin/admin_post_list.html')
@app.route("/listPost")
#@login_required_admin
def listPost():
    allRecord = Post.listAllPost()
    page = request.args.get('page', 1, type=int)
    listPost = Post.numberPostPerPage(page,10)
    object_dict = {x.id: x for x in allRecord}
    return json.dumps(object_dict);
   
@app.route("/deletePost", methods=['GET'])
@login_required_admin
def deletePost():
      id = request.args['id']
      Post.deletePost(id)
      return redirect('listPost')

#show form add post
@app.route("/formAddPost")
@login_required_admin
def formAddPost():
    return render_template('admin/admin_post_add.html')
#create new post
@app.route("/addPost", methods=['POST'])
@login_required_admin
def addPost():
    input = request.form
    post = Post(input['title'],input['content'])
    post.createPost()
    flash('Create new post is successful')
    return json.dumps({'status':'add_post_successful'})

#show form edit post
@app.route("/formEditPost",methods=['GET'])
@login_required_admin
def formEditPost():
    id = request.args['id']
    post = Post.findPostById(id)
    return render_template('admin/admin_post_update.html',post=post)
#update post in database
@app.route("/updatePost",methods=['POST'])
@login_required_admin
def updatePost():
    input = request.form
    id = input['id']
    post = Post(input['title'],input['content'])
    post.updatePost(id)
    flash('Update post is successful')
    return redirect(url_for('formEditPost',id=id))

#POST VIEW function
#show list all post
@app.route("/viewPost")
@login_required_user
def viewPost():
    page = request.args.get('page', 1, type=int)
    listPost = Post.numberPostPerPage(page,5)
    return render_template("user/post_list.html",listPost = listPost)   
#show detail post
@app.route("/detailPost")
@login_required_user
def detailPost():
    id = request.args['id']
    post = Post.findPostById(id)
    return render_template("user/post_detail.html",post = post)
    