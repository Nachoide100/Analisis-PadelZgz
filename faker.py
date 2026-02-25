import pandas as pd
import random
from datetime import datetime, timedelta
import uuid

# =====================================================================
# 1. REGLAS DE NEGOCIO (Aquí defines tu universo)
# =====================================================================
# He transcrito los datos exactos de tu Excel para los 2 primeros clubes.
# Solo tienes que añadir el resto de clubes copiando esta estructura.

clubes_data = {
    "Padel Deportivo Ebro": {
        "coordenadas": "41°40'04.3\"N 0°55'22.4\"W",
        "pistas": {"Interior": 5, "Exterior": 3},
        "precios": {
            "Laboral": {
                "Interior": [
                    {"inicio": "09:00", "fin": "16:00", "precio": 14.56},
                    {"inicio": "16:00", "fin": "17:00", "precio": 20.11},
                    {"inicio": "17:00", "fin": "20:30", "precio": 27.04},
                    {"inicio": "20:30", "fin": "21:30", "precio": 24.96},
                    {"inicio": "21:30", "fin": "23:00", "precio": 22.88}
                ],
                "Exterior": [
                    {"inicio": "09:00", "fin": "16:00", "precio": 7.80},
                    {"inicio": "16:30", "fin": "17:00", "precio": 12.83},
                    {"inicio": "17:00", "fin": "17:30", "precio": 17.83},
                    {"inicio": "17:30", "fin": "21:30", "precio": 22.88},
                    {"inicio": "21:30", "fin": "23:00", "precio": 20.80}
                ]
            },
            "Fin_Semana": {
                "Interior": [
                    {"inicio": "08:00", "fin": "12:30", "precio": 20.80},
                    {"inicio": "12:30", "fin": "13:00", "precio": 18.72},
                    {"inicio": "13:00", "fin": "16:00", "precio": 14.56},
                    {"inicio": "16:00", "fin": "21:00", "precio": 18.72}
                ],
                "Exterior": [
                    {"inicio": "08:00", "fin": "13:00", "precio": 16.64},
                    {"inicio": "13:00", "fin": "14:00", "precio": 15.96},
                    {"inicio": "14:00", "fin": "21:00", "precio": 14.56}
                ]
            }
        }
    },
    
    "SoccerWorld Zaragoza": {
        "coordenadas": "41°40'23.5\"N 0°54'03.1\"W",
        "pistas": {"Interior": 5, "Exterior": 6},
        "precios": {
            "Laboral": {
                "Interior": [
                    {"inicio": "08:00", "fin": "14:00", "precio": 20.79},
                    {"inicio": "14:00", "fin": "17:00", "precio": 28.08},
                    {"inicio": "17:00", "fin": "23:00", "precio": 32.76}
                ],
                "Exterior": [
                    {"inicio": "08:00", "fin": "14:00", "precio": 18.72},
                    {"inicio": "14:00", "fin": "16:30", "precio": 21.84},
                    {"inicio": "17:00", "fin": "23:00", "precio": 31.20}
                ]
            },
            "Fin_Semana": {
                "Interior": [
                    {"inicio": "09:00", "fin": "14:00", "precio": 28.08},
                    {"inicio": "14:00", "fin": "21:00", "precio": 24.96}
                ],
                "Exterior": [
                    {"inicio": "09:00", "fin": "14:00", "precio": 24.96},
                    {"inicio": "14:00", "fin": "21:00", "precio": 21.84}
                ]
            }
        }
    },

    "Montecanal centro deportivo": {
        "coordenadas": "41°37'46.8\"N 0°56'45.5\"W",
        "pistas": {"Interior": 6},
        "precios": {
            "Laboral": {
                "Interior": [
                    {"inicio": "08:00", "fin": "16:00", "precio": 17.27},
                    {"inicio": "16:00", "fin": "22:00", "precio": 35.36}
                ]
            },
            "Fin_Semana": {
                "Interior": [
                    {"inicio": "08:00", "fin": "21:00", "precio": 20.80}
                ]
            }
        }
    },

    "Padel Indoor Aragón": {
        "coordenadas": "41°38'39.4\"N 0°51'19.6\"W",
        "pistas": {"Interior": 6},
        "precios": {
            "Laboral": {
                "Interior": [
                    {"inicio": "08:00", "fin": "15:00", "precio": 15.81},
                    {"inicio": "15:00", "fin": "22:00", "precio": 31.83}
                ]
            },
            "Fin_Semana": {
                "Interior": [
                    {"inicio": "08:00", "fin": "14:00", "precio": 22.88},
                    {"inicio": "14:00", "fin": "17:00", "precio": 16.64},
                    {"inicio": "17:00", "fin": "23:00", "precio": 22.88}
                ]
            }
        }
    },

    "Regal Padel Club": {
        "coordenadas": "41°38'36.9\"N 0°56'06.4\"W",
        "pistas": {"Interior": 8},
        "precios": {
            "Laboral": {
                "Interior": [
                    {"inicio": "09:00", "fin": "16:00", "precio": 18.72},
                    {"inicio": "16:00", "fin": "23:00", "precio": 34.32}
                ]
            },
            "Fin_Semana": {
                "Interior": [
                    {"inicio": "08:00", "fin": "22:00", "precio": 23.92}
                ]
            }
        }
    },

    "Forus Aragonia": {
        "coordenadas": "41°38'26.9\"N 0°54'34.6\"W",
        "pistas": {"Exterior": 4},
        "precios": {
            "Laboral": {
                "Exterior": [
                    {"inicio": "07:00", "fin": "22:00", "precio": 30.58}
                ]
            },
            "Fin_Semana": {
                "Exterior": [
                    {"inicio": "09:00", "fin": "21:00", "precio": 30.58}
                ]
            }
        }
    },

    "Urban Sport": {
        "coordenadas": "41°40'18.6\"N 0°52'44.1\"W",
        "pistas": {"Interior": 9, "Semicubierta": 2, "Exterior": 2},
        "precios": {
            "Laboral": {
                "Interior": [
                    {"inicio": "07:00", "fin": "12:00", "precio": 22.05},
                    {"inicio": "13:00", "fin": "15:00", "precio": 14.56},
                    {"inicio": "15:00", "fin": "16:00", "precio": 22.05},
                    {"inicio": "16:00", "fin": "17:00", "precio": 25.80},
                    {"inicio": "17:00", "fin": "23:00", "precio": 33.08}
                ],
                "Semicubierta": [
                    {"inicio": "07:00", "fin": "15:00", "precio": 17.06},
                    {"inicio": "15:00", "fin": "15:30", "precio": 19.90},
                    {"inicio": "15:30", "fin": "17:00", "precio": 22.75},
                    {"inicio": "17:00", "fin": "23:00", "precio": 25.59}
                ],
                "Exterior": [
                    {"inicio": "07:00", "fin": "15:00", "precio": 13.32},
                    {"inicio": "15:00", "fin": "15:30", "precio": 15.40},
                    {"inicio": "15:30", "fin": "16:00", "precio": 17.48},
                    {"inicio": "16:00", "fin": "23:00", "precio": 19.56}
                ]
            },
            "Fin_Semana": {
                "Interior": [{"inicio": "08:00", "fin": "21:00", "precio": 25.17}],
                "Semicubierta": [{"inicio": "08:00", "fin": "21:00", "precio": 25.17}],
                "Exterior": [{"inicio": "08:00", "fin": "21:00", "precio": 19.97}]
            }
        }
    },

    "CDM Alberto Maestro": {
        "coordenadas": "41.6502602, -0.8649524",
        "pistas": {"Exterior": 3, "Semicubierta": 3},
        "precios": {
            "Laboral": {
                "Exterior": [
                    {"inicio": "09:00", "fin": "16:00", "precio": 18.00},
                    {"inicio": "16:00", "fin": "22:00", "precio": 24.00}
                ],
                "Semicubierta": [
                    {"inicio": "09:00", "fin": "16:00", "precio": 18.00},
                    {"inicio": "16:00", "fin": "17:00", "precio": 20.00},
                    {"inicio": "17:00", "fin": "22:00", "precio": 24.00}
                ]
            },
            "Fin_Semana": {
                "Exterior": [
                    {"inicio": "08:00", "fin": "16:00", "precio": 21.00},
                    {"inicio": "16:00", "fin": "22:00", "precio": 18.00}
                ],
                "Semicubierta": [
                    {"inicio": "08:00", "fin": "16:00", "precio": 22.50},
                    {"inicio": "16:00", "fin": "22:00", "precio": 18.00}
                ]
            }
        }
    },

    "CDM Bombarda Delicias": {
        "coordenadas": "41.6560839, -0.9182398",
        "pistas": {"Exterior": 2, "Semicubierta": 4},
        "precios": {
            "Laboral": {
                "Exterior": [
                    {"inicio": "09:00", "fin": "16:00", "precio": 18.00},
                    {"inicio": "16:00", "fin": "22:00", "precio": 24.00}
                ],
                "Semicubierta": [
                    {"inicio": "09:00", "fin": "16:00", "precio": 18.00},
                    {"inicio": "16:00", "fin": "17:00", "precio": 20.00},
                    {"inicio": "17:00", "fin": "22:00", "precio": 24.00}
                ]
            },
            "Fin_Semana": {
                "Exterior": [
                    {"inicio": "08:00", "fin": "16:00", "precio": 21.00},
                    {"inicio": "16:00", "fin": "22:00", "precio": 18.00}
                ],
                "Semicubierta": [
                    {"inicio": "08:00", "fin": "16:00", "precio": 22.50},
                    {"inicio": "16:00", "fin": "22:00", "precio": 18.00}
                ]
            }
        }
    },

    "Real Zaragoza Club De Tenis": {
        "coordenadas": "41°40'07.4\"N 0°58'43.1\"W",
        "pistas": {"Interior": 4, "Exterior": 5},
        "precios": {
            "Laboral": {
                "Interior": [
                    {"inicio": "08:00", "fin": "16:00", "precio": 18.72},
                    {"inicio": "16:00", "fin": "18:00", "precio": 29.82},
                    {"inicio": "18:00", "fin": "23:00", "precio": 35.36}
                ],
                "Exterior": [
                    {"inicio": "08:00", "fin": "17:00", "precio": 14.56},
                    {"inicio": "17:00", "fin": "18:00", "precio": 18.03},
                    {"inicio": "18:00", "fin": "23:00", "precio": 24.96}
                ]
            },
            "Fin_Semana": {
                "Interior": [
                    {"inicio": "09:00", "fin": "13:30", "precio": 35.36},
                    {"inicio": "13:30", "fin": "23:00", "precio": 18.72}
                ],
                "Exterior": [
                    {"inicio": "09:00", "fin": "13:00", "precio": 18.72},
                    {"inicio": "13:00", "fin": "18:00", "precio": 14.56},
                    {"inicio": "18:00", "fin": "23:00", "precio": 20.80}
                    ]
            }
        }
    },

    "Premium Padel Zaragoza": {
        "coordenadas": "41°35'42.2\"N 0°55'54.1\"W",
        "pistas": {"Interior": 2},
        "precios": {
            "Laboral": {
                "Interior": [
                    {"inicio": "07:00", "fin": "15:00", "precio": 14.56},
                    {"inicio": "16:00", "fin": "22:00", "precio": 29.12},
                    {"inicio": "22:00", "fin": "00:00", "precio": 22.88}
                ]
            },
            "Fin_Semana": {
                "Interior": [
                    {"inicio": "07:00", "fin": "00:00", "precio": 22.88}
                ]
            }
        }
    },

    "Padel corazonistas Moncayo": {
        "coordenadas": "41°38'17.2\"N 0°54'35.5\"W",
        "pistas": {"Semicubierta": 2},
        "precios": {
            "Laboral": {
                "Semicubierta": [
                    {"inicio": "08:00", "fin": "15:00", "precio": 15.60},
                    {"inicio": "15:00", "fin": "16:00", "precio": 21.86},
                    {"inicio": "16:00", "fin": "20:00", "precio": 24.96},
                    {"inicio": "20:00", "fin": "22:00", "precio": 21.86}
                ]
            },
            "Fin_Semana": {
                "Semicubierta": [
                    {"inicio": "08:00", "fin": "22:00", "precio": 21.84}
                ]
            }
        }
    },

    "Forus Siglo XXI": {
        "coordenadas": "41°40'31.5\"N 0°53'50.3\"W",
        "pistas": {"Exterior": 2},
        "precios": {
            "Laboral": {
                "Exterior": [
                    {"inicio": "07:00", "fin": "22:00", "precio": 20.60}
                ]
            },
            "Fin_Semana": {
                "Exterior": [
                    {"inicio": "08:00", "fin": "20:00", "precio": 20.60}
                ]
            }
        }
    },

    "Padel Indoor Cuarte": {
        "coordenadas": "41°35'52.6\"N 0°55'49.0\"W",
        "pistas": {"Interior": 4},
        "precios": {
            "Laboral": {
                "Interior": [
                    {"inicio": "08:00", "fin": "12:00", "precio": 18.72},
                    {"inicio": "12:00", "fin": "15:00", "precio": 20.79},
                    {"inicio": "15:00", "fin": "15:30", "precio": 24.96},
                    {"inicio": "15:30", "fin": "16:00", "precio": 29.11},
                    {"inicio": "16:00", "fin": "00:00", "precio": 33.28}
                ]
            },
            "Fin_Semana": {
                "Interior": [
                    {"inicio": "08:00", "fin": "00:00", "precio": 23.92}
                ]
            }
        }
    },

    "Momento Padel": {
        "coordenadas": "41°35'53.7\"N 0°55'43.7\"W",
        "pistas": {"Interior": 4},
        "precios": {
            "Laboral": {
                "Interior": [
                    {"inicio": "00:00", "fin": "03:00", "precio": 12.48},
                    {"inicio": "07:00", "fin": "15:00", "precio": 14.56},
                    {"inicio": "16:00", "fin": "20:00", "precio": 24.96},
                    {"inicio": "20:00", "fin": "22:00", "precio": 20.00},
                    {"inicio": "22:00", "fin": "00:00", "precio": 16.64}
                ]
            },
            "Fin_Semana": {
                "Interior": [
                    {"inicio": "07:00", "fin": "22:00", "precio": 20.00} 
                ]
            }
        }
    }
}

# Franjas horarias estándar a simular (cada hora y media)
franjas_generales = ["09:30", "11:00", "12:30", "14:00", "15:30", "17:00", "18:30", "20:00", "21:30"]

# =====================================================================
# 2. FUNCIONES AUXILIARES
# =====================================================================
def obtener_precio(reglas_club, tipo_dia, tipo_pista, hora_actual):
    """Busca en el diccionario el precio correspondiente a la hora indicada"""
    tramos = reglas_club["precios"].get(tipo_dia, {}).get(tipo_pista, [])
    for tramo in tramos:
        if tramo["inicio"] <= hora_actual <= tramo["fin"] or tramo["inicio"] <= hora_actual and tramo["fin"] < tramo["inicio"]: 
            return tramo["precio"]
    # Si no encuentra tramo exacto en los datos, ponemos un precio base por defecto
    return 15.00 

def generar_franjas_dinamicas(tramos_precios, duracion_minutos=90):
    """
    Lee los tramos de precios de un club para ese día y genera
    los huecos de reservas (ej. cada 90 mins) respetando sus aperturas y cierres.
    """
    franjas_validas = []
    formato = "%H:%M"
    
    # Si por algún error no hay tramos, devolvemos lista vacía
    if not tramos_precios:
        return []

    # Recorremos cada regla de precio (ej. de 09:00 a 16:00)
    for tramo in tramos_precios:
        # Convertimos el texto "09:00" a un objeto de tiempo de Python
        hora_actual = datetime.strptime(tramo["inicio"], formato)
        
        # Manejamos el caso especial de medianoche ("00:00" como cierre)
        if tramo["fin"] == "00:00":
            hora_fin = datetime.strptime("23:59", formato)
        else:
            hora_fin = datetime.strptime(tramo["fin"], formato)
            
        # Mientras quepa un partido de 90 minutos dentro de este horario...
        while hora_actual + timedelta(minutes=duracion_minutos) <= hora_fin:
            franja_texto = hora_actual.strftime(formato)
            
            # Evitamos duplicados por si los tramos de precios se pisan
            if franja_texto not in franjas_validas:
                franjas_validas.append(franja_texto)
                
            # Avanzamos 90 minutos al siguiente turno
            hora_actual += timedelta(minutes=duracion_minutos)
            
    # Ordenamos cronológicamente desde la mañana hasta la noche
    return sorted(list(set(franjas_validas)))

# =====================================================================
# 3. MOTOR DE PROBABILIDAD (El "Dado Virtual")
# =====================================================================
def calcular_probabilidad_ocupacion(hora, es_fin_de_semana, tipo_pista):
    """Aquí está la magia analítica. Definimos el % de ocupación según contexto."""
    prob_base = 0.0
    
    # A) Probabilidad por Franja Horaria (Lunes a Viernes)
    if not es_fin_de_semana:
        if hora < "13:30":
            prob_base = 0.25      # Mañanas laborables: 25% ocupación
        elif "13:30" <= hora < "15:00":
            prob_base = 0.15     
        elif "15:00" <= hora <  "17:00":
            prop_base = 0.35
        elif "17:00" <= hora < "21:00":
            prob_base = 0.95      # HORA PICO (Tardes): 90% ocupación (¡casi todo lleno!)
        else:
            prob_base = 0.50     # Noches (21:30 en adelante): 60%
            
    # B) Probabilidad por Fin de Semana (Sábados y Domingos)
    else:
        if hora < "10:00":
            prob_base = 0.60      
        elif "10:00" <= hora < "14:00":
            prob_base = 0.85      # Mañanas de finde: 85% ocupación
        elif "14:00" <= hora < "16:00":
            prob_base = 0.10      
        elif "16:00" <= hora < "18:00":
            prob_base = 0.35      
        else:
            prob_base = 0.50      # Tardes/Noche de finde: 65%

    # C) Modificador por Tipo de Pista (Zaragoza es ventosa/fría)
    # Penalizamos ligeramente las pistas exteriores porque la gente prefiere indoor
    if tipo_pista == "Exterior":
        prob_base -= 0.10 
        
    # Asegurarnos de que la probabilidad no salga de [0, 1]
    return max(0.0, min(1.0, prob_base))

# =====================================================================
# 4. BUCLE PRINCIPAL (Generación del Dataset)
# =====================================================================
datos_simulados = []
fecha_inicio = datetime.now()
dias_a_simular = 14 # Simulemos 2 semanas enteras para tener más datos

print("Iniciando simulación...")

for nombre_club, info_club in clubes_data.items():
    print(f"Simulando reservas para: {nombre_club}")
    
    for dia_delta in range(dias_a_simular):
        fecha_actual = fecha_inicio + timedelta(days=dia_delta)
        es_fin_semana = fecha_actual.weekday() >= 5 
        tipo_dia_str = "Fin_Semana" if es_fin_semana else "Laboral"
        
        # Iteramos por tipo de pista (Interior / Exterior)
        for tipo_pista, cantidad in info_club["pistas"].items():
            
            # Iteramos por cada pista física (ej. Pista 1, Pista 2...)
            for num_pista in range(1, cantidad + 1):
                nombre_pista = f"{tipo_pista} {num_pista}"
                
                # --- AQUÍ ESTÁ LA MEJORA MAGISTRAL ---
                # 1. Buscamos qué reglas de precios tocan hoy (Laboral o Fin de semana)
                tramos_de_hoy = info_club["precios"].get(tipo_dia_str, {}).get(tipo_pista, [])
                
                # 2. Le pedimos a nuestra función que construya las horas válidas
                franjas_dinamicas = generar_franjas_dinamicas(tramos_de_hoy, duracion_minutos=90)
                
                # Iteramos SOLO por las horas válidas en las que el club está abierto
                for hora in franjas_dinamicas:
                    
                    # 1. Calculamos la probabilidad teórica
                    probabilidad = calcular_probabilidad_ocupacion(hora, es_fin_semana, tipo_pista)
                    
                    # 2. Tiramos el dado virtual
                    estado = "Ocupada" if random.random() <= probabilidad else "Libre"
                    
                    # 3. Obtenemos el precio exacto
                    precio_hora = obtener_precio(info_club, tipo_dia_str, tipo_pista, hora)
                    
                    # 4. Guardamos la fila
                    datos_simulados.append({
                        "ID_Reserva": str(uuid.uuid4())[:8] if estado == "Ocupada" else None,
                        "Club": nombre_club,
                        "Coordenadas": info_club["coordenadas"],
                        "Fecha": fecha_actual.strftime("%Y-%m-%d"),
                        "Dia_Semana": fecha_actual.strftime("%A"),
                        "Es_Fin_Semana": 1 if es_fin_semana else 0,
                        "Hora": hora,
                        "Tipo_Pista": tipo_pista,
                        "Nombre_Pista": nombre_pista,
                        "Estado": estado,
                        "Precio_Euro": precio_hora,
                        "Ingreso_Generado": precio_hora if estado == "Ocupada" else 0.0
                    })

# =====================================================================
# 5. EXPORTACIÓN DEL RESULTADO
# =====================================================================
df_final = pd.DataFrame(datos_simulados)
nombre_archivo = "dataset_padel_zaragoza_simulado.csv"
df_final.to_csv(nombre_archivo, index=False, encoding='utf-8')

print(f"\n¡Éxito! Se han generado {len(df_final)} registros en '{nombre_archivo}'.")