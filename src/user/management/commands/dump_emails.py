import sys
from user.models import FruitUser

from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-o', '--output', type=str, help='Redirect output to a file.')
        parser.add_argument('--sendy', action='store_true', help='Format output as CSV for Sendy to import.')

    def handle(self, *args, **options):
        filename = options['output']
        if filename:
            out = open(filename, 'w+')
        else:
            out = sys.stdout
        try:
            row = ',{u.email}\n' if options['sendy'] else '{u.email}\n'
            for user in FruitUser.objects.active().iterator():
                out.write(row.format(u=user))

        finally:
            if filename:
                out.close()
            else:
                out.flush()
