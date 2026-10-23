import streamlit as st
import sqlite3
import pandas as pd
from config.settings import settings
from src.progol.combinatorio import generar_combinaciones_reducidas

# Configuración principal de la página
st.set_page_config(
    page_title="Predictor Deportivo IA - Progol",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo visual Fintech Minimalista
st.markdown("""
<style>
    .main { background-color: #0E1117; }
    .stMetric { background-color: #1F2B46; padding: 15px; border-radius: 10px; border: 1px solid #C7A05B; }
    h1, h2, h3 { color: #FFFFFF; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #C7A05B; color: #0E1117; font-weight: bold; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

st.title("⚽ Predictor Deportivo IA — Progol")
st.caption("Panel de Control Fintech & Optimización de Apuestas (+EV) | Mauricio Velasco")

# Menú Lateral
st.sidebar.header("⚙️ Configuración de Jornada")

def obtener_jornadas_disponibles():
    try:
        conn = sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT numero_jornada FROM progol_jornadas ORDER BY numero_jornada DESC")
        jornadas = [row[0] for row in cursor.fetchall()]
        conn.close()
        return jornadas if jornadas else [2254]
    except Exception:
        return [2254]

jornadas = obtener_jornadas_disponibles()
jornada_sel = st.sidebar.selectbox("Seleccionar Jornada Progol:", jornadas)
num_boletas = st.sidebar.slider("Número de Boletas Optimizadas (+EV):", min_value=1, max_value=20, value=5)

st.sidebar.markdown("---")
st.sidebar.markdown("**Parámetros de Modelo:**")
st.sidebar.text("• Dixon-Coles Tau: 0.10")
st.sidebar.text(f"• Base de datos: predictor.db")

# Consultar Partidos de la Jornada
def cargar_partidos(jornada):
    conn = sqlite3.connect(settings.DB_PATH)
    # Consulta tolerante a esquemas con SELECT * simplificado
    query = """
    SELECT 
        pj.casilla as Casilla,
        e_loc.nombre as Local,
        e_vis.nombre as Visitante,
        m.local_xg as xG_Local,
        m.visitante_xg as xG_Vis,
        p.prob_local as P_Loc,
        p.prob_empate as P_Emp,
        p.prob_visitante as P_Vis
    FROM progol_jornadas pj
    JOIN partidos p ON pj.partido_id = p.id
    JOIN equipos e_loc ON p.equipo_local_id = e_loc.id
    JOIN equipos e_vis ON p.equipo_visitante_id = e_vis.id
    LEFT JOIN metricas_avanzadas m ON p.id = m.partido_id
    WHERE pj.numero_jornada = ?
    ORDER BY pj.casilla ASC
    """
    try:
        df = pd.read_sql_query(query, conn, params=(jornada,))
    except Exception:
        # Fallback query si la casilla está en partidos
        query_alt = """
        SELECT 
            p.id as Casilla,
            e_loc.nombre as Local,
            e_vis.nombre as Visitante,
            m.local_xg as xG_Local,
            m.visitante_xg as xG_Vis,
            p.prob_local as P_Loc,
            p.prob_empate as P_Emp,
            p.prob_visitante as P_Vis
        FROM progol_jornadas pj
        JOIN partidos p ON pj.partido_id = p.id
        JOIN equipos e_loc ON p.equipo_local_id = e_loc.id
        JOIN equipos e_vis ON p.equipo_visitante_id = e_vis.id
        LEFT JOIN metricas_avanzadas m ON p.id = m.partido_id
        WHERE pj.numero_jornada = ?
        """
        df = pd.read_sql_query(query_alt, conn, params=(jornada,))
    finally:
        conn.close()
    return df

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📊 Partidos & Métricas Avanzadas — Jornada {jornada_sel}")
    df_partidos = cargar_partidos(jornada_sel)
    if not df_partidos.empty:
        st.dataframe(df_partidos, use_container_width=True)
    else:
        st.info("No se encontraron partidos para la jornada seleccionada.")

with col2:
    st.subheader("💡 Resumen de Métricas")
    st.metric(label="Jornada Activa", value=f"#{jornada_sel}")
    st.metric(label="Casillas Analizadas", value=len(df_partidos))
    st.metric(label="Modelo Activo", value="Dixon-Coles + xG")

st.markdown("---")
st.subheader("🎯 Boletas Generadas de Alto Valor Esperado (+EV)")

if st.button("🚀 Recalcular Boletas Optimizadas"):
    with st.spinner("Calculando matrices de probabilidad y generando combinaciones..."):
        boletas = generar_combinaciones_reducidas(jornada_sel, max_boletas=num_boletas)
        if boletas:
            for idx, (boleta, ev) in enumerate(boletas, 1):
                st.write(f"**Boleta #{idx:02d}** | Valor Esperado (EV): `{ev:.2f}`")
                st.code(" ".join(boleta), language="text")
        else:
            st.warning("No se generaron combinaciones para esta jornada.")