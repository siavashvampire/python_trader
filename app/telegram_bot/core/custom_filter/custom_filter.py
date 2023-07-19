from telegram import Message
from telegram.ext.filters import MessageFilter

from app.telegram_bot.user.api import check_exist_user, check_admin_user, check_access_user


# def dynamic_data_filter(data):
#     async def func(flt, _, query):
#         return flt.data in query.data
#
#     return filters.create(func, data=data)
#
#
# async def user_exist_filter(_, client: Client, message: Message):
#     return check_exist_user(message.from_user)


class UserExistFilter(MessageFilter):
    def __init__(self, only_start: bool = True):
        super().__init__()
        self.only_start: bool = only_start

    def filter(self, message: Message) -> bool:
        return check_exist_user(message.from_user)


class UserAdminFlagFilter(MessageFilter):
    def __init__(self, only_start: bool = True):
        super().__init__()
        self.only_start: bool = only_start

    def filter(self, message: Message) -> bool:
        return check_admin_user(message.from_user)


class UserAccessFilter(MessageFilter):
    def __init__(self, only_start: bool = True):
        super().__init__()
        self.only_start: bool = only_start

    def filter(self, message: Message) -> bool:
        return check_access_user(message.from_user)


user_exist_filter = UserExistFilter()
user_admin_filter = UserAdminFlagFilter()
access_filter = UserAccessFilter()
