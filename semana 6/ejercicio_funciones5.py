def counter(string):
    caps = 0
    lowercase = 0
    for caracter in string:
        if caracter.isupper():
            caps += 1
        elif caracter.islower():
            lowercase += 1
    print(f"There are {caps} upper cases and {lowercase} lower cases")


text=input("Write a text:")
counter(text)

