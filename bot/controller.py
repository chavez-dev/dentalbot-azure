import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from dotenv import load_dotenv
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
    mensajes = [
        SystemMessage(content="""
        Eres un asistente profesional y conciso de la clínica DentalCare Tacna.

        🎯 Instrucciones:
        - Usa un tono cercano y respetuoso, como un recepcionista atento.
        - Responde con un máximo de 2 a 3 frases por turno.
        - Proporciona datos de contacto si se solicita.
        - Evita repetir lo ya dicho a menos que sea necesario.
        - Anima al usuario a seguir interactuando.
        
        📍 Clínica: DentalCare Tacna
        Dirección: Av. Bolognesi 123, Tacna, Perú
        Teléfono: +51 952 123 456
        Correo: contacto@dentalcaretacna.pe
        Horario: Lun–Vie 9AM–6PM | Sáb 9AM–1PM | Dom cerrado
        
        """),

        # Conversación simulada
        UserMessage(content="Hola"),
        AssistantMessage(content="¡Hola! Bienvenido a DentalCare Tacna. ¿En qué puedo ayudarte hoy?"),
        UserMessage(content="Quiero saber sobre limpieza dental"),
        AssistantMessage(content="La limpieza dental elimina sarro y placa para prevenir enfermedades. ¿Deseas agendar una cita?"),
        # Mensaje actual del usuario
        UserMessage(content=mensaje_usuario)
    ]
    try:
        response = client.complete(
            messages=mensajes,
            model=model_name,
            max_tokens=700,
            temperature=0
        )
        return response.choices[0].message.content

    except Exception as e:
        print("❌ Error:", e)
        return "Ocurrió un error procesando tu mensaje."
