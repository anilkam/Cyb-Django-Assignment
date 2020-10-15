from django.contrib import admin
from .models import Employee, Department, Company

admin.site.register(Company)
admin.site.register(Employee)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
       list_filter = ('company', )
       list_display = ('name', 'company')
