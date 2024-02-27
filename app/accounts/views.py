from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
# Create your views here.
    
def register (request):
    """
        View function for user registration.

        It checks if the request method is POST. If so, it retrieves form values such as first name, last name, username, email, and passwords.
        It checks if the passwords match and if the username or email is already taken. If everything is valid, it creates a new user,
        saves it to the database, displays a success message, and redirects the user to the login page.

        If the passwords don't match or if the username/email is already taken, it displays an error message and redirects the user back to the registration page.

        If the request method is not POST, it renders the registration page for the user to input registration information.
    """

    if request.method == "POST":
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request,"That username is taken")
                return redirect ("register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,"That email is being used")
                    return redirect ("register")
                else:
                    # Everything looks good
                    user = User.objects.create_user(username=username, password=password, email=email,first_name=first_name,last_name=last_name)                    
                    user.save()
                    # email confirmation
                    template = render_to_string('partials/email_template.html',{'name':username})
                    email = EmailMessage (
                        "Thank you for accessing our website",
                        template,
                        settings.EMAIL_HOST_USER,
                        [email],
                        )
                    email.fail_silently=False
                    email.send()
                    messages.success(request,"You are now registered")
                    return redirect ("login")
        else:
            messages.error(request,"Passwords do not match")
            return redirect ("register")
    else:
        return render (request,"accounts/register.html")

def login (request):
    """
        View function for user login.

        It checks if the request method is POST, retrieves the username and password from the form data,
        try to authenticate the user using Django's authentication system, logs in the user if authentication is successful,
        displays a success message using Django's messages framework, and redirects the user to the index page.
        If authentication fails, it displays an error message and redirects the user back to the login page.

        If the request method is not POST, it renders the login page for the user to input credentials.
    """

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request,"You are now logged in")
            return redirect ("index")
        else:
            messages.error(request, "Invalid credentials")
            return redirect ("login")
    else:
        return render (request,"accounts/login.html")
    
def logout (request):
    """
        View function for user logout.

        It checks if the request method is POST, logs out the user using Django's authentication system,
        displays a success message using Django's messages framework, and redirects the user to the index page.
    """
    if request.method == "POST":
        auth.logout (request)
        messages.success(request, "You are now logged out")
        return redirect ("index")