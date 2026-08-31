const url = "https://api.restful-api.dev/objects";

async function listarObjetos() {
    const requestOptions = {
        method: "GET",
    };

    const response = await fetch(url, requestOptions);

    if (!response.ok) {
        console.error(`Error: ${response.status}`);
        return;
    }

    const objetos = await response.json();
    const conData = objetos.filter(obj => obj.data);

    conData.forEach(obj => {
        console.log(`ID: ${obj.id} | Nombre: ${obj.name}`);
        console.log("Datos:", obj.data);
    });

    return conData;
}

listarObjetos();