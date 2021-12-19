from telethon import TelegramClient, events
import asyncio
import os
from app import convos, logger
from app.state import State, Vars
import config
from app import events_filters as filters
from app import logger


if not os.path.exists('sessionFiles'):
    os.mkdir('sessionFiles')

proxy = {
    'proxy_type': 2,  # 2 means socks5
    'addr': '45.94.47.18',
    'port': 8062,
    'username': 'unergtzc-dest',
    'password': 'vc3h2h86oht1'
}

bot = TelegramClient(f'{Vars.sessions_dir}/bot',
                     config.TELEGRAM_API_ID, config.TELEGRAM_API_HASH, proxy=proxy)


async def add_event_handlers():
    logger.debug("Setting up events handlers")
    bot.add_event_handler(convos.admin_start,
                          events.NewMessage(func=filters.filter_admin_start))
    bot.add_event_handler(convos.handle_start, events.NewMessage(
        incoming=True, func=filters.filter_user_start))


async def on_ready():
    wait_time = 0.5
    if not bot.is_connected() or not await bot.is_user_authorized():
        await asyncio.sleep(wait_time)
    await add_event_handlers()
    await State.setup(bot)
    logger.info('Bot is ready!')

try:
    bot.start(bot_token=config.TELEGRAM_BOT_TOKEN)
    bot.loop.create_task(on_ready())
    bot.run_until_disconnected()
except KeyboardInterrupt:
    logger.info('Quiting bot ...')
    exit()
