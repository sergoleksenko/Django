from django.db import models


# Create your models here.
class Company(models.Model):
	name = models.CharField(max_length=100, unique=True)
	quota = models.IntegerField(help_text='Monthly transfer quota (TB)')

	class Meta:
		verbose_name_plural = 'Companies'

	def __str__(self):
		return self.name


class Employee(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100, unique=True)

	def __str__(self):
		return self.name


class Transfer(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	resource = models.URLField(max_length=200)
	bytes_amount = models.IntegerField(help_text='Amount of bytes transferred (bytes)')
	date = models.DateField()

	def __str__(self):
		return '{0} ({1})'.format(self.resource, self.bytes_amount)
