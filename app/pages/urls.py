from django.urls import path
from . import views

"""
    - The empty path ('') maps to the `index` view function with the name 'index'.
    - The path 'about' maps to the `about` view function with the name 'about'.
    - The path 'map' maps to the `map` view function with the name 'map'.
"""
urlpatterns = [
    path ("",views.index, name="index"),
    path ("about",views.about,name="about"),
    path("map",views.map,name="map"),
]