colors= {
    "yellow":"sun",
    "blue":"sea",
    "red":"roses",
    "black":"cat",
    "gray":"mouse",
    "white":"snow",
    "green":"trees"
}
deleted_items = colors.pop('black')
deleted_items = colors.pop('gray')
print(colors)
print(f'Deleted item: {deleted_items}')