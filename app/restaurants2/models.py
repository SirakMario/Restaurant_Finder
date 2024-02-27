from django.db import models
import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



# Create your models here.
class Restaurant(models.Model):
    # Define choices for the name of universities
    university_choices = (
        ("UNL","Universidade Nova de Lisboa"),
        ("ifgi","University of Münster"),
        ("UJI","Universitat Jaume I"),
    )
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True)
    place_id = models.CharField(max_length=200)
    rating = models.CharField(blank=True)
    opening_time = models.CharField(blank=True)
    closing_time = models.CharField(blank=True)
    type_food = models.TextField(blank=True)
    latitude = models.FloatField(blank=True)
    longtitude = models.FloatField(blank=True)
    university = models.CharField(max_length=200, blank=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name       
        
    
class Comment(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="comments",on_delete=models.CASCADE) # change the varible
    commenter_name = models.CharField(max_length=200)
    comment_body = models.TextField()
    user_rating = models.DecimalField (max_digits=2, decimal_places=1,validators=[MinValueValidator(0),MaxValueValidator(5)],default=0.0)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.restaurant.name