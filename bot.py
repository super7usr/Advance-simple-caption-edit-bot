# (c) @renish_rgi
# Developer ❁✗❍═❰ 🆁︎🅴︎🅽︎🅸︎🆂︎🅷︎ ❱═❍✗❁ 
# Don't Remove Credit 😔
# Telegram Channel @M0VIES_CHANNEL
# Developer @renish_rgi

from aiohttp import web
from pyrogram import Client
from config import Bots
from Bots.web_support import web_server
import motor.motor_asyncio
import asyncio
from Bots.task_processor import process_pending_tasks, send_restart_notification
import logging

logger = logging.getLogger(__name__)

class AutoCaptionBot(Client):
    def __init__(self):
        super().__init__(
            name="Advance-Caption-Bot",
            api_id=Bots.API_ID,
            api_hash=Bots.API_HASH,
            bot_token=Bots.BOT_TOKEN,
            workers=200,
            plugins={"root": "Bots"},
            sleep_threshold=15,
        )
        # Set up database connection for direct access
        mongodb = motor.motor_asyncio.AsyncIOMotorClient(Bots.DB_URL)
        self.db = mongodb[Bots.DB_NAME]

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.uptime = Bots.BOT_UPTIME
        self.force_channel = Bots.FORCE_SUB
        if Bots.FORCE_SUB:
            try:
                link = await self.export_chat_invite_link(Bots.FORCE_SUB)
                self.invitelink = link
            except Exception as e:
                print(e)
                print("Make Sure Bot admin in force sub channel")
                self.force_channel = None
        
        # Start web server
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Bots.PORT).start()
        
        # Send enhanced restart notification with code backup zip
        print(f"📸 Auto Caption Bot Is Started! ✨️")
        await send_restart_notification(self, include_zip=True)
        
        # Process any pending tasks from when the bot was offline
        asyncio.create_task(self._process_pending_tasks())
        
    async def _process_pending_tasks(self):
        """Process pending tasks after a short delay to ensure bot is fully initialized"""
        await asyncio.sleep(10)  # Wait 10 seconds after startup before processing tasks
        try:
            await process_pending_tasks(self)
        except Exception as e:
            logger.error(f"Error processing pending tasks: {e}")
            
    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped 🙄")
        
AutoCaptionBot().run()

# Developer ❁✗❍═❰ 🆁︎🅴︎🅽︎🅸︎🆂︎🅷︎ ❱═❍✗❁ 
# Don't Remove Credit 😔
# Telegram Channel @M0VIES_CHANNEL
# Developer @renish_rgi
