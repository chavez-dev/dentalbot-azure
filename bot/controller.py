from dental_chain.etapa1 import tagging_chain
from dental_chain.etapa2 import respuesta_chain
from dental_chain.etapa3 import markdown_chain
from dental_chain.etapa0 import simple_chain  # <- esta es nueva
import json

async def responder_azure(mensaje: str) -> str:
    try:
        # Etapa 1: detección de preguntas
        preguntas = tagging_chain.invoke({"mensaje": mensaje})
        print("🔹 Preguntas detectadas:")
        print(json.dumps(preguntas, indent=2, ensure_ascii=False))

        if not preguntas:
            # No hay preguntas, usar cadena simple
            respuesta = simple_chain.invoke({"mensaje": mensaje})
            print("🔹 Respuesta simple:")
            print(respuesta)
            return respuesta["respuesta"]  # Debe devolver {"respuesta": "..."}
        
        # Etapa 2: responder cada pregunta
        respuestas = [respuesta_chain.invoke({"pregunta": p["texto"]}) for p in preguntas]
        print("🔹 Respuestas generadas:")
        print(json.dumps(respuestas, indent=2, ensure_ascii=False))

        # Etapa 3: resumen en markdown
        respuestas_json = json.dumps(respuestas, ensure_ascii=False)
        resumen = markdown_chain.invoke({"respuestas_json": respuestas_json})
        print("🔹 Markdown generado:")
        print(json.dumps(resumen, indent=2, ensure_ascii=False))

        return resumen["respuesta"]

    except Exception as e:
        print("❌ Error en pipeline:", e)
        return "Lo siento, ocurrió un error procesando tu mensaje."
