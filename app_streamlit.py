import streamlit as st
import math

st.set_page_config(page_title="Cálculo de Palos", layout="centered")

st.title("📏 Cálculo Profesional de Palos para Núcleo")
st.write("Unidad de medida: **mm**")

# --- Función de validación ---
def validar(valor, nombre):
    if valor <= 0:
        st.error(f"❌ El valor de **{nombre}** debe ser mayor que 0.")
        st.stop()
    return valor

# --- Entradas ---
st.subheader("🔧 Parámetros de entrada")

w = validar(st.number_input("Tamaño de la Hoja (w)", min_value=1.0, step=1.0), "w")
v = validar(st.number_input("Tamaño de la Ventana (v)", min_value=1.0, step=1.0), "v")
l = validar(st.number_input("Largo de la Pierna (l)", min_value=1.0, step=1.0), "l")

st.write("---")

# Ruler
r_default = 350
mantener = st.radio("Tamaño del ruler", ["Mantener 350 mm", "Cambiar valor"])

if mantener == "Cambiar valor":
    r = validar(st.number_input("Nuevo valor del ruler (r)", min_value=1.0, step=1.0), "r")
else:
    r = r_default

st.write("---")

# Cool stree
cs_default = 2790
mantener = st.radio("Tamaño del cool stree", ["Mantener 2790 mm", "Cambiar valor"])

if mantener == "Cambiar valor":
    tmcs = validar(st.number_input("Nuevo valor del cool stree (tmcs)", min_value=1.0, step=1.0), "tmcs")
else:
    tmcs = cs_default

st.write("---")

# --- Cálculos base ---
cand_csjp = math.ceil((w / r) * 3)
cand_csjv = math.ceil((v / r) * 2)

# --- Procesamiento ---
st.subheader("📊 Resultados del cálculo")

if tmcs == l:
    size_csjv = w
    size_csjp = 0

    caven = tmcs / size_csjv
    tp_csjv = math.ceil(cand_csjv / caven)

    tp_entero_py = cand_csjp + cand_csjv

    st.success("Caso aplicado: **tmcs = l**")

    st.metric("Palos para las dos ventanas", cand_csjv)
    st.metric("Tamaño de corte ventana", f"{size_csjv} mm")
    st.metric("Palos tamano original para cortar (ventana)", tp_csjv)
    st.metric("Palos para yugo", "0 (tamaño original)")
    st.metric("Palos enteros necesarios para todo el Proyecto (Cortar-Pegar)", tp_entero_py)

elif ((l - w) + r) == tmcs:
    size_csjv = w
    size_csjp = w

    caven = tmcs / size_csjv
    tp_csjv = math.ceil(cand_csjv / caven)
    tp_csjp = math.ceil(cand_csjp / caven)

    tp_entero_py = cand_csjp + cand_csjv

    st.success("Caso aplicado: **(l - w) + r = tmcs**")

    st.metric("Palos para ventana", cand_csjv)
    st.metric("Tamaño ventana", f"{size_csjv} mm")
    st.metric("Palos a cortar (ventana)", tp_csjv)

    st.metric("Palos para yugo", cand_csjp)
    st.metric("Tamaño yugo", f"{size_csjp} mm")
    st.metric("Palos a cortar (yugo)", tp_csjp)

    st.metric("Palos enteros necesarios", tp_entero_py)

elif ((l - w) + r) > tmcs:
    size_csjv = w
    size_csjp = l - (tmcs + r)

    if size_csjp <= 0:
        st.error("❌ Error: el tamaño calculado para el yugo es inválido.")
        st.stop()

    caven = tmcs / size_csjv
    tp_csjv = math.ceil(cand_csjv / caven)

    caven2 = tmcs / size_csjp
    tp_csjp = math.ceil(cand_csjp / caven2)

    tp_entero_py = cand_csjp + cand_csjv

    st.success("Caso aplicado: **(l - w) + r > tmcs**")

    st.metric("Palos para ventana", cand_csjv)
    st.metric("Tamaño ventana", f"{size_csjv} mm")
    st.metric("Palos a cortar (ventana)", tp_csjv)

    st.metric("Palos para yugo", cand_csjp)
    st.metric("Tamaño yugo", f"{size_csjp} mm")
    st.metric("Palos a cortar (yugo)", tp_csjp)

    st.metric("Palos enteros necesarios", tp_entero_py)

else:
    st.warning("⚠ No se cumple ninguna condición del algoritmo original.")