import asyncio

from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import hd_actual_balance, hd_common, hd_transaction
from utils.log_init import log_init
from utils.set_commands import set_commands


async def on_startup(bot: Bot):
    await set_commands(bot)


async def on_shutdown(bot: Bot):
    pass


async def main():
    # Start logging
    log_init()

    # Initialize bot and retrieve TELEGRAM_TOKEN
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()

    # On startup and shutdown
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Include routers
    dp.include_routers(hd_common.router, hd_transaction.router, hd_actual_balance.router)

    # Start polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        #await request.close()  # Delete if no database is in use
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())