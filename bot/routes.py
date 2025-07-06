import asyncio
from flask import Blueprint, request, jsonify
from bot.controller import responder_azure

bot_bp = Blueprint("bot", __name__)

@bot_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mensaje_usuario = data.get("prompt", "")
    respuesta = asyncio.run(responder_azure(mensaje_usuario))
    return jsonify({"response": respuesta})
