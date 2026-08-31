const url = "https://api.restful-api.dev/objects";

async function listarObjetosAxios() {
    try {
        const response = await axios.get(url);
        const objetos = response.data;

        const conData = objetos.filter(obj => obj.data);

        conData.forEach(obj => {
            console.log(`ID: ${obj.id} | Nombre: ${obj.name}`);
            console.log("Datos:", obj.data);
        });

        return conData;
    } catch (error) {
        console.error(`Error: ${error.response?.status}`);
    }
}

listarObjetosAxios();