from menu import Menu

class Main:
    def __init__(self):
        self.menu = Menu()

    def run(self):
        self.menu.show_menu()

if __name__ == "__main__":
    app = Main()
    app.run()
