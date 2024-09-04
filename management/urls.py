from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login_page, name='login_page'),
    path('login-view/', views.login_view, name='login_view'),
    path('logout/', views.auth_logout, name='logout'),  # Use auth_logout here
    path('account_details/', views.account_details, name='account_details'),
    path('change-password/', views.change_password, name='change_password'),
    path('assistant_edit/<slug:slug>/', views.assistant_edit, name='assistant_edit'),
    path('assistant_list', views.assistant_list, name='assistant_list'),
    
    path('createAssistant', views.create_assistant, name='create_assistant'),
    path('assistants', views.list_assistants, name='list_assistants'),
    path('assistant/<str:assistant_id>', views.get_assistant, name='get_assistant'),
    path('assistant/<str:assistant_id>', views.update_assistant, name='update_assistant'),
    path('assistant/<str:assistant_id>', views.delete_assistant, name='delete_assistant'),
    
    path('call-listen', views.call_listen, name='call_listen')
]
