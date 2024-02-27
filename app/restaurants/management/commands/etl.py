import googlemaps
import csv
import pprint
import time
from django.conf import settings
import os

''' ---- How this Extract Load and Transform (ETL) Code Works---
The etl code makes an api request to the google maps to get the restaurants that are in a 
1000m radius of the three universities(Extract). The results from the api call contains a lot
of information. The results is cleaned up by obtaining only the relevant information that will 
be needed in the database (Transform).The clean up data is then stored in an excel sheet automatically. 
The information from the excel sheet is then loaded onto the database. (Load)
the database.

'''

def run_etl ():
    api_key = "AIzaSyABgdLOMdnhVT_rggwcbFMS2yDdfTpf2eY"


    # This connects to the google server with an api key
    gmaps = googlemaps.Client(key=api_key)


    # The coordinates of the three universities alongside the short form of their names are stored in lists
    novaims = [(38.731352, -9.160070), 'IMS']
    ifgi = [(51.969412, 7.595780), 'ifgi']
    uji = [(39.994487, -0.069388), 'UJI']

    universities = [novaims, ifgi, uji]

    # This writes the headings on the first row of the excel sheet
    data_file = os.path.join(settings.BASE_DIR, 'restaurants', 'management', 'commands', 'csv_output', 'restaurant_names.csv')
    with open(data_file, 'w', newline='') as file:
        headings = ['name', 'address', 'place_id', 'ratings', 'opening_time', 'closing_time', 'type_food',
                    'latitude', 'longitude', 'university']
        csv_writer = csv.writer(file)
        horizontal_row = [headings]  # For this code, it does a transpose so that the headings are written horizontal and not vertically
        csv_writer.writerows(horizontal_row)


    # for each university, the restaurants nearby will be obtained
    for uni in universities:
        # this makes an api call to the google server alongside the desired parameters and stores it as places
        places = gmaps.places_nearby(
            type='restaurant',
            location=uni[0],
            radius=1000,
        )
        restaurant_results = places['results']
        print(f"{uni[1]}: {restaurant_results}")


        def write_csv(single_place):
            """
            This functions gets the desired information from the response that is gotten from the api call. It stores
            them as various variables and stores it in a excel sheet. This is the 'transform' part of the code

            Some restaurants did  not have a closing and opening time so they were stored as a null value

            :param single_place: A single restaurant from the full list of restaurants obtained from the api call results

            """
            name = place['name']
            address = place['vicinity']
            place_id = place['place_id']
            # this gets particular information about the restaurant that can be used to get more details
            single_restaurant = gmaps.place(place_id=place_id)
            ratings = place.get('rating', 'no_rating')
            try:
                time_open_str = single_restaurant['result']['current_opening_hours']['periods'][0]['open']['time']
                time_close_str = single_restaurant['result']['current_opening_hours']['periods'][0]['close']['time']
                opening_time = time_open_str[:2] + ':' + time_open_str[2:]
                closing_time = time_close_str[:2] + ':' + time_open_str[2:]
            except KeyError:
                opening_time = 'null'
                closing_time = 'null'
            type_food_list = single_restaurant['result']['types']
            type_food = ', '.join(type_food_list)
            latitude = place['geometry']['location']['lat']
            longitude = place['geometry']['location']['lng']
            university = uni[1]
            is_published = 'true'
            restaurant_info = [name, address, place_id, ratings, opening_time, closing_time, type_food, latitude,
                            longitude, university, is_published]

            with open(data_file, mode='a', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(restaurant_info)

        """
        This get each restaurant in the results obtained from the api call and carries the write_csv function on
        each of the results. This extract the important information from each restaurant and stores it in an excel sheet.
        """
        for place in restaurant_results:
            write_csv(single_place=place)

            next_page_token = places.get('next_page_token')

        """
        Google API by default returns only 20 results. inorder to get more results, it gives a page token which can be
        used to retrieve the next 20 results. this while loops checks if the previous result had a 'next_page_token'
        in the results and then makes an api call if there is a next page token to get additional results. Once there is 
        no additional pages, the results that will be returned won't have the 'next_page_token' key as part of its results.
        """

        while next_page_token:
            time.sleep(2)
            new_page = gmaps.places_nearby(
                type='restaurant',
                location=uni[0],
                radius=1000,
                page_token=next_page_token
            )
            for restaurant in new_page:
                write_csv(single_place=restaurant)

            next_page_token = new_page.get('next_page_token')
            pprint.pprint(f"{uni[1]}: {new_page}")
