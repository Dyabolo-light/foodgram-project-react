import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient

OUR_DATABASE = {
    Ingredient: 'ingredients.csv',
}


class Command(BaseCommand):
    help = 'Загружает список ингредиентов из CSV файлов'

    def handle(self, *args, **options):
        for model, base in OUR_DATABASE.items():
            path = f'{settings.BASE_DIR}/data/{base}'
            with open(path, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)
            self.stdout.write(
                self.style.SUCCESS(f'Модель {model.__name__} загружена')
            )
