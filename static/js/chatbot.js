// Mostrar/ocultar ventana del bot
function toggleChat() {
    const chatWindow = document.getElementById("chat-window");
    if (chatWindow.classList.contains("hidden")) {
        chatWindow.classList.remove("hidden");
        document.getElementById("input").focus();
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

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: texto }),
        });

        const data = await res.json();
        agregarMensaje("bot", data.response);
    } catch (err) {
        console.error(err);
        agregarMensaje("bot", "⚠️ Ocurrió un error al conectar con el servidor.");
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
    agregarMensaje("bot", "👋 ¡Hola! Soy DentalBot. ¿En qué puedo ayudarte?");
});
