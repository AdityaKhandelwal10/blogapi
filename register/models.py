from django.db import models
from django.contrib.auth.models import AbstractUser

user_choices = (("Author", "Author"),
                ("Reader" ,"Reader"),
                )

class User(AbstractUser):
    email = models.EmailField()
    usertype = models.CharField(max_length = 20, choices = user_choices, default = 'Reader')

    def __str__(self):
        return self.username


class UserVerification(models.Model):
    """
        Table for User Verification with an OTP 
    """
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    otp = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add =True)
    modified_on = models.DateTimeField(auto_now = True)
    is_active = models.IntegerField(default =0)

    def __str__(self):
        return self.user.username

