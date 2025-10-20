#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot de Bienvenida para Slack - Jarvis
Este bot da la bienvenida a nuevos miembros y responde a mensajes directos y menciones.
"""

import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Configurar logging para depuración y seguimiento de errores
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar la aplicación de Slack con el token del bot
try:
    app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
    logger.info("Aplicación de Slack inicializada correctamente")
except Exception as e:
    logger.error(f"Error al inicializar la aplicación de Slack: {e}")
    raise


# Evento: Cuando un nuevo miembro se une al equipo
@app.event("team_join")
def handle_team_join(event, client, logger):
    """
    Maneja el evento cuando un nuevo miembro se une al workspace.
    Envía un mensaje de bienvenida personalizado al nuevo usuario.
    """
    try:
        user_id = event["user"]["id"]
        user_name = event["user"]["real_name"] or event["user"]["name"]
        
        # Mensaje de bienvenida personalizado
        welcome_message = (
            f"¡Hola <@{user_id}>! 👋\n\n"
            f"Bienvenido/a al workspace. Soy *Jarvis*, tu asistente virtual.\n\n"
            f"Estoy aquí para ayudarte. Puedes:\n"
            f"• Mencionarme en cualquier canal con `@Jarvis`\n"
            f"• Enviarme un mensaje directo\n"
            f"• Preguntarme lo que necesites\n\n"
            f"¡Espero que disfrutes tu estadía aquí! 🚀"
        )
        
        # Enviar mensaje de bienvenida por DM
        client.chat_postMessage(
            channel=user_id,
            text=welcome_message
        )
        
        logger.info(f"Mensaje de bienvenida enviado a {user_name} ({user_id})")
        
    except Exception as e:
        logger.error(f"Error al enviar mensaje de bienvenida: {e}")


# Evento: Cuando un miembro se une a un canal
@app.event("member_joined_channel")
def handle_member_joined_channel(event, client, logger):
    """
    Maneja el evento cuando un miembro se une a un canal específico.
    Envía un mensaje de bienvenida en el canal.
    """
    try:
        user_id = event["user"]
        channel_id = event["channel"]
        
        # Mensaje de bienvenida en el canal
        welcome_message = (
            f"¡Bienvenido/a <@{user_id}> al canal! 🎉\n"
            f"Me alegra que estés aquí. Si necesitas ayuda, solo menciónme."
        )
        
        client.chat_postMessage(
            channel=channel_id,
            text=welcome_message
        )
        
        logger.info(f"Mensaje de bienvenida enviado en canal {channel_id} para usuario {user_id}")
        
    except Exception as e:
        logger.error(f"Error al enviar mensaje de bienvenida en canal: {e}")


# Evento: Cuando el bot es mencionado en un mensaje
@app.event("app_mention")
def handle_app_mention(event, client, logger):
    """
    Maneja el evento cuando el bot es mencionado en un canal.
    Responde al usuario que mencionó al bot.
    """
    try:
        channel_id = event["channel"]
        user_id = event["user"]
        text = event.get("text", "")
        
        # Respuesta cuando el bot es mencionado
        response_message = (
            f"¡Hola <@{user_id}>! Soy Jarvis. 👋\n"
            f"¿En qué puedo ayudarte hoy?"
        )
        
        client.chat_postMessage(
            channel=channel_id,
            text=response_message,
            thread_ts=event.get("ts")  # Responder en el mismo hilo si es aplicable
        )
        
        logger.info(f"Respondido a mención de usuario {user_id} en canal {channel_id}")
        
    except Exception as e:
        logger.error(f"Error al responder a mención: {e}")


# Evento: Mensajes directos al bot
@app.event("message")
def handle_message(event, client, logger):
    """
    Maneja los mensajes directos enviados al bot.
    Responde de manera personalizada según el contenido del mensaje.
    """
    try:
        # Ignorar mensajes del bot mismo y mensajes con subtipos (ediciones, etc.)
        if event.get("subtype") is not None or event.get("bot_id") is not None:
            return
        
        channel_id = event["channel"]
        user_id = event["user"]
        text = event.get("text", "").lower()
        
        # Diferentes respuestas según el contenido del mensaje
        if "hola" in text or "hello" in text or "hi" in text:
            response = (
                f"¡Hola <@{user_id}>! 👋\n"
                f"Soy Jarvis, ¿en qué puedo ayudarte?"
            )
        elif "ayuda" in text or "help" in text:
            response = (
                f"¡Claro! Estoy aquí para ayudarte.\n\n"
                f"Puedes:\n"
                f"• Preguntarme cualquier cosa\n"
                f"• Mencionarme en canales con `@Jarvis`\n"
                f"• Enviarme mensajes directos como este\n\n"
                f"¿Qué necesitas saber?"
            )
        elif "gracias" in text or "thanks" in text:
            response = "¡De nada! Estoy aquí cuando me necesites. 😊"
        else:
            response = (
                f"He recibido tu mensaje: \"{event.get('text')}\"\n\n"
                f"Actualmente soy un bot básico, pero estoy aquí para ayudarte. "
                f"Si necesitas asistencia específica, mencióname en un canal o escribe 'ayuda'."
            )
        
        client.chat_postMessage(
            channel=channel_id,
            text=response
        )
        
        logger.info(f"Respondido a mensaje directo de usuario {user_id}")
        
    except Exception as e:
        logger.error(f"Error al manejar mensaje directo: {e}")


# Manejo global de errores
@app.error
def custom_error_handler(error, body, logger):
    """
    Maneja errores globales de la aplicación.
    Registra el error para depuración.
    """
    logger.error(f"Error: {error}")
    logger.error(f"Request body: {body}")


# Punto de entrada principal
if __name__ == "__main__":
    try:
        # Verificar que las variables de entorno estén configuradas
        bot_token = os.environ.get("SLACK_BOT_TOKEN")
        app_token = os.environ.get("SLACK_APP_TOKEN")
        
        if not bot_token:
            raise ValueError("SLACK_BOT_TOKEN no está configurado en las variables de entorno")
        if not app_token:
            raise ValueError("SLACK_APP_TOKEN no está configurado en las variables de entorno")
        
        logger.info("Iniciando Jarvis Bot en modo Socket...")
        
        # Iniciar el bot en modo Socket
        handler = SocketModeHandler(app, app_token)
        handler.start()
        
    except ValueError as ve:
        logger.error(f"Error de configuración: {ve}")
        logger.error("Asegúrate de tener un archivo .env con SLACK_BOT_TOKEN y SLACK_APP_TOKEN configurados")
    except Exception as e:
        logger.error(f"Error crítico al iniciar el bot: {e}")
        raise
