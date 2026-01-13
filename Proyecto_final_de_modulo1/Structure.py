class FinanceStructure:
    def __init__(self, title, amount, category, date, movement_type):
        self.title=title
        self.amount=float(amount)
        self.category=category
        self.date=date
        self.movement_type=movement_type


    def to_dict(self):
        return {
            "Title":self.title,
            "Amount":self.amount,
            "Category":self.category,
            "Date":self.date,
            "Type":self.movement_type
        }
