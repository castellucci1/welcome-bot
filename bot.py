import os
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Inicializar la app de Slack con los tokens
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Función auxiliar para obtener el nombre del usuario
def get_user_name(client, user_id):
    try:
        user_info = client.users_info(user=user_id)
        return user_info["user"]["real_name"] or user_info["user"]["name"]
    except:
        return "there"

# Respuestas del bot
def get_help_response():
    return """Hey there 👋
I'm Jarvis, here to give you a hand.
Here's what I can help you with:

• *help* or *hello* – Just to say hi.
• *sla* – Check the current SLAs and response times.
• *plugin* – Learn how to use the Strike plugin inside your workspace.
• *platform* – Step-by-step guide to work on the Strike platform.
• 💰 *bonuses* – Understand how performance bonuses are calculated.
• 💵 *payments* – Learn how payments work and when they're processed."""

def get_hello_response(user_name):
    return f"""Hey {user_name} 👋
I'm Jarvis — your assistant here at Strike.
Just type clearly what you need help with, and I'll do my best to answer or point you in the right direction."""

def get_fallback_response():
    return """Hmm, I don't have that info yet 🤔
If I don't have the answer, here's who can help you:

📞 **If you need support, please contact the right person directly:**
• Platform or login issues — NOT bugs → support@strike.sh
• Finance, blockers, or big-picture concerns — NOT performance inquiries → finance@strike.sh
• Already working with someone from the Hacking Team? → keep going with them
• Everything else → @Ailin Castellucci"""

def get_sla_response(user_name):
    msg1 = f"""Hey {user_name} 👋
Here's a quick reminder about SLAs for your pentests:

❗ **Assessment Updates** – Submit **at least one per week**, aligned with Pentest goals.
⚠️ **Missed SLAs** – Can affect your continuity in projects.
🔹 **Triaging & Vulnerabilities** – Be ready to collaborate with Triage or Hacking Team for tuning and escalations.
🔹 **Remember** – You have **24h to accept or decline pentests**."""
    
    msg2 = """**Reports** – Must be **clear & reproducible**; include all steps, tools, credentials, HTTP requests/responses, and attachments if needed.
**Rewards & Incentives** – High-quality work makes you eligible for **quarterly bonuses, special projects, Challenges invitations, swag, and more**.
A well-crafted report ensures your skills are recognized and your impact is seen. 🚀 💪"""
    
    return [msg1, msg2]

# Función para procesar comandos
def process_command(text, user_name):
    # Limpiar el texto y convertir a minúsculas
    text = text.lower().strip()
    # Remover menciones del bot
    text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()
    # Remover slash si existe
    text = text.lstrip('/')
    
    # Detectar comando
    if text in ['help', 'ayuda']:
        return get_help_response()
    elif text in ['hello', 'hi', 'hola', 'jarvis']:
        return get_hello_response(user_name)
    elif text in ['sla', 'slas']:
        return get_sla_response(user_name)
    elif text in ['plugin']:
        return "📦 *Strike Plugin Guide*\n\n_Coming soon! This section will explain how to use the Strike plugin inside your workspace._"
    elif text in ['platform']:
        return "🖥️ *Strike Platform Guide*\n\n_Coming soon! This will be a step-by-step guide to work on the Strike platform._"
    elif text in ['bonuses', 'bonus']:
        return "💰 *Performance Bonuses*\n\n_Coming soon! Learn how performance bonuses are calculated._"
    elif text in ['payments', 'payment', 'pagos']:
        return "💵 *Payments Information*\n\n_Coming soon! Learn how payments work and when they're processed._"
    else:
        return None

# Evento: Dar bienvenida cuando alguien se une al workspace
@app.event("team_join")
def handle_team_join(event, client, say):
    user_id = event["user"]["id"]
    user_name = get_user_name(client, user_id)
    say(
        text=f"¡Bienvenido al equipo, {user_name}! 👋 Soy Jarvis, tu asistente virtual. Escribe *help* para ver cómo puedo ayudarte.",
        channel=user_id
    )
    print(f"✅ Mensaje de bienvenida enviado a {user_name} ({user_id})")

# Evento: Responder cuando mencionan al bot
@app.event("app_mention")
def handle_mention(event, client, say):
    user_id = event["user"]
    text = event.get("text", "")
    user_name = get_user_name(client, user_id)
    
    response = process_command(text, user_name)
    
    if response:
        if isinstance(response, list):
            # Para SLA que tiene dos mensajes
            for msg in response:
                say(msg)
        else:
            say(response)
        print(f"✅ Respondido a mención de {user_name}: {text}")
    else:
        say(get_fallback_response())
        print(f"⚠️ Comando no reconocido de {user_name}: {text}")

# Evento: Responder a mensajes directos
@app.event("message")
def handle_message(event, client, say):
    # Ignorar mensajes del bot mismo
    if event.get("bot_id"):
        return
    
    # Solo responder a mensajes directos (DMs)
    if event.get("channel_type") == "im":
        user_id = event["user"]
        text = event.get("text", "")
        user_name = get_user_name(client, user_id)
        
        response = process_command(text, user_name)
        
        if response:
            if isinstance(response, list):
                # Para SLA que tiene dos mensajes
                for msg in response:
                    say(msg)
            else:
                say(response)
            print(f"✅ Respondido a DM de {user_name}: {text}")
        else:
            say(get_fallback_response())
            print(f"⚠️ Comando no reconocido en DM de {user_name}: {text}")

# Iniciar la app en Socket Mode
if __name__ == "__main__":
    try:
        handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
        print("⚡️ Jarvis está conectado y funcionando!")
        print("📋 Comandos disponibles: help, hello, sla, plugin, platform, bonuses, payments")
        handler.start()
    except Exception as e:
        print(f"❌ Error al iniciar el bot: {e}")
        print("Verifica que tus tokens en el archivo .env sean correctos.")