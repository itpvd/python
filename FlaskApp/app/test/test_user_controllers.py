import os
import unittest
from app import app,db,mail
 
class UserControllersTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
    def deleteUser(self, id):
        return self.app.get(
            '/deleteUser',
            data=dict(id=id),
            follow_redirects=True
        )
    def addUser(self, username, password,email,gender,birthday,phone,role):
        return self.app.post(
            '/addUser',
            data=dict(username=username, password=password,email=email,gender=gender,birthday=birthday,phone=phone,role=role),
            follow_redirects=True
        )
     def updateUser(self,id,username, password,email,gender,birthday,phone,role):
        return self.app.post(
            '/updateUser',
            data=dict(id=id,username=username, password=password,email=email,gender=gender,birthday=birthday,phone=phone,role=role),
            follow_redirects=True
        )

    def test_valid_user_delete(self):
        response = self.deleteUser(9)
        self.assertEqual(response.status_code, 200)
    def test_valid_addUser(self):
        response = self.addUser('daopv126','12345678A','patkennedy@gmail.com', 'male', '2-9-1996','09867546','user')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create user is successfull', response.data)
    def test_invalid_addUser_exists_user(self):
        response = self.addUser('daopv','12345678A','patkennedy@gmail.com', 'male', '2-9-1996','09867546','user')
        self.assertIn(b'Username already exists,please create another username', response.data)
    def test_invalid_addUser_length_password(self):
        response = self.addUser('daopv123','12345','patkennedy@gmail.com', 'male', '2-9-1996','09867546','user')
        self.assertIn(b'Password of at least 8 characters, including char and numbers, at least 1 capital letter', response.data)
    def test_invalid_addUser_capital_password(self):
        response = self.addUser('daopv123','1234567a','patkennedy@gmail.com', 'male', '2-9-1996','09867546','user')
        self.assertIn(b'Password of at least 8 characters, including char and numbers, at least 1 capital letter', response.data)
    def test_valid_update(self):
        response = self.updateUser(8,'dao4','12345678A','patkennedy@gmail.com', 'male', '2-9-1996','09867546','user')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Update user is successfull', response.data)

if __name__ == "__main__":
    unittest.main()
