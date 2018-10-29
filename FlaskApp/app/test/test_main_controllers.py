import os
import unittest
from app import app, db, mail
 
class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        mail.init_app(app)
        self.assertEqual(app.debug, False)
    def tearDown(self):
        pass

    def register(self, username, password, confirmpass,email,gender,birthday,phone):
        return self.app.post(
            '/register',
            data=dict(username=username, password=password, confirmpass=confirmpass,email=email,gender=gender,birthday=birthday,phone=phone),
            follow_redirects=True
        )
     def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def test_valid_user_registration(self):
        response = self.register('daopv12','12345678A','12345678A','patkennedy@gmail.com', 'male', '2-9-1996','09867546')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'daopv12 created successfully', response.data)
    def test_invalid_user_registration_different_passwords(self):
        response = self.register('daopv123','12345678A','12345678B','patkennedy@gmail.com', 'male', '2-9-1996','09867546')
        self.assertIn(b'Password must match with password confirm', response.data)
    def test_invalid_user_registration_exists_user(self):
        response = self.register('daopv','12345678A','12345678A','patkennedy@gmail.com', 'male', '2-9-1996','09867546')
        self.assertIn(b'Username already exists,please create another username', response.data)
    def test_invalid_user_registration_length_password(self):
        response = self.register('daopv123','12345','12345','patkennedy@gmail.com', 'male', '2-9-1996','09867546')
        self.assertIn(b'Password of at least 8 characters, including char and numbers, at least 1 capital letter', response.data)
    def test_invalid_user_registration_capital_password(self):
        response = self.register('daopv123','1234567a','1234567a','patkennedy@gmail.com', 'male', '2-9-1996','09867546')
        self.assertIn(b'Password of at least 8 characters, including char and numbers, at least 1 capital letter', response.data)
    def test_valid_user_login(self):
        response = self.login('daopv12','12345678A')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'daopv12', response.data)
        self.assertIn(b'Welcome to my blog', response.data)
    def test_valid_admin_login(self):
        response = self.login('admin','12345678A')
        self.assertEqual(response.status_code, 200)
        #print(response.data)
        self.assertIn(b'admin', response.data)
        self.assertIn(b'List User', response.data)
    def test_invalid_login_wrong_username(self):
        response = self.login('lalalala','12345678A')
        self.assertIn(b'User name or password is incorrect', response.data)
    def test_invalid_login_wrong_password(self):
            response = self.login('admin','12345678Ad')
            self.assertIn(b'User name or password is incorrect', response.data)

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
 
if __name__ == "__main__":
    unittest.main()
    