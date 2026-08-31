const url = "https://api.restful-api.dev/objects";

//Regristro//
const formRegistro = document.getElementById("formRegistro");

if (formRegistro) {
    const mensajeErrorRegistro = document.getElementById("mensajeError");

    formRegistro.addEventListener("submit", async (event) => {
        event.preventDefault();
        mensajeErrorRegistro.textContent = "";

        const nombre = document.getElementById("inputNombre").value;
        const password = document.getElementById("inputPassword").value;
        const nuevoUsuario = {
            name: nombre,
            data: {
                password: password,
            },
        };
        try {
            const response = await axios.post(url, nuevoUsuario, {
                headers: { "Content-Type": "application/json" },
            });
            const usuarioCreado = response.data;

            localStorage.setItem("usuario", JSON.stringify(usuarioCreado));

            alert(`Usuario creado correctamente! Tu id es ${usuarioCreado.id}`);

            window.location.href = "perfil.html";
        } catch (error) {
            mensajeErrorRegistro.textContent = "Ocurrió un error al crear tu cuenta. Intenta de nuevo.";
        }
    });
}


//login//
const formLogin = document.getElementById("formLogin");

if (formLogin) {
    const mensajeErrorLogin = document.getElementById("mensajeError");

    formLogin.addEventListener("submit", async (event) => {
        event.preventDefault();
        mensajeErrorLogin.textContent = "";

        const id = document.getElementById("inputId").value;
        const password = document.getElementById("inputPassword").value;

        try {
            const response = await axios.get(`${url}/${id}`);
            const usuario = response.data;

            if (usuario.data?.password !== password) {
                mensajeErrorLogin.textContent = "Contraseña incorrecta.";
                return;
            }

            localStorage.setItem("usuario", JSON.stringify(usuario));
            window.location.href = "perfil.html";

        } catch (error) {
            if (error.response?.status === 404) {
                mensajeErrorLogin.textContent = "No existe ningún usuario con ese ID.";
            } else {
                mensajeErrorLogin.textContent = "Ocurrió un error al iniciar sesión.";
            }
        }
    });
}


//perfil//
const card = document.getElementById("card");

if (card) {
    const usuarioGuardado = localStorage.getItem("usuario");

    if (!usuarioGuardado) {
        window.location.href = "login.html";
    } else {
        const usuario = JSON.parse(usuarioGuardado);

        card.innerHTML = `
            <p><strong>ID:</strong> ${usuario.id}</p>
            <p><strong>Nombre:</strong> ${usuario.name}</p>
            <p><strong>Datos:</strong> ${JSON.stringify(usuario.data)}</p>
        `;

        document.getElementById("btnLogout").addEventListener("click", () => {
            localStorage.removeItem("usuario");
            window.location.href = "login.html";
        });
    }
}


//cambio de contraseña//
const formCambio = document.getElementById("formCambio");

if (formCambio) {
    const mensajeCambio = document.getElementById("mensaje");

    formCambio.addEventListener("submit", async (event) => {
        event.preventDefault();
        mensajeCambio.textContent = "";
        mensajeCambio.className = "";

        const id = document.getElementById("inputId").value;
        const passwordActual = document.getElementById("inputPasswordActual").value;
        const passwordNueva = document.getElementById("inputPasswordNueva").value;
        const passwordConfirmar = document.getElementById("inputPasswordConfirmar").value;

        if (passwordNueva !== passwordConfirmar) {
            mostrarErrorCambio("La nueva contraseña y la confirmación no coinciden.");
            return;
        }

        try {
            const response = await axios.get(`${url}/${id}`);
            const usuario = response.data;

            if (usuario.data?.password !== passwordActual) {
                mostrarErrorCambio("La contraseña actual es incorrecta.");
                return;
            }

            const nuevosDatos = {
                data: {
                    ...usuario.data,
                    password: passwordNueva,
                },
            };

            await axios.patch(`${url}/${id}`, nuevosDatos, {
                headers: { "Content-Type": "application/json" },
            });

            mostrarExitoCambio("Contraseña actualizada correctamente.");
            formCambio.reset();

        } catch (error) {
            if (error.response?.status === 404) {
                mostrarErrorCambio("No existe ningún usuario con ese ID.");
            } else {
                mostrarErrorCambio("Ocurrió un error al cambiar la contraseña.");
            }
        }
    });

    function mostrarErrorCambio(texto) {
        mensajeCambio.textContent = texto;
        mensajeCambio.className = "error";
    }

    function mostrarExitoCambio(texto) {
        mensajeCambio.textContent = texto;
        mensajeCambio.className = "exito";
    }
}