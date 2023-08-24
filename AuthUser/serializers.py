from django.forms import ValidationError
from rest_framework import serializers
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from AuthUser.models import *
# from ..AuthenticateOurself.util import send_mail

class AuthUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = AuthUser
        fields = ["email","name","password","password2","tc"]
        extra_kwargs={
            'password':{"write_only":True}
        }

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("incorrect password")
        return attrs
    
    def create(self, validated_data):
        return AuthUser.objects.create_user(**validated_data)
    
class AuthLoginUserSerializers(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model = AuthUser
        fields = ['email','password']

class AuthUserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['id','email','name']

class AuthUserChangePassSerializers(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'passowrd'},write_only=True)
    class Meta:
        model = AuthUser
        fields = ['password','password2']
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Both Password is incorrect")
        user.set_password(password)
        user.save()
        return attrs

class AuthUserResetpasswordSerializers(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = AuthUser
        fields = ['email']
        
    def validate(self, attrs):
        email = attrs.get('email')
        if AuthUser.objects.filter(email = email).exists():
            user = AuthUser.objects.get(email = email)
            print(user,"hello")
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:4200/'+ uid + "/" + token
            data={
                'subject':"reset password",
                'body':"click on this link " + link,
                'to_email':user.email

            }
            util.send_mail(data)
            return attrs
        return serializers.ValidationError('This user is not register')

class AuthuserWillResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        model = AuthUser
        fields =['password','password2']
    
    def validate(self,attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                print('step1')
                raise serializers.ValidationError("Both password is not same ")
            print('step2')
            id = smart_str(urlsafe_base64_decode(uid))
            user = AuthUser.objects.get(id=id)
            print('step3',user)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Invalid token.')
            else:
                user.set_password(password)
                user.save()
                return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError("Token is not valid or expired")

