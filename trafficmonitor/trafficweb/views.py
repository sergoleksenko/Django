import requests
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from trafficmonitor import settings
from trafficweb.forms import CompanyForm, EmployeeForm

PAGING = 10


def get_companies():
	response = requests.get('{0}api/companies'.format(settings.BASE_URL))
	if response.status_code == 200:
		return response.json()


def paging(request, querySet):
	paginator = Paginator(querySet, PAGING)
	page = request.GET.get('page')
	page_obj = paginator.get_page(page)

	return page_obj


def companieslist(request):
	companies = paging(request, get_companies())

	return render(request, 'trafficweb/company_list.html', {'page_obj': companies})


def employeeslist(request):
	response = requests.get('{0}api/employees'.format(settings.BASE_URL))
	if response.status_code == 200:
		json = response.json()
		context = []

		for emp in json:
			company_response = requests.get('{0}api/companies/{1}'.format(settings.BASE_URL, emp['company']))
			company_json = company_response.json()
			context.append({'employee': emp, 'company': company_json['name']})

		employees = paging(request, context)

	return render(request, 'trafficweb/employee_list.html', {'page_obj': employees})


def generate(request):
	response = requests.post('{0}api/generate'.format(settings.BASE_URL))
	if response.status_code == 200:
		return render(request, 'trafficweb/transfers_generate.html')


def report(request):
	global month

	if request.GET.get('month_field') is not None:
		month = request.GET.get('month_field')

	response = requests.get('{0}api/report/{1}'.format(settings.BASE_URL, month))

	if response.status_code == 200:
		json = response.json()
		report = paging(request, json)

	return render(request, 'trafficweb/report_list.html', {'page_obj': report})


def companyadd(request):
	if request.method == 'POST':
		form = CompanyForm(request.POST)
		if form.is_valid():
			response = requests.post('{0}api/companies'.format(settings.BASE_URL), json=form.cleaned_data)
			if response.status_code == 201:
				return HttpResponseRedirect(reverse('companies'))
	else:
		form = CompanyForm(initial={'quota': 10})

	return render(request, 'trafficweb/company_add.html', {'form': form})


def companyedit(request, pk):
	if request.method == 'POST':
		form = CompanyForm(request.POST)
		if form.is_valid():
			response = requests.put('{0}api/companies/{1}'.format(settings.BASE_URL, pk), json=form.cleaned_data)
			if response.status_code == 200:
				return HttpResponseRedirect(reverse('companies'))
	else:
		response = requests.get('{0}api/companies/{1}'.format(settings.BASE_URL, pk))
		if response.status_code == 200:
			form = CompanyForm(response.json())

	return render(request, 'trafficweb/company_edit.html', {'form': form})


def companydelete(request, pk):
	if request.method == 'POST':
		response = requests.delete('{0}api/companies/{1}'.format(settings.BASE_URL, pk))
		if response.status_code == 204:
			return HttpResponseRedirect(reverse('companies'))

	return render(request, 'trafficweb/company_delete.html')


def employeeadd(request):
	json = get_companies()
	companies = [(0, '-----'), ] + [(j['id'], j['name']) for j in json]

	if request.method == 'POST':
		form = EmployeeForm(request.POST)
		form.fields['company'].choices = companies
		if form.is_valid():
			response = requests.post('{0}api/employees'.format(settings.BASE_URL), json=form.cleaned_data)
			if response.status_code == 201:
				return HttpResponseRedirect(reverse('employees'))
	else:
		form = EmployeeForm()
		form.fields['company'].choices = companies

	return render(request, 'trafficweb/employee_add.html', {'form': form})


def employeeedit(request, pk):
	json = get_companies()
	companies = [(0, '-----'), ] + [(j['id'], j['name']) for j in json]

	if request.method == 'POST':
		form = EmployeeForm(request.POST)
		form.fields['company'].choices = companies
		if form.is_valid():
			response = requests.put('{0}api/employees/{1}'.format(settings.BASE_URL, pk), json=form.cleaned_data)
			if response.status_code == 200:
				return HttpResponseRedirect(reverse('employees'))
	else:
		response = requests.get('{0}api/employees/{1}'.format(settings.BASE_URL, pk))
		if response.status_code == 200:
			form = EmployeeForm(response.json())
			form.fields['company'].choices = companies

	return render(request, 'trafficweb/employee_edit.html', {'form': form})


def employeedelete(request, pk):
	if request.method == 'POST':
		response = requests.delete('{0}api/employees/{1}'.format(settings.BASE_URL, pk))
		if response.status_code == 204:
			return HttpResponseRedirect(reverse('employees'))

	return render(request, 'trafficweb/employee_delete.html')
