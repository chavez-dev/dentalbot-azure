from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from dental_chain.llm import llm

class ResumenFinal(BaseModel):
    respuesta: str

prompt = PromptTemplate(
    input_variables=["respuestas_json"],
    template="""
Convierte esta lista de pares pregunta-respuesta en una sola respuesta clara en Markdown (que sea entendible).

{respuestas_json}

Devuelve solo un JSON como este:
{{ "respuesta": "texto markdown aquí" }}
"""
)

parser = JsonOutputParser(pydantic_object=ResumenFinal)
markdown_chain = prompt | llm | parser
