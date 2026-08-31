const url = "https://api.restful-api.dev/objects";

async function crearObjetoAxios(datosObjeto) {
    const requestOptions = {
        headers: { "Content-Type": "application/json" },
    };

    try {
        const response = await axios.post(url, datosObjeto, requestOptions);
        const nuevoObjeto = response.data;

        console.log("Objeto creado. Guarda este ID:", nuevoObjeto.id);
        return nuevoObjeto;
    } catch (error) {
        console.error(`Error: ${error.response?.status}`);
    }
}

const data = {
    name: "Kindle mini 2.0",
    data: {
        year: 2026,
        price: 350.00,
    },
};

crearObjetoAxios(data);