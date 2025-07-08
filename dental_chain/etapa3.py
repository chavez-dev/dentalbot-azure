from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from dental_chain.llm import llm

class ResumenFinal(BaseModel):
    respuesta: str

prompt = PromptTemplate(
    input_variables=["respuestas_json"],
    template="""
Dada la siguiente lista de pares pregunta-respuesta en formato JSON:
Recuerda lo que el usuario ha dicho antes y da continuidad a la conversación.

{respuestas_json}

Genera una respuesta única, clara y coherente basada en toda la información. Devuelve dos versiones:

1. Una respuesta en **formato Markdown**, con títulos, listas u otros elementos si es necesario.
2. La misma respuesta pero en texto plano (sin ningún formato Markdown).

Devuelve el resultado como un JSON con la siguiente estructura:
{{ 
  "respuesta": "respuesta en formato markdown aquí", 
  "respuesta2": "misma respuesta en texto plano aquí" 
}}
"""
)
parser = JsonOutputParser(pydantic_object=ResumenFinal)
markdown_chain = prompt | llm | parser
