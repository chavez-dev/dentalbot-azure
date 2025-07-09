# dental_chain/etapa6_reserva.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field
from dental_chain.llm import llm

# 1️⃣ Modelo Pydantic para validar y estructurar los datos de la reserva
class Reserva(BaseModel):
    nombre: str = Field(description="Nombre completo del paciente")
    dni: str = Field(description="Número de DNI del paciente")
    telefono: str = Field(description="Número de teléfono del paciente")
    servicio: str = Field(description="Servicio dental solicitado")
    fecha_programada: str = Field(description="Fecha y hora de la cita solicitada")
    tracking: str = Field(description="Código de verificación o seguimiento de Yape")

# 2️⃣ Parser para el modelo
parser = JsonOutputParser(pydantic_object=Reserva)

# 3️⃣ Prompt para extraer datos de reserva
prompt = ChatPromptTemplate.from_template("""
Eres un asistente de DentalCare Tacna. Un usuario ha proporcionado información para reservar una cita dental. 
Extrae los siguientes datos en formato JSON estrictamente válido:

- nombre
- dni
- telefono
- servicio
- fecha_programada
- tracking

{format_instructions}

Mensaje:
{mensaje}
""")

# 4️⃣ Chain principal (prompt + LLM + parser)
reserva_chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser

# 5️⃣ Runnable que simula enviar los datos a un endpoint (aquí solo imprime)
def simular_envio(reserva: Reserva):
    print("📤 Enviando datos al sistema de reservas (simulado):")
    print(reserva.json(indent=2, ensure_ascii=False))
    return "✅ Reserva procesada correctamente"

# 6️⃣ Pipeline: extraer datos → enviar (simulado)
reserva_pipeline = (
    RunnableLambda(lambda msg: {"mensaje": msg}) |
    reserva_chain |
    RunnableLambda(simular_envio)
)

# 7️⃣ Prueba local
if __name__ == "__main__":
    mensaje_prueba = """
    Hola, soy Carla Rivera, mi DNI es 12345678, mi teléfono es 987654321.
    Quiero una limpieza dental para el martes a las 9 am. El código de Yape es ABC123.
    """
    resultado = reserva_pipeline.invoke(mensaje_prueba)
    print(resultado)
