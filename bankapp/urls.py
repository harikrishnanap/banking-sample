from . import views
from django.urls import path
app_name = 'bankapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('get-branches/<str:district_id>', views.get_branches, name='view branches'),
]