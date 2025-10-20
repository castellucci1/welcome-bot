# Welcome Bot - Jarvis 🤖

Bot de bienvenida inteligente para Slack que da la bienvenida a nuevos miembros y responde a mensajes.

## 📋 Descripción

Jarvis es un bot de Slack desarrollado en Python que:
- ✅ Da la bienvenida automáticamente a nuevos miembros del workspace
- ✅ Saluda a usuarios que se unen a canales específicos
- ✅ Responde a menciones del bot en canales
- ✅ Gestiona mensajes directos con respuestas inteligentes
- ✅ Incluye manejo de errores y logging completo

## 🚀 Características

- **Bienvenida automática**: Cuando un usuario se une al workspace, recibe un mensaje de bienvenida personalizado
- **Bienvenida en canales**: Saluda a usuarios que se unen a canales
- **Respuesta a menciones**: Responde cuando es mencionado con `@Jarvis`
- **Mensajes directos**: Procesa y responde mensajes directos
- **Manejo de errores**: Sistema robusto de logging y manejo de excepciones
- **Socket Mode**: Funciona sin necesidad de exponer un endpoint público

## 📦 Requisitos

- Python 3.8 o superior
- Una aplicación de Slack configurada
- Tokens de acceso de Slack

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/castellucci1/welcome-bot.git
cd welcome-bot
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto basándote en `.env.example`:

```bash
cp .env.example .env
```

Edita el archivo `.env` y completa con tus tokens:

```
SLACK_BOT_TOKEN=xoxb-tu-token-de-bot
SLACK_SIGNING_SECRET=tu-signing-secret
SLACK_APP_TOKEN=xapp-tu-app-token
```

## 🔑 Configuración de la App de Slack

### 1. Crear la aplicación en Slack

1. Ve a [https://api.slack.com/apps](https://api.slack.com/apps)
2. Haz clic en "Create New App" → "From scratch"
3. Dale un nombre (ej: "Jarvis Bot") y selecciona tu workspace

### 2. Configurar Socket Mode

1. Ve a "Socket Mode" en el menú lateral
2. Activa Socket Mode
3. Copia el **App-Level Token** (comienza con `xapp-`)
4. Guárdalo como `SLACK_APP_TOKEN` en tu archivo `.env`

### 3. Configurar Bot Token Scopes

Ve a "OAuth & Permissions" y agrega los siguientes scopes:

**Bot Token Scopes:**
- `app_mentions:read` - Leer menciones del bot
- `channels:history` - Ver mensajes en canales públicos
- `channels:read` - Ver información de canales públicos
- `chat:write` - Enviar mensajes
- `groups:history` - Ver mensajes en canales privados
- `groups:read` - Ver información de canales privados
- `im:history` - Ver mensajes directos
- `im:read` - Ver información de mensajes directos
- `im:write` - Enviar mensajes directos
- `mpim:history` - Ver mensajes en mensajes grupales
- `users:read` - Ver información de usuarios

### 4. Habilitar eventos

1. Ve a "Event Subscriptions"
2. Activa "Enable Events"
3. En "Subscribe to bot events", agrega:
   - `team_join` - Cuando un usuario se une al workspace
   - `member_joined_channel` - Cuando un usuario se une a un canal
   - `app_mention` - Cuando mencionan al bot
   - `message.im` - Mensajes directos al bot

### 5. Instalar la app en tu workspace

1. Ve a "Install App"
2. Haz clic en "Install to Workspace"
3. Autoriza la aplicación
4. Copia el **Bot User OAuth Token** (comienza con `xoxb-`)
5. Guárdalo como `SLACK_BOT_TOKEN` en tu archivo `.env`

### 6. Obtener el Signing Secret

1. Ve a "Basic Information"
2. En "App Credentials", copia el **Signing Secret**
3. Guárdalo como `SLACK_SIGNING_SECRET` en tu archivo `.env`

## ▶️ Ejecutar el Bot

```bash
python bot.py
```

Si todo está configurado correctamente, verás:

```
INFO - Aplicación de Slack inicializada correctamente
INFO - Iniciando Jarvis Bot en modo Socket...
⚡️ Bolt app is running!
```

## 🧪 Probar el Bot

### Prueba 1: Mensaje de Bienvenida a Nuevos Miembros
- Invita a un nuevo usuario a tu workspace
- El bot enviará automáticamente un mensaje de bienvenida por DM

### Prueba 2: Mención del Bot
- En cualquier canal donde esté el bot, escribe: `@Jarvis hola`
- El bot responderá en el canal

### Prueba 3: Mensaje Directo
- Envía un mensaje directo al bot
- Prueba diferentes mensajes como "hola", "ayuda", "gracias"

## 🐛 Solución de Problemas Comunes

### Error: "dispatch_failed"
**Causa**: Problemas con tokens, permisos o configuración de eventos.

**Solución**:
1. Verifica que todos los tokens estén correctamente configurados en `.env`
2. Asegúrate de que Socket Mode esté activado
3. Confirma que todos los permisos (scopes) estén agregados
4. Reinstala la app en el workspace si es necesario

### Error: "Token no está configurado"
**Causa**: Variables de entorno no cargadas.

**Solución**:
1. Verifica que el archivo `.env` existe en la raíz del proyecto
2. Asegúrate de que las variables estén correctamente escritas
3. Reinicia el bot después de modificar el archivo `.env`

### El bot no responde
**Causa**: Eventos no configurados o bot no invitado al canal.

**Solución**:
1. Verifica que los eventos estén suscritos en la configuración de Slack
2. Invita al bot al canal: `/invite @Jarvis`
3. Revisa los logs del bot para ver errores

## 📁 Estructura del Proyecto

```
welcome-bot/
├── bot.py              # Código principal del bot
├── requirements.txt    # Dependencias de Python
├── .env.example       # Ejemplo de variables de entorno
├── .gitignore         # Archivos a ignorar en git
├── README.md          # Documentación
└── Procfile           # Configuración para despliegue (opcional)
```

## 🚢 Despliegue (Opcional)

### Heroku

1. Crea un archivo `Procfile`:
```
worker: python bot.py
```

2. Despliega en Heroku:
```bash
heroku create nombre-de-tu-bot
heroku config:set SLACK_BOT_TOKEN=tu-token
heroku config:set SLACK_APP_TOKEN=tu-app-token
heroku config:set SLACK_SIGNING_SECRET=tu-secret
git push heroku main
heroku ps:scale worker=1
```

## 📝 Logs

El bot genera logs detallados que incluyen:
- Inicialización de la aplicación
- Mensajes de bienvenida enviados
- Menciones y mensajes directos procesados
- Errores y excepciones

Los logs se muestran en la consola con formato:
```
2025-10-20 14:19:02 - __main__ - INFO - Mensaje de bienvenida enviado a Usuario (U12345)
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

- **castellucci1** - [GitHub](https://github.com/castellucci1)

## 🙏 Agradecimientos

- [Slack Bolt for Python](https://slack.dev/bolt-python/) - Framework utilizado
- Comunidad de Slack por la documentación y ejemplos

---

¿Preguntas? Abre un [issue](https://github.com/castellucci1/welcome-bot/issues) en el repositorio.

