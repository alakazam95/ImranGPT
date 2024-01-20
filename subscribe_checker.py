from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import Bot


class BanMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def on_pre_process_message(self, message: types.Message, data: dict):
        # ID или username канала
        channel_id = '@vedachjo'

        user_channel_status = await self.bot.get_chat_member(channel_id, message.from_user.id)
        if user_channel_status.status == 'left':
            # Пользователь не подписан на канал
            await self.send_subscription_request(message)
            raise CancelHandler()

    async def send_subscription_request(self, message: types.Message):
        text = '<b>👋 Добро пожаловать, {}!\n\n' \
               'Для использования нашего бота Вы должны быть подписанным на наш канал.</b>'.format(
            message.from_user.full_name)

        reg_buttons = types.InlineKeyboardMarkup()
        reg_buttons.add(types.InlineKeyboardButton(text='✅ Подписаться на канал', url='https://t.me/vedachjo'))

        await message.answer(text, parse_mode='HTML', reply_markup=reg_buttons)
