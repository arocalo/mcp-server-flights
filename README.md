# MCP Server Flights

Este proyecto implementa un servidor MCP (Model Context Protocol) para recomendar vuelos entre diferentes ciudades, usando la librería `fastmcp` y la especificación MCP. Permite consultar vuelos disponibles, orígenes, destinos y meses, así como obtener sugerencias si los datos proporcionados no son válidos o están incompletos.

## Requisitos

- Python 3.8 o superior
- Acceso a internet para instalar dependencias

## Instalación

1. **Clona el repositorio o descarga los archivos del proyecto.**

2. **Crea y activa un entorno virtual:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. **Instala las dependencias:**

```powershell
pip install -r requirements.txt
```

## Ejecución del servidor

Ejecuta el servidor MCP con el siguiente comando:

```powershell
mcp run .\mcp-server-flights.py -t sse
```

Esto iniciará el servidor en modo SSE (Server-Sent Events) en el puerto por defecto (8000).

## Endpoints y herramientas disponibles

- **recommend_flights**: Recomienda vuelos según origen, destino y mes. Devuelve errores claros si falta información o si los datos no son válidos.
- **get_available_options**: Devuelve los orígenes, destinos y meses disponibles. Permite filtrar por origen.
- **airports (recurso)**: Devuelve información general sobre orígenes, destinos y meses disponibles.

## Ejemplo de uso

Puedes interactuar con el servidor usando clientes compatibles con MCP o mediante la CLI de MCP.

Además, si usas Visual Studio Code, puedes acceder al archivo `mcp.json`, pulsar en **Start** y utilizar el chat de Copilot para interactuar fácilmente con el servidor y probar las recomendaciones de vuelos directamente desde el editor.

## Estructura del proyecto

- `mcp-server-flights.py`: Código principal del servidor MCP.
- `requirements.txt`: Lista de dependencias del proyecto.
- `README.md`: Este archivo.

## Notas

- El servidor utiliza datos de vuelos simulados (fake data) para propósitos de demostración.

