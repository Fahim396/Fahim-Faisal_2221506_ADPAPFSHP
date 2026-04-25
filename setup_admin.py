import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_harvest.settings')
django.setup()

try:
    from accounts.models import User

    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@smartharvest.ai')

    if not User.objects.filter(username=admin_username).exists():
        print(f"Creating superuser: {admin_username}")
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password,
            role='admin',
            first_name='System',
            last_name='Admin'
        )
        print("Superuser created successfully.")
    else:
        print(f"Superuser {admin_username} already exists.")
except Exception as e:
    print(f"Warning: Could not create admin user: {e}")
    traceback.print_exc()
    print("Continuing build anyway...")
