from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        allowed_paths = [reverse('login_page'), reverse('logout')]
        if not request.user.is_authenticated and request.path_info not in allowed_paths:
            return redirect('login_page')
        return self.get_response(request)