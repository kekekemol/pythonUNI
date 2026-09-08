from django.db import models

# Create your models here.
class employee(models.Model):
    emp_id = models.IntegerField(primary_key=True)
    emp_firstName = models.CharField(max_length=100)
    emp_lastName = models.CharField(max_length=100)
    emp_email = models.EmailField()
    emp_salary = models.FloatField()