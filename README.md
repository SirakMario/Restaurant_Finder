# restaurante-finder-final-app

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Django Version](https://img.shields.io/badge/django-5.0.1-green.svg)](https://www.djangoproject.com/download/)

GeoTech group programming course repo

Developers:
- Sirak Asfaha
- Joseph Paintsil
- Guilherme Viegas

## About the App

Resturante locator is a website created to help Geospatial Technology students locate a suitable restaurant near the campus. It allows users to filter by certain preferences and also allows users to comment on their experience in a restaurant they visited. Users also have an additional feature where they can use the website to get directions to a chosen restaurant. Restaurants close to Nova Information Management School (NOVA IMS) Lisbon, University of Münster, Institute for Geoinformatics (ifgi), and Universitat Jaume I (UJI) were considered for the app since these are the partner universities for the Geospatial Technologies program.

### Functionality of the Website

The entire process of the website can be divided into three main components, namely:
1. Extract, Transform, and Load.
2. Utilizing APIs with the Django framework to make and receive API calls.
3. Create, Read, Update, and Delete.
4. Docker

#### 1. Extract, Transform, and Load

Google Places API was used to retrieve restaurants within a distance of 1000 meters from both NOVA IMS and ifgi schools. The API call returned a JSON with restaurants that met these requirements, alongside various information about them. The relevant information was extracted from the JSON results and stored in an Excel file (Transform). Django was then utilized to retrieve information from the Excel sheet and transfer it into the PostgreSQL database (Load).

#### 2. Utilizing APIs with the Django framework to make and receive API calls

To prevent users from getting direct access to the database, APIs were used as an intermediary between the user and the database. The Django framework was utilized in achieving this. API calls were made when the user navigated from one page to another, as well as when they made, edited, and deleted comments. This improved the security of the database and prevented the database from being infiltrated.

#### 3. Create Read Update and Delete

A comment section was created under each restaurant. Users can CREATE comments, READ other users' comments, UPDATE their comments by making edits to them, as well as DELETE their comments.

#### 4. Docker

The various parts of the website were put in a Docker container, and then the service was run on a remote server to make the website accessible through an IP address.

### Additional Functions

Open Streets Map and Leaflet Js were used to create a map where users could navigate from their current location to a selected restaurant. The user has the option of getting directions to a selected restaurant. A route is established on the map and dynamically adjusts as the user progresses. The routing feature provides guidance to the user throughout the journey until reaching the final destination.

## The Website

![website pciture](https://github.com/geotech-programming-project/restaurante-finder-final/blob/main/website.png)

The website is made up of different pages. The pages are as follows:

- Home
- About
- Map
- Restaurants
- Register (If the user is not logged in)
- Login (If the user is not logged in)
- Logout Button (If the user is logged in)

### Home

The main page is the home page. The home page initially displays a few top highly-rated restaurants. The user additionally has the choice to select the university they want to explore for nearby restaurants, along with specifying the rating of the restaurants they wish to view. The restaurants that meet the requirements are displayed when the user clicks on the submit form button.

These restaurants are obtained from the database, which contains the restaurants that were obtained from the Google API and the ones that were added by the admin. The addition of restaurants by the admin would be explained further in this README. The user can filter the restaurants that are being displayed by searching by the restaurant name. The other parts of the website just give additional information on what the user can do with the app, such as leaving a review, finding a restaurant near them, and requesting the addition of a new restaurant.

### About

This page gives a brief overview of what the website is about. It also shows the people who developed the website, namely, Joseph, Guilherme, and Sirak, alongside their respective email accounts. This will allow the user to contact any of the developers if they experience a problem with the website or want to add their restaurant to the website. There is also a button named "View Restaurants" which users can use to go to the "Restaurants" page directly.

### Map

This page shows a map that was created with leaflet. The default base map is Open Street Map. The user can use the layer control icon on the top right to change the base map to Satellite Map, Google Street Map, or Hybrid (which combines the satellite map and the Google street map). The user can utilize the dropdown button located below the layer control to determine which university they wish to observe regarding restaurants around the school they intend to locate.

When the user selects a university from the drop-down list, the map is zoomed to that particular university, and the university can be seen with a green marker while the restaurants near the university are displayed with a green marker. The location of the user is displayed with a blue circle. Additionally, the user can click on a restaurant icon to display the name of the restaurant. This is to give the user an idea of the...

### Restaurants

This page lets users see all the restaurants in our database without any limits. Users can explore freely without needing to set any rules or conditions. It's like opening a door to a world of different places to eat.

### Register

This button is used for registering new users on the platform. Users must provide their name, username, email, and password to register. An email is automatically sent to the user after they register to welcome them to the platform.

### Login

A user who has already been registered on the platform can log in with his username and password.

### Logout

A user who is logged in can log out of the website using the logout button.

### Website Functionality

- **Filtering:** The user gets to filter the restaurants by their name, the university they are located at, or the ratings of the restaurants. More filters will be added in the second release of the website.

- **Navigation:** Upon selecting a restaurant of interest, users are redirected to another page featuring a map interface. On this page, a routing path is displayed, guiding users from their current location to the selected restaurant. This interactive map enhances user experience by providing clear directions to the desired destination.

- **Commenting:** Users can comment on the restaurant they have been to. They can also update the comments they have posted about the restaurant. Additionally, they can delete the comment they have posted. This gives the restaurants a Create, Read, Update, and Delete functionality.

## How the website runs

### Django Model

This project leverages Django, a high-level Python web framework, in conjunction with PostgreSQL. The Django configurations can be set for the website to run on a local computer or on a django websever. The Django will be explained in a bit more details in this section.


#  Project Structure
![folder_structure](https://github.com/geotech-programming-project/restaurante-finder-final/blob/main/file_structure.png)
The project folder consists of folders and python scripts that are required for the functionality of the website. The function of each folder is explained below. vital scripts in certain folders are also explained underneath their parent folders below.

- **accounts:**
  
These accounts handles the registeration, logging in and loggin out of users.

- **media:**
  
When the admin adds a picture to a restaurant or edit a restaurant's picture, the picture he uploads is stored here.

- **pages:**
  
This contains the views.py which has functions that displays restaurants on the home page and also has function for searching and filtering results. It also has a url.py which is responsible for redirecting of urls. The other python files are django configurations.

- **restaurant_app:**
  
The main website folder is called 'restaurant_app'. This folder contains the configurations for the projects. In the settings.py, the django configurations needed for the website such as the base directory, the folder where the static html files will be placed and much more can be found here.

*  urls.py
  
This is a python file found in the restaurant_app folder.This is responsible for running the urls. when the user accesses a certain url, the functions in this python file redirects the request to another python script depending on the url that is being accessed. If the script that the user is being directed to is another url.py, then that code will also redirect the user to another script untill it's finally redirected to a script that will render and html page which will be displayed on the website. The other files found inside this folder are related to django functioanlity and settings

- **restaurants:**

* migrations
  
This folder has scripts that creates tables in the postgres database. when this script is run, the tables and columns in the script will be created in the postgres.'python manage.py makemigrations' and then 'python manage.py migrate' commands are used to create the table.

* urls.py
  
This script redirects the user to a python script or python function in a script based on the url request that is being made.

*  admin.py
  
Django creates an inbuilt administator page where the administator of the websites can edit infomation from that page. The admin needs to login with his credenials and he will be able to manage information from this page. The admin.py in this folder and other folders is responsible for adding additional information on the admin page.

* apps.py
  
This was created by default by django

* forms.py
  
This python file has the comment form that is rendered when the user needs to make a comment on a restaurant.

*choices.py

It has the choices the user has to select on various part of the website.

- **static:**

This contains the html and css files that are used on the website.

- **templates:**

Contains part of the html and css files that are used on the website

- **manage.py:**

This is the main script that is run by the 'python manage.py runserver' in the terminal. This generates an local IP address in the terminal that will be used to run the website.



# How to run the website with Django

- **Python Packages used:**
In order to run the website from the code, make sure you have these python packages installed:
- Django 5.0.1
- psycopg2 2.9.9
- pillow 10.2.0
- googlemaps 4.10.0
- requests 2.31.0

- **Ensure that you have the proper database configuration as specified in the 'settings.py' file under the 'restaurant_app' module.:**
  
  ![configurations](https://github.com/geotech-programming-project/restaurante-finder-final/blob/main/configuration_picture.png)
  
- **Migration Generation:**
run the code **'python manage.py makemigrations'** and then **'python manage.py migrate'** in the terminal.This will create the necessary tables in postgres. Ensure that your current directory is the main folder.

- **ETL Execution (Extract, Transform, Load):**

In order to retrieve the information from the google maps API onto the postgres database, you need to run the command **'python manage.py load_restaurants'**

- **Launching the Server:**
 
To run the website, you need to run the command **'python manage.py runserver'**


### Docker Containers

The Django application itself was served on the top of Docker containers, which enable the architecture to be designed in microservices. Therefore we got 2 containers (services): The Django app and the PostgreSQL database.

### Azure Virtual Machine

To host the application in the World Wide Web, the authors made use of a Azure Virtual Machine (VM), which functions as a Server for us in this project. The specific configuration of the Server as set through a terraform file (IaC).


![website pciture](https://github.com/geotech-programming-project/restaurante-finder-final/blob/main/restaurante_app_tech_diagram.png)

in order to make the application available online, a few commands must be run sequentially:

### From within an azure shell, terraform may be used to spin up Azure cloud resources in a Infrastructure as Code (IaC) manner.
#### `terraform init`

### Then a terraform script (azure_vm.tf) may guide the creation of the cloud reseurces we need
#### `terraform apply`

### Get into the Azure Virtual Machine
#### `ssh useradmin@<public_ip>`

### Build the docker-compose application
#### `docker-compose up --build`

