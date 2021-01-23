"""myblogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from blog.views import home, display, profile, search, post_share, detail, update, delete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', home, name="home"),
    path('blogs/', display, name="posts"),
    path('tag/<slug:tag_slug>/', display, name="posts_by_tag"),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', profile, name="profile"),
    path('search/', search, name='search'),
    path('share/<id>', post_share, name="share"),
    path('blog/', detail, name="detail"),
    path('update/<id>', update, name="update"),
    path('delete/<id>', delete, name="delete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)