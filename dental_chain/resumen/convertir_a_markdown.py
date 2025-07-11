from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from dental_chain.llm import llm

class ResumenFinal(BaseModel):
    respuesta: str

prompt = PromptTemplate(
    input_variables=["respuestas_json"],
    template="""
Toma la siguiente lista de pares pregunta-respuesta en formato JSON:

{respuestas_json}

No inventes ni agregues información adicional.

Devuelve dos versiones:
1. "respuesta": Las mismas respuestas con formato Markdown.
2. "respuesta2": Las mismas respuestas en texto plano (sin formato).

Formato de salida:
{{ 
  "respuesta": "contenido en Markdown", 
  "respuesta2": "contenido en texto plano" 
}}
"""
)
parser = JsonOutputParser(pydantic_object=ResumenFinal)
markdown_chain = prompt | llm | parser
