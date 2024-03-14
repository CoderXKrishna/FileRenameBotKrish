import logging
import os
import pyrogram
from pyrogram import filters
from pyrogram.errors import FileIdInvalid, MessageNotModified

import database.database as sql
from PIL import Image

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


class MyBot(pyrogram.Client):
    pass


@MyBot.on_message(filters.photo)
async def save_photo(bot: MyBot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return

    download_location = get_download_location(update)

    if update.media_group_id is not None:
        await sql.df_thumb(update.from_user.id, update.message_id)
        await bot.download_media(
            message=update,
            file_name=download_location
        )
    else:
        await sql.df_thumb(update.from_user.id, update.message_id)
        await bot.download_media(
            message=update,
            file_name=download_location
        )
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.SAVED_CUSTOM_THUMB_NAIL,
            reply_to_message_id=update.message_id
        )


def get_download_location(update):
    if update.media_group_id is not None:
        return Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/" + str(update.media_group_id) + "/"
    else:
        return Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"


@MyBot.on_message(filters.command(["delthumb"]))
async def delete_thumbnail(bot: MyBot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return

    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"

    try:
        await sql.del_thumb(update.from_user.id)
    except:
        pass

    try:
        os.remove(thumb_image_path)
    except FileNotFoundError:
        pass
    except Exception as e:
        logger.error(f"Error deleting thumbnail: {e}")

    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id
    )


@MyBot.on_message(filters.command(["showthumb"]))
async def show_thumb(bot: MyBot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return

    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"

    if not os.path.exists(thumb_image_path):
        mes = await thumb(update.from_user.id)
        if mes is None:
            await bot.send_message(
                chat_id=update.chat.id,
                text=Translation.NO_THUMB_FOUND,
                reply_to_message_id=update.message_id
            )
            return

        try:
            async with bot.get_messages(update.chat.id, mes.msg_id) as m:
                m = await m.download()
                thumb_image_path = m.file_path
        except FileIdInvalid:
            pass
        except MessageNotModified:
            pass
        except Exception as e:
            logger.error(f"Error downloading thumbnail: {e}")
            return

    try:
        await bot.send_photo(
            chat_id=update.chat.id,
            photo=thumb_image_path,
            reply_to_message_id=update.message_id
        )
    except FileNotFoundError:
        pass
    except Exception as e:
        logger.error(f"Error sending thumbnail: {e}")
