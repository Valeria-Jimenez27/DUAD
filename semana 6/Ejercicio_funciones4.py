def my_string():
    string="I focus on what really matters"
    reversed_text=""
    for index in range(len(string)-1,-1,-1):
        reversed_text+=string[index]
    return reversed_text

result=my_string()
print(result)