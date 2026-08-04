#Name: Ahmad Kamal Akasyah Bin Rohaizan
#Student ID : 52213109023
#Class: L01-B01
#Online Practical Test

#Creating staff object 
class Staff:
    def __init__(self, staff_id, name):
        self.staff_id = staff_id
        self.name = name

    def displayStaff(self):
        print("Staff ID:", self.staff_id)
        print("Staff Name:", self.name)

# Getting Staff ID and Name
print("Enter Staff Information")
name1 = input("Please enter name: ")
userid1 = input("Please enter Staff ID: ")
staff1=Staff(userid1, name1)

print("\nEnter Staff 2 Information")
name2 = input("Please enter name: ")
userid2 = input("Please enter Staff ID: ")
staff2=Staff(userid2, name2)

#Displaying Staff ID and Name
print("\n---Staff Details---")

staff1.displayStaff()
print()
staff2.displayStaff()

# Getting working hours
print("\n--- Salary Calculation ---")

regular_hours = int(input("Please enter regular hours worked: "))
overtime_hours = int(input("Please enter overtime hours worked: "))


# Exception handling for hourly wage
try:
    hourly_wage = float(input("Please enter hourly wage rate: "))

except ValueError:
    print("Error: Hourly wage rate must be a number.")
    hourly_wage = 0



# Function to calculate salary
def calculateSalary(regular_hours, overtime_hours, hourly_wage):

    # Maximum overtime is 5 hours
    if overtime_hours > 5:
        overtime_hours = 5

    # Calculate payment
    regular_pay = regular_hours * hourly_wage
    overtime_pay = overtime_hours * hourly_wage * 1.7

    total_salary = regular_pay + overtime_pay

    return total_salary



# Calculate and display salary
salary = calculateSalary(regular_hours, overtime_hours, hourly_wage)

print("Weekly Pay = RM", salary)