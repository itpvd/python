import os
import unittest
from app import app,db,mail
 
class PostControllersTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
    def deletePost(self, id):
        return self.app.get(
            '/deletePost',
            data=dict(id=id),
            follow_redirects=True
        )
    def addPost(self, title, content):
        return self.app.post(
            '/addPost',
            data=dict(title=title, content=content),
            follow_redirects=True
        )
    def updatePost(self,id,title, content):
        return self.app.post(
            '/updatePost',
            data=dict(id=id,title=title, content=content),
            follow_redirects=True
        )
        
    def test_valid_post_delete(self):
        response = self.deletePost(9)
        self.assertEqual(response.status_code, 200)
    def test_valid_addPost(self):
        response = self.addPost('post','post is first')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create new post is successful', response.data)
    def test_valid_updatePost(self):
        response = self.updatePost(4,'update python','python')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Update post is successful', response.data)

if __name__ == "__main__":
    unittest.main()
