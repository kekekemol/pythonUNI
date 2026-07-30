#Name: Ahmad Kamal Akasyah Bin Rohaizan
#Student ID : 52213109023

#Getting Staff ID and Name (a)
name = str(input("please enter name: "))
userid = int(input("please enter Staff ID :"))

#collecting input for hours
total_regular_hours = int(input("please enter total regular hours for this month:  "))
total_overtime_hours = int(input("please enter total overtime hours for this month: "))

hourly_wage = 35


#Function for calculateSalary (b)
def calculateSalary(regular_hours,overtime_hours,hourly_wage):
    regular_hours_pay = hourly_wage * regular_hours
    overtime_hours_pay = overtime_hours * 1.5 * hourly_wage

    return regular_hours_pay + overtime_hours_pay

print(calculateSalary)