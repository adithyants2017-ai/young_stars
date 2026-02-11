
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'club_project.settings')
django.setup()

from django.contrib.auth.models import User
from club_app.models import MembershipRequest

def verify_system():
    print("--- 1. Checking Users ---")
    admin = User.objects.filter(username='admin').first()
    president = User.objects.filter(username='president').first()
    print(f"Admin exists: {admin is not None}")
    print(f"President exists: {president is not None}")
    
    if president:
        print(f"President is staff: {president.is_staff}")
        print(f"President has 'change_membershiprequest' permission: {president.has_perm('club_app.change_membershiprequest')}")

    print("\n--- 2. verifying Aadhaar Encryption ---")
    req = MembershipRequest(
        name="Test User",
        mobile="1234567890",
        email="test@example.com",
        blood_group="O+",
        skill="Architecture"
    )
    original_aadhaar = "123412341234"
    req.set_aadhaar(original_aadhaar)
    req.save()
    
    # Reload from DB
    loaded_req = MembershipRequest.objects.get(id=req.id)
    print(f"Encrypted in DB: {loaded_req.aadhaar_encrypted}")
    print(f"Is Encrypted != Original: {loaded_req.aadhaar_encrypted != original_aadhaar}")
    
    decrypted = loaded_req.get_aadhaar()
    print(f"Decrypted: {decrypted}")
    print(f"Decryption successful: {decrypted == original_aadhaar}")
    
    # Cleanup
    loaded_req.delete()
    print("\nVerification Complete.")

if __name__ == '__main__':
    verify_system()
