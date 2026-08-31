const url = "https://api.restful-api.dev/objects";

async function obtenerObjetoPorIdAxios(id) {
    try {
        const response = await axios.get(`${url}/${id}`);
        const objeto = response.data;

        console.log("Objeto encontrado:", objeto);
        return objeto;
    } catch (error) {
        console.error(`Error: ${error.response?.status} - Objeto no encontrado`);
    }
}

obtenerObjetoPorIdAxios("ff8081819f7e10ae019fe890389b17e6");