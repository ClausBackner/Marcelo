import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Dashboard de Objetivos")

# Subir archivo Excel
uploaded_file = st.file_uploader("Sube tu archivo de Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Leer el archivo Excel
        df = pd.read_excel(uploaded_file, sheet_name="Hoja1")

        # Limpiar espacios en los nombres de las columnas
        df.columns = df.columns.str.strip()

        # Renombrar columnas en caso de que tengan nombres diferentes
        rename_dict = {
            "OBJETIVO": "Objetivo",
            "objetivo": "Objetivo",
            "INDICADOR": "Indicador",
            "indicador": "Indicador"
        }
        df.rename(columns=rename_dict, inplace=True)

        # Verificar si las columnas necesarias existen
        required_columns = ["Objetivo", "Indicador"]
        years_columns = [col for col in df.columns if "AÑO" in col]  # Filtrar columnas de años

        if all(col in df.columns for col in required_columns) and years_columns:
            # Selección del objetivo
            selected_objective = st.selectbox("Selecciona un Objetivo", df["Objetivo"].unique())

            # Filtrar datos por el objetivo seleccionado
            df_filtered = df[df["Objetivo"] == selected_objective]

            # Crear DataFrame para la gráfica de años
            df_melted = df_filtered.melt(id_vars=["Objetivo"], value_vars=years_columns, 
                                         var_name="Año", value_name="Valor")

            # Crear gráfica solo con los años
            fig = px.bar(df_melted, x="Año", y="Valor", color="Año", title=f"Objetivo: {selected_objective}")

            # Mostrar gráfica
            st.plotly_chart(fig)

            # Mostrar los nombres de los KPI debajo de la gráfica sin los valores
           
            kpi_list = df_filtered["Indicador"].tolist()
            st.write(", ".join(kpi_list))  # Mostrar solo los nombres de los KPI como texto en línea

        else:
            st.error("Las columnas necesarias no están presentes en el archivo.")

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
