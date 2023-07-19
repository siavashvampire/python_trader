from app.telegram_bot.main import telegram_app


def add_message(text: str):
    telegram_app.send_queue.put([0, text])
