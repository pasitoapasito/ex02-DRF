import re

from django.contrib.auth.hashers          import check_password

from rest_framework                       import serializers
from rest_framework.serializers           import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class SignUpSerializer(ModelSerializer):
    
    def create(self, validated_data):
        email    = validated_data.get('email')
        password = validated_data.get('password')
            
        email_regexp    = '^\w+([\.-]?\w+)*@\w+(\.\w{2,3})+$'
        password_regexp = '\S{8,20}$'
        
        if not re.match(email_regexp, email):
            raise serializers.ValidationError('message : invalid email')
        
        if not re.match(password_regexp, password):
            raise serializers.ValidationError('message : invalid password')
        
        user = User.objects.create_user(**validated_data)  # self.Meta.model.objects.create_user(**validated_data)
        return user
    
    class Meta:
        model        = User  # get_user_model()
        fields       = ['email', 'nickname', 'password']
        extra_kwargs = {'password' : {'write_only' : True}}
        
        
class SignInSerializer(TokenObtainPairSerializer):
    email    = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, write_only=True, max_length=100)
    
    def validate(self, data):
        email    = data.get('email')
        password = data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('detail : user not existed')
        
        if not check_password(password, user.password):
            raise serializers.ValidationError('detail : invalid password')
        
        token         = super().get_token(user)
        refresh_token = str(token)
        access_token  = str(token.access_token)
        
        data = {
            'refresh' : refresh_token,
            'access'  : access_token
        }
        
        return data
        
    class Meta:
        model = User
        fields = ['email', 'password']