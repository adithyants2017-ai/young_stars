from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('join/', views.join_club, name='join'),
    path('events/', views.events_list, name='events'),
    path('gallery/', views.gallery, name='gallery'),
    path('dashboard/', views.member_dashboard, name='member_dashboard'),
    path('manage/', views.manage_content, name='manage_content'),
    path('manage/news/', views.upload_news, name='upload_news'),
    path('manage/gallery/', views.upload_gallery, name='upload_gallery'),
]
