async function obtenerUsuario() {
    const response = await fetch("https://reqres.in/api/users/2", {
        headers: { "x-api-key": "pro_8a05f48f5e089a6ee6f70a879ff60a3d6fce85cfe3c426dbf2339fc827d24307" }
    });

    console.log("Status:", response.status);

    const data = await response.json();
    console.log("Respuesta completa:", data);
}

obtenerUsuario();