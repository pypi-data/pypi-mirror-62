"""dj18 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django.contrib.auth.views

from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

from pwdtk.testviews import home
from pwdtk.testviews import logout_view
from pwdtk.testviews import protected
from pwdtk.views import password_change


urlpatterns = [
    url(r'^$', home, name='pwdtk_test_home'),
    url(r'^login', django.contrib.auth.views.login,
        name='pwdtk_test_login'),
    url(r'^logout', logout_view,
        name='pwdtk_test_logout'),
    url(r'^protected', protected,
        name='pwdtk_test_protected'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ch_passwd/', password_change, name='password_change'),
    # url('^ch_passwd/$', 'django.contrib.auth.views.password_change',
    #     {'post_change_redirect': 'next_page'}, name='password_change'),
    # url('^ch_passwd/$', 'django.contrib.auth.views.password_change',
    #     name='password_change'),
    url('^pwd_change_done$', home,
        name='password_change_done'),
]
