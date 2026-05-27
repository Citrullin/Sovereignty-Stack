import os
import sys
import django

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')
django.setup()

from organization.models import Organization
from django.contrib.auth import get_user_model

User = get_user_model()

if not Organization.objects.exists():
    Organization.objects.create(name='Homelab')
    print("Created Organization: Homelab")
else:
    print("Organization already exists.")

if not User.objects.filter(email='admin@homelab.local').exists():
    user = User.objects.create(email='admin@homelab.local', organization=Organization.objects.first(), is_staff=True, is_superuser=True)
    user.set_password('chiefonboardingpassword')
    user.save()
    print("Created Superuser: admin@homelab.local")
else:
    print("Superuser admin@homelab.local already exists.")

akadmin, created = User.objects.get_or_create(email='akadmin@homelab.local', defaults={'organization': Organization.objects.first(), 'is_staff': True, 'is_superuser': True})
if not created and not akadmin.is_superuser:
    akadmin.is_superuser = True
    akadmin.is_staff = True
    akadmin.save()
    print("Updated akadmin@homelab.local to Superuser.")
elif created:
    akadmin.set_password('chiefonboardingpassword')
    akadmin.save()
    print("Created Superuser: akadmin@homelab.local")


