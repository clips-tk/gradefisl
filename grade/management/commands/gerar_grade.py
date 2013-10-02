from django.core.management.base import BaseCommand, CommandError
from grade.views import gerar_grade

class Command(BaseCommand):
    args = 'no args can be provided'
    help = 'Generate grids from data dump'

    def handle(self, *args, **options):
        self.stdout.write('Started generating grids.')
        gerar_grade({})
        self.stdout.write('Successfully generated grids.')