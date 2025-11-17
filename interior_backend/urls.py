"""interior_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/blog/', include('apps.blog.urls')),
    path('api/cms/', include('apps.cms.urls')),
    path('api/company/', include('apps.company.urls')),
    path('api/contact/', include('apps.contact.urls')),
    path('api/ecommerce/', include('apps.ecommerce.urls')),
    path('api/estimation/', include('apps.estimation.urls')),
    path('api/projects/', include('apps.projects.urls')),
    path('api/', include('apps.api.urls')),
]
