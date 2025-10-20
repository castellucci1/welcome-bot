# Bot de Bienvenida para Slack 🤖

Bot de bienvenida automatizado para Slack que saluda a nuevos miembros cuando se unen a un canal, responde a mensajes directos y menciones.

## ¿Qué hace este bot?

Este bot de Slack proporciona las siguientes funcionalidades:

- **Bienvenida automática**: Cuando un nuevo miembro se une a un canal, el bot envía un mensaje de bienvenida personalizado
- **Respuesta a menciones**: El bot responde cuando es mencionado en cualquier canal
- **Mensajes directos**: Responde a mensajes directos enviados al bot
- **Comando /hola**: Comando personalizado para saludar (opcional, requiere configuración en Slack)

## Requisitos previos

Antes de comenzar, asegúrate de tener lo siguiente:

- Python 3.7 o superior instalado en tu sistema
- Una cuenta de Slack con permisos de administrador para crear aplicaciones
- Acceso a un workspace de Slack donde instalar el bot

## Configuración en Slack

### 1. Crear una aplicación de Slack

1. Ve a [https://api.slack.com/apps](https://api.slack.com/apps)
2. Haz clic en **"Create New App"** (Crear Nueva Aplicación)
3. Selecciona **"From scratch"** (Desde cero)
4. Ingresa un nombre para tu aplicación (ej: "Bot de Bienvenida")
5. Selecciona el workspace donde deseas instalar el bot
6. Haz clic en **"Create App"** (Crear Aplicación)

### 2. Configurar permisos del bot (OAuth & Permissions)

1. En el menú lateral, ve a **"OAuth & Permissions"**
2. En la sección **"Scopes"**, agrega los siguientes **Bot Token Scopes**:
   - `app_mentions:read` - Para leer menciones del bot
   - `channels:history` - Para leer el historial de canales públicos
   - `channels:read` - Para ver información de canales públicos
   - `chat:write` - Para enviar mensajes
   - `im:history` - Para leer mensajes directos
   - `im:read` - Para ver mensajes directos
   - `im:write` - Para enviar mensajes directos
   - `users:read` - Para obtener información de usuarios

3. Desplázate hacia arriba y haz clic en **"Install to Workspace"** (Instalar en Workspace)
4. Autoriza la aplicación
5. Copia el **"Bot User OAuth Token"** (comienza con `xoxb-`), lo necesitarás después

### 3. Habilitar Socket Mode

1. En el menú lateral, ve a **"Socket Mode"**
2. Activa Socket Mode
3. Dale un nombre al token (ej: "Socket Token")
4. Copia el **"App-Level Token"** (comienza con `xapp-`), lo necesitarás después

### 4. Suscribirse a eventos (Event Subscriptions)

1. En el menú lateral, ve a **"Event Subscriptions"**
2. Activa **"Enable Events"**
3. En **"Subscribe to bot events"**, agrega los siguientes eventos:
   - `member_joined_channel` - Para detectar cuando un miembro se une a un canal
   - `app_mention` - Para detectar menciones del bot
   - `message.im` - Para recibir mensajes directos

4. Haz clic en **"Save Changes"** (Guardar Cambios)

### 5. Obtener el Signing Secret

1. En el menú lateral, ve a **"Basic Information"**
2. En la sección **"App Credentials"**, encontrarás el **"Signing Secret"**
3. Haz clic en **"Show"** y copia el valor, lo necesitarás después

### 6. (Opcional) Configurar comando slash

Si deseas usar el comando `/hola`:

1. En el menú lateral, ve a **"Slash Commands"**
2. Haz clic en **"Create New Command"**
3. Ingresa `/hola` como comando
4. Agrega una descripción
5. Guarda el comando

## Instalación y configuración local

### 1. Clonar el repositorio

```bash
git clone https://github.com/castellucci1/welcome-bot.git
cd welcome-bot
```

### 2. Crear un entorno virtual (recomendado)

```bash
# En Linux/MacOS
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

1. Copia el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

2. Edita el archivo `.env` y agrega tus tokens:

```env
SLACK_BOT_TOKEN=xoxb-tu-token-de-bot
SLACK_APP_TOKEN=xapp-tu-token-de-app
SLACK_SIGNING_SECRET=tu-signing-secret
```

**Importante**: Nunca compartas ni subas tu archivo `.env` a un repositorio público.

### 5. Ejecutar el bot

```bash
python bot.py
```

Si todo está configurado correctamente, deberías ver el mensaje:

```
⚡️ Bot de bienvenida iniciado en modo Socket
```

## Uso del bot

### Probar el bot

1. **Invita el bot a un canal**:
   - En Slack, ve a un canal
   - Escribe `/invite @NombreDeTuBot`

2. **Agrega un nuevo miembro al canal**:
   - El bot enviará automáticamente un mensaje de bienvenida

3. **Menciona el bot**:
   - Escribe `@NombreDeTuBot hola` en cualquier canal
   - El bot responderá

4. **Envía un mensaje directo**:
   - Abre un mensaje directo con el bot
   - Envía cualquier mensaje
   - El bot responderá

## Despliegue en Heroku

### Requisitos previos

- Cuenta de Heroku ([registrarse aquí](https://signup.heroku.com/))
- Heroku CLI instalado ([descargar aquí](https://devcenter.heroku.com/articles/heroku-cli))

### Pasos para desplegar

1. **Iniciar sesión en Heroku**:

```bash
heroku login
```

2. **Crear una aplicación de Heroku**:

```bash
heroku create nombre-de-tu-bot
```

3. **Configurar variables de entorno en Heroku**:

```bash
heroku config:set SLACK_BOT_TOKEN=xoxb-tu-token-de-bot
heroku config:set SLACK_APP_TOKEN=xapp-tu-token-de-app
heroku config:set SLACK_SIGNING_SECRET=tu-signing-secret
```

4. **Desplegar el bot**:

```bash
git push heroku main
```

5. **Verificar que el bot esté ejecutándose**:

```bash
heroku logs --tail
```

## Estructura del proyecto

```
welcome-bot/
│
├── bot.py                  # Archivo principal del bot
├── requirements.txt        # Dependencias de Python
├── .env.example           # Plantilla de variables de entorno
├── .env                   # Variables de entorno (no incluido en git)
├── .gitignore            # Archivos ignorados por git
├── Procfile              # Configuración para Heroku
└── README.md             # Este archivo
```

## Solución de problemas

### El bot no responde

- Verifica que Socket Mode esté habilitado en tu aplicación de Slack
- Asegúrate de que todos los tokens en `.env` sean correctos
- Verifica que el bot esté invitado al canal donde estás probando
- Revisa los logs en la consola para ver errores

### Error "SLACK_APP_TOKEN no está configurado"

- Asegúrate de haber creado un token de Socket Mode en la configuración de tu aplicación de Slack
- Verifica que el token esté correctamente copiado en tu archivo `.env`

### El bot no envía mensajes de bienvenida

- Verifica que hayas agregado el evento `member_joined_channel` en Event Subscriptions
- Asegúrate de que el bot tenga los permisos necesarios (scopes)
- El bot debe estar en el canal para detectar nuevos miembros

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Soporte

Si encuentras algún problema o tienes preguntas, por favor abre un issue en el repositorio de GitHub.

---

Desarrollado con ❤️ para la comunidad de Slack
