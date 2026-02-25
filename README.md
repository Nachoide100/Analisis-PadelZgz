# 🎾 Padel Data Analytics & Revenue Management (Zaragoza)

## 📌 Visión General del Proyecto
Este es un proyecto *End-to-End* de Ingeniería y Análisis de Datos centrado en el modelo de negocio de los clubes de pádel en la ciudad de Zaragoza y sus alrededores. La verdad que es últimamente mis amigos y yo siempre estamos mirando a ver a qué pista y a qué hora podemos ir para que nos salga más barato. Asi pues, con este proyecto buscaba, en principio un objetivo, pero que luego fueron dos: 
  1. Investigar y analizar los precios de las pistas de los clubes de padel en Zaragoza para poder, de un vistazo, saber dónde y cuándo es más rentable jugar.
  2. Ya que estábamos, analizar el mercado padelístico en mi ciudad y ver, a través del análisis de datos, si podia proponer alguna mejora económica a algún club (de la cual pudiera salir yo también beneficiado jeje).

Espero que os guste! La verdad que lo yo lo he disfrutado bastante y me he llevado alguna sorpresa (el próximo finde creao que cambiaremos de pista de juego jajaa). 


## 🛠️ Stack Tecnológico

**Extracción y Simulación de Datos** <br>
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)

**Base de Datos & Capa Semántica** <br>
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

**Business Intelligence & UI/UX** <br>
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![DAX](https://img.shields.io/badge/DAX-00599C?style=for-the-badge&logo=microsoft&logoColor=white)

---

## 🏗️ Fases del Proyecto y Arquitectura

### 1. 🔍 Recopilación de Datos Base (Mapeo Manual)
Para garantizar la precisión del modelo de negocio, la primera fase consistió en un trabajo de investigación y recolección manual. 
* Se mapearon los principales clubes de Zaragoza y su área metropolitana.
* Se estructuraron las franjas horarias operativas de cada centro.
* Se extrajeron las tarifas y políticas de precios (Pricing) dependiendo del tipo de pista (Interior, Exterior, Semicubierta) y de la franja del día.

(Esto lo tuve que hacer manualmente porque Playtomic tenía una gran defensa anti - scrapping asi que si alguien quiere los datos están en el .csv de PAPAPADEL.)

### 2. 🎲 Simulación de Demanda Algorítmica (Python)
Ante la imposibilidad de extraer datos transaccionales privados de los clubes, se desarrolló un script en Python para generar un *dataset* sintético de reservas de alta fidelidad para un periodo de **dos semanas**.
* **Modelos Probabilísticos:** Los datos no son aleatorios. Se programaron lógicas de probabilidad basadas en el comportamiento real del consumidor (ej. mayor probabilidad de reservas en horario de tarde/noche en días laborales, y picos de ocupación matinal en fines de semana).
* **Variables generadas:** ID de reserva, club, fechas, horas, estado (Libre/Ocupada) e ingresos generados vs. potenciales.

### 3. 🗄️ Capa Semántica y Data Warehouse (PostgreSQL)
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
---

### 4. 🎨 Diseño del Dashboard y UI/UX
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

## 💡 Top 5 Business Insights y Conclusiones (Propuestas de Valor)

El objetivo final de este modelo de datos no es solo descriptivo, sino **prescriptivo**. Tras analizar la ocupación y el *Lost Revenue*, se proponen las siguientes 5 estrategias de *Revenue Management* aplicables a los clubes analizados:

* 📉 **1. Estrategia de Precio Dinámico para Mañanas laborales**
  * **El Dato:** Las mañanas de diario (antes de las 14:00h) sufren una ocupación crítica.
  * **La Acción:** Crear una "Tarifa Plana Matinal" o bonos especiales con un 30% de descuento. Esto permite cubrir costes fijos (luz, alquiler) atrayendo a nichos con flexibilidad horaria (estudiantes, freelancers), sin sobrecargar las horas premium.

* 📈 **2. Optimización del precio en Horas Pico**
  * **El Dato:** A partir de las 17:00h (L-V), la ocupación se dispara, llegando al límite de capacidad entre las 18:00h y las 20:30h.
  * **La Acción:** Al existir una demanda inelástica, se recomienda aplicar **Precios Dinámicos** en esos huecos premium. Hay clubes que ya lo hacen pero otros (por ejemplo el Forus Aragonia) mantiene la misma tarifa para todas sus pistas a lo largo del día, lo que evita reservar matinales (demasiado caro) y no aprovecha las horas pico. 

* 🏆 **3. Rescate de las Tardes de Fin de Semana**
  * **El Dato:** El fin de semana invierte la tendencia: las mañanas son fuertes, pero las tardes sufren una caída severa de demanda.
  * **La Acción:** Rellenar este valle de 14:00h a 18:00h pivotando de vender "pistas sueltas" a vender "eventos".Organizar torneos "Americanas", competiciones mixtas o días familiares para solucionar la fricción del usuario a la hora de organizar partidos en ese horario.

* 🚨 **4. Recuperación de Ingresos: El modelo "Última hora"**
  * **El Dato:** De los 244.000€ de facturación potencial, solo se capturaron 120.000€, dejando **124.000€ de Lost Revenue** (dinero perdido por pistas vacías).
  * **La Acción:** Considerar cada pista no vendida como un coste hundido. Se propone implementar alertas de **Último Minuto (90 mins antes) con un 50% de descuento** automatizadas vía App, Telegram o WhatsApp. El coste marginal es cero y transforma un agujero financiero en beneficio neto.

---
Perfil -> [Perfil](https://github.com/Nachoide100/Nachoide100.git)

Contacto -> [LinkedIn](https://www.linkedin.com/in/jos%C3%A9-ignacio-rubio-194471308/)
