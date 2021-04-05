from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from register.models import User, UserVerification
from .models import Blogs,Category
from django.db.models import Q
from django.core.paginator import    Paginator                                              

#Blog CRUD operations API

class CreateBlog(APIView):
    authentication_classes =[authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        username = request.data.get('username')

        blog_title = request.data.get('title')
        blog_desc = request.data.get('description')
        blog_content = request.data.get('content')
        blog_category = request.data.get('category')

        try :

            user = User.objects.get(username = username)
            category = Category.objects.get(category = blog_category)
            new_blog = Blogs(user = user, title = blog_title, 
                            desc = blog_desc, content = blog_content)
            
            new_blog.save()
            new_blog.category.add(category)
            new_blog.save()

            return JsonResponse({'New Blog created :': blog_title, 'Created by :': username})
        except Exception as e:
            return JsonResponse({'Error' : str(e)})
    
    
class RetrieveBlogs(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    

    def get(self, request, format = None):
        blogs = Blogs.objects.all()
        
        # category = request.body.get('category')
        # blogs = blogs.objects.get()

        data = list(blogs.values())
        return JsonResponse(data, safe = False)

    def post(self,request, format = None):

        # username = request.data.get('username')
        user = request.user
        category = request.body.get('category')
        
        blogs = Blogs.objects.filter(user = user)
        # if(Blogs.objects.filter(user = user).exists()):
        if(blogs is not None):
            # blogs = Blogs.objects.filter(user = user)
            data = list(blogs.values())
                
            return JsonResponse(data, safe = False)
            
        else:
            return JsonResponse({"Error" : "You havent written any blog", 
                                    "user" : user.username}, safe =False )

class UpdateBlog(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pass

class Blogfilter(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request, format = None):
        try : 
            user1 = request.data.get('author')
                # user = request.user
            category = request.data.get('category')
            page_number = request.data.get('page_number')
            page_size = request.data.get('page_size')
                # blogs = Blogs.objects.filter(user = user)
                # if(Blogs.objects.filter(user = user).exists()):
            user = User.objects.get(username = user1)
            blogs = Blogs.objects.filter(Q(user = user.id) or Q(category = category))

            paginator = Paginator(blogs.values() , page_size)
            page_obj = paginator.get_page(page_number)

            if blogs:
                    # blogs = Blogs.objects.filter(user = user)
                data = list(page_obj)
                        
                return JsonResponse(data, safe = False)
                    
            else:
                return JsonResponse({"Empty" : "You havent written any blog", 
                                            "user" : user.username}, safe =False )
            
        except Exception as e:
            return JsonResponse({'Error' : str(e)})
