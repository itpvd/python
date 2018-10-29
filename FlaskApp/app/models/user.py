from flask_sqlalchemy import SQLAlchemy
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    gender = db.Column(db.String(128))
    birthday =db.Column(db.DateTime)
    phone = db.Column(db.String(128))
    role = db.Column(db.String(10))
    def __init__(self,username,password,email,gender,birthday,phone,role):
        self.username = username
        self.password = password
        self.email = email
        self.gender = gender
        self.birthday = birthday
        self.phone = phone
        self.role = role
        
    #query list all user
    def listAllUser():
        list = User.query.all()
        return list
    # number user per page pagination
    def numberUserPerPage(pages,number):
        result = User.query.paginate(page=pages, per_page=number)
        return result
    #find user by id = idUser
    def findUserById(idUser):
        user = User.query.filter_by(id=idUser).first()
        return user
    #find user by username = name
    def findUserByName(name):
        user = User.query.filter_by(username=name).first()
        return user
     #find user by username = name
    def findUserByEmail(mail):
        user = User.query.filter_by(email=mail).first()
        return user
    #create new user
    def createUser(self):
        db.session.add(self)
        db.session.commit()
    #delete user where id = idUser
    def deleteUser(idUser):
        User.query.filter_by(id=idUser).delete()
        db.session.commit()
    #update user
    def updateUser(self,idUser):
        user= User.query.filter_by(id=idUser).first()
        user.password = self.password
        user.role = self.role
        user.email = self.email
        user.gender = self.gender
        user.phone= self.phone
        user.birthday = self.birthday
        db.session.commit()
    #function check user exists
    def userExists(name):
        user = User.findUserByName(name)
        if user:
            return True
        else:
            return False
    #function check pass 
    def checkLenPass(password):
        if password.__len__()>8 and password.isalpha() ==False and password.isnumeric()==False and password.islower()==False:
            return True
        else:
            return False
    #furnction alert register user:
    def alertRegister(username,password,passwordcf):
        alert=''
        if User.userExists(username):
            alert='Username already exists,please create another username'
        elif password!=passwordcf:
            alert='Password must match with password confirm'
        else:
            alert='Password of at least 8 characters, including char and numbers, at least 1 capital letter'
        return alert
    #furnction alert change password:
    def alertChangePassword(password,oldpassword,newpassword,passwordcf):
        alert=''
        if password!=oldpassword:
            alert='Old password invalid'
        elif password!=passwordcf:
            alert='New password must match with password confirm'
        else:
            alert='Password of at least 8 characters, including char and numbers, at least 1 capital letter'
        return alert
   