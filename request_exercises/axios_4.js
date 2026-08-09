const url = "https://api.restful-api.dev/objects";

async function actualizarObjetoAxios(id, nuevosDatos) {
    const requestOptions = {
        headers: { "Content-Type": "application/json" },
    };

    try {
        const response = await axios.patch(`${url}/${id}`, nuevosDatos, requestOptions);
        const objetoActualizado = response.data;

        console.log("Objeto actualizado:", objetoActualizado);
        return objetoActualizado;
    } catch (error) {
        console.error(`Error: ${error.response?.status} - No se pudo actualizar`);
    }
}
actualizarObjetoAxios("ff8081819f7e10ae019fe890389b17e6", {
    data: {
        price: 377.00
    }
});