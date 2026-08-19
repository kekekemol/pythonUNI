# Name : Ahmad Kamal Akasyah Bin Rohaizan
# Student Identification Number : 52213109023
# Class : L01
# Practical Lab : Lab3

from django.shortcuts import render
from .models import employee as Employee


def employee(request):
    employee = None

    if request.method == 'POST':
        employee, created = Employee.objects.update_or_create(
            emp_id=request.POST.get('id'),
            defaults={
                'emp_firstName': request.POST.get('first_name'),
                'emp_lastName': request.POST.get('last_name'),
                'emp_salary': request.POST.get('salary'),
                'emp_email': request.POST.get('email')
            }
        )

    return render(request, 'KamalApp/employee.html', {
        'employee': employee
    })
