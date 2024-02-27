from django.urls import path
from . import views

"""         
- The path 'login' maps to the login view function defined in views.py and is named 'login'.
- The path 'register' maps to the register view function defined in views.py and is named 'register'.
- The path 'logout' maps to the logout view function defined in views.py and is named 'logout'. 
"""

urlpatterns = [
    path ("login",views.login, name="login"),
    path ("register",views.register,name="register"),
    path ("logout",views.logout,name="logout"),
]