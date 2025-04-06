import re, os, time
id_pattern = re.compile(r'^.\d+$') 

class Bots(object):
    API_ID = os.environ.get("API_ID", "")
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    
    # Bot username (derived from token or from env var)
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "AUTO_caption_rgi_bot")
    
    # start_pic
    BOT_PIC = os.environ.get("BOT_PIC", "https://envs.sh/5bc.jpg")

    # web response configuration
    BOT_UPTIME = time.time()
    PORT = int(os.environ.get("PORT", "8080"))

    # force subs channel ( required.. 😥)
    FORCE_SUB = os.environ.get("FORCE_SUB", "M0VIES_CHANNEL") 
    
    # database config ( required.. 😥)
    DB_NAME = os.environ.get("DB_NAME", "M0VIES_CHANNEL")     
    DB_URL = os.environ.get("DB_URL", "")

    # default caption 
    DEF_CAP = os.environ.get("DEF_CAP", "<b><a href='https//:t.me/M0VIES_CHANNEL'>{file_name} \n\nMain Telegram Channel: @M0VIES_CHANNEL</a></b>",
    )

    # sticker Id
    STICKER_ID = os.environ.get("STICKER_ID", "CAACAgIAAxkBAAELFqBllhB70i13m-woXeIWDXU6BD2j7wAC9gcAAkb7rAR7xdjVOS5ziTQE")

    # admin id  ( required.. 😥)
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1927155351').split()]
    

# Developer ❁✗❍═❰ 🆁︎🅴︎🅽︎🅸︎🆂︎🅷︎ ❱═❍✗❁ 
# Don't Remove Credit 😔
# Telegram Channel @M0VIES_CHANNEL
# Developer @renish_rgi
