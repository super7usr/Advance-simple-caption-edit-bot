from aiohttp import web
from config import Bots
import time, datetime

CaptionBot = web.RouteTableDef()

@CaptionBot.get("/", allow_head=True)
async def root_route_handler(request):
    uptime = time.time() - Bots.BOT_UPTIME
    uptime_str = str(datetime.timedelta(seconds=int(uptime)))
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Auto Caption Bot</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
                text-align: center;
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            .img-container {{
                width: 100%;
                max-width: 300px;
                margin: 0 auto 20px auto;
                border-radius: 10px;
                overflow: hidden;
            }}
            .img-container img {{
                width: 100%;
                height: auto;
                display: block;
            }}
            h1 {{
                color: #0088cc;
            }}
            .stats {{
                margin: 20px 0;
                padding: 10px;
                background-color: #f9f9f9;
                border-radius: 5px;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #888;
            }}
            .bot-link {{
                display: inline-block;
                margin: 20px auto;
                padding: 12px 24px;
                background-color: #0088cc;
                color: white;
                text-decoration: none;
                font-weight: bold;
                border-radius: 30px;
                transition: background-color 0.3s;
            }}
            .bot-link:hover {{
                background-color: #006699;
            }}
            .bot-title {{
                cursor: pointer;
                transition: color 0.3s;
            }}
            .bot-title:hover {{
                color: #006699;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="https://t.me/{Bots.BOT_USERNAME}" style="text-decoration: none;">
                <h1 class="bot-title">🤖 Auto Caption Bot</h1>
            </a>
            <div class="img-container">
                <a href="https://t.me/{Bots.BOT_USERNAME}">
                    <img src="{Bots.BOT_PIC}" alt="Bot Image" onerror="this.src='https://telegram.org/img/t_logo.png?1'">
                </a>
            </div>
            <p>An advanced Telegram bot that automatically adds captions to your media files.</p>
            <div class="stats">
                <p><strong>Bot Status:</strong> 🟢 Online</p>
                <p><strong>Uptime:</strong> {uptime_str}</p>
            </div>
            <p>Use this bot to automatically add captions to videos, photos, and documents in your Telegram channels.</p>
            
            <a href="https://t.me/{Bots.BOT_USERNAME}" class="bot-link">
                Open Bot in Telegram
            </a>
            
            <div class="footer">
                <p>Running on Replit • Channel: <a href="https://t.me/{Bots.FORCE_SUB}" style="color: #0088cc;">@{Bots.FORCE_SUB}</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return web.Response(text=html_content, content_type="text/html")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(CaptionBot)
    return web_app
