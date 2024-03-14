import logging
import os
import random
import time
from typing import Union

import pyrogram
from pyrogram.errors import UserNotParticipant, UserBannedInChannel

import hachoir.metadata
import hachoir.parser
from PIL import Image

# the logging things
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

# Initialize Pyrogram Client
logging.getLogger("pyrogram").setLevel(logging.WARNING)
app = pyrogram.Client(name="Mai_bOTs")

# from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import progress_for_pyrogram
from helper_funcs.help_Nekmo_ffmpeg import take_screen_shot

@app.on_message(pyrogram.filters.command(["c2v"]))
async def convert_to_video(client: pyrogram.Client, message: pyrogram.types.Message):
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await client.get_chat_member(update_channel, message.chat.id)
            if user.status == "kicked":
                await message.reply_text("Sorry, You are **B A N N E D**")
                return
        except UserNotParticipant:
            await message.reply_text(
                text="**Please Join My Update Channel Before Using Me..**",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
                ])
            )
            return

    if message.reply_to_message is not None:
        download_location = Config.DOWNLOAD_LOCATION + "/"
        file_name = download_location
        a = await client.send_message(
            chat_id=message.chat.id,
            text=Translation.DOWNLOAD_START,
            reply_to_message_id=message.message_id
        )
        c_time = time.time()
        the_real_download_location = await client.download_media(
            message=message.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.DOWNLOAD_START,
                a,
                c_time
            )
        )
        if the_real_download_location is not None:
            await client.edit_message_text(
                text=Translation.SAVED_RECVD_DOC_FILE,
                chat_id=message.chat.id,
                message_id=a.message_id
            )
            logger.info(the_real_download_location)

            width = 0
            height = 0
            duration = 0
            metadata = hachoir.metadata.extractMetadata(hachoir.parser.createParser(the_real_download_location))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(message.from_user.id) + ".jpg"
            if not os.path.exists(thumb_image_path):
                thumb_image_path = await take_screen_shot(
                    the_real_download_location,
                    os.path.dirname(the_real_download_location),
                    random.randint(
                        0,
                        duration - 1
                    )
                )
            logger.info(thumb_image_path)

            metadata = hachoir.metadata.extractMetadata(hachoir.parser.createParser(thumb_image_path))
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")

            Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
            img = Image.open(thumb_image_path)
            img.resize((90, height))
            img.save(thumb_image_path, "JPEG")

            c_time = time.time()
            try:
                await client.send_video(
                    chat_id=message.chat.id,
                    video=the_real_download_location,
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    thumb=thumb_image_path,
                    reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        a,
                        c_time
                    )
                )
            except UserBannedInChannel:
                await message.reply_text(
                    text="**You are banned from this channel.**",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
                    ])
                )
            finally:
                try:
                    os.remove(the_real_download_location)
                    os.remove(thumb_image_path)
                except
