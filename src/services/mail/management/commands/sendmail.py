from django.conf import settings
from django.core.management.base import BaseCommand

from services.mail import send_templated_email


class Command(BaseCommand):
    help = 'Sends an email to the specified email addresses'

    def add_arguments(self, parser):
        parser.add_argument('emails', nargs='+', type=str)
        parser.add_argument(
            '-t',
            '--template',
            help='Select template to send in the email',
            default='welcome',
            type=str,
            # choices=,  TODO show all available templates
        )

    def handle(self, *args, **options):
        self.stdout.write(f'Using {settings.EMAIL_BACKEND}')
        send_templated_email(
            options['emails'], options['template'], fail_silently=False
        )
        self.stdout.write(self.style.SUCCESS('Email sent!'))
