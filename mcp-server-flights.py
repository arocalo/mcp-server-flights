from mcp.server.fastmcp import FastMCP
from typing import List, Dict

mcp = FastMCP("MCP-SERVER-FLIGHTS")

FAKE_FLIGHTS = [
    {"origen": "MAD", "destino": "NYC", "mes": "enero", "precio": 450},
    {"origen": "MAD", "destino": "NYC", "mes": "febrero", "precio": 420},
    {"origen": "MAD", "destino": "CDG", "mes": "enero", "precio": 120},
    {"origen": "BCN", "destino": "NYC", "mes": "enero", "precio": 500},
]

@mcp.tool()
def recommend_flights(origen: str = None, destino: str = None, mes: str = None) -> List[Dict]:
    """
    Recomienda vuelos según origen, destino y mes.
    - origen: código IATA (ej: MAD, BCN) - OBLIGATORIO
    - destino: código IATA (ej: NYC, CDG) - OBLIGATORIO
    - mes: mes en minúsculas en español (ej: enero, febrero) - OBLIGATORIO
    
    Si falta algún campo, devuelve un mensaje claro indicando qué falta.
    Si no hay vuelos, muestra destinos y fechas disponibles desde el origen.
    Usa get_available_options() para conocer las opciones válidas.
    """
    campos_faltantes = []
    if origen is None:
        campos_faltantes.append("origen")
    if destino is None:
        campos_faltantes.append("destino")
    if mes is None:
        campos_faltantes.append("mes")
    
    if campos_faltantes:
        opciones = get_available_options()
        return [{
            "error": "Información incompleta",
            "campos_faltantes": campos_faltantes,
            "mensaje": f"Para buscar vuelos necesito que me proporciones: {', '.join(campos_faltantes)}",
            "sugerencias": {
                "origenes_disponibles": opciones["origenes_disponibles"],
                "destinos_disponibles": opciones["destinos_disponibles"],
                "meses_disponibles": opciones["meses_disponibles"]
            }
        }]
    
    opciones = get_available_options()
    errores_validacion = []
    
    if origen not in opciones["origenes_disponibles"]:
        errores_validacion.append(f"Origen '{origen}' no válido. Opciones: {opciones['origenes_disponibles']}")
    
    if destino not in opciones["destinos_disponibles"]:
        errores_validacion.append(f"Destino '{destino}' no válido. Opciones: {opciones['destinos_disponibles']}")
    
    if mes not in opciones["meses_disponibles"]:
        errores_validacion.append(f"Mes '{mes}' no válido. Opciones: {opciones['meses_disponibles']}")
    
    if errores_validacion:
        return [{
            "error": "Datos inválidos",
            "errores": errores_validacion,
            "mensaje": "Por favor, corrige los datos e intenta nuevamente"
        }]
    
    results = [
        f for f in FAKE_FLIGHTS
        if f["origen"] == origen and f["destino"] == destino and f["mes"] == mes
    ]
    
    if results:
        return results
    
    destinos_desde_origen = sorted(set(
        f["destino"] for f in FAKE_FLIGHTS 
        if f["origen"] == origen
    ))
    
    meses_desde_origen = sorted(set(
        f["mes"] for f in FAKE_FLIGHTS 
        if f["origen"] == origen
    ))
    
    destinos_desde_origen_destino = sorted(set(
        f["destino"] for f in FAKE_FLIGHTS 
        if f["origen"] == origen and f["mes"] == mes
    ))
    
    meses_desde_origen_destino = sorted(set(
        f["mes"] for f in FAKE_FLIGHTS 
        if f["origen"] == origen and f["destino"] == destino
    ))
    
    return [{
        "mensaje": "No se encontraron vuelos para los criterios especificados",
        "criterios_busqueda": {
            "origen": origen,
            "destino": destino,
            "mes": mes
        },
        "alternativas_disponibles": {
            "todos_destinos_desde_origen": destinos_desde_origen,
            "todos_meses_desde_origen": meses_desde_origen,
            "destinos_disponibles_en_mes_especificado": destinos_desde_origen_destino,
            "meses_disponibles_para_destino_especificado": meses_desde_origen_destino
        },
        "sugerencias": [
            f"Destinos disponibles desde {origen}: {', '.join(destinos_desde_origen)}",
            f"Meses disponibles desde {origen}: {', '.join(meses_desde_origen)}",
            f"Para el mes de {mes}, destinos disponibles desde {origen}: {', '.join(destinos_desde_origen_destino) if destinos_desde_origen_destino else 'Ninguno'}",
            f"Para el destino {destino}, meses disponibles desde {origen}: {', '.join(meses_desde_origen_destino) if meses_desde_origen_destino else 'Ninguno'}"
        ]
    }]

@mcp.tool()
def get_available_options(origen: str = None) -> Dict[str, List[str]]:
    """
    Consulta todos los destinos, orígenes y meses disponibles en la base de datos.
    Si se proporciona un origen, muestra solo los destinos y meses disponibles desde ese origen.
    - origen: código IATA opcional para filtrar (ej: MAD, BCN)
    """
    if origen:
        destinos = sorted(set(f["destino"] for f in FAKE_FLIGHTS if f["origen"] == origen))
        meses = sorted(set(f["mes"] for f in FAKE_FLIGHTS if f["origen"] == origen))
        
        return {
            "origen_especificado": origen,
            "destinos_disponibles_desde_origen": destinos,
            "meses_disponibles_desde_origen": meses,
            "todos_los_origenes_disponibles": sorted(set(f["origen"] for f in FAKE_FLIGHTS))
        }
    else:
        origenes = sorted(set(f["origen"] for f in FAKE_FLIGHTS))
        destinos = sorted(set(f["destino"] for f in FAKE_FLIGHTS))
        meses = sorted(set(f["mes"] for f in FAKE_FLIGHTS))
        
        return {
            "origenes_disponibles": origenes,
            "destinos_disponibles": destinos,
            "meses_disponibles": meses
        }

@mcp.resource("airports://info")
def airports() -> Dict[str, List[str]]:
    """
    Recurso que devuelve los orígenes y destinos disponibles.
    Sirve para que el LLM guíe al usuario con entradas válidas.
    """
    origenes = sorted(set(f["origen"] for f in FAKE_FLIGHTS))
    destinos = sorted(set(f["destino"] for f in FAKE_FLIGHTS))
    meses = sorted(set(f["mes"] for f in FAKE_FLIGHTS))
    
    return {
        "origenes": origenes, 
        "destinos": destinos,
        "meses": meses,
        "mensaje": "Usa get_available_options() para obtener información más detallada filtrada por origen"
    }

if __name__ == "__main__":
    mcp.run()