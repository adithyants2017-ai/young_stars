from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from .models import MembershipRequest
import string
import random

@receiver(post_save, sender=MembershipRequest)
def create_user_for_member(sender, instance, created, **kwargs):
    print(f"DEBUG: MembershipRequest signal triggered for {instance.email}. Status: {instance.status}")
    if instance.status == 'Approved':
        print(f"DEBUG: Status is Approved. Checking for existing user: {instance.email}")
        # Check if user already exists based on email
        if not User.objects.filter(username=instance.email).exists():
            # Use provided password or generate random
            password = instance.password
            print(f"DEBUG: Creating user with password present: {bool(password)}")
            if not password:
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            user = User.objects.create_user(
                username=instance.email,
                email=instance.email,
                password=password,
                first_name=instance.name.split(' ')[0]
            )
            
            # Add to Member group
            group = Group.objects.get(name='Member')
            user.groups.add(group)
            
            print(f"DEBUG: User successfully created for {instance.email}")
        else:
            print(f"DEBUG: User already exists for {instance.email}")
            # In production, send this via email:
            # send_mail(
            #     'Welcome to Young Stars Club',
            #     f'Your membership is approved. Login with Username: {instance.email} Password: {password}',
            #     'admin@youngstars.com',
            #     [instance.email],
            #     fail_silently=False,
            # )
