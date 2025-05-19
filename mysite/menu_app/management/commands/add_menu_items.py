from django.core.management.base import BaseCommand, CommandError
from menu_app.models import MenuItem

class Command(BaseCommand):
    help = 'Adds some initial menu items to the database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding menu items...'))

        # Delete existing menu items for 'main_menu' to avoid duplicates
        MenuItem.objects.filter(menu_name='main_menu').delete()

        # Create parent menu items
        home = MenuItem.objects.create(menu_name='main_menu', title='Home', url='/')
        about = MenuItem.objects.create(menu_name='main_menu', title='About Us', url='/about/')
        services = MenuItem.objects.create(menu_name='main_menu', title='Services', url='/services/')

        # Create child menu items
        web_development = MenuItem.objects.create(
            menu_name='main_menu',
            title='Web Development',
            url='/services/web/',
            parent=services
        )
        mobile_development = MenuItem.objects.create(
            menu_name='main_menu',
            title='Mobile Development',
            url='/services/mobile/',
            parent=services
        )
        contact = MenuItem.objects.create(
            menu_name='main_menu',
            title='Contact',
            url='/contact/'
        )

        self.stdout.write(self.style.SUCCESS("Successfully added menu items for 'main_menu'."))