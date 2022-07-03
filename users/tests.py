import json

from rest_framework.test             import APITestCase
from rest_framework_simplejwt.tokens import OutstandingToken

from users.models import User

class UserSignUpTest(APITestCase):
    
    maxDiff = None
    
    def test_success_user_signup(self):
        data = {
            'email'    : 'DGK-test-01@gmail.com',
            'nickname' : 'DGK-01',
            'password' : 'DGK12345678'
        }
        
        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            {
                'email'    : 'DGK-test-01@gmail.com',
                'nickname' : 'DGK-01'
            }
        )
    

class UserSignInTest(APITestCase):
    
    maxDiff = None
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email    = 'DGK-test@gmail.com',
            nickname = 'DGK01',
            password = 'DGK12345678'
        )

    def test_success_user_signin(self):
        data = {
            'email'    : 'DGK-test@gmail.com',
            'nickname' : 'DGK01',
            'password' : 'DGK12345678'
        }
        
        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        
        user  = User.objects.get(email='DGK-test@gmail.com')
        token = OutstandingToken.objects.get(user=user).token
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(token, response.json()['refresh'])