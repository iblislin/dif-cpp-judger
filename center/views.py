from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout as dj_logout
from django.conf import settings

from social.apps.django_app.views import auth


def index(request):
    return render(request, 'center/index.html')

def login(request):
    return auth(request, 'facebook')

def logout(request):
    return dj_logout(request, settings.LOGIN_REDIRECT_URL)
