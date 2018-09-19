from django.urls import path

from . import views

urlpatterns = [
	path('companies', views.companieslist, name='companies'),
	path('employees', views.employeeslist, name='employees'),
	path('generate', views.generate, name='transfers_generate'),
	path('report', views.report, name='report'),
	path('companies/add', views.companyadd, name='company_add'),
	path('companies/<int:pk>/edit', views.companyedit, name='company_edit'),
	path('companies/<int:pk>/delete', views.companydelete, name='company_delete'),
	path('employees/add', views.employeeadd, name='employee_add'),
	path('employees/<int:pk>/edit', views.employeeedit, name='employee_edit'),
	path('employees/<int:pk>/delete', views.employeedelete, name='employee_delete'),
]
