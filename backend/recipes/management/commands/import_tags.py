import csv
import os
import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from tags.models import Tag

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
    filemode='w',
)

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data') 


class Command(BaseCommand):
    help = 'Load data from csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='tags.csv', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(
                os.path.join(DATA_ROOT, options['filename']),
                newline='',
                encoding='utf8'
            ) as csv_file:
                data = csv.reader(csv_file)
                for row in data:
                    name, color, slug = row
                    Tag.objects.get_or_create(
                        name=name,
                        color=color,
                        slug=slug
                    )
        except FileNotFoundError:
            raise CommandError('Добавьте файл tags в директорию data')
        logging.info('Successfully loaded all data into database')