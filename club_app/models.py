from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os
import base64

# Generate a key if not exists (In production, this should be in env vars)
# For this demo, we'll use a hardcoded key or generate one if missing
# ideally load from os.environ.get('ENCRYPTION_KEY')
# For simplicity in this run, we'll mock the key retrieval

def get_cipher_suite():
    key = os.environ.get('ENCRYPTION_KEY')
    if not key:
        # Fallback for demo purposes - DO NOT USE IN PRODUCTION
        key = Fernet.generate_key()
    return Fernet(key)

class News(models.Model):
    TYPE_CHOICES = [
        ('Update', 'Update'),
        ('Charity', 'Charity'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Update')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

class MembershipRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    aadhaar_encrypted = models.TextField(help_text="Encrypted Aadhaar Number") 
    blood_group = models.CharField(max_length=5)
    skill = models.TextField()
    password = models.CharField(max_length=128, blank=True, null=True, help_text="Stored password for user creation upon approval")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def set_aadhaar(self, aadhaar_number):
        if not aadhaar_number:
            return
        key = self._get_or_create_key()
        f = Fernet(key)
        self.aadhaar_encrypted = f.encrypt(aadhaar_number.encode()).decode()

    def get_aadhaar(self):
        if not self.aadhaar_encrypted:
            return None
        key = self._get_or_create_key()
        f = Fernet(key)
        try:
            return f.decrypt(self.aadhaar_encrypted.encode()).decode()
        except:
            return "Error Decrypting"

    def _get_or_create_key(self):
        key_path = 'secret.key'
        if os.path.exists(key_path):
            with open(key_path, 'rb') as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(key)
            return key

    def __str__(self):
        return f"{self.name} - {self.status}"

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('Sports', 'Sports'),
        ('Arts', 'Arts'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Sports')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class GalleryImage(models.Model):
    caption = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='gallery/')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize logic: Max width 800px, preserve aspect ratio
            max_width = 800
            if img.width > max_width:
                output_size = (max_width, int(img.height * (max_width / img.width)))
                img = img.resize(output_size, Image.Resampling.LANCZOS)
                
                # Save back to memory
                buffer = BytesIO()
                img.save(buffer, format='JPEG', quality=85)
                val = buffer.getvalue()
                
                # Update the image field with the compressed content
                self.image.save(self.image.name, ContentFile(val), save=False)
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.caption or "Gallery Image"

class ClubSettings(models.Model):
    logo = models.ImageField(upload_to='assets/', blank=True, null=True)
    club_name = models.CharField(max_length=100, default="Young Stars")
    instagram_url = models.URLField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Club Settings"

    def __str__(self):
        return self.club_name
