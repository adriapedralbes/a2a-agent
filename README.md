# Sistema Multi-Agente de Desarrollo con Protocolo A2A

Este proyecto implementa un sistema de desarrollo colaborativo utilizando el protocolo Agent-to-Agent (A2A) de Google. Permite que múltiples agentes especializados trabajen juntos para planificar e implementar una aplicación web, con mínima intervención humana después del prompt inicial.

## Vista General

El sistema consta de tres agentes principales que se comunican entre sí a través del protocolo A2A:

1. **Agente Planificador**:
   - Recibe instrucciones del usuario
   - Crea un plan detallado (plan.md) para el proyecto
   - Genera una lista de tareas organizada (tasks.md) dividida en secciones frontend y backend
   - Coordina el trabajo entre los agentes especialistas

2. **Agente Frontend**:
   - Especialista en desarrollo frontend
   - Implementa las tareas de frontend definidas en tasks.md
   - Marca las tareas completadas con una X
   - Crea los archivos y directorios necesarios para la interfaz de usuario

3. **Agente Backend**:
   - Especialista en desarrollo backend
   - Implementa las tareas de backend definidas en tasks.md
   - Marca las tareas completadas con una X
   - Crea los archivos y directorios necesarios para el servidor y la API

El sistema utiliza el Desktop Commander MCP para proporcionar a los agentes acceso al sistema de archivos y capacidades de terminal.

## Estructura del Proyecto

```
/home/adria/a2a-agent/
├── agents/
│   ├── planner/          # Agente para planificación del proyecto
│   │   ├── server.py     # Servidor A2A del planificador
│   │   └── client.py     # Cliente para el agente planificador
│   ├── frontend/         # Agente para desarrollo frontend
│   │   ├── server.py     # Servidor A2A del frontend
│   │   └── client.py     # Cliente para el agente frontend
│   └── backend/          # Agente para desarrollo backend
│       ├── server.py     # Servidor A2A del backend
│       └── client.py     # Cliente para el agente backend
├── common/               # Código compartido entre agentes
│   └── utils.py          # Utilidades comunes
├── plan.md               # Plan del proyecto (generado por el agente planificador)
├── tasks.md              # Lista de tareas (generada por el agente planificador)
├── .env                  # Variables de entorno (claves API)
└── run_agents.sh         # Script para iniciar los agentes
```

## Configuración

1. Crea un entorno virtual de Python:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   ```

2. Crea un archivo `.env` basado en `.env.example`:

   ```
   OPENAI_API_KEY=tu_clave_api_openai
   ```

3. Instala Desktop Commander MCP:

   ```bash
   npx @wonderwhy-er/desktop-commander@latest setup
   ```

4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

El script `run_agents.sh` facilita la ejecución de los diferentes agentes:

```bash
./run_agents.sh
```

Este script proporciona un menú para seleccionar qué agentes ejecutar:

1. Todos los agentes (Planificador, Frontend, Backend)
2. Solo agente Planificador
3. Solo agente Frontend
4. Solo agente Backend
5. Agentes Frontend y Backend

### Flujo de trabajo típico:

1. **Planificación del proyecto**:
   - Ejecuta el Agente Planificador
   - Proporciona una descripción del proyecto web que deseas crear
   - El agente generará archivos plan.md y tasks.md

2. **Desarrollo**:
   - Ejecuta los Agentes Frontend y Backend
   - Estos agentes analizarán tasks.md y comenzarán a implementar sus tareas respectivas
   - Los agentes marcarán las tareas como completadas en tasks.md

3. **Iteración**:
   - Los agentes continuarán trabajando hasta que todas las tareas estén completadas
   - Puedes hacer ajustes al plan.md o tasks.md manualmente si es necesario

## Cómo funciona el protocolo A2A

El protocolo Agent-to-Agent (A2A) de Google define un estándar para la comunicación entre agentes a través de endpoints HTTP:

- **Agent Card**: Un documento JSON que describe las capacidades y endpoints de un agente
- **API de Tareas**: Endpoints para enviar tareas a los agentes y recibir respuestas
- **Formato de Mensaje Estandarizado**: Una estructura consistente para los mensajes intercambiados

Cada agente en este sistema implementa el protocolo A2A, lo que permite una colaboración fluida y estandarizada.

## Ejemplo de Uso

Ejemplo de interacción con el sistema:

1. **Usuario**: "Necesito una aplicación web para gestionar un inventario de productos, con formularios para añadir/editar productos y una página para ver todos los productos."

2. **Agente Planificador**: 
   - Crea plan.md con la arquitectura (React frontend, Node.js backend, MongoDB)
   - Genera tasks.md con tareas específicas para frontend y backend

3. **Agente Frontend**:
   - Implementa componentes React, formularios, páginas, etc.
   - Marca tareas como completadas

4. **Agente Backend**:
   - Implementa API REST, modelos de datos, autenticación, etc.
   - Marca tareas como completadas

Al final, tienes una aplicación web funcional creada con mínima intervención humana.
