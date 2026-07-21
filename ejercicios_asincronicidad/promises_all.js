function getPokemon(id) {
    return fetch(`https://pokeapi.co/api/v2/pokemon/${id}`)
        .then(response => response.json());
}

Promise.all([
    getPokemon(7),
    getPokemon(10),
    getPokemon(15)
])
    .then(pokemons => {
        pokemons.forEach(pokemon => {
            console.log(pokemon.name);
        });
    })
    .catch(error => {
        console.error("Error fetching pokemons:", error);
    });