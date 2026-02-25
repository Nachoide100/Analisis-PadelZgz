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

(Esto lo tuve que hacer manualmente porque Playtomic tenía una gran defensa anti - scrapping asi que si alguien quiere los datos están en el .csv de PAPAPADEL.)

### 2. Simulación de Demanda Algorítmica (Python)
Ante la imposibilidad de extraer datos transaccionales privados de los clubes, se desarrolló un script en Python para generar un *dataset* sintético de reservas de alta fidelidad para un periodo de **dos semanas**.
* **Modelos Probabilísticos:** Los datos no son aleatorios. Se programaron lógicas de probabilidad basadas en el comportamiento real del consumidor (ej. mayor probabilidad de reservas en horario de tarde/noche en días laborales, y picos de ocupación matinal en fines de semana).
* **Variables generadas:** ID de reserva, club, fechas, horas, estado (Libre/Ocupada) e ingresos generados vs. potenciales.

### 3. Capa Semántica y Data Warehouse (PostgreSQL)
Los datos brutos generados se ingirieron en una base de datos relacional para realizar el trabajo pesado de transformación y agregación antes de la visualización.
* **DDL y Tablas:** Creación de la tabla principal optimizando los tipos de datos.
```sql
-- Borramos la tabla si ya existía para empezar limpios
DROP TABLE IF EXISTS reservas_padel CASCADE;

-- Creamos la tabla con los tipos de datos optimizados
CREATE TABLE reservas_padel (
    "ID_Reserva" VARCHAR(10),        
    "Club" VARCHAR(100) NOT NULL,    -- Nombre del club
    "Coordenadas" VARCHAR(100),      -- Latitud y Longitud
    "Fecha" DATE NOT NULL,           -- Formato YYYY-MM-DD
    "Dia_Semana" VARCHAR(15),        -- Ej: Monday, Tuesday...
    "Es_Fin_Semana" SMALLINT,        -- 1 para finde, 0 para laboral
    "Hora" TIME NOT NULL,            -- Formato HH:MM
    "Tipo_Pista" VARCHAR(50),        -- Interior, Exterior, Semicubierta
    "Nombre_Pista" VARCHAR(50),      -- Ej: Interior 1
    "Estado" VARCHAR(15),            -- Ocupada o Libre
    "Precio_Euro" NUMERIC(6, 2),     -- Hasta 9999.99 (2 decimales)
    "Ingreso_Generado" NUMERIC(6, 2) -- Dinero real ingresado
);
```
* **Vistas Analíticas (Views):** Se programaron consultas SQL avanzadas (incluyendo *CTEs* y *Window Functions*) para calcular métricas clave de negocio:

#### Lost revenue: ¿cuánto dinero está perdiendo el club al no ocupar las pistas libres según el precio de cada una?
```sql
CREATE OR REPLACE VIEW vw_kpi_diario_club AS
SELECT 
    Club,
    Fecha,
    Es_Fin_Semana,
    COUNT(*) AS total_turnos_posibles,
    SUM(CASE WHEN Estado = 'Ocupada' THEN 1 ELSE 0 END) AS turnos_ocupados,
    ROUND((SUM(CASE WHEN Estado = 'Ocupada' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS pct_ocupacion,
    SUM(Ingreso_Generado) AS ingreso_real_eur,
    SUM(Precio_Euro) AS ingreso_potencial_eur,
    SUM(Precio_Euro - Ingreso_Generado) AS lost_revenue_eur -- Dinero dejado de ganar
FROM 
    reservas_padel
GROUP BY 
    Club, Fecha, Es_Fin_Semana
ORDER BY 
    Fecha, Club;
```
#### Tasa de ocupación diaria: ¿Qué porcentaje de las pistas están ocupadas durante el tiempo de análisis?
```sql
  CREATE OR REPLACE VIEW vw_rendimiento_franjas AS
  WITH Franjas_Categorizadas AS (
    SELECT 
        *,
        CASE 
            WHEN Hora < '14:00' THEN '1. Mañana'
            WHEN Hora >= '14:00' AND Hora < '18:00' THEN '2. Tarde'
            ELSE '3. Noche'
        END AS franja_comercial
    FROM 
        reservas_padel
  )
  SELECT 
    Club,
    Es_Fin_Semana,
    franja_comercial,
    AVG(Precio_Euro) AS precio_medio_ofertado,
    SUM(CASE WHEN Estado = 'Ocupada' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS tasa_ocupacion_pct
  FROM 
    Franjas_Categorizadas
  GROUP BY 
    Club, Es_Fin_Semana, franja_comercial;
 ```
 #### Análisis de retención y optimización energética: ¿Qué porcentaje de las pistas se reserva consecutivamente permitiendo ahorrar energía al club?
 ```sql
CREATE OR REPLACE VIEW vw_ocupacion_consecutiva AS
WITH Pistas_Ordenadas AS (
    SELECT 
        Club,
        Fecha,
        Nombre_Pista,
        Tipo_Pista,
        Hora,
        Estado,
        LAG(Estado, 1) OVER(PARTITION BY Club, Nombre_Pista, Fecha ORDER BY Hora) as estado_turno_anterior
    FROM 
        reservas_padel
)
SELECT 
    Club,
    Tipo_Pista, 
    COUNT(*) as total_reservas_exitosas,
    SUM(CASE WHEN estado_turno_anterior = 'Ocupada' THEN 1 ELSE 0 END) as reservas_consecutivas,
    ROUND(SUM(CASE WHEN estado_turno_anterior = 'Ocupada' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pct_back_to_back
FROM 
    Pistas_Ordenadas
WHERE 
    Estado = 'Ocupada'
GROUP BY 
    Club, Tipo_Pista;
```

### 4. Modelado y BI (Power BI & DAX)
Conexión directa entre Power BI y PostgreSQL para la ingesta del modelo tabular.
* **Modelo en Estrella:** Creación de una tabla `Calendario` dinámica en DAX para garantizar el correcto flujo de los filtros temporales y evitar relaciones de *Muchos a Muchos*.
* **Lenguaje DAX:** Desarrollo de Nuevas Columnas (para categorización de franjas comerciales y tipos de días aplicando la Máxima de Roche) y Medidas dinámicas (Porcentaje de ocupación real iterativo, Ticket medio, etc.) adaptables al *Contexto de Filtro*.

### 5. Diseño del Dashboard y UI/UX
Se ha diseñado un Cuadro de Mando interactivo con estética "Premium", dividido en páginas orientadas a diferentes perfiles de negocio:

* **Página 1: Visión General (Perfil Directivo/Inversor)**
  * KPIs financieros principales (Ingreso Real, Pérdidas totales y % de ocupación).
  * Gráficos de tendencias temporales, mapas de geolocalización de rendimiento y clubes en peligro.
    
    ![informe1](https://github.com/Nachoide100/Analisis-PadelZgz/blob/54c2602187bb19b1d9c26d07d6439522a6c0f19a/visualizations/Captura%20de%20pantalla%202026-02-25%20150626.png)
    
* **Página 2: Inteligencia Operativa y Pricing (Perfil Manager/Operaciones)**
  * Matrices (Heatmaps) de calor para detectar cuellos de botella por día y franja horaria. 
  * Análisis de infraestructura (rendimiento pistas indoor vs outdoor).
  * Gráficos de dispersión y rankings de pistas.
  * Determinación de objetivo de % de reservas consecutivas.
    
   ![informe2](https://github.com/Nachoide100/Analisis-PadelZgz/blob/54c2602187bb19b1d9c26d07d6439522a6c0f19a/visualizations/Captura%20de%20pantalla%202026-02-25%20150634.png)
   
* **🚀 Feature Destacada: Custom Tooltip Page**
  * Se implementó una página oculta de "Información sobre herramientas". Al pasar el ratón sobre los clubes en el mapa interactivo, se despliega un mini-informe emergente con las peores horas de ocupación específicas de ese activo, logrando una experiencia de usuario (UX) inmersiva.
    
![tooltip](https://github.com/Nachoide100/Analisis-PadelZgz/blob/54c2602187bb19b1d9c26d07d6439522a6c0f19a/visualizations/Captura%20de%20pantalla%202026-02-25%20150551.png)

---

## 📂 Estructura del Repositorio
* `/scripts_python`: Código fuente de la simulación probabilística de reservas.
* `/sql`: Scripts DDL de creación de tablas y las consultas SQL de las vistas.
* `/powerbi`: (Opcional) Archivo `.pbix` o capturas de pantalla del Dashboard en alta resolución.
