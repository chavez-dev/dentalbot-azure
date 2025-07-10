from dental_chain.procesamiento.detectar_preguntas import tagging_chain
from dental_chain.respuestas.generar_respuestas_de_preguntas import respuesta_chain
from dental_chain.resumen.convertir_a_markdown import markdown_chain
from dental_chain.procesamiento.detectar_intencion import intencion_chain
from dental_chain.conversacion.chat_memoria import chat_chain
from dental_chain.resumen.reserva_confirmacion import reserva_chain, enviar_a_google_forms
from langchain_core.messages import HumanMessage, AIMessage
import json

# Lista para mantener la conversación del chat
chat_conversation = []

# Variable global para almacenar reserva pendiente
pending_reserva = None

async def responder_azure(mensaje: str) -> str:
    global pending_reserva

    try:
        intencion = intencion_chain.invoke({"mensaje": mensaje})
        print(f"🧭 Intención detectada: {intencion}")

        # Si hay una reserva pendiente y el usuario responde Sí
        if pending_reserva and mensaje.strip().lower() in ["sí", "si", "yes"]:
            resultado = enviar_a_google_forms(pending_reserva)
            pending_reserva = None
            return resultado

        # Si hay una reserva pendiente y el usuario responde No
        elif pending_reserva and mensaje.strip().lower() == "no":
            pending_reserva = None
            return "❌ Reserva cancelada. Por favor, proporciona nuevamente los datos si deseas reservar otra cita."

        # Si la intención es hacer una reserva
        elif intencion == "reserva":
            resultado = reserva_chain.invoke({"mensaje": mensaje})
            if isinstance(resultado, dict):  # Devuelve los datos formateados sin reservar aún
                pending_reserva = resultado
                resumen = (
                    "📋 Estos son los datos de tu reserva:\n\n"
                    f"🧑 Nombre: {resultado['nombre']}\n"
                    f"🆔 DNI: {resultado['dni']}\n"
                    f"📞 Celular: {resultado['celular']}\n"
                    f"🦷 Servicio: {resultado['servicio']}\n"
                    f"📅 Fecha: {resultado['fecha_programada']}\n"
                    f"💳 Código Yape: {resultado['tracking']}\n\n"
                    "¿✅ Son correctos estos datos? (Responde Sí o No)"
                )
                return resumen

            else:
                return resultado

        # Si es una pregunta
        elif intencion == "pregunta":
            preguntas = tagging_chain.invoke({"mensaje": mensaje})
            print("🔹 Preguntas detectadas:")
            print(json.dumps(preguntas, indent=2, ensure_ascii=False))
            respuestas = [respuesta_chain.invoke({"pregunta": p["texto"]}) for p in preguntas]
            print("🔹 Respuestas generadas:")
            print(json.dumps(respuestas, indent=2, ensure_ascii=False))

            # Resumen en markdown
            respuestas_json = json.dumps(respuestas, ensure_ascii=False)
            resumen = markdown_chain.invoke({"respuestas_json": respuestas_json})
            print("🔹 Markdown generado:")
            print(json.dumps(resumen, indent=2, ensure_ascii=False))

            chat_conversation.append(HumanMessage(content=mensaje))
            chat_conversation.append(AIMessage(content=resumen["respuesta2"]))
            return resumen["respuesta"]

        # Si es un mensaje general del chat
        elif intencion == "chat":
            chat_conversation.append(HumanMessage(content=mensaje))
            respuesta = chat_chain.invoke({"chat_conversation": chat_conversation})
            chat_conversation.append(AIMessage(content=respuesta))
            return respuesta

    except Exception as e:
        print("❌ Error en pipeline:", e)
        return "Lo siento, ocurrió un error procesando tu mensaje."
