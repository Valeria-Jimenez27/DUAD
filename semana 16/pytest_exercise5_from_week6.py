def counter(string):
    caps = 0
    lowercase = 0
    for caracter in string:
        if caracter.isupper():
            caps += 1
        elif caracter.islower():
            lowercase += 1
    return caps, lowercase


if __name__ == "__main__":
    text = input("Write a text: ")
    caps, lower = counter(text)
    print(f"There are {caps} upper cases and {lower} lower cases")