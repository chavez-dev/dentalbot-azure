// Mostrar/ocultar ventana del bot
let chatIniciado = false; // bandera para saber si ya se envió el mensaje inicial

function toggleChat() {
    const chatWindow = document.getElementById("chat-window");
    if (chatWindow.classList.contains("hidden")) {
        chatWindow.classList.remove("hidden");
        document.getElementById("input").focus();

        if (!chatIniciado) {
            agregarMensaje(
                "bot",
                "👋 ¡Hola! Soy DentalBot. ¿En qué puedo ayudarte?"
            );
            chatIniciado = true;
        }
    } else {
        chatWindow.classList.add("hidden");
    }
}

// Agregar mensajes al chat
function agregarMensaje(tipo, texto) {
    const chat = document.getElementById("chat");
    const msg = document.createElement("div");
    const html = marked.parse(texto);
    msg.className = "msg " + tipo;
    msg.innerHTML = `<span>${html}</span>`;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}

// Enviar mensaje
async function enviar() {
    const input = document.getElementById("input");
    const texto = input.value.trim();
    if (!texto) return;

    agregarMensaje("user", texto);
    input.value = "";

    mostrarLoading(); // mostrar mensaje de loading

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: texto }),
        });

        const data = await res.json();
        eliminarLoading(); // quitar el loading antes de la respuesta
        agregarMensaje("bot", data.response);
    } catch (err) {
        console.error(err);
        eliminarLoading(); // quitar el loading en caso de error
        agregarMensaje("bot", "⚠️ Ocurrió un error al conectar con el servidor.");
    }
}




function mostrarLoading() {
    const chat = document.getElementById("chat");
    const msg = document.createElement("div");
    msg.className = "msg bot loading";
    msg.innerHTML = `
        <span>
            <i class="fas fa-spinner fa-spin"></i> DentalBot está escribiendo...
        </span>
    `;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}

function eliminarLoading() {
    const chat = document.getElementById("chat");
    const loadingMsg = chat.querySelector(".msg.bot.loading");
    if (loadingMsg) {
        chat.removeChild(loadingMsg);
    }
}



// Enviar con Enter
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("input");
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            enviar();
        }
    });

    // Mostrar chat al hacer clic en el ícono del bot
    const botIcon = document.getElementById("bot-icon");
    botIcon.addEventListener("click", toggleChat);

    // Mensaje inicial
});



