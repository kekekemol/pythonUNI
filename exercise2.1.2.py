#Exercise1
x = "cat and dog"

a = "cat"
b = "dog"
c = "mouse"

print(a not in x)
print(b not in x)
print(c in x)

#Exercise2
birth_year = 1967
birth_month = 2
birth_day = 14

current_year = 2000
current_month = 1
current_day = 1

# Calculate total days
total_days = ((current_year - birth_year) * 365.25) - ((31 - current_day) + birth_day)

print("Ahmad was", total_days, "days old on January 1, 2000")

#Exercise3
a = 7

b = a*1432
c = a+10017
d = a -- 10017
e = a/0.0006983240223463687
f = a//0.0006983
print(b)
print(c)
print(d)
print(e)
print(f)

#Exercise4
a = int(input("Input an integer : "))

