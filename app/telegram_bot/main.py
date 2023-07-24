from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler, CallbackContext, PicklePersistence, \
    PersistenceInput
from app.telegram_bot.start.main import main_app
from app.telegram_bot.start.main import start_new_user, start_exist_user, say_start_user
from app.telegram_bot.handler import callback_query_handler
from app.telegram_bot.user.main import without_access_user
from core.config.Config import token_telegram, telegram_channel_id
from app.telegram_bot.core.custom_filter.custom_filter import user_exist_filter, access_filter
from app.telegram_bot.core.error_handler.error import error_handler

from queue import Queue


class TelegramApp:
    send_queue: Queue[list[int, str]]

    def __init__(self):
        self.telegram_application = Application.builder().token(token_telegram).build()

        job_queue = self.telegram_application.job_queue
        job_queue.run_repeating(self.send_message_func, interval=10, first=10)

        self.telegram_application.add_handler(
            MessageHandler(filters.COMMAND & filters.Regex("start") & ~user_exist_filter, start_new_user))
        self.telegram_application.add_handler(
            MessageHandler(filters.COMMAND & filters.Regex("start") & user_exist_filter, start_exist_user))
        self.telegram_application.add_handler(MessageHandler(~user_exist_filter, say_start_user))

        self.telegram_application.add_handler(MessageHandler(~access_filter & user_exist_filter, without_access_user))

        self.telegram_application.add_handler(MessageHandler(access_filter, main_app))

        self.telegram_application.add_handler(CallbackQueryHandler(callback_query_handler))

        self.telegram_application.add_error_handler(error_handler)

        self.send_queue = Queue()
        # self.run_all()
        # self.thread = Thread(target=self.getting_data_thread)
        # self.start_thread()

    def run_all(self) -> None:
        # self.telegram_application.
        self.telegram_application.run_polling()
        # async with self.telegram_application:
        #     # await self.telegram_application.initialize()  # inits bot, update, persistence
        #     await self.telegram_application.start()
            # await self.telegram_application.updater.start_polling()


    async def send_message_func(self, context: CallbackContext) -> None:
        try:
            user_id, text = self.send_queue.get(timeout=1)
            await context.bot.send_message(chat_id=telegram_channel_id, text=text)

            self.send_queue.task_done()
        except:
            pass


telegram_app = TelegramApp()
# telegram_app.run_all()
