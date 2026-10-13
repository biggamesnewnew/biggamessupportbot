import telebot
from telebot import types

# Инициализация бота с вашим токеном
TOKEN = "8879235375:AAFr4vW8CE938MJjpjl0GRhvPQHm1rFGOk8"
bot = telebot.TeleBot(TOKEN)

# ID владельца (сюда будут приходить сообщения от пользователей)
# Замените 000000000 на ваш реальный Telegram ID
OWNER_ID = 000000000 

# Словарь для отслеживания состояния пользователей (кто сейчас пишет вопрос владельцу)
waiting_for_question = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_ask = types.KeyboardButton("1. Спросить владельца")
    btn_back = types.KeyboardButton("Назад")
    markup.add(btn_ask, btn_back)
    
    welcome_text = (
        "Вас приветствует тех поддержка BigGames, выберите тему вашего вопроса:\n\n"
        "*(Примечание: если бот вдруг перестал работать, просто напишите свой вопрос сюда — "
        "ответ от владельца все равно будет!)*"
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text

    if text == "1. Спросить владельца":
        waiting_for_question[chat_id] = True
        
        # Убираем или оставляем клавиатуру по желанию, здесь просто просим ввести текст
        bot.send_message(
            chat_id, 
            "✏️ Напишите интересующий вас вопрос, и владелец обязательно ответит вам:"
        )

    elif text == "Назад":
        waiting_for_question.pop(chat_id, None)
        send_welcome(message)

    else:
        # Проверяем, находится ли пользователь в режиме отправки вопроса владельцу,
        # либо если бот «перестал работать» / пользователь пишет текст напрямую
        if waiting_for_question.get(chat_id, False) or True: # True срабатывает на любой текст (удобно для приема вопросов в любое время)
            bot.send_message(
                chat_id, 
                "✅ Ваш вопрос отправлен владельцу! Ожидайте ответа."
            )
            
            # Если указан ID владельца, пересылаем ему сообщение
            if OWNER_ID != 000000000:
                user_info = f"📩 Новый вопрос от @{message.from_user.username or 'не указан'} (ID: {chat_id}):\n\n{text}"
                bot.send_message(OWNER_ID, user_info)
            
            # Сбрасываем статус ожидания
            waiting_for_question[chat_id] = False


if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()