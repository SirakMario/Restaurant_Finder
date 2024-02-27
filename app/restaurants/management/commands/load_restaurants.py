import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from restaurants.models import Restaurant
import os
from .etl import run_etl



class Command(BaseCommand):
    """
    Management command to load data from a restaurant CSV file into the database.

    Usage:
    python manage.py command_name

    This command loads data from a CSV file containing restaurant information.
    """
    # Call the run_etl function
    run_etl()
    
    # Set help text for the command
    help = 'Load data from restaurant CSV'

    
    def handle(self, *args, **kwargs):
        # Path to the CSV file
        data_file = os.path.join(settings.BASE_DIR, 'restaurants', 'management', 'commands', 'csv_output', 'restaurant_names.csv')
        
        # Columns to gather data from in the CSV
        keys = ("name","address","place_id","ratings","opening_time","closing_time","type_food","latitude","longitude","university")  # the CSV columns we will gather data from.
        
        records = []
        with open(data_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append({k: row[k] for k in keys})

        # extract the latitude and longitude from the Point object
        for record in records: 
            existing_record = Restaurant.objects.filter(name=record["name"]).first()
            
            if existing_record is None:
                # add the data to the database
                Restaurant.objects.update_or_create(
                    name=record["name"],
                    address=record["address"],
                    place_id=record["place_id"],
                    rating = record["ratings"],
                    opening_time= record["opening_time"],
                    closing_time= record["closing_time"],
                    type_food= record["type_food"],
                    latitude= record["latitude"],
                    longtitude= record["longitude"],
                    university= record["university"], )
            else:
                print(f"{record['name']} already exists")
        print ("DONE")
