#getting input by user
fahrenheit = float(input("enter temp in fahrenheit:"))

#converter or formula 
celcius = (5/9)*(fahrenheit-32)

#selective for different temp
if celcius >= 100:
    print(celcius, "The tempreture is boiling")

elif celcius >= 40:
    print(celcius, "The tempreture is Hot")

elif celcius > 0:
    print(celcius,"The temp is cold")

elif celcius < 0:
    print(celcius, "Freezing")

    

