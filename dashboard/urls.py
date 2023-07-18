from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard,name='home'),
    path('login',views._login,name='login'),
    path('logout',views._logout,name='logout'),
    path('register',views.register,name='register'),
    path('leads',views.leads,name='leads'),
    path('create_lead',views.create_lead,name='create_lead'),
    path('add_user',views.create_staff_user,name='create_staff_user'),
]
