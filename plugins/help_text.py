#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K & @No_OnE_Kn0wS_Me
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import time
from typing import Union

from pyrogram import filters, Client as Mai_bOTs
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from database.database import Database


class Config:
    UPDATE_CHANNEL = "my_update_channel"
    BANNED_USERS = [123456789]


class Translation:
    HELP_USER = "This is the help message"
    START_TEXT = "Hello, {first_name}! Welcome to my bot."
    RENAME_HELP = "This is the rename help message"
    C2V_HELP = "This is the file to video help message"
    CCAPTION_HELP = "This is the custom caption help message"
    THUMBNAIL_HELP = "This is the thumbnail help message"
    ABOUT_ME = "This is the about message"


def send_error(client: Mai_bOTs, update, text: str):
    update.reply_text(text, reply_markup=ReplyKeyboardMarkup.remove_keyboard())


def send_info(client: Mai_bOTs, update, text: str):
    update.reply_text(text, reply_markup=ReplyKeyboardMarkup.remove_keyboard())


def is_banned(user_id: int) -> bool:
    return user_id in Config.BANNED_USERS


def is_admin(client: Mai_bOTs, chat_id: int, user_id: int) -> bool:
    try:
        return client.get_chat_member(chat_id, user_id).status in ("administrator", "creator")
    except:
        return False


def is_member(client: Mai_bOTs, chat_id: int, user_id: int) -> bool:
    try:
        return client.get_chat_member(chat_id, user_id).status != "left"
    except:
        return False


def is_channel_member(client: Mai_bOTs, chat_id: int, user_id: int) -> bool:
    try:
        return client.get_chat_member(chat_id, user_id).status != "left"
    except UserNotParticipant:
        return False


def send_start_message(client: Mai_bOTs, update):
    send_info(client, update, Translation.START_TEXT.format(update.from_user.first_name))


def send_help_message(client: Mai_bOTs, update):
    send_info(client, update, Translation.HELP_USER)


@Mai_bOTs.on_message(pyrogram.filters.command(["help"]))
async def help_user(bot: Mai_bOTs, update):
    if is_banned(update.from_user.id):
        return
    if not is_channel_member(bot, Config.UPDATE_CHANNEL, update.from_user.id):
        await update.reply_text(
            text="**Due To The Huge Traffic Only Channel Members Can Use This Bot Means You Need To Join The Below Mentioned Channel Before Using Me! **",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{Config.UPDATE_CHANNEL}")]
            ]))
        return
    send_help_message(bot, update)


@Mai_bOTs.on_message(pyrogram.filters.command(["start"]))
async def start_me(bot: Mai_bOTs, update):
    if is_banned(update.from_user.id):
        return
    if not is_member(bot, update.chat.id, update.from_user.id):
        send_error(bot, update, "You are not a member of this chat")
        return
    if not is_channel_member(bot, Config.UPDATE_CHANNEL, update.from_user.id):
        await update.reply_text(
            text="**Due To The Huge Traffic Only Channel Members Can Use This Bot Means You Need To Join The Below Mentioned Channel Before Using Me! **",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{Config.UPDATE_CHANNEL}")]
            ]))
        return
    send_start_message(bot, update)


@Mai_bOTs.on_callback_query()
async def cb_handler(client: Mai_bOTs, query: CallbackQuery):
    data = query.data
    if data == "rnme":
        await query.message.edit_text(
