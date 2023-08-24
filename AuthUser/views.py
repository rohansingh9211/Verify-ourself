from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from AuthUser.serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.
# ------> Generate seperate token <------

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class AuthUserRegisterView(APIView):
    def post(self,request):
        serializers=AuthUserSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            user = serializers.save()
            token = get_tokens_for_user(user)
            return Response({'msg':"Register successfull","token":token},status=status.HTTP_201_CREATED)
        return Response({"msg":"user is not valid"},status=status.HTTP_400_BAD_REQUEST)


class AuthUserLogin(APIView):
    def post(self,request):
        serializers = AuthLoginUserSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            email = serializers.data.get('email')
            password =serializers.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"msg":"Login successfully","token":token["access"]},status=status.HTTP_200_OK)
        return Response({"msg":"error"},status=status.HTTP_400_BAD_REQUEST)
    
class AuthUserProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializers = AuthUserProfileSerializers(request.user)
        return Response(serializers.data,status=status.HTTP_200_OK) 
    
class AuthUserChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=AuthUserChangePassSerializers(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':"Password change successfully"},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
class AuthUserResetpasswordView(APIView):
    def post(self,request):
        serializers=AuthUserResetpasswordSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            return Response({"msg":"reset link send successfully to your email"},status=status.HTTP_200_OK)
        return Response({"msg":"This email is not register please register first"},status=status.HTTP_404_NOT_FOUND)
    
class AuthuserWillResetPasswordView(APIView):
    def post(self,request,uid,token):
        serializer = AuthuserWillResetPasswordSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':"your password reset successfully"} ,status=status.HTTP_200_OK)
        return Response({"msg":"Both password does not match perfectly"},status= status.HTTP_400_BAD_REQUEST)