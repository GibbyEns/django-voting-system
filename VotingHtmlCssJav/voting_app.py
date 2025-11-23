"""
================================
Accessible Voting & Survey System
Created by: Xolewe, Nongcebo, Wendy, Asemahle
GirlCode Project
================================

A Django-based web application for accessible voting and surveys.

To run:
    python voting_app.py runserver

Then open: http://127.0.0.1:8000/
"""

import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse, FileResponse
from django.urls import path
from django.core.wsgi import get_wsgi_application

# ================================
# Django Settings
# ================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='django-insecure-key-change-in-production',
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
        MIDDLEWARE=['django.middleware.common.CommonMiddleware'],
        INSTALLED_APPS=['django.contrib.staticfiles'],
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR],
        }],
        STATIC_URL='/static/',
        STATICFILES_DIRS=[BASE_DIR],
    )

# ================================
# Views
# ================================
def serve_html(request):
    """Serve the main HTML file"""
    file_path = os.path.join(BASE_DIR, 'index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/html')

def serve_css(request):
    """Serve the CSS file"""
    file_path = os.path.join(BASE_DIR, 'styles.css')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/css')

def serve_js(request):
    """Serve the JavaScript file"""
    file_path = os.path.join(BASE_DIR, 'script.js')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='application/javascript')

# ================================
# URLs
# ================================
urlpatterns = [
    path('', serve_html),
    path('styles.css', serve_css),
    path('script.js', serve_js),
]

# ================================
# WSGI Application
# ================================
application = get_wsgi_application()

# ================================
# Run Server
# ================================
if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append('runserver')
    execute_from_command_line(sys.argv)
