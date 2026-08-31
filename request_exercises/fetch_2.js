const url = "https://api.restful-api.dev/objects";

async function crearObjeto(datosObjeto) {
    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datosObjeto),
    };

    const response = await fetch(url, requestOptions);

    if (!response.ok) {
        console.error(`Error: ${response.status}`);
        return;
    }

    const nuevoObjeto = await response.json();
    console.log("Objeto creado, con este ID:", nuevoObjeto.id);
    return nuevoObjeto;
}

const data = {
    name: "Kindle mini",
    data: {
        year: 2025,
        price: 250.00,
    },
};

crearObjeto(data);