import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data(show_spinner="Cargando datos...")
def cargar_ficheros()->tuple[pd.DataFrame,pd.DataFrame]:
    df1 = pd.read_csv('parte_1.csv',low_memory = False)
    df2 = pd.read_csv('parte_2.csv',low_memory=False)
    df = pd.concat([df1, df2], ignore_index=True)

    df = df.drop_duplicates()
    return df
     
st.set_page_config(
    page_title="VENTAS TOTALES ALIMENTACIÓN KPIS",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title("⚙️ Opciones")
    st.divider()

    # Selector de página/sección
    pagina = st.selectbox(
        "Selecciona una sección",
        ["📈 Visualizaciones generales ventas", "🏪Información por tienda","🌎 Información a nivel estado", "📝 Resumen ejecutivo"]
    )
    st.divider()
    st.caption("© 2025 - VentasKPIs")

#########################
## CONTENIDO PRINCIPAL
#########################

# Título principal
st.title("🚀 Dashboard Alimentación Compañía 2025")
st.markdown("**Resumido, graficado, explicado**... y puede que con algún detalle adicional😊")
st.divider()
df= cargar_ficheros()


if pagina == "📈 Visualizaciones generales ventas":
    st.header("🔎 Visualizaciones y más información")
    subpagina = st.selectbox(
        "Selecciona una sección",
        ["Conteo general" ,"Análisis en términos medios", "Análisis estacionalidad ventas"]
    )
    st.divider()

    if subpagina == "Conteo general":
        st.subheader("📋 Resumen General del Dataset")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Total de Filas",
                value=f"{len(df):,}",
                help="Número total de entradas del archivo"
            )
            
        with col2:
            st.metric(
                label="📁 Total de Columnas",
                value=len(df.columns),
                help="Número de variables disponibles"
            )
            
        with col3:
            st.metric(
                label="🏪 Total de Tiendas",
                value=df['store_nbr'].nunique(),
                help="Tiendas únicas en los datos"
                )
            
        with col4:
            st.metric(
                label="📦 Total de Productos",
                value=df['id'].nunique(),
                help="Productos únicos vendidos"
                )
        st.divider()

        st.subheader("📌 Información Relevante")
        expander_info = st.expander("💰 Datos Comerciales", expanded=True)
            
        with expander_info:
            col_info1, col_info2 = st.columns(2)
                
            with col_info1:
                st.markdown("##### 🌎 Distribución Geográfica")
                estados = sorted(df["state"].dropna().unique())
                n_estados = len(estados)
                    
                st.write(f"**Estados Empresa:** {n_estados}")
                estados_str = ", ".join(estados)
                st.info(f"📍 {estados_str}")
                    
                st.markdown("##### 📅 Periodo Datos")
                year_min = df["year"].min()
                year_max = df["year"].max()
                st.write(f"**Rango de años:** {year_min} - {year_max}")
                    
            with col_info2:
                st.markdown("##### 📆 Meses Disponibles por Año")
                meses_por_year = df.groupby("year")["month"].apply(lambda x: sorted(x.unique()))
                    
                for year, meses in meses_por_year.items():
                    meses_badges = " ".join([f"{m}" for m in meses])
                    st.write(f"**{year}:** {meses_badges}")

    elif subpagina == "Análisis en términos medios":
        st.subheader("📋 Resumen General Ventas")
        total_ventas = df["sales"].sum()
        venta_promedio = df["sales"].mean()
        transacciones = len(df)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(
                label="💰 Ventas Totales",
                value=f"{total_ventas:,.0f}€",
                help="Suma total de ventas"
            )
        with m2:
            st.metric(
                label="📊 Venta Promedia",
                value=f"{venta_promedio:,.2f}€",
                help="Promedio por transacción"
            )
        with m3:
            st.metric(
                label="📥 Total Transacciones",
                value=f"{transacciones:,}",
                help="Número total de registros"
            )
        
        st.divider()
        st.subheader('📝 Análisis en términos medios')
        expander_info = st.expander("📈 Estadísticas", expanded=True)
        with expander_info:
            st.markdown("### 🥇 Top 10 Familias Productos")
            top_familias = (
                df.groupby("family")["sales"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

            for i, (familia, ventas) in enumerate(top_familias.items(), 1):
                st.write(f"**{i}. {familia}** - {ventas:,.0f}€ ")
            
            st.divider()
            
            # Segunda tabla - Tiendas
            st.markdown('### 🏪 Distribución Ventas por Tienda')
            ventas_por_tienda = df.groupby('store_nbr')['sales'].sum().sort_values(ascending=False)
            top_10_tiendas = ventas_por_tienda.nlargest(10)
            otros = ventas_por_tienda.sum() - top_10_tiendas.sum()

            # Crear datos para el gráfico
            labels = [f"Tienda {idx}" for idx in top_10_tiendas.index] + ['Otras']
            values = list(top_10_tiendas.values) + [otros]


            fig = px.pie(
                values=values,
                names=labels,
                title="Distribución ventas por tiendas"
            )

            st.plotly_chart(fig)
            # Tercera tabla - Promociones
            st.markdown("### 🔝 Top 10 Tiendas en Ventas con Promoción")
            df_promo = df[df["onpromotion"] > 0]
            
            if not df_promo.empty:
                top_tiendas_promo = (
                    df_promo
                    .groupby("store_nbr")["sales"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(10)
                )
                
                for i, (tienda, ventas) in enumerate(top_tiendas_promo.items(), 1):
                    st.write(f"**{i}. Tienda {tienda}** - {ventas:,.0f}€")
            else:
                st.warning("No hay datos disponibles de productos en promoción")


    elif subpagina == "Análisis estacionalidad ventas":
        st.subheader('🍁 Análisis estacionalidad ventas')
        expander_info = st.expander("🍃 Detalles estacionales", expanded=True)
        with expander_info:
            st.markdown("#### 💯 Día Semana Más Ventas por Término Medio")
            df_dia = df.groupby("day_of_week")["sales"].mean().reset_index().sort_values(by='sales',ascending = False)
            max = df_dia['sales'].max()
            day = df_dia.loc[df_dia['sales'] == max,'day_of_week'].iloc[0]
            st.write(f"**· {day}**: {max:,.2f} ventas por término medio")

            st.divider()
            st.markdown("#### 🗓️ Volumen Ventas Medio por Semana del Año (2013-2017)")
            años = sorted(df['year'].unique())
            for año in años:
                if año ==  2017:    
                    df_2017 = df[(df['week'] != 52) & (df['year'] == 2017)]
                    ventas_semana = df_2017[df_2017['sales'] > 0].groupby('week')['sales'].mean().reset_index().sort_values(by = 'sales',ascending = False)
                else:
                    df_año = df[df['year'] == año]
                    ventas_semana = df_año[df_año['sales'] > 0].groupby('week')['sales'].mean().reset_index().sort_values(by = 'sales',ascending = False)
                st.write(f"### {año}")
                maximo = ventas_semana['sales'].max()
                minimo = ventas_semana['sales'].min()
                top_semanas = ventas_semana.head(5)
                mejor_semana = ventas_semana.loc[ventas_semana.sales == maximo,'week'].iloc[0]
                peor_semana = ventas_semana.loc[ventas_semana.sales == minimo,'week'].iloc[0]
                st.write(f"**Mejor** Semana {año} →  **Semana {mejor_semana}**: :green[**{maximo:,.2f}**] ventas promedio")
                st.write(f"**Peor** Semana {año} →  **Semana {peor_semana}**: :red[**{minimo:,.2f}**] ventas promedio")
                st.write('##### Top 5 Semanas')
                for i,semana in enumerate(top_semanas['week'],1):
                    sales = top_semanas.loc[top_semanas.week == semana,'sales'].iloc[0]
                    st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**{i}. Semana {semana}**: {sales:,.2f} ventas promedio")

            st.divider()
            st.markdown("#### ➡️ Volumen Ventas Medio por Mes (2013-2017)")
            months = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
            años = sorted(df['year'].unique())
            for año in años:
                df_año = df[df['year'] == año]
                ventas_mes = df_año[df_año['sales'] > 0].groupby('month')['sales'].mean().reset_index().sort_values(by = 'sales',ascending = False)
                st.write(f"### {año}")
                maximo = ventas_mes['sales'].max()
                minimo = ventas_mes['sales'].min()
                top_meses = ventas_mes.head(5)
                mejor_mes = ventas_mes.loc[ventas_mes.sales == maximo,'month'].iloc[0]
                peor_mes = ventas_mes.loc[ventas_mes.sales == minimo,'month'].iloc[0]
                st.write(f"**Mejor** Mes {año} →  **Mes {mejor_mes} ({months[mejor_mes]})**: :green[**{maximo:,.2f}**] ventas promedio")
                st.write(f"**Peor** Mes {año} →  **Mes {peor_mes} ({months[peor_mes]})**: :red[**{minimo:,.2f}**] ventas promedio")
                st.write('##### Top 5 Meses')
                for i,mes in enumerate(top_meses['month'],1):
                    sales = top_meses.loc[top_meses.month == mes,'sales'].iloc[0]
                    st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**{i}. Mes {mes} ({months[mes]})**: {sales:,.2f} ventas promedio")

    if st.checkbox("💻 Mostrar vista previa de datos"):
        st.dataframe(df.head(500))

elif pagina == "🏪Información por tienda":
    st.header("📊 Gráficos por Tienda")
    tiendas = df['store_nbr'].unique().tolist()
    opcion = st.selectbox(
        'Elige una de las tiendas disponibles',
        sorted(tiendas),
        index=None,
        placeholder="Selecciona una de las tiendas disponibles..."
    )
    if opcion:
        st.write(f"Seleccionaste: {opcion}")
        st.divider()
        df_tienda = df[df.store_nbr == opcion]

        #LINE CHART
        st.subheader(f"💰 Número Total Ventas por Año - Tienda {opcion}")
        df_ventas_año = df_tienda.groupby('year')['sales'].sum().sort_values(ascending = True).sort_index()
        st.markdown('**Distribución de ventas por años**')
        df_aux = df_ventas_año.copy().reset_index()
        años_con_datos = sorted(df_tienda['year'].unique())
        for año in años_con_datos:
            sale = df_aux.loc[df_aux.year == año,'sales'].iloc[0]
            st.write(f"- **{año}**: {sale:,.2f} ventas")
        df_ventas_año.index = df_ventas_año.index.astype(str)
        st.markdown(f"#### 📈 Gráfico de Líneas Tienda {opcion}")
        st.line_chart(df_ventas_año)
        max_sales = df_aux['sales'].max()
        st.markdown(f"Año con :green[**más**] ventas: **{df_aux.loc[df_aux['sales'] == max_sales,'year'].iloc[0]}** (:green[**{max_sales:,.2f}**] ventas)")
        min_sales = df_aux['sales'].min()
        st.markdown(f"Año con :red[**menos**] ventas: **{df_aux.loc[df_aux['sales'] == min_sales,'year'].iloc[0]}** (:red[**{min_sales:,.2f}**] ventas)")
        st.divider()

        #BAR CHART
        st.subheader(f"📦 Número Total Productos Vendidos por Año - Tienda {opcion}")
        transacciones_año = df_tienda.groupby('year').size()
        productos_unicos_año = df_tienda.groupby('year')['id'].nunique().reset_index()
        df_aux_bar = transacciones_año.copy()
        df_aux = df_aux_bar.reset_index()
        df_final = df_aux.rename(columns = {0:'products'})
        st.markdown('**Distribución de cantidad de productos distintos vendidos por años**')
        for año in años_con_datos:
            sale = productos_unicos_año.loc[productos_unicos_año.year == año,'id'].iloc[0]
            st.write(f"- **{año}**: {sale:,} tipos distintos de productos vendidos")

        st.markdown(f"#### 📊 Gráfico de Barras Tienda {opcion}")
        st.bar_chart(df_final.set_index('year'))

        max_sales = df_final['products'].max()
        st.markdown(f"Año con :green[**más**] productos totales vendidos: **{df_final.loc[df_final['products'] == max_sales,'year'].iloc[0]}** (:green[**{max_sales:,}**] productos vendidos)")
        min_sales = df_final['products'].min()
        st.markdown(f"Año con :red[**menos**] productos totales vendidos: **{df_final.loc[df_final['products'] == min_sales,'year'].iloc[0]}** (:red[**{min_sales:,}**] productos vendidos)")
        st.divider()

        #BAR CHART
        st.subheader(f"🏪 Número Total Productos Vendidos en Promoción - Tienda {opcion}")
        df_promocion = df_tienda[df_tienda.onpromotion > 0]

        if not df_promocion.empty:
            # Agrupar por año y familia
            ventas_por_tipo = df_promocion.groupby(['year', 'family']).size().reset_index(name='quantity')
            st.markdown("**Resumen por familia:**")
            
            # Top 5 familias en promoción
            top_familias = ventas_por_tipo.groupby('family')['quantity'].sum().nlargest(5)

            for familia, cantidad in top_familias.items():
                st.write(f"- **{familia}**: {cantidad:,} productos en promoción")

            ventas_por_tipo.index = ventas_por_tipo.index.astype(str)
            st.markdown(f"#### 📊 Gráfico de Barras Productos en Promoción Tienda {opcion}")
            st.bar_chart(ventas_por_tipo[['year','quantity']].set_index('year'))      
        else:
            st.info(f"La tienda {opcion} no tiene productos vendidos en promoción")
elif pagina == '🌎 Información a nivel estado':
    st.header("🌎 Gráficos e Información por Estado")
    estados = df['state'].unique().tolist()
    opcion = st.selectbox(
        'Elige uno de los estados disponibles',
        sorted(estados),
        index=None,
        placeholder="Selecciona uno de los estados disponibles..."
    )
    if opcion:
        st.write(f"Seleccionaste: {opcion}")
        st.divider()
        df_estado = df[df.state == opcion]

        st.subheader(f'📥 Número Total Transacciones por Año - Estado {opcion}')
        df_transacciones = df_estado.groupby('year')['transactions'].count().reset_index()
        for year in df_transacciones['year']:
            st.write(f"- **{year}**: {df_transacciones.loc[df_transacciones.year == year,'transactions'].iloc[0]:,} transacciones")
        max_sales = df_transacciones['transactions'].max()
        st.markdown(f"Año con :green[**más**] transacciones: **{df_transacciones.loc[df_transacciones['transactions'] == max_sales,'year'].iloc[0]}** (:green[**{max_sales:,}**] transacciones)")
        min_sales = df_transacciones['transactions'].min()
        st.markdown(f"Año con :red[**menos**] transacciones: **{df_transacciones.loc[df_transacciones['transactions'] == min_sales,'year'].iloc[0]}** (:red[**{min_sales:,}**] transacciones)")
        st.divider()    

        st.subheader(f'📈 Ranking Tiendas con Más Ventas - Estado {opcion}')
        top_tiendas = df_estado.groupby('store_nbr')['sales'].sum()\
            .sort_values(ascending=False)\
            .head(10)\
            .reset_index()

        for i, (_, row) in enumerate(top_tiendas.iterrows(), 1):
            st.write(f"**{i}**. **Tienda {int(row['store_nbr'])}**: {row['sales']:,.0f}€")
        st.divider()

        st.subheader(f'🏪 Producto Más Vendido por Tienda - Estado {opcion} ')
        top_tiendas = df_estado.groupby('store_nbr')['sales'].sum()\
            .sort_values(ascending=False)\
            .index.tolist()

        # Para cada tienda, encontrar su producto más vendido
        for tienda in top_tiendas:
            df_tienda = df_estado[df_estado['store_nbr'] == tienda]
            
            if not df_tienda.empty:
                # Encontrar producto más vendido (por ventas totales)
                producto_top = df_tienda.groupby('family')['sales'].sum()\
                    .sort_values(ascending=False)\
                    .head(1)\
                    .reset_index()
                
                familia_top = producto_top['family'].iloc[0]
                ventas_top = producto_top['sales'].iloc[0]
                
                # Mostrar resultado
                st.write(f"**Tienda** :red[**{tienda}**]:")
                st.write(f"&nbsp;&nbsp;🏆 **{familia_top}**: 💰 {ventas_top:,.0f}€")

elif pagina == "📝 Resumen ejecutivo":
    st.subheader("📝 Resumen ejecutivo")
    m1, m2, m3 = st.columns(3)
    with m1:
        top_tiendas = df.groupby('store_nbr')['sales'].sum()\
            .sort_values(ascending=False)\
            .reset_index()
        top = top_tiendas.loc[1,'store_nbr']
        peor = top_tiendas.loc[53,'store_nbr']
        st.markdown('#### 🏪 Tiendas')
        st.markdown(f"- :green[**Top**] tienda : **{top}**")
        st.markdown(f"- :red[**Peor**] tienda : **{peor}**")
        st.caption("Basado en ventas totales")
    with m2:
        df_states = df.groupby('state')['sales'].sum().sort_values(ascending = False).reset_index()
        top = df_states.loc[1,'state']
        peor = df_states.loc[15,'state']
        st.markdown('#### 🌎 Estados')
        st.markdown(f"- :green[**Top**] estado : **{top}**")
        st.markdown(f"- :red[**Peor**] estado : **{peor}**")
        st.caption("Basado en ventas totales")
    with m3:
        df_años = df.groupby('year')['sales'].sum().reset_index()
        dieciseis = df_años.loc[df_años.year == 2016,'sales'].iloc[0]
        diecisiete = df_años.loc[df_años.year == 2017,'sales'].iloc[0]
        st.markdown('##### 🗓️ Comparativa Años (2016-2017)')
        st.markdown(f"- 2016 : **{dieciseis:,.2f}**")
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp; - {dieciseis*2/3:,.2f} ventas aprox. hasta agosto")
        st.markdown(f"- 2017 : **{diecisiete:,.2f}** (ventas hasta agosto)")
        st.caption("Basado en ventas totales")
    st.divider()
    st.subheader('🟢 Gráficos relevantes - Visualizaciones generales')

    st.markdown('#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🎯Ranking Productos Más Vendidos (TOP 10)')
    top_familias = (
        df.groupby("family")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10).reset_index())
    st.bar_chart(top_familias.set_index('family'))

    st.markdown('#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🎯Ranking Tiendas con Más Ventas en Promoción (TOP 10)')
    df_promo = df[df["onpromotion"] > 0]
    
    if not df_promo.empty:
        top_tiendas_promo = (
            df_promo
            .groupby("store_nbr")["sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10).reset_index()
        )
    st.bar_chart(top_tiendas_promo.set_index('store_nbr'))

    st.markdown('#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🎯Día con Más Ventas (Comparativa)')
    df_dia = df.groupby("day_of_week")["sales"].mean().reset_index().sort_values(by='sales',ascending = False)
    st.bar_chart(df_dia.set_index('day_of_week'))
    st.subheader('🟠 Gráficos relevantes - Información a nivel estado')
    estados = df['state'].unique().tolist()
    opcion = st.selectbox(
        'Elige uno de los estados para observar sus gráficos',
        sorted(estados),
        index=None,
        placeholder="Selecciona uno de los estados disponibles..."
    )
    if opcion:
        st.write(f"Seleccionaste: {opcion}")
        df_estado = df[df.state == opcion]
        
        st.markdown(f'#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🌎 Número Total Transacciones por Año - Estado {opcion}')
        df_transacciones = df_estado.groupby('year')['transactions'].count().sort_values(ascending = True).sort_index()
        df_transacciones.index = df_transacciones.index.astype(str)
        st.line_chart(df_transacciones) 
      

