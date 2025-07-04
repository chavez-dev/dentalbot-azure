import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración desde el .env
endpoint = os.getenv("AZURE_INFERENCE_SDK_ENDPOINT")
model_name = os.getenv("DEPLOYMENT_NAME")
key = os.getenv("AZURE_INFERENCE_SDK_KEY")

# Cliente del modelo
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Función para responder mensajes del usuario
def responder_azure(mensaje_usuario):
    try:
        response = client.complete(
            messages=[
                SystemMessage(content="""
                Eres un asistente profesional y conciso de la clínica DentalCare Tacna.

                    🎯 Instrucciones:
                    - Usa un tono cercano y respetuoso, como un recepcionista atento.
                    - Responde con un máximo de 2 a 3 frases por turno.
                    - Si el usuario pregunta por información de contacto, proporciónala de manera directa pero cálida.
                    - Si ya se ha mencionado información recientemente, evita repetirla a menos que sea necesario.
                    - Anima al usuario a continuar si parece interesado (por ejemplo, "¿Deseas agendar una cita?" o "¿Te gustaría saber más sobre ese servicio?").


                    📍 Clínica: DentalCare Tacna
                    Dirección: Av. Bolognesi 123, Tacna, Perú
                    Teléfono: +51 952 123 456
                    Correo: contacto@dentalcaretacna.pe
                    Horario: Lun–Vie 9AM–6PM | Sáb 9AM–1PM | Dom cerrado
                """),
                UserMessage(content=mensaje_usuario)
            ],
            model=model_name,
            max_tokens=700
        )

        return response.choices[0].message.content

    except Exception as e:
        import traceback
        print("⚠️ Error al conectar con Azure:", e)
        traceback.print_exc()  # Imprime el error completo
        return "Lo siento, ocurrió un error al procesar tu mensaje."
