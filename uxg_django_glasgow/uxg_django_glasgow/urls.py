"""uxg_django_glasgow URL Configuration

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
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import include
from uxg import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("", views.index, name="index"),
    path('uxg/', include('uxg.urls')),
    path('admin/', admin.site.urls),
    path('signup/', views.register, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='uxg/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='uxg/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('api/communities/', views.community_list, name='community-list'),
    path('api/communities/<int:community_id>/', views.community_detail, name='community-detail'),
    path('communities/', views.community_page, name='community-page'),
    path('communities/<int:community_id>/', views.community_detail_page, name='community-detail-page'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
