#Name: Ahmad Kamal Akasyah Bin Rohaizan
#Student ID : 52213109023

# Getting Staff ID and Name
name = input("Please enter name: ")
userid = int(input("Please enter Staff ID: "))

# Total hours worked
hours_worked = int(input("Please enter total hours worked: "))

hourly_wage = 35

def calculateSalary(hours_worked, hourly_wage):
    if hours_worked <= 6:
        regular_hours = hours_worked
        overtime_hours = 0
    else:
        regular_hours = 6
        overtime_hours = hours_worked - 6

        # Maximum overtime is 5 hours
        if overtime_hours > 5:
            overtime_hours = 5

    regular_pay = regular_hours * hourly_wage
    overtime_pay = overtime_hours * hourly_wage * 1.7

    return regular_pay + overtime_pay

salary = calculateSalary(hours_worked, hourly_wage)

print("Weekly Pay =", salary)