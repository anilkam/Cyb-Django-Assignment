from django.contrib import admin
from .models import Employee, Department, Company
from django_reverse_admin import ReverseModelAdmin
from nested_admin import NestedStackedInline, NestedModelAdmin
from django.contrib.admin import ModelAdmin
admin.site.site_header = "Employee management Admin"

@admin.register(Employee)
class EmployeeAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = [('user', {'fields': ['username', 'first_name', 'last_name']}),
                      ]


class MembershipInline(NestedStackedInline):
    model = Employee.department.through


class EmployeeInlineAdmin(NestedStackedInline):
    # inline_type = 'stacked'
    # inline_reverse = [('user', {'fields': ['username', 'first_name', 'last_name']}),                   ]
    model = Employee


# @admin.register(Department)
class DepartmentAdmin(NestedStackedInline):
    model = Department
    # list_filter = ('company', )
    # list_display = ('name', 'company')
    extra = 1
    inlines = [MembershipInline]

class CompanyAdmin(NestedModelAdmin):
    model = Company
    inlines = [DepartmentAdmin]

admin.site.register(Company, CompanyAdmin)
