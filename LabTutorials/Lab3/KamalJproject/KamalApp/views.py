# Name : Ahmad Kamal Akasyah Bin Rohaizan
# Student Identification Number : 52213109023
# Class : L01
# Practical Lab : Lab3

from django.shortcuts import render


def employee(request):
    employee = {
        'id': 1001,
        'first_name': 'Ahmad',
        'last_name': 'Kamal',
        'salary': 3500,
        'email': 'ahmad@example.com'
    }

    return render(request, 'KamalApp/employee.html', {
        'employee': employee
    })