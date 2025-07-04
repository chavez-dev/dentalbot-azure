# Requisitos:
# pip install langchain-openai langchain-core python-dotenv pydantic

import os
import dotenv
from pydantic import BaseModel
from langchain_openai import AzureChatOpenAI  # integración Azure en LangChain
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.pydantic import PydanticOutputParser
dotenv.load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_INFERENCE_SDK_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_INFERENCE_SDK_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")  # eg. "phi-4"
API_VERSION = os.getenv("OPENAI_API_VERSION", "2024-03-01-preview")

# 1. Modelo Pydantic para salida estructurada
class RespuestaClinica(BaseModel):
    intencion: str
    valido: bool
    respuesta: str

# 2. Parser con JsonOutputParser
parser = PydanticOutputParser(pydantic_object=RespuestaClinica)

# 3. Plantilla de prompt con CoT y formateo
prompt = PromptTemplate(
    template="""
Eres un asistente profesional de DentalCare Tacna. Solo respondes preguntas sobre servicios, citas, horarios o contacto.

Sigue estos pasos (Chain‑of‑Thought):
1. Detecta intención.
2. Verifica si es relevante para la clínica.
3. Decide si responder o rechazar.
4. Si respondes, hazlo en máximo 3 frases.
5. Devuelve un JSON con los campos: intencion, valido, respuesta.

{format_instructions}

Mensaje del usuario:
{mensaje}
""",
    input_variables=["mensaje"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# 4. Configura el cliente LLM de Azure
llm = AzureChatOpenAI(
    openai_api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=DEPLOYMENT_NAME,
    api_version=API_VERSION,
    temperature=0.7,
)

# 5. Construye la cadena LangChain: prompt → LLM → parser
chain = prompt | llm | parser

# 6. Función para responder solo con el campo "respuesta"
def responder_azure(mensaje_usuario: str) -> str:
    try:
        resultado: RespuestaClinica = chain.invoke({"mensaje": mensaje_usuario})
        return resultado.respuesta
    except Exception as e:
        print("❌ Error:", e)
        return "Lo siento, ocurrió un error procesando tu mensaje."

# 🧪 Prueba básica
if __name__ == "__main__":
    print(responder_azure("¿Cuál es su horario de atención?"))
