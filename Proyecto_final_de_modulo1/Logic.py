from datetime import datetime
from Structure import FinanceStructure
from Save_data import DataStorage

class FinancialManager:
    def __init__(self, movements_file="financemanager.csv", categories_file="categories.csv"):
        self.movements_file=movements_file
        self.categories_file=categories_file

        self.datastorage=DataStorage.load_movements(self.movements_file)
        self.categories=DataStorage.load_categories(self.categories_file)


    def add_category(self, category):
        if not category or not category.strip():
            raise ValueError("Category cannot be empty or blank space.")
        if category.strip() in self.categories:
            raise ValueError("Category already exists.")
        
        self.categories.append(category.strip())
        DataStorage.save_categories(self.categories, self.categories_file)


    def add_movement(self, title, amount, category, date, movement_type):
        if not self.categories:
            raise ValueError("You must add a category before adding movements!")
        if not all([title.strip(), category.strip(), date.strip(), movement_type.strip()]):
            raise ValueError("Please fill in all the fields correctly (no blank spaces).")
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("The amount must be greater than zero.")
        except ValueError:
            raise ValueError("Amount must be a valid number.")
        try:
            datetime.strptime(date.strip(), "%d-%m-%Y")
        except ValueError:
            raise ValueError("Date must be in DD-MM-YYYY format.")
        new_movement = FinanceStructure(title.strip(), amount, category.strip(), date.strip(), movement_type.strip())
        self.datastorage.append(new_movement.to_dict())
        DataStorage.save_movements(self.datastorage, self.movements_file)

