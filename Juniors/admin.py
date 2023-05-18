from django.contrib import admin
from .models import Juniors


class JuniorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone_number', 'city', 'age')
    list_filter = ('city', 'age')
    search_fields = ('full_name', 'email', 'phone_number')


admin.site.register(Juniors, JuniorsAdmin)
