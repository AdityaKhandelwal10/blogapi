from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import User,UserVerification
from rest_framework.authtoken.models import Token
import json
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
import random
from django.core.cache import cache
from django.contrib.auth import authenticate 


# Create your views here.
class RegisterUser(APIView):
    """ 
    View to register user to the database using authtoken
    """
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny,]
    
    def post(self, request, format= None):
        register_data = json.loads(request.body.decode('utf-8'))

        try:
            username = register_data.get('username')
            email = register_data.get('email')
            password = register_data.get('password')
            new_user = User(username = username, email = email, is_active = 0)
            new_user.set_password(password)
            new_user.save()

            # Otp
            otp = random.randint(1000,9999)

            #entering data in UserVerification Table
            UserVerification.objects.create(user = new_user, otp = otp)

            # Setting cache here
            cache.set(username,otp,60)

            # Send Email to User
            subject = "Account Verification Mail"
            body = "The otp for you account verification is "+ str(otp)
            email_from = settings.EMAIL_HOST_USER
            email_recepient = [email,]
            send_mail(subject, body, email_from, email_recepient)

            return JsonResponse({'New user created :' : register_data , 'Otp' : otp, 'Mail' : 'email sent'})

        except Exception as e:
            return JsonResponse({"Error": str(e)}, safe = False)

class VerifyUser(APIView):

    permission_classes =[permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        otp = request.data.get('otp')
        otp = int(otp)
        try:
            user = User.objects.get(username = username)
            user_verify = UserVerification.objects.get(user = user.pk)
            
            otp_cache = cache.get(username)
            otp_model = user_verify.otp

            if(otp_model == otp and otp_cache == otp):
                user_verify.is_active = 1
                user_verify.save()
                user.is_active = 1
                user.save()
                cache.delete(username)
                return JsonResponse({"User Verified : " : username})

            else:
                return JsonResponse({"The given OTP is incorrect or expired pls try again ": "Verification Failed",
                                        "Given Otp:" : otp, "Otp model:" : otp_model, "otp cache:": otp_cache})   
        
        except Exception as e:
            return JsonResponse({"Error": str(e)}, safe = False)

class GenerateToken(APIView):
    """
    generate token for someone whose otp has timed out 
    """
    #fetch the user first and see if they are already verified,
    # if they are not, generate the otp and add another entry with the same name 
    # fast forward to the verify token
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        username = request.data.get('username')
        
        if(User.objects.filter(username = username).exists()):
            user = User.objects.get(username = str(username))
            userverify= UserVerification.objects.get(user=user)

            if(userverify.is_active ==0 and user.is_active == 0) :
                # Otp
                otp = random.randint(1000,9999)
                
                #setting in cache
                cache.delete(username)
                cache.set(username,otp,180)

                # Send Email to User
                subject = "Account Verification Mail"
                body = "The otp for you account verification is "+ str(otp)
                email_from = settings.EMAIL_HOST_USER
                email_recepient = [user.email,]
                send_mail(subject, body, email_from, email_recepient)

                #changing the user verification table
                userverify.otp = otp
                userverify.save()

                return JsonResponse({'Mail sent to :' : username , 'Otp' : otp})
            
            else: 
                return JsonResponse({'This user is already verified :' : username })

        else :
            return JsonResponse({'Error :' :'This user does not exist'})

class LoginUser(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, format = None):

        try:
            username = request.data.get('username') 
            password = request.data.get('password')
            
            user = authenticate(username = username, password = password)
            if user is not None:
                if(user.is_active):
                    token = Token.objects.create(user =user)

                    return JsonResponse({"Token key:": token.key})
                else:
                    return JsonResponse({"Error" : "Please verify your email first"})
            
            else:
                return JsonResponse({"Unsuccessful login" : "Please check again"}) 
        
        except Exception as e:
             return JsonResponse({"Error": str(e)}, safe = False)

class LogoutUser(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        try:
            username = request.data.get('username')

            user = User.objects.get(username = username)
            token = Token.objects.get(user = user)
            
            token.delete()

            return JsonResponse({"Successful Logout" : username}) 

        except Exception as e:
            return JsonResponse({"Error": str(e)},safe = False)