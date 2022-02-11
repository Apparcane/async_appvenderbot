from aiogram import executor
from create_bot import dp

from handlers import admin, client, commands, callback_query, other

# admin.register_handlers_admin(dp)
commands.register_handlers_commands(dp)
client.register_handlers_clients(dp)
callback_query.register_handlers_commands(dp)
# other.register_handlers_other(dp)

if __name__ == "__main__":
    executor.start_polling(dispatcher = dp)