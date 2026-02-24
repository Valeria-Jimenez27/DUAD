from scripts_CRUD import create_address, get_all_addresses

create_address("Guadalupe", "San José", 1)

addresses = get_all_addresses()

for address in addresses:
    print(address.id, address.street, address.city, address.user_id)