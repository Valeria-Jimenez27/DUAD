name=input("Entry your name")
last_name=input("Entry your last name")
age=int(input("Entry your age"))

if (age<=2):
    print("Baby")
elif (age<=12):
    print("Children")
elif (age<=16):
    print("Preadolescent")
elif (age<=18):
    print("Teenager")
elif (age<=30):
    print("Young Adult")
elif (age<65):
    print("Adult")
elif (age>=65):
    print("Senior citizen")
