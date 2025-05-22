import json

file_json = "pokemones.json"

def load_pokemones():
    try:
        with open(file_json, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_pokemones(pokemones):
    with open(file_json, "w", encoding="utf-8") as f:
        json.dump(pokemones, f,)

def new_pokemon():
    name = input("Pokemon's Name: ")
    types_input = input("Pokemon type: ").split(",")
    types = [t.strip().capitalize() for t in types_input]

    hp = int(input("HP: "))
    attack = int(input("Attack: "))
    defense = int(input("Defense: "))
    sp_attack = int(input("Sp. Attack: "))
    sp_defense = int(input("Sp. Defense: "))
    speed = int(input("Speed: "))

    base = {
        "HP": hp,
        "Attack": attack,
        "Defense": defense,
        "Sp. Attack": sp_attack,
        "Sp. Defense": sp_defense,
        "Speed": speed
    }

    pokemon = {
        "name": {
            "english": name
        },
        "type": types,
        "base": base
    }

    print("New Pokemon:")
    print(json.dumps(pokemon))

    return pokemon

def final_pokemones(pokemones):
    print("Complete list:")
    for index, p in enumerate(pokemones, start=1):
        name = p.get("name", {}).get("english", "Unknow")
        typos = ', '.join(p.get("type", []))
        print(f"{index}. {name} - Type(s): {typos}")

def main():
    pokemones = load_pokemones()
    new = new_pokemon()
    pokemones.append(new)
    save_pokemones(pokemones)
    print(f"Pokemon '{new['name']['english']}' correctly added to '{file_json}'.")
    final_pokemones(pokemones)

if __name__ == "__main__":
    main()
