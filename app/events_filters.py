from telethon import types, events
from app.state import State
from app import logger


def filter_start(event: events.NewMessage):
    return event.message.message.startswith('/start')


def filter_admin(event: events.NewMessage):
    return event.message.peer_id.user_id == State.admin.id


def filter_admin_start(event):
    if filter_admin(event):
        logger.debug("Admin filtered")
        return filter_start(event)


def filter_user_start(event):
    if not filter_admin(event):
        logger.debug("Admin filtered")
        return filter_start(event)
