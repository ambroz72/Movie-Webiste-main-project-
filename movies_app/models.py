from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):       
    c_category = models.CharField(max_length=50,null=True)

class Movies(models.Model):
    m_cat =models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    m_title = models.CharField(max_length=100,null=True)
    m_desc = models.TextField(null=True)
    m_DOB=models.DateField(null=True)
    m_act = models.CharField(max_length=100,null=True)
    m_youtube = models.TextField(null=True)
    m_img=models.ImageField(upload_to='gallery/',null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    

class Movie_cart(models.Model):       #user....
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    film= models.ForeignKey(Movies,on_delete=models.CASCADE,null=True)
      
class Users(models.Model):     
    e_movie = models.ForeignKey(Movies,on_delete=models.CASCADE,null=True)
    e_category =models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    e_user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    e_cart = models.ForeignKey(Movie_cart, on_delete=models.CASCADE,null=True)
    e_fname = models.CharField(max_length=30,null=True)
    e_lname = models.CharField(max_length=30,null=True)
    e_email = models.EmailField(null=True)
    e_post=models.CharField(max_length=50,null=True)
    e_photo = models.ImageField(upload_to='image/',null=True)
    
class Review(models.Model):
    re_movie = models.ForeignKey(Movies,on_delete=models.CASCADE,null=True)
    re_user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    re_name=models.CharField(max_length=20,null=True)
    re_feed=models.CharField(max_length=100,null=True)
    re_post=models.CharField(max_length=200,null=True)
    re_rating=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    re_DOB=models.DateField(null=True)
    
    # def get_movie_title(self):
    #     if self.re_movie:
    #         return self.re_movie.m_title
    #     else:
    #         return None
    