
from django.urls import path, include
from . import views

urlpatterns = [
     path('create/', views.CreateBlog.as_view()),
     path('retrieve/', views.RetrieveBlogs.as_view()),
     path('blogfilter/', views.Blogfilter.as_view()),
     
    #  path('verify/', views.VerifyUser.as_view() )
]
