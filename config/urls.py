"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # django all-auth
    path('accounts/', include('accounts.urls', namespace='accounts')),  # local app
    path('products/', include('shop.urls', namespace='shop')),  # local app
    path('blog/', include('blog.urls', namespace='blog')),  # local app

    # path('api-auth/', include('rest_framework.urls')),  # drf
    # path('api-token-auth/', views.obtain_auth_token),   # token auth
    path('dj-rest-auth/', include('dj_rest_auth.urls')),   # dj-rest-auth

    path('', include('pages.urls')),  # local app
    path('', include('cart.urls', namespace='cart')),  # local app

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "pages.views.page_not_found_view"
