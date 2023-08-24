from django.urls import path,include
from AuthUser.views import *
urlpatterns = [
    path("register", AuthUserRegisterView.as_view(), name='register'),
    path("login", AuthUserLogin.as_view(), name='login'),
    path("profile", AuthUserProfile.as_view(), name='profile'),
    path("changepassword", AuthUserChangePasswordView.as_view(), name='change password' ),
    path('resetpassword',AuthUserResetpasswordView.as_view(), name="resetpassword"),
    path('resetpasswordwill/<uid>/<token>/',AuthuserWillResetPasswordView.as_view(),name="changepasswordwill")
]
