def manejar_reserva(texto):
    import re

    nombre = re.search(r"soy\s+(\w+)", texto.lower())
    fecha = re.search(r"\b\d{4}-\d{2}-\d{2}\b", texto)
    hora = re.search(r"\b\d{2}:\d{2}\b", texto)
    servicio = re.search(r"(limpieza|ortodoncia|blanqueamiento|endodoncia)", texto.lower())

    if nombre and fecha and hora and servicio:
        return f"✅ ¡Cita reservada! {nombre.group(1).capitalize()}, tu cita para {servicio.group(1)} ha sido agendada el {fecha.group()} a las {hora.group()}."
    else:
        return "Para reservar una cita necesito: tu nombre, servicio, fecha (YYYY-MM-DD) y hora (HH:MM)."
