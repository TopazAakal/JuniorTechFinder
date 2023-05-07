"""JuniorTechFinder URL Configuration

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
from django.urls import path
import Core.views
import Juniors.views
import Recruiters.views
import Authentication.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Core.views.homePage, name='home'),
    path('aboutUs/', Core.views.aboutUsPage, name='aboutUs'),
    path('siteRules/', Core.views.siteRulesPage, name='siteRules'),
    path('contactUs/', Core.views.contactUsPage, name='contactUs'),
    path('createProfile/', Juniors.views.createProfile, name='createProfile'),
    path('showProfile/<int:pk>', Juniors.views.showProfile, name='showProfile'),
    path('checkProfile/', Juniors.views.checkProfile, name='checkProfile'),
    path('editProfile/<int:pk>', Juniors.views.editProfile, name='editProfile'),
    path('showProfileRecruiter/<int:pk>',
         Recruiters.views.showProfileRecruiter, name='showProfileRecruiter'),
    path('editProfileRecruiter/<int:pk>',
         Recruiters.views.editProfileRecruiter, name='editProfileRecruiter'),
    path('createProfileRecruiters/', Recruiters.views.createProfileRecruiters,
         name='createProfileRecruiters'),
    # path('checkProfileUser/', Authentication.views.checkProfileUser,
    # name='checkProfileUser'),
    path('checkProf/', Recruiters.views.checkProf, name='checkProf'),
    path('jobs/', Recruiters.views.jobList, name='jobList'),
    path('postJob/', Recruiters.views.postJob, name='postJob'),
    path('deleteJob/<int:job_id>/', Recruiters.views.deleteJob, name='deleteJob'),
    path('jobs/<int:job_id>/', Recruiters.views.jobDetail, name='jobDetail'),
    path('login/', Authentication.views.login_view, name='login'),
    path('signup/', Authentication.views.signup_view, name='signup'),
    path('logout/', Authentication.views.logout_view, name='logout'),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
