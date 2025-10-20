#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bot de bienvenida para Slack
Este bot da la bienvenida a nuevos miembros cuando se unen a un canal,
responde a mensajes directos y menciones.
"""

import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Inicializar la aplicación de Slack con los tokens del entorno
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


# Evento: Cuando un miembro se une a un canal
@app.event("member_joined_channel")
def handle_member_joined_channel(event, say, client):
    """
    Maneja el evento cuando un nuevo miembro se une a un canal.
    Envía un mensaje de bienvenida personalizado al canal.
    """
    user_id = event["user"]
    channel_id = event["channel"]
    
    # Obtener información del usuario
    try:
        user_info = client.users_info(user=user_id)
        user_name = user_info["user"]["real_name"] or user_info["user"]["name"]
    except Exception as e:
        print(f"Error al obtener información del usuario: {e}")
        user_name = f"<@{user_id}>"
    
    # Enviar mensaje de bienvenida al canal
    welcome_message = f"¡Hola {user_name}! 👋 Bienvenido/a al canal. ¡Nos alegra tenerte aquí!"
    
    try:
        say(text=welcome_message, channel=channel_id)
    except Exception as e:
        print(f"Error al enviar mensaje de bienvenida: {e}")


# Evento: Mensajes en los que el bot es mencionado
@app.event("app_mention")
def handle_mention(event, say):
    """
    Maneja el evento cuando el bot es mencionado en un mensaje.
    Responde al usuario que mencionó al bot.
    """
    user_id = event["user"]
    text = event.get("text", "")
    
    # Responder a la mención
    response = f"¡Hola <@{user_id}>! 👋 Soy el bot de bienvenida. ¿En qué puedo ayudarte?"
    
    try:
        say(response)
    except Exception as e:
        print(f"Error al responder a la mención: {e}")


# Evento: Mensajes directos al bot
@app.event("message")
def handle_message_events(event, say):
    """
    Maneja los mensajes directos enviados al bot.
    Responde con un mensaje amigable.
    """
    # Verificar que no sea un mensaje del propio bot para evitar bucles
    if event.get("bot_id"):
        return
    
    # Verificar que sea un mensaje directo (canal tipo 'im')
    channel_type = event.get("channel_type")
    
    if channel_type == "im":
        user_id = event["user"]
        text = event.get("text", "")
        
        # Responder al mensaje directo
        response = f"¡Hola <@{user_id}>! 👋 Gracias por tu mensaje. Soy el bot de bienvenida y estoy aquí para dar la bienvenida a nuevos miembros."
        
        try:
            say(response)
        except Exception as e:
            print(f"Error al responder al mensaje directo: {e}")


# Comando: Comando de prueba (opcional)
@app.command("/hola")
def handle_hola_command(ack, respond, command):
    """
    Maneja el comando /hola (si está configurado en Slack).
    Responde con un mensaje de saludo.
    """
    # Reconocer el comando inmediatamente
    ack()
    
    user_id = command["user_id"]
    response = f"¡Hola <@{user_id}>! 👋 ¿Cómo estás? Soy el bot de bienvenida."
    
    try:
        respond(response)
    except Exception as e:
        print(f"Error al responder al comando: {e}")


# Iniciar la aplicación en modo Socket
if __name__ == "__main__":
    # Obtener el token de la aplicación para Socket Mode
    app_token = os.environ.get("SLACK_APP_TOKEN")
    
    if not app_token:
        print("Error: SLACK_APP_TOKEN no está configurado en las variables de entorno.")
        exit(1)
    
    if not os.environ.get("SLACK_BOT_TOKEN"):
        print("Error: SLACK_BOT_TOKEN no está configurado en las variables de entorno.")
        exit(1)
    
    if not os.environ.get("SLACK_SIGNING_SECRET"):
        print("Error: SLACK_SIGNING_SECRET no está configurado en las variables de entorno.")
        exit(1)
    
    print("⚡️ Bot de bienvenida iniciado en modo Socket")
    
    # Iniciar el manejador de Socket Mode
    handler = SocketModeHandler(app, app_token)
    handler.start()
