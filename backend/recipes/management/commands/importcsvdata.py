import csv
import logging

from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredient

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
    filemode='w',
    encoding='utf-8'
)

CSV_PATH = '../data/ingredients.csv'


class Command(BaseCommand):
    help = 'Load data from csv file into the database'

    def handle(self, *args, **kwargs):
        try:
            with open(
                CSV_PATH,
                newline='',
                encoding='utf8'
            ) as csv_file:
                fieldnames = ['name', 'measurement_unit']
                reader = csv.DictReader(csv_file, fieldnames=fieldnames)
                Ingredient.objects.bulk_create(
                                Ingredient(**data) for data in reader
                )
        except Exception as error:
            CommandError(error)
        logging.info('Successfully loaded all data into database')
