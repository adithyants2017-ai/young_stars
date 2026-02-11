from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import News, MembershipRequest

class ClubAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create User
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create Admin
        self.admin = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')
        
    def test_news_model(self):
        news = News.objects.create(title="Test News", content="Content", author=self.user)
        self.assertEqual(str(news), "Test News")
        self.assertEqual(News.objects.count(), 1)

    def test_membership_request_encryption(self):
        aadhaar = "123412341234"
        req = MembershipRequest(
            name="Applicant",
            mobile="9876543210",
            email="app@test.com",
            blood_group="B+",
            skill="Dancing"
        )
        req.set_aadhaar(aadhaar)
        req.save()
        
        # Verify encryption in DB (should not be plain text)
        req.refresh_from_db()
        self.assertNotEqual(req.aadhaar_encrypted, aadhaar)
        
        # Verify decryption
        self.assertEqual(req.get_aadhaar(), aadhaar)

    def test_public_views(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_join_form_submission(self):
        data = {
            'name': 'New Member',
            'mobile': '9876543210',
            'email': 'new@test.com',
            'aadhaar_number': '123412341234',
            'blood_group': 'A+',
            'skill': 'Singing'
        }
        response = self.client.post(reverse('join'), data)
        # Should redirect to home on success
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(MembershipRequest.objects.count(), 1)
        
        # Verify saved data
        req = MembershipRequest.objects.first()
        self.assertEqual(req.name, 'New Member')
        self.assertEqual(req.get_aadhaar(), '123412341234')

    def test_admin_access(self):
        self.client.login(username='admin', password='password')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
