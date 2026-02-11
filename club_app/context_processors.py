from .models import ClubSettings

def club_info(request):
    try:
        return {'club_settings': ClubSettings.objects.first()}
    except:
        return {}
