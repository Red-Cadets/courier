import functools
from app.utils.admin import is_admin
from app import bot


def admins_only(f):
    """
    Decorator that requires the user to be authenticated and an admin
    :param f:
    :return:
    """
    @functools.wraps(f)
    def admins_only_wrapper(*args, **kwargs):
        message = args[0]
        ID = str(message.from_user.id)
        if is_admin(ID):
            return f(*args, **kwargs)
        else:
            error_message = """
            У Вас нет прав администратора ⛔️
            """
            bot.send_message(message.chat.id, error_message)
    return admins_only_wrapper
