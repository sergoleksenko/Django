from django.urls import path

from . import views

urlpatterns = [
	path('companies', views.CompaniesList.as_view()),
	path('companies/<int:pk>', views.CompaniesDetail.as_view()),
	path('employees', views.EmployeesList.as_view()),
	path('employees/<int:pk>', views.EmployeesDetail.as_view()),
	path('generate', views.generateTransfers),
	path('report/<str:pk>', views.report),
]
