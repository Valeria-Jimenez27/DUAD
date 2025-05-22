import csv

file_csv = "videogames.csv"
headers = ["Name", "Genre", "Developer", "ESRB Rating"]

def videogames_tab_csv():
    n = int(input("How many video games do you want to enter? "))

    with open(file_csv, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file,delimiter='\t')
        writer.writerow(headers)

        for index in range(n):
            print(f"\nVideogame #{index + 1}")
            name = input("Name: ")
            genre = input("Genre: ")
            developer = input("Developer: ")
            rating = input("ESRB Rating: ")
            writer.writerow([name, genre, developer, rating])

    print(f"\nThere are {n} videogames in '{file_csv}'\n")

    with open(file_csv, 'r', encoding='utf-8') as file:
        reader = csv.reader(file,delimiter='\t')
        for row in reader:
            print(row)

videogames_tab_csv()
