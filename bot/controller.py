from dental_chain.etapa1 import tagging_chain
from dental_chain.etapa2 import respuesta_chain
from dental_chain.etapa3 import markdown_chain
from dental_chain.etapa0 import simple_chain
from dental_chain.etapa5 import chat_chain  # ← memoria chatbot
from langchain_core.messages import HumanMessage, AIMessage
import json
from dental_chain.etapa6_reserva import reserva_chain

# 🧠 Historial de conversación en memoria (por sesión)
chat_conversation = []

async def responder_azure(mensaje: str) -> str:
    try:
        ##############################
        # Hola, quiero una cita para ortodoncia el viernes a las 10:30 a.m. Mi nombre es Carla López, mi DNI es 72398412, celular 955431298. Ya pagué con Yape, el código es 8472XYC.

        if any(x in mensaje.lower() for x in ["reservar", "cita", "agenda", "yape", "atención el", "confirmar cita"]):
            print("📌 Posible mensaje de reserva detectado:")
            resultado = reserva_chain.invoke({"mensaje": mensaje})
            print("📝 Resultado reserva_chain:")
            print(resultado)
            return resultado
        #########################33
        # Etapa 1: detectar preguntas
        preguntas = tagging_chain.invoke({"mensaje": mensaje})
        print("🔹 Preguntas detectadas:")
        print(json.dumps(preguntas, indent=2, ensure_ascii=False))

        if not preguntas:
            # 🔁 Si no hay preguntas, usa memoria tipo chatbot
            chat_conversation.append(HumanMessage(content=mensaje))
            respuesta = chat_chain.invoke({"chat_conversation": chat_conversation})
            chat_conversation.append(AIMessage(content=respuesta))
            print("🧠 Respuesta con memoria:")
            print(respuesta)
            print("🔹 Conversación en memoria:")
            for msg in chat_conversation:
                print(f"  [{msg.type}] {msg.content}")
            return respuesta

        # Etapa 2: responder cada pregunta detectada
        respuestas = [respuesta_chain.invoke({"pregunta": p["texto"]}) for p in preguntas]
        print("🔹 Respuestas generadas:")
        print(json.dumps(respuestas, indent=2, ensure_ascii=False))

        # Etapa 3: resumen en markdown
        respuestas_json = json.dumps(respuestas, ensure_ascii=False)
        resumen = markdown_chain.invoke({"respuestas_json": respuestas_json})
        print("🔹 Markdown generado:")
        print(json.dumps(resumen, indent=2, ensure_ascii=False))

        # 🧠 Agrega a la memoria de conversación
        chat_conversation.append(HumanMessage(content=mensaje))
        chat_conversation.append(AIMessage(content=resumen["respuesta2"]))
        print("🔹 Conversación en memoria:")
        for msg in chat_conversation:
            print(f"  [{msg.type}] {msg.content}")

        return resumen["respuesta"]

    except Exception as e:
        print("❌ Error en pipeline:", e)
        return "Lo siento, ocurrió un error procesando tu mensaje."
