from django.contrib import admin

# Register your models here.

from app.models import Profile,PersonalDetails,BankDetails

admin.site.register(Profile)
admin.site.register(PersonalDetails)
admin.site.register(BankDetails)