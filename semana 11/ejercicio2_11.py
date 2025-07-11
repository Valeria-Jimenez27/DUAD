class Person:
    def __init__(self,name):
        self.name= name


class Bus:
    def __init__(self,max_passengers):
        self.max_passengers= max_passengers
        self.passengers= []
    

    def add_passenger(self,person):
        if len(self.passengers)< self.max_passengers:
            self.passengers.append(person)
            print(f"{person.name} is on the bus.")
        else:
            print("The bus is full")
            return
    

    def drop_off_passenger(self, name):
        for p in self.passengers:
            if p.name == name:
                self.passengers.remove(p)
                print(f"{name} drop off of the bus.")
                return

if __name__ == "__main__":
    bus= Bus(max_passengers=3)

    name1= input("Enter the first passenger: ")
    bus.add_passenger(Person(name1))

    name2= input("Enter the second passenger: ")
    bus.add_passenger(Person(name2))

    name3= input("Enter the third passenger: ")
    bus.add_passenger(Person(name3))

    name4= input("Enter the fourth passenger: ")
    bus.add_passenger(Person(name4))

    drop_name= input("Who wants to get off the bus?: ")
    bus.drop_off_passenger(drop_name)

    print("List of passengers: ")
    for p in bus.passengers:
        print(f"- {p.name}")
