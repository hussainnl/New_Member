import asyncio
import os
from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def get_invite_link(chat_id: int):
    """To get the invite link for the passed member ,that work for one time"""

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    await app.initialize()
    await app.start()

    invite_link = await app.bot.create_chat_invite_link(
        chat_id=chat_id,
        member_limit=1,
        creates_join_request=False
    )

    await app.stop()
    return invite_link.invite_link


