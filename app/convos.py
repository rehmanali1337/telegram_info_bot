from telethon import events, TelegramClient, errors
from telethon.tl.custom import Button
from app.state import State
import os
from app import logger
from pprint import pprint
import json
import asyncio


def _text_button(text):
    return Button.text(text=text)


async def handle_start(event: events.NewMessage):
    logger.debug(f"New /start event")
    user = await State.db.get_user_by_id(event.message.peer_id.user_id)
    if user is None:
        logger.debug(f"User not in the db. Adding now")
        user = await State.bot.get_entity(event.message.peer_id)
        await State.db.add_user(user)
    return await user_conversation(event)


def _text_from_file(path):
    with open(path) as f:
        return f.read()


def _read_dir_tree(path: str):
    for data in os.walk(path):
        logger.debug(f"Read data from {path}")
    print(data)
    return _text_from_file(f"{path}/message.txt"), data[2]


def _read_path(path):
    dirs = [d for d in os.listdir(path) if os.path.isdir(f"{path}/{d}")]
    files = [d for d in os.listdir(path) if os.path.isfile(f"{path}/{d}")]
    return files, dirs


def _read_tree(keys=[]):
    tree = json.load(open("tree.json"))
    for key in keys:
        tree = tree.get("buttons").get(key)
    return tree


def arrange_btns(buttons_list: list):
    btns = []
    tmp = list()
    for index, btn in enumerate(buttons_list):
        tmp.append(btn)
        if len(tmp) == 2 or len(buttons_list) == index + 1:
            btns.append(tmp.copy())
            tmp = list()

    return btns if len(btns) > 0 else None


async def _new_text_message(conv: TelegramClient.conversation, filter_func: callable):
    return (await conv.wait_event(events.NewMessage(func=filter_func))).text
    # return r.text


async def user_conversation(event: events.NewMessage):
    logger.debug(f"Starting the conversation for user {event.message.peer_id}")
    root_path = "./Tree"
    path = root_path
    text = None
    async with State.bot.conversation(event.message.peer_id, timeout=10000000000000000) as conv:
        while True:

            files, folders = _read_path(path)
            if path != root_path:
                folders.append("Back")
            text = _text_from_file(f"{path}/{files[0]}")

            buttons = arrange_btns([_text_button(text)
                                    for text in folders])
            await conv.send_message(text, buttons=buttons)
            selected_btn = await _new_text_message(conv, lambda x: x.message.message in folders)
            logger.debug(f"Selected button : {selected_btn}")

            if selected_btn == "Back":
                to_remove = path.split("/").pop(-1)
                path = path.replace(to_remove, '')
                continue

            files, folders = _read_path(f"{path}/{selected_btn}")
            text = _text_from_file(f"{path}/{selected_btn}/message.txt")
            await conv.send_message(text)

            # print(path)
            if len(folders) > 0:
                # print(path)
                path = f"{path}/{selected_btn}"


async def admin_start(event: events.NewMessage):
    return await send_announcement(event)


async def _announce_to_users(message: str):
    users = await State.db.get_all_users()
    wait_time = 300
    for user in users:
        try:
            await State.bot.send_message(user[0], message)
            await asyncio.sleep(3)
        except errors.FloodWaitError as e:
            logger.info(
                f"Need to wait for {e.seconds} seconds because of flood wait")
            await asyncio.sleep(e.seconds + 3)
        except errors.PeerFloodError:
            logger.info(f"Need to wait for {wait_time}")
            await asyncio.sleep(wait_time)
        except Exception as e:
            logger.debug("Unhandled exception on announcements", exc_info=True)
            await asyncio.sleep(wait_time)


async def send_announcement(event: events.NewMessage):
    logger.debug("Sending announcement")
    async with State.bot.conversation(event.message.peer_id) as conv:
        buttons_texts = ["Send Announcement"]
        buttons = arrange_btns([_text_button(text)
                                for text in buttons_texts])
        await conv.send_message("Admin Menu", buttons=buttons)
        selected_btn = await _new_text_message(conv, lambda x: x.message.message in buttons_texts)
        if selected_btn == "Send Announcement":
            await conv.send_message("Enter the message you want to send?")
            text = await _new_text_message(conv, filter_func=None)
            logger.debug(f"Announcing the text : {text}")
            asyncio.create_task(_announce_to_users(text))
            await conv.send_message("Bot is sending the announcements")
