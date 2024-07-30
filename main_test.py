from main import get_audio_from_text

get_audio_from_text(
    base_title="",
    input_text="""
 Me gusta vestir ropa cómoda durante el fin de semana.
 Este libro puede valer mucho en unos años.
 Vi a un niño caer del columpio, pero no se lastimó.
 Vamos a construir una casa en el campo.
 Debes sustituir el azúcar con miel para una opción más saludable.
 Es importante incluir frutas y verduras en tu dieta diaria.
 Podemos atribuir el éxito del proyecto al trabajo en equipo.
 Al llegar a casa, lo primero que hago es desvestirse y ponerme ropa cómoda.
 ¿Quieres venir a la fiesta - Por supuesto!
 Voy a poner la mesa para la cena.
                """,
    original_lan="",
    target_lan="en",
    is_slow_org=False,
    is_slow_tra=False,
    silence_seconds=5,
    first_original=True
)
