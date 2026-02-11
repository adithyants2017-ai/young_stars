
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'club_project.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from club_app.models import MembershipRequest, ClubSettings

def init_db():
    # Seed Club Settings
    club_settings, created = ClubSettings.objects.get_or_create(id=1)
    club_settings.instagram_url = "https://www.instagram.com/_young__stars?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
    club_settings.phone_number = "9061601870"
    club_settings.save()
    print("Club Settings updated with Social and Contact info.")

    # Create Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        print("Superuser 'admin' created.")
    else:
        print("Superuser 'admin' already exists.")

    # Create Groups
    president_group, created = Group.objects.get_or_create(name='President')
    member_group, created = Group.objects.get_or_create(name='Member')
    contributor_group, created = Group.objects.get_or_create(name='Contributor')
    
    # Assign Permissions to President
    mr_ct = ContentType.objects.get_for_model(MembershipRequest)
    change_mr = Permission.objects.get(codename='change_membershiprequest', content_type=mr_ct)
    president_group.permissions.add(change_mr)

    # Assign Permissions to Contributor
    from club_app.models import News, GalleryImage
    news_ct = ContentType.objects.get_for_model(News)
    gallery_ct = ContentType.objects.get_for_model(GalleryImage)
    
    perms = [
        Permission.objects.get(codename='add_news', content_type=news_ct),
        Permission.objects.get(codename='change_news', content_type=news_ct),
        Permission.objects.get(codename='add_galleryimage', content_type=gallery_ct),
        Permission.objects.get(codename='change_galleryimage', content_type=gallery_ct),
    ]
    for perm in perms:
        contributor_group.permissions.add(perm)

    print("Groups and permissions configured.")

    # Create Sample President User
    if not User.objects.filter(username='president').exists():
        president = User.objects.create_user('president', 'president@example.com', 'presidentpass')
        president.is_staff = True  # Required to access Admin
        president.save()
        president.groups.add(president_group)
        print("User 'president' created with staff access.")
    else:
        print("User 'president' already exists.")

    # Create Sample Member User
    if not User.objects.filter(username='member').exists():
        member = User.objects.create_user('member', 'member@example.com', 'memberpass')
        member.groups.add(member_group)
        print("User 'member' created.")
    else:
        print("User 'member' already exists.")

    # Create Sample Contributor User
    if not User.objects.filter(username='editor').exists():
        editor = User.objects.create_user('editor', 'editor@example.com', 'editorpass')
        editor.is_staff = True  # Added so they can log into /admin/
        editor.save()
        editor.groups.add(contributor_group)
        print("User 'editor' created with staff access.")
    else:
        # Also ensure existing editor gets staff access
        editor = User.objects.get(username='editor')
        if not editor.is_staff:
            editor.is_staff = True
            editor.save()
            print("Updated existing 'editor' with staff access.")
        print("User 'editor' already exists.")

if __name__ == '__main__':
    init_db()
