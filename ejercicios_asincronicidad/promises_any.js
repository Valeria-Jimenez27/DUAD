function getPokemon(id) {
    return fetch(`https://pokeapi.co/api/v2/pokemon/${id}`)
        .then(response => response.json());
}

Promise.any([
    getPokemon(1),
    getPokemon(4),
    getPokemon(7)
])
    .then(firstPokemon => {
        console.log("The first one to resolve was:", firstPokemon.name);
    })
    .catch(error => {
        console.error("All promises failed:", error);
    });