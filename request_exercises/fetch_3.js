const url = "https://api.restful-api.dev/objects";

async function obtenerObjetoPorId(id) {
    const requestOptions = {
        method: "GET",
    };

    const response = await fetch(`${url}/${id}`, requestOptions);

    if (!response.ok) {
        console.error(`Error: ${response.status} - Objeto no encontrado`);
        return;
    }

    const objeto = await response.json();
    console.log("Objeto encontrado:", objeto);
    return objeto;
}
obtenerObjetoPorId("ff8081819f7e10ae019fe87333ec17b9");