class Hobbies:
    def __init__(self):
        print("I really enjoy practicing some hobbies")
    
    def show_my_hobbies(self):
        print("I like to do punch needle, I love reading comics and I enjoy cooking for people that I love")

class Job:
    def __init__(self):
        print("I work as a virtual assistant for CSAMs in Microsoft")
    

    def show_my_work(self):
        print("Everyday I create Power presentations, Words documents, handle their agenda and more")

class Me(Hobbies,Job):
    def __init__(self):
        Hobbies.__init__(self)
        Job.__init__(self)
    

    def introduce_me(self):
        print("Thats what I like and what I do")
        self.show_my_hobbies()
        self.show_my_work()

me=Me()
me.introduce_me()