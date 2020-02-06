"""tsechack URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from adminusers import views as adminusers_views
from dashboard import views as dashboard_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='adminusers/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='adminusers/logout.html'), name='logout'),
    path('register/', adminusers_views.register, name="register"),
    path('dashboard/', dashboard_views.dashboard, name="dashboard"),
    path('interest/', dashboard_views.interest, name="interest"),
    path('dashboard/shortlist', dashboard_views.shortlist, name="shortlist"),
    path('dashboard/phone_interview', dashboard_views.phone_interview, name="phone-interview"),
    path('dashboard/phone_interview/<str:pk>', dashboard_views.phone_interview_detail, name="phone-interview-detail"),
    path('induction/<str:pk>', dashboard_views.induction, name="induction-email"),
    path('dashboard/shortlist/email', dashboard_views.shortlist_email, name="shortlist-email"),
    path('dashboard/<str:pk>', dashboard_views.detailview, name="detail"),
    path('experience/', dashboard_views.experience, name="experience"),
    path('experience/post', dashboard_views.form2_post, name="form2-post"),
    path('interview/<str:pk>', dashboard_views.interview_timing, name="interview-timing"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
