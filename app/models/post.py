from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    def __init__(self,title,content):
        self.title = title
        self.content = content
        
    #list all post
    def listAllPost():
        list = Post.query.all()
        return list
    #number post per page
    def numberPostPerPage(pages,number):
        result = Post.query.paginate(page=pages, per_page=number)
        return result
    #find post by id = idPost
    def findPostById(idPost):
        post = Post.query.filter_by(id=idPost).first()
        return post
    #create new post
    def createPost(self):
        db.session.add(self)
        db.session.commit()
    #delete post where id=idPost
    def deletePost(idPost):
        Post.query.filter_by(id=idPost).delete()
        db.session.commit()
    #update post
    def updatePost(self,idPost):
        post= Post.query.filter_by(id=idPost).first()
        post.title = self.title
        post.content = self.content
        db.session.commit()
