import streamlit as st
import math
import json


st.set_page_config(page_title="Cálculo de Palos", layout="centered")

st.title("📏 Cálculo Profesional de Palos para Núcleo")
st.write("Unidad de medida: **mm**")

# --- Función de validación ---
def validar(valor, nombre):
    if valor <= 0:
        st.error(f"❌ El valor de **{nombre}** debe ser mayor que 0.")
        st.stop()
    return valor
# --- Boton copiar reporte WhatsApp ---
def boton_copiar_reporte(texto):

    texto_js = json.dumps(texto)

    st.markdown(f"""
        <textarea id="reporte_oculto" style="position:absolute; left:-9999px; top:-9999px;">{texto}</textarea>

        <button id="btn_copiar_reporte" style="
            background-color:#4CAF50;
            color:white;
            padding:10px 18px;
            border:none;
            border-radius:8px;
            font-size:16px;
            font-weight:bold;
            cursor:pointer;
            display:flex;
            align-items:center;
            gap:8px;
            transition:0.2s;
        ">
        📄 Copiar reporte
        </button>

        <script>
        const boton = document.getElementById("btn_copiar_reporte");
        boton.addEventListener("click", () => {{
            const area = document.getElementById("reporte_oculto");
            area.select();
            document.execCommand("copy");

            boton.style.backgroundColor = "#2E7D32";
            boton.innerText = "✔ Copiado";
            setTimeout(() => {{
                boton.style.backgroundColor = "#4CAF50";
                boton.innerText = "📄 Copiar reporte";
            }}, 1500);
        }});
        </script>
    """, unsafe_allow_html=True)

# --- Generar Reporte WS ---
import urllib.parse

def generar_texto_reporte(caso, cand_csjv, size_csjv, tp_csjv, 
                          cand_csjp, size_csjp, tp_csjp, tp_entero_py):

    texto = f"""
📌 *Reporte del Proyecto*
Caso aplicado: {caso}

🪟 *Ventanas*
• Palos necesarios: {cand_csjv}
• Tamaño por C/U: {size_csjv} mm
• Palos originales: {tp_csjv}

🦵 *Yugo (3 piernas)*
• Palos necesarios: {cand_csjp}
• Tamaño por C/U: {size_csjp} mm
• Palos originales: {tp_csjp}

📦 *Total del Proyecto*
Palos enteros necesarios: {tp_entero_py}
"""
    return texto

# --- Funcion Mostrar Resultados ---
def mostrar_resultados(caso, cand_csjv, size_csjv, tp_csjv, cand_csjp, size_csjp, tp_csjp, tp_entero_py):
    st.success(f"Caso aplicado: **{caso}**")

    # Bloque 1: Ventanas
    with st.container():
        st.subheader("Palos para Cubrir las dos ventanas")
        col1, col2, col3 = st.columns(3)

        col1.metric("Cantidad de palos", cand_csjv)
        col2.metric("Tamaño de corte por C/U", f"{size_csjv} mm")
        col3.metric("Palos tamaño original", tp_csjv)

        st.write("---")

    # Bloque 2: Yugo
    with st.container():
        st.subheader("Palos para Cubrir el Yugo de las tres piernas")
        col1, col2, col3 = st.columns(3)

        col1.metric("Cantidad de palos", cand_csjp)
        col2.metric("Tamaño de corte por C/U", f"{size_csjp} mm")
        col3.metric("Palos tamaño original", tp_csjp)

        st.write("---")

    # Bloque 3: Total del proyecto
    with st.container():
        st.subheader("Total del Proyecto")
        st.metric("Palos enteros necesarios (Cortar-Pegar)", tp_entero_py)

    # Generar Text reporte de WhatsApp
    texto = generar_texto_reporte(
        caso, cand_csjv, size_csjv, tp_csjv,
        cand_csjp, size_csjp, tp_csjp,
        tp_entero_py
    )

    st.write("### Copiar reporte")
    st.code(texto, language="markdown")



# --- Entradas ---
st.subheader("🔧 Parámetros de entrada")

w = validar(st.number_input("Tamaño de la Hoja (w)", min_value=100.0, step=1.0), "w")
v = validar(st.number_input("Tamaño de la Ventana (v)", min_value=100.0, step=1.0), "v")
l = validar(st.number_input("Largo de la Pierna (l)", min_value=100.0, step=1.0), "l")

st.write("---")

# Ruler
r_default = 45
mantener = st.radio("Tamaño del ruler", ["Mantener 45 mm", "Cambiar valor"])

if mantener == "Cambiar valor":
    r = validar(st.number_input("Nuevo valor del ruler (r)", min_value=45.0, step=1.0), "r")
else:
    r = r_default

st.write("---")

# Cool stree
cs_default = 2750
mantener = st.radio("Tamaño del cool stree", ["Mantener 2750 mm", "Cambiar valor"])

if mantener == "Cambiar valor":
    tmcs = validar(st.number_input("Nuevo valor del cool stree (tmcs)", min_value=2750.0, step=1.0), "tmcs")
else:
    tmcs = cs_default

st.write("---")

# --- Cálculos base ---
cand_csjp = math.ceil(w / r) * 3
cand_csjv = math.ceil(v / r) * 2

# --- Procesamiento ---
st.subheader("📊 Resultados del cálculo")

# Evaluación de casos
if tmcs == l + r:
    size_csjv = w
    size_csjp = 0
    mm_tp_csjv = cand_csjv * size_csjv     
    tp_csjv = math.ceil(mm_tp_csjv / tmcs)

    tp_csjp = 0
    
    tp_entero_py = tp_csjp + tp_csjv + cand_csjp

    mostrar_resultados("Tamano del CS igual al Largo", cand_csjv, size_csjv, tp_csjv, cand_csjp, size_csjp, tp_csjp, tp_entero_py)
    
elif (tmcs + w) == l + r:
    size_csjv = w
    size_csjp = w
    
    mm_tp_csjv = cand_csjv * size_csjv     
    tp_csjv = math.ceil(mm_tp_csjv / tmcs)
    
    if size_csjp > (tmcs/2):
        tp_csjp = cand_csjp
    else:
        mm_tp_csjp = cand_csjp * size_csjp
        tp_csjp = math.ceil(mm_tp_csjp / tmcs)
    
    tp_entero_py = tp_csjp + tp_csjv + cand_csjp

    mostrar_resultados("Tamano CS llega hasta el inicio del Yugo", cand_csjv, size_csjv, tp_csjv, cand_csjp, size_csjp, tp_csjp, tp_entero_py)
    
elif (tmcs + w) < l + r:
    size_csjv = w
    size_csjp = (l + r) - tmcs

    if size_csjp <= 0:
        st.error("❌ Error: el tamaño calculado para el yugo es inválido.")
        st.stop()
    
    mm_tp_csjv = cand_csjv * size_csjv     
    tp_csjv = math.ceil(mm_tp_csjv / tmcs)
    if size_csjp > (tmcs/2):
        tp_csjp = cand_csjp
    else:
        mm_tp_csjp = cand_csjp * size_csjp
        tp_csjp = math.ceil(mm_tp_csjp / tmcs)
    
    tp_entero_py = tp_csjv + tp_csjp + cand_csjp

    mostrar_resultados("Tamano CS mas pequeno que el Largo", cand_csjv, size_csjv, tp_csjv, cand_csjp, size_csjp, tp_csjp, tp_entero_py)

else:
    st.warning("⚠ No se cumple ninguna condición del algoritmo original.")