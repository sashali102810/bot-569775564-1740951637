Для создания Telegram-бота, который показывает случайные факты о кошках по команде `/cat`, мы будем использовать библиотеку `python-telegram-bot` версии 20.x. Также добавим обработку ошибок и логирование.

### Шаги:
1. Установите необходимые библиотеки:
   ```bash
   pip install python-telegram-bot requests
   ```

2. Создайте файл `cat_fact_bot.py` и добавьте следующий код:

```python
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Функция для получения случайного факта о кошках
async def get_cat_fact():
    url = "https://catfact.ninja/fact"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("fact", "Не удалось получить факт о кошках.")
    except requests.RequestException as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        return "Произошла ошибка при получении факта о кошках."

# Обработчик команды /cat
async def cat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Пользователь {update.effective_user.username} запросил факт о кошках.")
    fact = await get_cat_fact()
    await update.message.reply_text(fact)

# Обработчик ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Ошибка: {context.error}")
    await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")

# Основная функция для запуска бота
def main():
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("cat", cat_command))

    # Регистрация обработчика ошибок
    application.add_error_handler(error_handler)

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
```

### Описание кода:
1. **Логирование**: Используем стандартный модуль `logging` для логирования событий и ошибок.
2. **Получение факта о кошках**: Используем API `https://catfact.ninja/fact` для получения случайного факта о кошках.
3. **Обработчик команды `/cat`**: Когда пользователь отправляет команду `/cat`, бот запрашивает факт о кошках и отправляет его пользователю.
4. **Обработка ошибок**: Если происходит ошибка при запросе к API или в работе бота, она логируется, и пользователю отправляется сообщение об ошибке.
5. **Запуск бота**: Бот запускается с помощью метода `run_polling()`.

### Как запустить бота:
1. Замените `'YOUR_BOT_TOKEN'` на токен вашего бота, который вы получили от BotFather.
2. Запустите скрипт:
   ```bash
   python cat_fact_bot.py
   ```

Теперь ваш бот будет отвечать на команду `/cat` случайным фактом о кошках. Если произойдет ошибка, она будет залогирована, и пользователь получит сообщение об ошибке.