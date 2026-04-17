import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a superuser automatically from environment variables'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', '').strip()
        password = os.environ.get('ADMIN_PASSWORD', '').strip()
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com').strip()

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                f'INIT_ADMIN: Skipped. ADMIN_USERNAME="{username}" or password was missing.'
            ))
            return

        self.stdout.write(f'INIT_ADMIN: Attempting to ensure superuser "{username}" exists...')

        if User.objects.filter(username=username).exists():
            u = User.objects.get(username=username)
            u.set_password(password)
            u.is_superuser = True
            u.is_staff = True
            u.save()
            self.stdout.write(self.style.SUCCESS(f'INIT_ADMIN: SUCCESS. User "{username}" already existed, password has been refreshed.'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'INIT_ADMIN: SUCCESS. New superuser "{username}" has been created.'))
