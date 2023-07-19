from telegram import Update
from telegram.ext import ContextTypes
from app.telegram_bot.logs.main import percent_currency_handler, percent_currency_show_handler, separate_otc_handler, \
    over_all_handler, percent_all_currency_handler, percent_location_handler, country_handler
from app.telegram_bot.user.model.query_handlers import access_query_handler
from core.config.Config import telegram_channel_id


async def callback_query_handler(update: Update, context: ContextTypes) -> None:
    chat_data = context.chat_data

    if 'app' in chat_data.keys() and not chat_data['app'] == '':
        if chat_data['app'] == 'user':
            if chat_data['state'] == 'insert_wait_for_accept':
                await access_query_handler(update, context)

        elif chat_data['app'] == 'main_app':
            query = update.callback_query
            data = str(query.data)

            if data == 'percent_currency':
                chat_data['app'] = 'percent_currency'
                await context.bot.deleteMessage(chat_id=update.effective_message.chat.id,
                                                message_id=update.effective_message.id)
                await percent_currency_handler(update, context)
                await query.answer()
            elif data == 'percent_all_currency':
                chat_data['app'] = 'percent_all_currency'
                await context.bot.deleteMessage(chat_id=update.effective_message.chat.id,
                                                message_id=update.effective_message.id)
                await percent_all_currency_handler(update, context)
                await query.answer()
            elif data == 'percent_location':
                chat_data['app'] = 'percent_location'
                await context.bot.deleteMessage(chat_id=update.effective_message.chat.id,
                                                message_id=update.effective_message.id)
                await percent_location_handler(update, context)
                await query.answer()
            elif data == 'accuracy_all_currency':
                chat_data['app'] = ''
                await context.bot.deleteMessage(chat_id=update.effective_message.chat.id,
                                                message_id=update.effective_message.id)
                # await percent_location_handler(update, context)
                await query.answer()

        elif chat_data['app'] == 'percent_currency':
            query = update.callback_query
            await context.bot.deleteMessage(chat_id=update.effective_message.chat.id,
                                            message_id=update.effective_message.id)

            chat_data['app'] = 'percent_currency_show'
            await percent_currency_show_handler(update, context)
            await query.answer()

        elif chat_data['app'] == 'percent_currency_show':
            query = update.callback_query
            data = str(query.data)
            await context.bot.deleteMessage(chat_id=update.effective_message.chat.id,
                                            message_id=update.effective_message.id)

            chat_data['app'] = ''
            if 'separate_otc' in data:
                await separate_otc_handler(update, context)
            elif 'over_all' in data:
                await over_all_handler(update, context)

        elif chat_data['app'] == 'percent_all_currency':
            query = update.callback_query
            data = str(query.data)
            await context.bot.deleteMessage(chat_id=update.effective_message.chat.id,
                                            message_id=update.effective_message.id)

            chat_data['app'] = ''
            if 'separate_otc' in data:
                await separate_otc_handler(update, context)
            elif 'over_all' in data:
                await over_all_handler(update, context)

            await query.answer()

        elif chat_data['app'] == 'percent_location':
            query = update.callback_query
            data = str(query.data)
            await context.bot.deleteMessage(chat_id=update.effective_message.chat.id,
                                            message_id=update.effective_message.id)

            chat_data['app'] = ''
            await country_handler(update, context)

            await query.answer()
