import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a superuser automatically from environment variables'

    def handle(self, *args, **options):
        self.stdout.write('DEBUG_ADMIN: --- InitAdmin Command Started ---')
        try:
            username = os.environ.get('ADMIN_USERNAME', '').strip()
            password = os.environ.get('ADMIN_PASSWORD', '').strip()
            email = os.environ.get('ADMIN_EMAIL', 'admin@example.com').strip()

            self.stdout.write(f'DEBUG_ADMIN: Configured Username: "{username}"')
            self.stdout.write(f'DEBUG_ADMIN: Password set? {"YES" if password else "NO"}')

            if not username or not password:
                self.stdout.write(self.style.WARNING(
                    f'DEBUG_ADMIN: ABORTED. Mandatory variables missing.'
                ))
                return

            self.stdout.write('DEBUG_ADMIN: Checking database connection...')
            user_count = User.objects.count()
            self.stdout.write(f'DEBUG_ADMIN: Database connected. Current user count: {user_count}')

            if User.objects.filter(username=username).exists():
                u = User.objects.get(username=username)
                u.set_password(password)
                u.is_superuser = True
                u.is_staff = True
                u.save()
                self.stdout.write(self.style.SUCCESS(f'DEBUG_ADMIN: SUCCESS. Refreshed password for "{username}".'))
            else:
                self.stdout.write(f'DEBUG_ADMIN: Creating new superuser "{username}"...')
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'DEBUG_ADMIN: SUCCESS. Created new superuser "{username}".'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'DEBUG_ADMIN: FATAL ERROR: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write('DEBUG_ADMIN: --- InitAdmin Command Finished ---')
