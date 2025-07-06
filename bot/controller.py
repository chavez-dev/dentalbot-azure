# Requisitos:
# pip install langchain-openai langchain-core python-dotenv pydantic

import os
import dotenv
from pydantic import BaseModel
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.pydantic import PydanticOutputParser

dotenv.load_dotenv()

# Validación básica
AZURE_OPENAI_API_KEY = os.getenv("AZURE_INFERENCE_SDK_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_INFERENCE_SDK_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("OPENAI_API_VERSION", "2024-03-01-preview")

if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, DEPLOYMENT_NAME]):
    raise EnvironmentError("❌ Faltan variables de entorno necesarias para conectarse a Azure OpenAI.")

# 1. Modelo Pydantic
class RespuestaClinica(BaseModel):
    intencion: str
    valido: bool
    respuesta: str

# 2. Parser
parser = PydanticOutputParser(pydantic_object=RespuestaClinica)

# 3. Prompt Template
prompt = PromptTemplate(
    template="""
Eres un asistente profesional de DentalCare Tacna. Solo respondes preguntas sobre servicios, citas, horarios o contacto.

Sigue estos pasos (Chain-of-Thought):
1. Detecta la intención.
2. Verifica si es relevante para la clínica.
3. Decide si debes responder o rechazar.
4. Si respondes, hazlo en máximo 3 frases.
5. Devuelve un JSON con los campos: intencion, valido, respuesta.
6. La salida debe ser JSON estricto y válido.

{format_instructions}

Mensaje del usuario:
{mensaje}
""",
    input_variables=["mensaje"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# 4. Cliente Azure OpenAI
llm = AzureChatOpenAI(
    openai_api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=DEPLOYMENT_NAME,
    api_version=API_VERSION,
    temperature=0.7,
)

# 5. Cadena
chain = prompt | llm | parser

# 6. Función para responder
def responder_azure(mensaje_usuario: str) -> str:
    try:
        resultado: RespuestaClinica = chain.invoke({"mensaje": mensaje_usuario})
        print("✅ Respuesta estructurada:", resultado)
        print("✅ Respuesta:", resultado.respuesta)
        return resultado.respuesta
    except Exception as e:
        print("❌ Error al procesar el mensaje:", e)
        return "Lo siento, ocurrió un error procesando tu mensaje."
