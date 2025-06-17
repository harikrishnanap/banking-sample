from . import views
from django.urls import path

app_name = 'credentials'

urlpatterns = [
    path('register', views.register, name='register'),
    path('application', views.application, name='application'),
    # path('demo_application', views.formApplication, name='demo_application'),
    # path('get_district/', views.get_district, name='get_district'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('get-branches/<int:district_id>/', views.get_branches, name='get_branches'),


]
