"""
Telegram Caption Bot optimized for Cloudflare Pages deployment.
This script focuses solely on the Bots folder functionality and provides
a clean interface for Cloudflare Pages deployment.
"""
import os
import sys
import asyncio
import logging
from pyrogram import Client
import flask
from flask import Flask, render_template, request, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(stream=sys.stdout)
    ]
)
logger = logging.getLogger("CLOUDFLARE_BOT")

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "a-secret-key")

# Bot configuration
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
API_ID = os.environ.get("API_ID", "7331072")
API_HASH = os.environ.get("API_HASH", "f0bc2baeedff0926f9082880c326a475")

# Global bot instance
bot = None
bot_info = None
bot_started = False
bot_status = "Not started"

#######################################
# Bot functionality
#######################################

async def start_bot():
    """Start the Telegram bot"""
    global bot, bot_info, bot_started, bot_status
    
    try:
        logger.info("Starting Telegram bot...")
        
        # Configure plugins from the Bots directory
        plugins = dict(root="Bots")
        
        # Create the bot client
        bot = Client(
            "Advance-Caption-Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=plugins
        )
        
        # Start the bot
        await bot.start()
        bot_info = await bot.get_me()
        
        logger.info(f"Bot started successfully: @{bot_info.username}")
        logger.info(f"Bot ID: {bot_info.id}")
        logger.info(f"Bot Name: {bot_info.first_name}")
        
        bot_started = True
        bot_status = "Running"
        
        return True
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        bot_status = f"Error: {str(e)}"
        return False

async def stop_bot():
    """Stop the Telegram bot"""
    global bot, bot_started, bot_status
    
    if bot and bot.is_connected:
        await bot.stop()
        logger.info("Bot stopped.")
        
        bot_started = False
        bot_status = "Stopped"
        return True
    
    return False

#######################################
# Web routes
#######################################

@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html', 
                          bot_status=bot_status,
                          bot_info=bot_info)

@app.route('/status')
def status():
    """Show bot status page"""
    return render_template('status.html',
                          bot_status=bot_status,
                          bot_info=bot_info)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "bot_running": bot_started,
        "bot_status": bot_status
    })

@app.route('/api/start-bot', methods=['POST'])
def api_start_bot():
    """API endpoint to start the bot"""
    if bot_started:
        return jsonify({"status": "error", "message": "Bot is already running"})
    
    async def start_bot_async():
        await start_bot()
    
    asyncio.run(start_bot_async())
    
    return jsonify({
        "status": "success", 
        "message": "Bot started successfully", 
        "bot_status": bot_status
    })

@app.route('/api/stop-bot', methods=['POST'])
def api_stop_bot():
    """API endpoint to stop the bot"""
    if not bot_started:
        return jsonify({"status": "error", "message": "Bot is not running"})
    
    async def stop_bot_async():
        await stop_bot()
    
    asyncio.run(stop_bot_async())
    
    return jsonify({
        "status": "success", 
        "message": "Bot stopped successfully", 
        "bot_status": bot_status
    })

@app.route('/commands')
def commands():
    """Show available bot commands"""
    return render_template('commands.html')

#######################################
# Static file support for Cloudflare Pages
#######################################

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files for Cloudflare Pages"""
    if os.path.exists(os.path.join('static', path)):
        return app.send_static_file(path)
    else:
        return "Not found", 404

#######################################
# Main functions
#######################################

def start_background_bot():
    """Start the bot in the background"""
    async def run_bot():
        await start_bot()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

if __name__ == "__main__":
    # Start the bot in a separate thread
    import threading
    bot_thread = threading.Thread(target=start_background_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Get port from environment
    port = int(os.environ.get("PORT", 5000))
    
    # Start the Flask app
    app.run(host="0.0.0.0", port=port)