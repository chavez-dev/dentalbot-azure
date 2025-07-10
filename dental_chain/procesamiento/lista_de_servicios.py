from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from dental_chain.llm import llm
from dental_chain.utils.constants import SERVICIOS_LISTA

class Servicio(BaseModel):
    servicio: str = Field(description="Nombre del servicio mencionado")
    descripcion: str = Field(description="Descripción breve del servicio")
    tipo: str = Field(description="Clasificación general del servicio, por ejemplo: Preventivo, Estético, Correctivo, etc.")
    frecuencia_recomendada: str = Field(description="Con qué frecuencia se recomienda realizar este servicio")

parser = JsonOutputParser(pydantic_object=Servicio)

prompt = ChatPromptTemplate.from_template("""
Eres un asistente de DentalCare Tacna. Los servicios disponibles son:

{servicios}

A partir del siguiente mensaje del usuario, identifica UN servicio mencionado de la lista y genera:
- una breve descripción (máximo 3 frases),
- el tipo de servicio (por ejemplo: Preventivo, Estético, Correctivo, Quirúrgico),
- y la frecuencia recomendada para realizarlo.

Responde solo si el servicio está en la lista.
Devuelve en formato JSON estricto con los campos: servicio, descripcion, tipo, frecuencia_recomendada.

{format_instructions}

Mensaje:
{mensaje}
""")

servicios_str = "\n".join([f"- {s}" for s in SERVICIOS_LISTA])

etapa4_chain = prompt.partial(servicios=servicios_str, format_instructions=parser.get_format_instructions()) | llm | parser
