from datetime import date

import random
from dateutil.relativedelta import relativedelta
from django.db.models import F
from django.db.models import Sum, IntegerField
from django.db.models.functions import Cast
from faker import Faker
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from trafficapi.models import Company, Employee, Transfer
from trafficapi.serializers import CompanySerializer, EmployeeSerializer


# Create your views here.
class CompaniesList(generics.ListCreateAPIView):
	queryset = Company.objects.all()
	serializer_class = CompanySerializer


class CompaniesDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Company.objects.all()
	serializer_class = CompanySerializer


class EmployeesList(generics.ListCreateAPIView):
	queryset = Employee.objects.all()
	serializer_class = EmployeeSerializer


class EmployeesDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Employee.objects.all()
	serializer_class = EmployeeSerializer


@api_view(['POST'])
def generateTransfers(request):
	current_date = date.today()
	past_date = current_date + relativedelta(months=-6)
	employee = Employee.objects.all()

	while past_date <= current_date:
		for emp in employee:
			for i in range(1, random.randint(0, 5)):
				# currently bytes_amount is from 100 bytes to 10 Tb
				Transfer(employee=emp, resource=Faker().url(),
				         bytes_amount=(random.randint(100, 10995116277760)),
				         date=past_date).save()
		past_date = past_date + relativedelta(days=+random.randint(3, 5))

	return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def report(request, pk):
	queryset = Transfer.objects.values(company_id=F('employee__company_id'), name=F('employee__company__name'),
	                                   quota=F('employee__company__quota')).annotate(
			used=Cast(Sum('bytes_amount') / 1099511627776, IntegerField())).order_by('employee__company_id').filter(
			date__contains='-{0}-'.format(pk))

	return Response(queryset, status=status.HTTP_200_OK)
