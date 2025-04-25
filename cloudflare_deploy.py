"""
Helper script for deploying to Cloudflare Pages.
This script prepares the static files needed for Cloudflare Pages deployment.
"""
import os
import shutil
import logging
import zipfile
import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DEPLOY")

# Required static files
REQUIRED_FILES = [
    "_headers",
    "_redirects",
    "favicon.svg",
    "index.html",
    "robots.txt",
    "sitemap.xml",
    "status.html",
    "commands.html",
    "bot_limitations.html",
]

def create_zip_package():
    """
    Create a ZIP package of the static files for Cloudflare Pages deployment.
    """
    # Get timestamp for the ZIP file name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"telegram-bot-cf-pages-{timestamp}.zip"
    
    logger.info(f"Creating ZIP package: {zip_filename}")
    
    # Create a temporary directory for static files
    temp_dir = "cf_pages_deploy"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Copy all required files from the static directory
    for filename in REQUIRED_FILES:
        source_path = os.path.join("static", filename)
        dest_path = os.path.join(temp_dir, filename)
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            logger.info(f"Copied: {filename}")
        else:
            logger.warning(f"File not found: {filename}")
    
    # Create index.html in temp directory if it doesn't exist
    index_path = os.path.join(temp_dir, "index.html")
    if not os.path.exists(index_path):
        with open(index_path, "w") as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Telegram Caption Bot</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
</head>
<body data-bs-theme="dark">
    <div class="container py-4">
        <div class="card">
            <div class="card-header">
                <h1>Telegram Caption Bot</h1>
            </div>
            <div class="card-body">
                <div class="alert alert-success">
                    <h4>Bot is Running</h4>
                    <p>The Telegram bot is active and running. Chat with <a href="https://t.me/Elizabeth_Olsen_robot">@Elizabeth_Olsen_robot</a> on Telegram.</p>
                </div>
                <p>This is the static page version for Cloudflare Pages. All bot functionality runs on the server.</p>
                <a href="commands.html" class="btn btn-primary">View Commands</a>
            </div>
        </div>
    </div>
</body>
</html>""")
            logger.info("Created default index.html")
    
    # Create a ZIP file containing all the files
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    logger.info(f"ZIP package created: {zip_filename}")
    
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
    logger.info("Temporary directory cleaned up")
    
    return zip_filename

if __name__ == "__main__":
    zip_file = create_zip_package()
    print(f"Deployment package created: {zip_file}")
    print("You can now upload this file to Cloudflare Pages.")