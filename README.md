# 📊 Dashboard de Ventas: Empresa de Alimentación 🚀

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://proyectofinalvisuadashboard.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/pandas-Data_Analysis-150458.svg?logo=pandas)](https://pandas.pydata.org/)

> **Transformando millones de registros en decisiones estratégicas al instante.** > 
> Este proyecto es una solución analítica de alto nivel diseñada para el CEO y la Dirección de Ventas de una importante multinacional de alimentación, con el objetivo de evaluar el rendimiento comercial de cara al cierre de año.

Puedes probar la aplicación desplegada en Streamlit Cloud aquí: **[🔗 Acceder al Dashboard](https://proyectofinalvisuadashboard.streamlit.app/)**

---

## 📑 Secciones del Dashboard

La herramienta está dividida en cuatro módulos principales, diseñados para navegar desde lo más general hasta el detalle local más granular:

* 🌍 **1. Visualizaciones Generales:** Una radiografía global del negocio. Incluye conteos masivos (tiendas, productos, estados), promedios de facturación, el codiciado "Top 10" de familias de productos, y un análisis profundo de la estacionalidad (mejores/peores días, semanas y meses).
* 🏪 **2. Información por Tienda:** Análisis microscópico. Permite seleccionar una tienda concreta y estudiar su curva de ventas anual, el volumen de catálogo movido y, críticamente, la efectividad de los productos vendidos bajo promoción.
* 🗺️ **3. Información a Nivel Estado:** Perspectiva regional. Ideal para ver transacciones anuales, qué tiendas tiran del carro en cada zona y cuál es la "familia de productos estrella" que domina el mercado local.
* 📝 **4. Resumen Ejecutivo (Bonus):** Un panel directo y al grano. Pensado para que los ejecutivos consuman los *insights* más críticos en menos de 1 minuto, comparativas de años y los gráficos más relevantes consolidados.

---

## 💡 Comentarios e Insights del Dashboard

Tras procesar y visualizar los datos, el dashboard revela varias conclusiones estratégicas vitales para la compañía:

1. **Monopolio de Categorías:** Las familias `GROCERY I` y `BEVERAGES` no solo lideran, sino que aplastan al resto del catálogo en volumen de facturación. Cualquier interrupción en la cadena de suministro de estas dos familias sería crítica para la empresa.
2. **Disparidad del Rendimiento de Tiendas:** El dashboard evidencia una brecha enorme de facturación entre la tienda líder (Tienda 44, con más de 63 millones) y las de la cola (Tienda 52, con apenas 2.7 millones). Esto sugiere la necesidad de replicar el modelo de la tienda 44 o reevaluar la viabilidad de las ubicaciones menos rentables.
3. **El "Efecto Espejismo" de 2017:** A simple vista en las gráficas temporales, 2017 parece ser un año desastroso con una fuerte caída en ventas. Sin embargo, el análisis estacional detallado demuestra que los datos de 2017 solo llegan hasta agosto (semana 33 aprox.). Si proyectamos el rendimiento de 2016 hasta ese mismo mes, 2017 en realidad mantiene un ritmo de crecimiento competitivo.
4. **Poder de la Promoción:** En el desglose por tiendas, los gráficos de barras confirman que las campañas promocionales tienen un impacto directo y desproporcionado en categorías específicas, sirviendo como palanca rápida para vaciar inventario o impulsar métricas a final de mes.

---

## 🛠️ Tecnologías y Requisitos

Este proyecto ha sido construido puramente en Python, priorizando el rendimiento para manejar millones de filas de datos (uso optimizado de lectura de CSVs mediante carga selectiva de columnas).

Las dependencias exactas (`requirements.txt`) para levantar este proyecto son:

```text
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
openpyxl>=3.0.0
text´´´
---

## ⚙️ Cómo ejecutar el Dashboard en local
Si deseas clonar este proyecto y ejecutarlo en tu propia máquina para explorar el código o los datos, sigue estos pasos:

1. Clona el repositorio:
Abre tu terminal y ejecuta:

git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO

2. Crea y activa un entorno virtual (Recomendado):

# En Windows:
python -m venv venv
venv\Scripts\activate

# En macOS/Linux:
python3 -m venv venv
source venv/bin/activate

3. Instala las dependencias necesarias:

pip install -r requirements.txt
