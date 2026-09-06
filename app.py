import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
# Pega aquí tu API KEY de Google AI Studio entre las comillas
GOOGLE_API_KEY = "AQ.Ab8RN6KUSXA8-pfqEY50ZVRvVtWiLd6LPhsoMtkYwu4FJ7kcyw"

# Configuramos Gemini
genai.configure(api_key=GOOGLE_API_KEY)
# Usamos un modelo rápido y bueno para chat
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Runner Caffè Italiano", page_icon="☕")

# --- LA PERSONALIDAD DE LA IA ---
# Estas son las instrucciones maestras para Gemini.
INSTRUCCIONES_SISTEMA = """
Eres el encargado (o un cliente exigente) de un café muy concurrido en Roma.
El usuario es un "Runner" (ayudante de camarero) aprendiendo italiano.
Tu objetivo es ayudarle a practicar situaciones reales.

REGLAS DE COMPORTAMIENTO:
1.  **Rol Principal:** Mantén siempre tu papel de italiano nativo en el café. Sé dinámico, a veces impaciente, a veces amable, como en la vida real.
2.  **Idioma:** Háblale SIEMPRE en italiano para la simulación.
3.  **Correcciones (El Profesor Oculto):** Si el usuario comete un error gramatical o usa una palabra incorrecta en hostelería, detén la simulación momentáneamente.
    *   Usa un formato claro, por ejemplo: "⚠️ [CORRECCIÓN: ... explicación en ESPAÑOL ...]"
    *   Después de corregir en español, vuelve inmediatamente a tu personaje en italiano y repite la frase o continúa la acción.
4.  **Variedad:** Nunca repitas la misma conversación. Cambia los pedidos, los problemas y tu estado de ánimo.

EJEMPLOS DE SITUACIONES PARA INICIAR (Empieza tú):
*   "Scusi, ragazzo, questo caffè è freddo. Me lo cambia?"
*   "Senti, al tavolo 12 manca l'acqua e lo zucchero, sbrigati!"
*   "Buongiorno, per me un macchiato caldo e un cornetto alla crema, da portare via."
"""

# --- INTERFAZ DE LA APP ---
st.title("☕ Caffè Roma: Práctica para Runner")
st.caption("Habla en italiano. Gemini te corregirá en español si te equivocas.")

# Inicializar el historial del chat si no existe
if "history" not in st.session_state:
    # Iniciamos el chat con las instrucciones y un primer saludo de la IA
    st.session_state.chat_session = model.start_chat(history=[
        {'role': 'user', 'parts': [INSTRUCCIONES_SISTEMA + "\n\nEmpieza la simulación ahora."]},
    ])
    st.session_state.history = st.session_state.chat_session.history

# Mostrar el historial de mensajes
for message in st.session_state.history:
    # Ocultamos el mensaje de sistema inicial para que no moleste
    if INSTRUCCIONES_SISTEMA in message.parts[0].text:
        continue
        
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Campo para que el usuario escriba
if prompt := st.chat_input("Escribe tu respuesta en italiano..."):
    # 1. Mostrar mensaje del usuario
    st.chat_message("user").markdown(prompt)
    
    # 2. Enviar a Gemini y obtener respuesta
    try:
        response = st.session_state.chat_session.send_message(prompt)
        # 3. Mostrar respuesta de la IA
        st.chat_message("assistant").markdown(response.text)
    except Exception as e:
        st.error(f"Error al conectar con Gemini: {e}")

# Botón para reiniciar la conversación
if st.button("🔄 Nueva situación"):
    del st.session_state.chat_session
    del st.session_state.history
    st.rerun()
