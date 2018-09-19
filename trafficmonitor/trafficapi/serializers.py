from rest_framework import serializers

from trafficapi.models import Company, Employee, Transfer


class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields = '__all__'


class TransferSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transfer
		fields = '__all__'
