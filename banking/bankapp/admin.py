from django.contrib import admin
from .models import Application, AccountType, District, Branches, Document


# Register your models here.

class TypeAdmin(admin.ModelAdmin):
    list_display = ['Type_name']


admin.site.register(AccountType, TypeAdmin)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(District, DistrictAdmin)


class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'district']


admin.site.register(Branches, BranchAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'age', 'dob', 'phone', 'district', 'branch', 'account', 'document']
    preserve_filters = {'email': ['name,']}


admin.site.register(Application, ApplicationAdmin)


class DocAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Document, DocAdmin)
