.# 🎾 Padel Data Analytics & Revenue Management (Zaragoza)

## 📌 Visión General del Proyecto
Este es un proyecto *End-to-End* de Ingeniería y Análisis de Datos centrado en el modelo de negocio de los clubes de pádel en la ciudad de Zaragoza y sus alrededores. El objetivo principal es construir una arquitectura de datos completa para analizar la ocupación, la eficiencia operativa y el coste de oportunidad (*Lost Revenue*), aplicando técnicas de Business Intelligence.

## 🛠️ Stack Tecnológico
* **Generación de Datos:** Python (Pandas, Numpy, Random/Probabilidad).
* **Base de Datos & Capa Semántica:** PostgreSQL.
* **Business Intelligence & UI:** Power BI (DAX, Modelado Relacional).

---

## 🏗️ Fases del Proyecto y Arquitectura

### 1. Recopilación de Datos Base (Mapeo Manual)
Para garantizar la precisión del modelo de negocio, la primera fase consistió en un trabajo de investigación y recolección manual. 
* Se mapearon los principales clubes de Zaragoza y su área metropolitana.
* Se estructuraron las franjas horarias operativas de cada centro.
* Se extrajeron las tarifas y políticas de precios (Pricing) dependiendo del tipo de pista (Interior, Exterior, Semicubierta) y de la franja del día.

### 2. Simulación de Demanda Algorítmica (Python)
Ante la imposibilidad de extraer datos transaccionales privados de los clubes, se desarrolló un script en Python para generar un *dataset* sintético de reservas de alta fidelidad para un periodo de **dos semanas**.
* **Modelos Probabilísticos:** Los datos no son aleatorios. Se programaron lógicas de probabilidad basadas en el comportamiento real del consumidor (ej. mayor probabilidad de reservas en horario de tarde/noche en días laborales, y picos de ocupación matinal en fines de semana).
* **Variables generadas:** ID de reserva, club, fechas, horas, estado (Libre/Ocupada) e ingresos generados vs. potenciales.

### 3. Capa Semántica y Data Warehouse (PostgreSQL)
Los datos brutos generados se ingirieron en una base de datos relacional para realizar el trabajo pesado de transformación y agregación antes de la visualización.
* **DDL y Tablas:** Creación de la tabla principal optimizando los tipos de datos.
* **Vistas Analíticas (Views):** Se programaron consultas SQL avanzadas (incluyendo *CTEs* y *Window Functions*) para calcular métricas clave de negocio:
  * Tasa de ocupación diaria y cálculo de ingresos perdidos (*Lost Revenue*).
  * Ranking de rentabilidad por pista física (uso de `DENSE_RANK()`).
  * Análisis de retención y optimización energética (reservas consecutivas *Back-to-Back* usando `LAG()`).

### 4. Modelado y BI (Power BI & DAX)
Conexión directa entre Power BI y PostgreSQL para la ingesta del modelo tabular.
* **Modelo en Estrella:** Creación de una tabla `Calendario` dinámica en DAX para garantizar el correcto flujo de los filtros temporales y evitar relaciones de *Muchos a Muchos*.
* **Lenguaje DAX:** Desarrollo de Nuevas Columnas (para categorización de franjas comerciales y tipos de días aplicando la Máxima de Roche) y Medidas dinámicas (Porcentaje de ocupación real iterativo, Ticket medio, etc.) adaptables al *Contexto de Filtro*.

### 5. Diseño del Dashboard y UI/UX
Se ha diseñado un Cuadro de Mando interactivo con estética "Premium", dividido en páginas orientadas a diferentes perfiles de negocio:

* **Página 1: Visión General (Perfil Directivo/Inversor)**
  * KPIs financieros principales (Ingreso Real vs Ingreso Potencial).
  * Gráficos de tendencias temporales y mapas de geolocalización de rendimiento.
* **Página 2: Inteligencia Operativa y Pricing (Perfil Manager/Operaciones)**
  * Matrices (Heatmaps) de calor para detectar cuellos de botella por hora y día.
  * Análisis de infraestructura (rendimiento pistas indoor vs outdoor).
  * Gráficos de dispersión y rankings de pistas "Matagigantes".
* **🚀 Feature Destacada: Custom Tooltip Page**
  * Se implementó una página oculta de "Información sobre herramientas". Al pasar el ratón sobre los clubes en el mapa interactivo, se despliega un mini-informe emergente con las peores horas de ocupación específicas de ese activo, logrando una experiencia de usuario (UX) inmersiva.

---

## 📂 Estructura del Repositorio
* `/scripts_python`: Código fuente de la simulación probabilística de reservas.
* `/sql`: Scripts DDL de creación de tablas y las consultas SQL de las vistas.
* `/powerbi`: (Opcional) Archivo `.pbix` o capturas de pantalla del Dashboard en alta resolución.
