from dental_chain.etapa1 import tagging_chain
from dental_chain.etapa2 import respuesta_chain
from dental_chain.etapa3 import markdown_chain
from dental_chain.etapa0 import simple_chain
from dental_chain.etapa5 import chat_chain  # ← memoria chatbot
import json

# 🧠 Historial de conversación en memoria (por sesión)
chat_conversation = []

async def responder_azure(mensaje: str) -> str:
    try:
        preguntas = tagging_chain.invoke({"mensaje": mensaje})
        print("🔹 Preguntas detectadas:")
        print(json.dumps(preguntas, indent=2, ensure_ascii=False))

        if not preguntas:
            # 🔁 Si no hay preguntas, usa memoria tipo chatbot
            chat_conversation.append(("user", mensaje))
            respuesta = chat_chain.invoke({"chat_conversation": chat_conversation})
            chat_conversation.append(("ai", respuesta))
            print("🧠 Respuesta con memoria:")
            print(respuesta)
            print("🔹 Conversación el chat:")
            print(chat_conversation)
            return respuesta

        # Etapa 2: responder cada pregunta
        respuestas = [respuesta_chain.invoke({"pregunta": p["texto"]}) for p in preguntas]
        print("🔹 Respuestas generadas:")
        print(json.dumps(respuestas, indent=2, ensure_ascii=False))

        # Etapa 3: resumen en markdown
        respuestas_json = json.dumps(respuestas, ensure_ascii=False)
        resumen = markdown_chain.invoke({"respuestas_json": respuestas_json})
        print("🔹 Markdown generado:")
        print(json.dumps(resumen, indent=2, ensure_ascii=False))
        chat_conversation.append(("user", mensaje))
        chat_conversation.append(("ai", resumen["respuesta2"]))
        print("🔹 Conversación el chat:")
        print(chat_conversation)
        return resumen["respuesta"]

    except Exception as e:
        print("❌ Error en pipeline:", e)
        return "Lo siento, ocurrió un error procesando tu mensaje."
