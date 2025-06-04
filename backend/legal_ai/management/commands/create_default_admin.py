from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create default admin user"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="12345678",
            )
            self.stdout.write(self.style.SUCCESS("Admin user created"))
        else:
            self.stdout.write("Admin user already exists")
