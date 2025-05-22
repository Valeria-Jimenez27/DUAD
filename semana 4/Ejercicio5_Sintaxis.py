number_grades=int(input("Entry your number of grades:"))
number_approvals=0
number_failings=0
pass_rates=0
failing_rate=0
total_average=0
counter=1

while (counter<=number_grades):
    grades = float(input(f"Entry your grade {counter}: "))
    total_average+= grades

    if (grades>=70):
        number_approvals=number_approvals+1
        pass_rates+=grades
    else:
        number_failings =number_failings+1
        failing_rate+=grades
    counter=counter+1
if (number_approvals>0):
    pass_rates/=number_approvals
else:
    pass_rates=0
if (number_failings>0):
    failing_rate/=number_failings
else:
    failing_rate=0

if (total_average>0):
    total_average/=number_grades
else:
    total_average=0

print(f"Your number of passing grades is: {number_approvals}")
print(f"Your passing grade point average is: {pass_rates}")
print(f"Your number of failing grades is: {number_failings}")
print(f"Your failing grade point average is: {failing_rate}")
print(f"Your total average is: {total_average}")






