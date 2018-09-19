from django.contrib import admin

# Register your models here.
from trafficapi.models import Company, Employee, Transfer


@admin.register(Company)
class CompaniesAdmin(admin.ModelAdmin):
	list_display = ['name', 'quota']


@admin.register(Employee)
class EmployeesAdmin(admin.ModelAdmin):
	list_display = ['name', 'email', 'company']


@admin.register(Transfer)
class TransfersAdmin(admin.ModelAdmin):
	list_display = ['employee', 'resource', 'bytes_amount', 'date']
