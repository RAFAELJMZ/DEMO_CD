"""
URL configuration for argon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from apps.dashboard import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('bitacora/', views.bitacora, name='bitacora'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/<int:profile_id>', views.edit_profile, name='edit_profile'),
    path('delete_profile/<int:profile_id>', views.delete_profile, name='delete_profile'),
    path('delete_bitacora/<int:bitacora_id>', views.delete_bitacora, name='delete_bitacora'),

    path('export/', views.report, name='report-general'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('close/', views.close, name='close'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)