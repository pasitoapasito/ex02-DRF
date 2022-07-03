from rest_framework.views                 import APIView
from rest_framework.permissions           import AllowAny, IsAuthenticated
from rest_framework.response              import Response
from rest_framework_simplejwt.tokens      import OutstandingToken, BlacklistedToken

from drf_yasg          import openapi
from drf_yasg.utils    import swagger_auto_schema

from users.serializers import SignUpSerializer, SignInSerializer
    
class UserSignUpView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=SignUpSerializer, responses={201: SignUpSerializer})
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class UserSignInView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=SignInSerializer, responses={200: 'refresh : refresh_token, access : access_token'})
    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        
        if serializer.is_valid():
            token = serializer.validated_data
            return Response(token, status=200)
        return Response(serializer.errors, status=400)
        
        
class UserSignOutView(APIView):
    permission_classes = [IsAuthenticated]
    
    post_params = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'refesh_token': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    )
    @swagger_auto_schema(request_body=post_params, responses={200: f'user nickname signout success'})
    def post(self, request):
        user = request.user
        
        for token in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=token)
        
        return Response({'message' : f'user {user.nickname} signout success'}, status=200)


class UserinfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(responses={200: 'user authorization success'})
    def get(self, request):
        user = request.user
        return Response({'message' : f'{user.nickname} Authorization success'}, status=200)