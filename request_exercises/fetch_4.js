const url = "https://api.restful-api.dev/objects";

async function actualizarObjeto(id, nuevosDatos) {
    const requestOptions = {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(nuevosDatos),
    };

    const response = await fetch(`${url}/${id}`, requestOptions);

    if (!response.ok) {
        console.error(`Error: ${response.status} - No se pudo actualizar`);
        return;
    }

    const objetoActualizado = await response.json();
    console.log("Objeto actualizado:", objetoActualizado);
    return objetoActualizado;
}
actualizarObjeto("ff8081819f7e10ae019fe87333ec17b9", { name: "Kindle actualizada", data: { price: 220.00 } });