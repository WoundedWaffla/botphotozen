import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

# Токены
TELEGRAM_TOKEN = '7796872269:AAHA9FafaSO5Q-8NMnjrccMQAEmzBjTkiIE'
REPLICATE_API_TOKEN = 'ВАШ_REPLICATE_ТОКЕН'

bot = telegram.Bot(token=TELEGRAM_TOKEN)


# Приветственное сообщение
def start(update, context):
    update.message.reply_text("Привет! Напиши мне описание картинки, и я сгенерирую её для тебя.")


# Обработка текстовых сообщений
def handle_message(update, context):
    user_prompt = update.message.text
    update.message.reply_text("🎨 Генерирую изображение... Это может занять несколько секунд.")

    # Генерация изображения
    image_url = generate_image(user_prompt)

    if image_url and len(image_url) > 0:
        bot.send_photo(chat_id=update.message.chat_id, photo=image_url[0])
    else:
        update.message.reply_text("❌ Не удалось сгенерировать изображение. Попробуй другой запрос.")


# Функция генерации изображения через Replicate
def generate_image(prompt):
    url = "https://api.replicate.com/v1/predictions "
    headers = {
        "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "version": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        "input": {
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
            "num_outputs": 1
        }
    }

    response = requests.post(url, headers=headers, json=data)
    output = response.json()

    return output.get("output")


# Основной запуск
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()