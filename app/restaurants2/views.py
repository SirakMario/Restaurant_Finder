from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Restaurant, Comment
from .forms import CommentForm
from .choices import rating_choices, university_choices
import datetime
from django.contrib import messages, auth

# Create your views here.
def index(request):
    restaurants = Restaurant.objects.all().filter(is_published=True)
    
    paginator = Paginator (restaurants,9)
    page = request.GET.get('page')
    paged_restaurants = paginator.get_page(page)
    context = {
        'restaurants':paged_restaurants
    }
    
    return render(request,"restaurants/restaurants.html",context)

def restaurant (request,restaurant_id):
    restaurant = get_object_or_404 (Restaurant,pk=restaurant_id)
    
    num_comments = Comment.objects.filter(restaurant=restaurant).count()
    
    # Check if the current user has already commented on this restaurant
    user_has_commented = False
    if request.user.is_authenticated:
        user_comments = Comment.objects.filter(restaurant=restaurant, commenter_name=request.user.username)
        if user_comments.exists():
            user_has_commented = True
    
    context = {
        'user_has_commented': user_has_commented,
        'restaurant': restaurant,
        'num_comments' : num_comments,
    }
    return render(request,"restaurants/restaurant.html", context)
    
def search(request):
    queryset_restaurant = Restaurant.objects.order_by("-rating")
    
    # Keywords
    if "keywords" in request.GET:
        keywords = request.GET["keywords"]
        if keywords:
            queryset_restaurant = queryset_restaurant.filter(name__icontains=keywords) # filter for similar names of restaurants
            
    if "university" in request.GET:
        university = request.GET["university"]
        if university:
            queryset_restaurant = queryset_restaurant.filter(university__iexact=university) #filter for exact match
    
    if "rating" in request.GET:
        rating = request.GET["rating"]
        if rating:
            queryset_restaurant = queryset_restaurant.filter(rating__gte=rating) # gte stands for greater than
            
    context = {
        "restaurants": queryset_restaurant, 
        "rating_choices" : rating_choices,
        "university_choices": university_choices,
        "values": request.GET
    }
    return render(request,"restaurants/search.html", context)

def add_comment(request, restaurant_id):
    eachRestaurant = Restaurant.objects.get(id=restaurant_id)
    
    form = CommentForm(eachRestaurant)
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=eachRestaurant)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data ['comment_body'];
            
            c = Comment (restaurant = eachRestaurant, commenter_name = name, comment_body = body, date_added =datetime.datetime.now())
            c.save()

            return redirect(reverse("restaurant", args=[restaurant_id]))
        else:
            messages.error(request,"The email is invalid")
            #print ("form is invalid") # Add msg alert instead of printing
    else:
        form = CommentForm()
    context = {
        'form': form
    }
    
    return render (request,'restaurants/add_comment.html', context)

def delete_comment(request, restaurant_id):
    comment = Comment.objects.filter(restaurant=restaurant_id).first() #.last()
    restaurant_id = comment.restaurant.id
    comment.delete()

    return redirect(reverse("restaurant", args=[restaurant_id]))

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(reverse("restaurant", args=[comment.restaurant.id]))
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment
    }
    
    return render(request, 'restaurants/update_comment.html', context)
