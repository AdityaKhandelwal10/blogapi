
from django.urls import path, include
from . import views

urlpatterns = [
     path('register/', views.RegisterUser.as_view()),
     path('verify/', views.VerifyUser.as_view()),
     path('generateotp/', views.GenerateToken.as_view()),
     path('login/', views.LoginUser.as_view()),
     path('logout/', views.LogoutUser.as_view())
]
