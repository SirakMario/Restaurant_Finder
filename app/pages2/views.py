from django.shortcuts import render
from restaurants.models import Restaurant
from restaurants.choices import rating_choices, university_choices


# Create your views here.
def index(request):
    """
        View function for the index page.

        It gets the first 6 published restaurants from the database and passes them to the template context.
        Additionally, it includes choices for ratings and universities in the context.

        Parameters:
        - request: HttpRequest object representing the request from the user.

        Returns:
        - Renders the index.html template with the provided context.
    """

    restaurants = Restaurant.objects.all().filter(is_published=True)[:6]
    
    context = {
        "restaurants":restaurants,
        "rating_choices" : rating_choices,
        "university_choices": university_choices,
    }
     
    return render(request,"pages/index.html", context)


def about(request):
    return render(request, "pages/about.html")

def map (request):
    '''
        Retrieve the name, latitude, and longitude of all restaurants from the database and stores them in a list.
        Then, it includes this list of restaurant locations in the context and renders the map.html template with the context.
    '''
    restaurant_locations = list(Restaurant.objects.values("name","latitude","longtitude"))
    context = {"restaurant_locations":restaurant_locations}
    return render(request,"pages/map.html",context)

def map_search (request): 
    queryset_restaurant = Restaurant.objects.order_by("-rating")
    
    # Keywords
    if "Keywords" in request.GET:
        Keywords = request.GET["Keywords"]
        if Keywords:
            queryset_restaurant = queryset_restaurant.filter(name__icontains=Keywords)
            
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
