"""visualization URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from . import visualizertest
#from . import visualizer
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^visualizertest/', visualizertest.main)
]

urlpatterns += [
    path('visualizer/', include('visualizer.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/visualizer/')),
]

urlpatterns += [
    path('add/', include('addLineItem.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/add/')),
]

urlpatterns += [
    path('addFormSubs/', include('addLineItem.urls')),
]

urlpatterns += [
    path('add/saveLineItem/', include('addLineItem.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/saveLineItem/')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/addFormSubs/')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)