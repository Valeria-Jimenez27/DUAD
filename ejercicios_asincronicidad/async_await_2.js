async function obtenerUsuario() {
    try {
        const response = await fetch("https://reqres.in/api/users/23", {
            headers: { "x-api-key": "pro_8a05f48f5e089a6ee6f70a879ff60a3d6fce85cfe3c426dbf2339fc827d24307" }
        });

        if (!response.ok) {
            throw new Error(`Usuario no encontrado (status ${response.status})`);
        }

        const data = await response.json();
        console.log("Respuesta completa:", data);
    } catch (error) {
        console.error("Error:", error.message);
    }
}

obtenerUsuario();