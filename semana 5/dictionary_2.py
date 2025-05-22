
first_list = ["name", "last name", "age", "favorite meal", "favorite color"]
second_list = ["Valeria", "Jiménez Gómez", "27", "canelones", "yellow"]

lists = {}

for index in range(len(first_list)):
    lists[first_list[index]] = second_list[index] 
print(lists)
