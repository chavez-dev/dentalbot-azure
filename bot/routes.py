from flask import Blueprint, request, jsonify
from .controller import responder_azure

bot_bp = Blueprint("bot", __name__)

@bot_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mensaje_usuario = data.get("prompt", "")
    respuesta = responder_azure(mensaje_usuario)
    return jsonify({"response": respuesta})
