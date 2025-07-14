import requests
import uuid
import re
from datetime import datetime, timedelta
import pytz

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableMap
from pydantic import BaseModel, Field
from dental_chain.llm import llm
from dental_chain.utils.constants import FORM_FIELDS, GOOGLE_FORMS_URL, SERVICIOS_LISTA
LIMA_TZ = pytz.timezone("America/Lima")


class Reserva(BaseModel):
    nombre: str = Field(description="Nombre completo del paciente")
    dni: str = Field(description="Número de DNI del paciente")
    celular: str = Field(description="Número de teléfono del paciente")
    servicio: str = Field(description="Servicio dental solicitado")
    fecha_programada: str = Field(
        description="Fecha y hora de la cita solicitada")
    tracking: str = Field(
        description="Código de verificación o seguimiento de Yape")


def enviar_a_google_forms(reserva_dict):
    print(reserva_dict)
    reserva = Reserva(**reserva_dict)
    reserva_id = str(uuid.uuid4())
    payload = {
        FORM_FIELDS["id"]: reserva_id,
        FORM_FIELDS["nombre"]: reserva.nombre,
        FORM_FIELDS["dni"]: reserva.dni,
        FORM_FIELDS["celular"]: reserva.celular,
        FORM_FIELDS["servicio"]: reserva.servicio.upper(),
        FORM_FIELDS["fecha_programada"]: reserva.fecha_programada,
        FORM_FIELDS["tracking"]: reserva.tracking,
    }
    try:
        response = requests.post(
            GOOGLE_FORMS_URL,
            data=payload,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "mode": "no-cors"
            }
        )
        confirmacion = confirmacion_chain.invoke(reserva.dict())
        return f"{confirmacion} \n\n ✅ Reserva registrada correctamente. Código: {reserva_id}"
    except Exception as e:
        print("❌ Error al enviar a Google Forms:", e)
        return "❌ No se pudo registrar la reserva"


def formatear_fecha(fecha_str: str) -> str:
    try:
        match = re.search(
            r"(lunes|martes|miércoles|jueves|viernes|sábado|domingo)[^\d]*(\d{1,2}) ?(am|pm)", fecha_str.lower())
        if match:
            dia_semana, hora, meridiano = match.groups()
            hora = int(hora)
            if meridiano == "pm" and hora < 12:
                hora += 12

            hoy = datetime.now(LIMA_TZ)
            dias_semana = ["lunes", "martes", "miércoles",
                           "jueves", "viernes", "sábado", "domingo"]
            objetivo_idx = dias_semana.index(dia_semana)

            dias_hasta = (objetivo_idx - hoy.weekday() + 7) % 7 or 7
            fecha_objetivo = hoy + timedelta(days=dias_hasta)
            fecha_formateada = fecha_objetivo.replace(
                hour=hora, minute=0, second=0, microsecond=0)

            return fecha_formateada.strftime("%d-%m-%Y %H:%M")
    except Exception as e:
        print("❌ Error al formatear fecha:", e)

    return fecha_str


# def decision_logic(output):
#     datos = output["datos"]
#     valido_datos = output["valido_datos"]
#     valido_servicio = output["valido_servicio"]

#     if valido_datos["valido"] and valido_servicio:
#         fecha_normalizada = formatear_fecha_chain.invoke(
#             datos["fecha_programada"])
#         datos["fecha_programada"] = fecha_normalizada
#         return datos

#     if not valido_datos["valido"]:
#         faltantes = valido_datos["faltantes"]
#         mensaje = "⚠️ No puedo realizar una reserva porque faltan los siguientes datos: " + \
#             ", ".join(faltantes)
#         return mensaje

#     servicio = datos.get("servicio", "").strip()
#     return f"🚫 El servicio '{servicio}' no está disponible en DentalCare Tacna. Revisa la lista de servicios ofrecidos."


def validar_servicio(reserva: dict) -> bool:
    servicio = reserva.get("servicio", "").strip().lower()
    return servicio in [s.lower() for s in SERVICIOS_LISTA]


def validar_datos(reserva: dict) -> dict:
    campos_requeridos = ["nombre", "dni", "celular",
                         "servicio", "fecha_programada", "tracking"]
    campos_faltantes = [
        campo for campo in campos_requeridos if not reserva.get(campo)]
    return {
        "valido": len(campos_faltantes) == 0,
        "faltantes": campos_faltantes
    }


def mensaje_error_si_incompleto(valido: bool) -> str:
    if valido:
        return "✅ Datos completos. Procediendo con la reserva..."
    return "⚠️ Faltan datos importantes. Asegúrate de proporcionar nombre, DNI, teléfono, servicio, fecha y código de Yape."


parser = JsonOutputParser(pydantic_object=Reserva)

prompt = ChatPromptTemplate.from_template("""
Eres un asistente de DentalCare Tacna. Un usuario ha proporcionado información para reservar una cita dental. 
Extrae los siguientes datos en formato JSON estrictamente válido, si no hay ningun dato, devuelve vacío en formato JSON:

- nombre
- dni
- celular
- servicio
- fecha_programada
- tracking

{format_instructions}

Mensaje:
{mensaje}
""")

confirmacion_prompt = ChatPromptTemplate.from_template("""
Devuelve solo el siguiente texto:
📅 ¡Reserva Confirmada!

🙋‍♂️ Paciente: {nombre}  
🦷 Servicio: {servicio}  
🗓️ Fecha programada: {fecha_programada}

📍 Te esperamos en DentalCare Tacna.
🕒 Por favor llega 10 minutos antes de tu cita.

Gracias por confiar en nosotros 💙
""")

confirmacion_usuario_prompt = ChatPromptTemplate.from_template("""
Analiza el siguiente mensaje y responde exclusivamente con "true" o "false".

Mensaje del usuario:
"{mensaje}"

- Responde "true" si el usuario está confirmando o aceptando los datos.
- Responde "false" si está cancelando, rechazando, tiene dudas o cambia de tema.

Tu respuesta debe ser solo: true o false, sin explicaciones, ni símbolos, tal cual.
""")

decision_prompt = ChatPromptTemplate.from_template("""
Actúa como un asistente de DentalCare Tacna. Has recibido los siguientes elementos:

- Datos extraídos del usuario:
{datos}

- Resultado de validación de datos:
{valido_datos}

- Validación del servicio:
{valido_servicio}

Sigue estas instrucciones cuidadosamente:

1. Si faltan datos requeridos, responde con un mensaje que comience con ⚠️, indicando los campos que faltan.
2. Si el servicio no es válido, responde con un mensaje que comience con 🚫, indicando que no está en la lista.
3. Si todo es válido, responde con un JSON puro (sin etiquetas, sin formato Markdown, sin comillas triples ni código bloque). El formato exacto debe ser:

REGLAS IMPORTANTES:
- No incluyas explicaciones ni texto adicional.
- No uses formato Markdown como ```json o etiquetas similares.
- Solo responde con el JSON si todo es correcto, o el mensaje de error si hay problemas.

{{
  "nombre": "...",
  "dni": "...",
  "celular": "...",
  "servicio": "...",
  "fecha_programada": "...",
  "tracking": "..."
}}

""")


confirmacion_usuario_chain = confirmacion_usuario_prompt | llm | StrOutputParser()
confirmacion_chain = confirmacion_prompt | llm | StrOutputParser()
validar_datos_chain = RunnableLambda(validar_datos)
validar_servicio_chain = RunnableLambda(validar_servicio)
formatear_fecha_chain = RunnableLambda(formatear_fecha)

decision_chain = decision_prompt | llm | StrOutputParser()
extract_chain = prompt.partial(
    format_instructions=parser.get_format_instructions()) | llm | parser
validacion_chain = RunnableMap({
    "datos": lambda r: r,
    "valido_datos": validar_datos_chain,
    "valido_servicio": validar_servicio_chain,
})
# decision_chain = RunnableLambda(decision_logic)

normalizar_fecha_chain = RunnableLambda(
    lambda d: {
        **d,
        "datos": {
            **d["datos"],
            "fecha_programada": formatear_fecha_chain.invoke(d["datos"]["fecha_programada"])
            if d["datos"].get("fecha_programada") else ""
        }
    }
)


reserva_chain = extract_chain | validacion_chain | normalizar_fecha_chain | decision_chain
