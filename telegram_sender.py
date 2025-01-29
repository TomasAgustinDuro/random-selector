from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from scrapper_disk import Browser
from dotenv import load_dotenv
import os

load_dotenv()

# Tomar el token de la variable de entorno
TOKEN = os.getenv('TELEGRAM_TOKEN')

playlist_url = ""

# Maneja el comando /start para iniciar el bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global playlist_url
   
    # Pregunta por la URL de la playlist e informa los comandos
    await update.message.reply_text(
        "¡Hola! Soy tu bot de Telegram. Envíame el enlace de una playlist y te recomendaré un disco aleatorio. 🎶\n"
        "Usa /cambiar para cambiar la playlist seleccionada\n"
    )

# Maneja los mensajes enviados por el usuario
async def send_daily_recommendation(application: Application, chat_id: int):
    global playlist_url
    if not playlist_url:  # Asegúrate de que la URL esté configurada antes de enviar la recomendación
        await application.bot.send_message(chat_id=chat_id, text="No se ha configurado una URL de playlist. Por favor, envía un enlace para analizarla.")
        return
    
    try:
        # Crear una instancia del navegador y seleccionar un disco aleatorio
        browser = Browser()
        chosen_disk = browser.random_disk(playlist_url)  # Pasar la URL de la playlist
        response = f"Te recomiendo escuchar el disco: {chosen_disk[0]} en este enlace: {chosen_disk[1]}"
    
        # Cerrar el navegador
        browser.close_browser()

        # Enviar la recomendación al chat
        await application.bot.send_message(chat_id=chat_id, text=response)
    except Exception as e:
        print(f"Error en send_daily_recommendation: {e}")  # Depuración de errores
        await application.bot.send_message(chat_id=chat_id, text="Hubo un error al obtener la recomendación.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global playlist_url
    playlist_url = update.message.text
        # Crear una instancia del navegador y seleccionar un disco aleatorio
    if playlist_url:  # Solo si ya se configuró la URL de la playlist
            print("Iniciando recomendación diaria...")  # Depuración
            # Ejecuta la recomendación de inmediato y luego comienza el intervalo de 1 minuto
            await send_daily_recommendation(context.application, update.message.chat_id)
    else:
            await update.message.reply_text("Por favor, ingresa una URL de playlist primero.")


def main():
    # Crear la aplicación
    application = Application.builder().token(TOKEN).build()

    # Agregar manejadores
    application.add_handler(CommandHandler("Recomendar", start))  # Maneja el comando /start
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Captura cualquier mensaje de texto

    # Iniciar el bot
    print("Bot iniciado... 🚀")
    application.run_polling()

if __name__ == "__main__":
    main()
