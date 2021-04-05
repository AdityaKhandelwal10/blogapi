from django.db import models
from register.models import User


class Category(models.Model):
    category = models.CharField(max_length = 40)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Category"


class Blogs(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 144, blank=False)
    desc = models.CharField(max_length = 144, blank=True)
    content = models.TextField()
    category = models.ManyToManyField(Category, blank =True)
    
    def __str__(self):
        return self.title 

    class Meta:
        verbose_name_plural = "Blogs"