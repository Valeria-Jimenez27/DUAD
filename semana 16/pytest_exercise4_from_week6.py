def my_string(text="I focus on what really matters"):
    reversed_text=""
    for index in range(len(text)-1,-1,-1):
        reversed_text+=text[index]
    return reversed_text

result=my_string()
print(result)