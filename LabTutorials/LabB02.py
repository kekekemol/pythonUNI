#Name : Ahmad Kamal Akasyah Bin Rohaizan
#Student Identification Number : 52213109023
#Class : L01-B01
#Online Practical Test


# Creating Staff class
class Staff:
    def __init__(self, staff_id, name):
        self.staff_id = staff_id
        self.name = name

    def displayStaff(self):
        print("Staff ID:", self.staff_id)
        print("Staff Name:", self.name)



# (a) Accept user input of Staff ID and name
print("Enter Staff 1 Information")

staff_id1 = input("Please enter Staff ID: ")
name1 = input("Please enter Staff Name: ")

staff1 = Staff(staff_id1, name1)



print("\nEnter Staff 2 Information")

staff_id2 = input("Please enter Staff ID: ")
name2 = input("Please enter Staff Name: ")

staff2 = Staff(staff_id2, name2)



# Display staff details
print("\n--- Staff Details ---")

staff1.displayStaff()

print()

staff2.displayStaff()



# (b) Function to calculate salary
def calculateSalary(total_hours, hourly_wage):

    # Regular working hours is 6 hours
    regular_hours = 6


    # Automatically calculate overtime hours
    if total_hours > regular_hours:
        overtime_hours = total_hours - regular_hours
    else:
        overtime_hours = 0


    # Maximum overtime hours is 5 hours
    if overtime_hours > 5:
        overtime_hours = 5


    # Calculate payment
    regular_pay = regular_hours * hourly_wage

    overtime_pay = overtime_hours * hourly_wage * 1.7


    total_salary = regular_pay + overtime_pay

    return total_salary



# Getting working hours and wage
print("\n--- Salary Calculation ---")

total_hours = int(input("Please enter total hours worked: "))


# (c) Exception handling for hourly wage
try:
    hourly_wage = float(input("Please enter hourly wage rate: "))

except ValueError:
    print("Error: Hourly wage rate must be a number.")
    hourly_wage = 0



# Calculate and display salary
salary = calculateSalary(total_hours, hourly_wage)

print("Weekly Pay = RM", salary)