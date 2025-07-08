from django.urls import path
from userauth import views

app_name= "userauth"

urlpatterns = [
    path("signup/", views.signup,name="signup"),
    path("login/", views.signin,name="login"),
    path("logout/", views.signout,name="signout"),
]

