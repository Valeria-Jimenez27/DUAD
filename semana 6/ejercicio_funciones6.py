def word_order(words):
    list=words.split("-")
    list.sort()
    result="-".join(list)
    return(list)


entry=input("Enter your list of words")
result=word_order(entry)
print(result)