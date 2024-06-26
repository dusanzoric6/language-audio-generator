from main import get_audio_from_text

get_audio_from_text(
    base_title="",
    input_text="""
                ingeniero.
 me gusta tocar el piano.
 me gusta montar en bici.
 por supuesto, eso sí.
 al principio.
 al final.
 tímida.
 habladora.
 oscuridad.
 oscuro.
 me encanta.
                """,
    original_lan="",
    target_lan="en",
    is_slow_org=False,
    is_slow_tra=False,
    silence_seconds=1,
    first_original=True
)
