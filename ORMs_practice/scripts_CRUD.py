from sqlalchemy.orm import Session
from Manage_data import User, Car, Address
from engine_installation import engine

#Crear/Modificar/Eliminar un usuario nuevo:
def create_user(name, birth_date, email):
    with Session(engine) as session:
        new_user = User(
            name=name,
            birth_date=birth_date,
            email=email
        )
        session.add(new_user)
        session.commit()
        print(f"User with ID {new_user.id} created successfully!")


def update_user(user_id, new_name=None, new_email=None):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            print("User not found")
            return
        if new_name:
            user.name = new_name
        if new_email:
            user.email = new_email
        session.commit()
        print(f"User with ID {user_id} updated successfully!")


def delete_user(user_id):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            print("User not found")
            return
        session.delete(user)
        session.commit()
        print(f"User with ID {user_id} deleted successfully!")

#Crear/Modificar/Eliminar un automóvil nuevo.
def create_car(brand, model, user_id=None):
    with Session(engine) as session:
        new_car = Car(
            brand=brand,
            model=model,
            user_id=user_id
        )
        session.add(new_car)
        session.commit()
        print(f"Car with ID {new_car.id} created successfully!")

def update_car(car_id, new_brand=None, new_model=None):
    with Session(engine) as session:
        car = session.get(Car, car_id)
        if not car:
            print("Car not found")
            return
        if new_brand:
            car.brand = new_brand
        if new_model:
            car.model = new_model
        session.commit()
        print(f"Car with ID {car_id} updated successfully!")

def delete_car(car_id):
    with Session(engine) as session:
        car = session.get(Car, car_id)
        if not car:
            print("Car not found")
            return
        session.delete(car)
        session.commit()
        print(f"Car with ID {car_id} deleted successfully!")

#Crear/Modificar/Eliminar una dirección nueva.
def create_address(street, city, user_id):
    with Session(engine) as session:
        new_address = Address(
            street=street,
            city=city,
            user_id=user_id
        )
        session.add(new_address)
        session.commit()
        print(f"Address with ID {new_address.id} created successfully!")

def update_address(address_id, new_street=None, new_city=None):
    with Session(engine) as session:
        address = session.get(Address, address_id)
        if not address:
            print("Address not found")
            return
        if new_street:
            address.street = new_street
        if new_city:
            address.city = new_city
        session.commit()
        print(f"Address with ID {address_id} updated successfully!")

def delete_address(address_id):
    with Session(engine) as session:
        address = session.get(Address, address_id)
        if not address:
            print("Address not found")
            return
        session.delete(address)
        session.commit()
        print(f"Address with ID {address_id} deleted successfully!")

#Asociar un automóvil a un usuario.
def assign_car_to_user(car_id, user_id):
    with Session(engine) as session:
        car = session.get(Car, car_id)
        user = session.get(User, user_id)
        if not car or not user:
            print("User or Car not found")
            return
        car.user = user
        session.commit()
        print(f"Car with ID {car_id} assigned to user with ID {user_id} successfully!")

#Consultar todos los usuarios.
def get_all_users():
    with Session(engine) as session:
        users = session.query(User).all()
        return users

#Consultar todos los automóviles.
def get_all_cars():
    with Session(engine) as session:
        cars = session.query(Car).all()
        return cars

#Consultar todas las direcciones.
def get_all_addresses():
    with Session(engine) as session:
        addresses = session.query(Address).all()
        return addresses


