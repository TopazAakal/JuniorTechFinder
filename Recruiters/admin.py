from django.contrib import admin

from .models import Recruiters, JobListing


class RecruitersAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name',
                    'phone_number', 'city', 'age', 'company')
    list_filter = ('city', 'age')
    search_fields = ('email', 'full_name', 'city', 'company')


admin.site.register(Recruiters, RecruitersAdmin)


class JobListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'recruiter',
                    'location', 'salary', 'date_posted')
    list_filter = ('recruiter', 'location')
    search_fields = ('title', 'description', 'location')


admin.site.register(JobListing, JobListingAdmin)
