from dotenv import load_dotenv
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Cargar variables del archivo .env
load_dotenv()

# Leer variables de entorno (sin claves en el código)
endpoint = os.getenv("AZURE_INFERENCE_SDK_ENDPOINT")
model_name = os.getenv("DEPLOYMENT_NAME")
key = os.getenv("AZURE_INFERENCE_SDK_KEY")

# Inicializar cliente de Azure
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Consulta al modelo
response = client.complete(
    messages=[
        SystemMessage(content="""
            Eres un asistente virtual profesional y cordial de la clínica dental **DentalCare Tacna**. Tu función es brindar información precisa y clara sobre la clínica.

            **Información oficial:**
            - Dirección: Av. Bolognesi 123, Tacna, Perú
            - Teléfono: +51 952 123 456
            - Correo: contacto@dentalcaretacna.pe
            - Horarios: Lun-Vie 9am–6pm, Sáb 9am–1pm, Domingos cerrado

            Responde con amabilidad y profesionalismo.
        """),
        UserMessage(content="¿Cuál es el número de teléfono de la clínica?")
    ],
    model=model_name,
    max_tokens=500
)

# Mostrar respuesta
print(response.choices[0].message.content)
