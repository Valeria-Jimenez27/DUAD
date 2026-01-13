import FreeSimpleGUI as sg
from Logic import FinancialManager
from Save_data import DataStorage
from datetime import datetime

class PersonalInterface:
    def __init__(self):
        sg.theme("DarkPurple")
        self.manager=FinancialManager()
        layout=[
            [sg.Text("Personal Finance Manager", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=self.get_table_data(),
                    headings=["Title", "Amount", "Category", "Date", "Type"],
                    key="-TABLE-",
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                    auto_size_columns=True,
                    expand_x=True,
                    expand_y=True,
                    row_colors=self.get_row_colors())],
            [sg.Button("Add Category"),
            sg.Button("Add Expense"),
            sg.Button("Add Income"),
            sg.Button("Delete Movement"),
            sg.Button("Summary by Month"),
            sg.Button("Exit")]
        ]
        self.window=sg.Window("Finance Manager", layout, size=(700, 350))


    def get_table_data(self):
        sorted_movements=sorted(
            self.manager.datastorage,
            key=lambda m: datetime.strptime(m["Date"], "%d-%m-%Y")
        )
        table_data = []
        for m in sorted_movements:
            amount = float(m["Amount"])
            display_amount = f"- ₡{amount:,.2f}" if m["Type"]=="Expense" else f"+ ₡{amount:,.2f}"
            table_data.append([m["Title"], display_amount, m["Category"], m["Date"], m["Type"]])
        return table_data


    def get_row_colors(self):
        sorted_movements = sorted(
            self.manager.datastorage,
            key=lambda m: datetime.strptime(m["Date"], "%d-%m-%Y")
        )
        colors=[]
        for i, m in enumerate(sorted_movements):
            colors.append((i,'white','red'if m["Type"]=="Expense"else'green'))
        return colors


    def refresh_table(self):
        self.window["-TABLE-"].update(values=self.get_table_data(), row_colors=self.get_row_colors())


    def delete_selected_movement(self):
        selected_indices=self.window["-TABLE-"].SelectedRows
        if not selected_indices:
            sg.popup_error("Please select a movement to delete!")
            return
        confirm = sg.popup_yes_no("Are you sure you want to delete the selected movement?")
        if confirm!="Yes":
            return
        index_to_delete = selected_indices[0]
        self.manager.datastorage.pop(index_to_delete)
        DataStorage.save_movements(self.manager.datastorage,self.manager.movements_file)
        sg.popup("Movement deleted successfully!")
        self.refresh_table()


    def open_input_window(self, title, fields, save_callback):
        layout=[[sg.Text(title, font=("Helvetica", 12, "bold"))]]
        for label, key, field_type, options in fields:
            if field_type=="input":
                layout.append([sg.Text(label),sg.Input(key=key, default_text=options)])
            elif field_type=="combo":
                layout.append([sg.Text(label),sg.Combo(options, key=key)])
        layout.append([sg.Button("Save"), sg.Button("Cancel")])
        window=sg.Window(title,layout, modal=True)
        while True:
            e,v=window.read()
            if e in (sg.WIN_CLOSED, "Cancel"):
                break
            if e=="Save":
                try:
                    save_callback(v)
                    break
                except Exception as error:
                    sg.popup_error(error)
        window.close()


    def open_category_window(self):
        def save_category(values):
            self.manager.add_category(values["Category"])
            sg.popup("Category added!")
        fields=[("New Category:", "Category", "input", "")]
        self.open_input_window("Add Category", fields, save_category)


    def open_movement_window(self, movement_type):
        if not self.manager.categories:
            sg.popup_error("You must add a category first!")
            return
        def save_movement(values):
            self.manager.add_movement(
                values["Title"],
                values["Amount"],
                values["Category"],
                values["Date"],
                movement_type
            )
            sg.popup(f"{movement_type} added successfully!")
            self.refresh_table()
        fields = [
            ("Title:", "Title", "input", ""),
            ("Amount(₡):", "Amount", "input", ""),
            ("Category:", "Category", "combo", self.manager.categories),
            ("Date (DD-MM-YYYY):", "Date", "input", datetime.now().strftime("%d-%m-%Y"))
        ]
        self.open_input_window(f"New {movement_type}", fields, save_movement)


    def open_month_summary(self):
        def show_summary(values):
            try:
                month=int(values["-MONTH-"])
                year=int(values["-YEAR-"])
                if month < 1 or month > 12:
                    raise ValueError("Invalid Month")
                self.show_movements_by_month(month,year)
            except Exception as e:
                sg.popup_error(str(e))
        fields=[
            ("Month (1-12):", "-MONTH-", "input", ""),
            ("Year (YYYY):", "-YEAR-", "input", "")
        ]
        self.open_input_window("Summary by Month", fields, show_summary)


    def show_movements_by_month(self, month, year):
        filtered=[m for m in self.manager.datastorage
                    if datetime.strptime(m["Date"], "%d-%m-%Y").month==month
                    and datetime.strptime(m["Date"], "%d-%m-%Y").year==year]
        if not filtered:
            sg.popup("No moves for this month.", keep_on_top=True)
            return
        headings=["Title", "Amount", "Category", "Date", "Type"]
        table_data=[[m["Title"], m["Amount"], m["Category"], m["Date"], m["Type"]] for m in filtered]
        row_colors=[]
        for i, m in enumerate(filtered):
            row_colors.append((i, 'white', 'red' if m["Type"]=="Expense" else'green'))
        layout=[
            [sg.Table(values=table_data,
                    headings=headings,
                    row_colors=row_colors,
                    auto_size_columns=True,
                    justification='center',
                    num_rows=min(15, len(table_data)))],
            [sg.Button("Close")]
        ]
        window=sg.Window(f"Movements {month}/{year}", layout,modal=True)
        while True:
            e, _ =window.read()
            if e in (sg.WIN_CLOSED, "Close"):
                break
        window.close()


    def run_interface(self):
        while True:
            event, _ =self.window.read()
            match event:
                case sg.WIN_CLOSED |"Exit":
                    break
                case "Add Category":
                    self.open_category_window()
                case "Add Expense":
                    self.open_movement_window("Expense")
                case "Add Income":
                    self.open_movement_window("Income")
                case "Summary by Month":
                    self.open_month_summary()
                case "Delete Movement":
                    self.delete_selected_movement()
        self.window.close()
