from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login_page, name='login_page'),
    #path('login-view/', views.login_view, name='login_view'),
    path('logout/', views.auth_logout, name='logout'),  # Use auth_logout here
    path('account_details/', views.account_details, name='account_details'),
    path('change-password/', views.change_password, name='change_password'),
    path('assistant_edit/<slug:slug>/', views.assistant_edit, name='assistant_edit'),
    path('assistant_list', views.assistant_list, name='assistant_list'),
]
