import csv

class DataStorage:

    @staticmethod
    def save_movements(movements_list, filename):
        headers = ["Title", "Amount", "Category", "Date", "Type"]


        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(movements_list)


    @staticmethod
    def load_movements(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader=csv.DictReader(file)
                return [row for row in reader]
        except FileNotFoundError:
            return []
        
    
    @staticmethod
    def save_categories(category_list, filename="categories.csv"):
        headers=["Category"]
        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer=csv.writer(file)
            writer.writerow(headers)
            for category in category_list:
                writer.writerow([category])


    @staticmethod
    def load_categories(filename="categories.csv"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader=csv.DictReader(file)
                return [row["Category"] for row in reader]
        except FileNotFoundError:
            return []





