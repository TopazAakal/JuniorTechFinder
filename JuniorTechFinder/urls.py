
from django.contrib import admin
from django.urls import path
import Core.views
import Juniors.views
import Recruiters.views
import Authentication.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Core
    path('', Core.views.homePage, name='home'),
    path('aboutUs/', Core.views.aboutUsPage, name='aboutUs'),
    path('siteRules/', Core.views.siteRulesPage, name='siteRules'),
    path('contactUs/', Core.views.contactUsPage, name='contactUs'),
    # Juniors
    path('createProfile/', Juniors.views.createProfile, name='createProfile'),
    path('showProfile/<int:pk>', Juniors.views.showProfile, name='showProfile'),
    path('checkProfile/', Juniors.views.checkProfile, name='checkProfile'),
    path('editProfile/<int:pk>', Juniors.views.editProfile, name='editProfile'),
    path('juniorList/', Juniors.views.juniorList, name='juniorList'),
    path('suggestions/', Juniors.views.suggestions, name='suggestions'),
    path('generate_new_suggestions/', Juniors.views.generate_new_suggestions,
         name='generate_new_suggestions'),
    path('apply/<int:job_id>/', Recruiters.views.apply_job, name='apply_job'),
    # Recruiters
    path('submit_interest/<int:job_id>/', Recruiters.views.submit_interest, name='submit_interest'),
    path('view_applicants/<int:job_id>/', Recruiters.views.view_applicants, name='view_applicants'),
    path('showProfileRecruiter/<int:pk>',
         Recruiters.views.showProfileRecruiter, name='showProfileRecruiter'),
    path('editProfileRecruiter/<int:pk>',
         Recruiters.views.editProfileRecruiter, name='editProfileRecruiter'),
    path('createProfileRecruiters/', Recruiters.views.createProfileRecruiters,
         name='createProfileRecruiters'),
    path('checkProf/', Recruiters.views.checkProf, name='checkProf'),
    path('jobs/', Recruiters.views.jobList, name='jobList'),
    path('postJob/', Recruiters.views.postJob, name='postJob'),
    path('deleteJob/<int:job_id>/', Recruiters.views.deleteJob, name='deleteJob'),
    path('jobs/<int:job_id>/', Recruiters.views.jobDetail, name='jobDetail'),
    path('editJob/<int:job_id>', Recruiters.views.editJob, name='editJob'),
    # Authentication
    path('login/', Authentication.views.login_view, name='login'),
    path('signup/', Authentication.views.signup_view, name='signup'),
    path('logout/', Authentication.views.logout_view, name='logout'),
    # Admin
    path('admin/', admin.site.urls),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
