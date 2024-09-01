from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login_page, name='login_page'),
    #path('login-view/', views.login_view, name='login_view'),
    path('logout/', views.auth_logout, name='logout'),  # Use auth_logout here
    path('protected/', views.protected_view, name='protected_view'),
    path('change-password/', views.change_password, name='change_password')
]
