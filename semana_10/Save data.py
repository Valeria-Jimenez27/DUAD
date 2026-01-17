import FreeSimpleGUI as sg
import csv

class DataStorage:
    
    @classmethod
    def save_data(movements_list, filename):
        if not movements_list:
            print("No data to save.")
            return
        headers= ["Title", "Amount", "Category", "Date"]

        try:
            with open(filename, "w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(movements_list)
                print(f"Data saved sucessfully in {filename}.")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    @classmethod
    def load_data(filename):
        try: 
            with open(filename,"r",encoding="utf-8") as file:
                reader=csv.DictReader(file)
                data=[row for row in reader]    
            print(f"Data loaded successfully from {filename}.")
            return data
        except FileNotFoundError:
            print(f"File '{filename}' not found. Try again")
            return []
        except Exception as e:
            print(f"Error loading data: {e}")
            return []
