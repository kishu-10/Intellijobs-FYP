import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from users.abstract import District, Province


class Command(BaseCommand):
    help = 'create countries to the database table from csv file'

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, 'fixtures/country.csv'), 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip first line
            for row in reader:
                province = Province.objects.get(province_code=row[1]) 
                district, created = District.objects.get_or_create(
                    name=row[0],
                    province=province.id,
                )
