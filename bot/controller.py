from dental_chain.procesamiento.detectar_preguntas import tagging_chain
from dental_chain.respuestas.generar_respuestas_de_preguntas import respuesta_chain
from dental_chain.resumen.convertir_a_markdown import markdown_chain
from dental_chain.procesamiento.detectar_intencion import intencion_chain
from dental_chain.conversation.chat_memoria import chat_chain  # ← memoria chatbot
from langchain_core.messages import HumanMessage, AIMessage
import json
from dental_chain.resumen.reserva_confirmacion import reserva_chain

chat_conversation = []

async def responder_azure(mensaje: str) -> str:
    try:
        intencion = intencion_chain.invoke({"mensaje": mensaje})
        print(f"🧭 Intención detectada: {intencion}")

        if intencion == "reserva":
            resultado = reserva_chain.invoke({"mensaje": mensaje})
            return resultado

        elif intencion == "pregunta":
            preguntas = tagging_chain.invoke({"mensaje": mensaje})
            print("🔹 Preguntas detectadas:")
            print(json.dumps(preguntas, indent=2, ensure_ascii=False))
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

        elif intencion == "chat":
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

    except Exception as e:
        print("❌ Error en pipeline:", e)
        return "Lo siento, ocurrió un error procesando tu mensaje."
