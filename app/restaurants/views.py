from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Restaurant, Comment
from .forms import CommentForm
from .choices import rating_choices, university_choices
import datetime
from django.contrib import messages, auth

# Create your views here.
def index(request):
    """
    View function for rendering the index page.
    
    Retrieves all published restaurants, paginates them, 
    and passes them to the 'restaurants.html' template.

    Args:
    - request: HttpRequest object

    Returns:
    - Rendered template with paginated restaurants
    """
    restaurants = Restaurant.objects.all().filter(is_published=True)    # Get all published restaurants
    
    # Paginate the restaurants, displaying 9 per page
    paginator = Paginator (restaurants,9)
    page = request.GET.get('page')
    paged_restaurants = paginator.get_page(page)
    
    # Prepare the context to be passed to the restaurants template
    context = {
        'restaurants':paged_restaurants
    }
    
    # Render the template with paginated restaurants
    return render(request,"restaurants/restaurants.html",context)

def restaurant (request,restaurant_id):
    """
    View function for rendering individual restaurant details.
    
    Retrieves the restaurant object using the provided restaurant_id,
    counts the number of comments for the restaurant, and checks if 
    the current user has already commented on the restaurant.

    Args:
    - request: HttpRequest object
    - restaurant_id: ID of the restaurant

    Returns:
    - Rendered template with restaurant details
    """
    # Get the restaurant object using restaurant_id
    restaurant = get_object_or_404 (Restaurant,pk=restaurant_id)
    
    # Check if the user has already commented on this restaurant
    existing_comment = Comment.objects.filter(restaurant=restaurant, commenter_name=request.user.username).first()
    
    # Count the number of comments for the restaurant
    num_comments = Comment.objects.filter(restaurant=restaurant).count()
    
    
    context = {
        'existing_comment':existing_comment,
        'restaurant': restaurant,
        'num_comments' : num_comments,
    }
    return render(request,"restaurants/restaurant.html", context)
    
def search(request):
    """
    View function for searching restaurants based on provided criteria.
    
    Retrieves all restaurants, orders them by rating, and filters
    them based on provided search criteria (keywords, university, rating).

    Args:
    - request: HttpRequest object

    Returns:
    - Rendered template with search results
    """
    # Get all restaurants and order them by rating
    queryset_restaurant = Restaurant.objects.order_by("-rating")
    
    # Filter restaurants based on provided search criteria
    # Keywords
    if "keywords" in request.GET:
        keywords = request.GET["keywords"]
        if keywords:
            # Filter for restaurants with names containing provided keywords
            queryset_restaurant = queryset_restaurant.filter(name__icontains=keywords) # Filter for similar names of restaurants
    
    # University        
    if "university" in request.GET:
        university = request.GET["university"]
        if university:
            # Filter for restaurants located at the exact university provided
            queryset_restaurant = queryset_restaurant.filter(university__iexact=university) # Filter for exact match
    
    # Rating
    if "rating" in request.GET:
        rating = request.GET["rating"]
        if rating:
            # Filter for restaurants with ratings greater than or equal to the provided rating
            queryset_restaurant = queryset_restaurant.filter(rating__gte=rating) # gte stands for greater than
    
    # Prepare context to pass to the search.html template    
    context = {
        "restaurants": queryset_restaurant, 
        "rating_choices" : rating_choices,
        "university_choices": university_choices,
        "values": request.GET
    }
    return render(request,"restaurants/search.html", context)

def add_comment(request, restaurant_id):
    """
    View function for adding a comment to a restaurant.
    
    Retrieves the restaurant for which the comment is being added,
    initializes the comment form, and processes the form data.

    Args:
    - request: HttpRequest object
    - restaurant_id: ID of the restaurant

    Returns:
    - Rendered template with comment form
    """
    # Get the restaurant for which the comment is being added
    eachRestaurant = Restaurant.objects.get(id=restaurant_id)
    
    # Initialize the comment form for the restaurant
    form = CommentForm(eachRestaurant)
    
    if request.method == "POST":
        # If the request method is POST, process the form data
        form = CommentForm(request.POST, instance=eachRestaurant)
        if form.is_valid():
            # If the form is valid, extract the comment details
            name = request.user.username
            body = form.cleaned_data ['comment_body']
            user_rating = form.cleaned_data ['user_rating']
            
            # Create a new comment instance
            c = Comment (restaurant = eachRestaurant, commenter_name = name, comment_body = body, user_rating=user_rating ,date_added =datetime.datetime.now())
            c.save()

            # Redirect the user back to the restaurant page after adding the comment
            return redirect(reverse("restaurant", args=[restaurant_id]))
        else:
            # If the form is invalid, display an error message
            messages.error(request,"The email is invalid")
    else:
        # If the request method is not POST, create an empty form
        form = CommentForm()
    
    # Prepare the context to be passed to the add_comment.html template
    context = {
        'form': form
    }
    
    return render (request,'restaurants/add_comment.html', context)

def delete_comment(request, restaurant_id):
    """
    View function for deleting a comment.
    
    Retrieves the comment associated with the provided restaurant_id
    and deletes it.

    Args:
    - request: HttpRequest object
    - restaurant_id: ID of the restaurant

    Returns:
    - Redirects to the restaurant page after deleting the comment
    """
    comment = Comment.objects.filter(restaurant=restaurant_id).first() #.last()
    restaurant_id = comment.restaurant.id
    comment.delete()

    return redirect(reverse("restaurant", args=[restaurant_id]))

def edit_comment(request, comment_id):
    """
    View function for editing a comment.
    
    Retrieves the comment based on the provided comment_id, processes
    the form data, and saves the changes.

    Args:
    - request: HttpRequest object
    - comment_id: ID of the comment

    Returns:
    - Rendered template with comment form
    """
    # Get the comment based on the provided comment_id
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.method == "POST":
        # If the request method is POST, process the form data
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            # If the form is valid, save the changes
            form.save()
            # Redirect the user back to the restaurant page after editing the comment
            return redirect(reverse("restaurant", args=[comment.restaurant.id]))
    else:
        # If the request method is not POST, create a form instance with the existing comment data
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment
    }
    
    return render(request, 'restaurants/update_comment.html', context)
