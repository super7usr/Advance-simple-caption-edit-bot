# Task Processor for Telegram Caption Bot
# This module processes pending tasks that were saved when the bot was offline

import asyncio
import logging
import os
import zipfile
import io
from datetime import datetime
from pyrogram import Client
from pyrogram.errors import FloodWait
from .database import (
    get_pending_tasks, mark_task_completed, mark_task_failed, chnl_ids
)
from config import Bots

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TaskProcessor")

async def create_code_backup():
    """Create a zip file containing the current code as backup"""
    memory_file = io.BytesIO()
    
    # List of important non-Python files to include
    important_files = [
        'README.md',
        'ENHANCED_RELIABILITY.md',
        'DEPLOYMENT.md',
        'KEEP_ALIVE.md',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'app.json',
        'LICENSE',
        '.env.example',
        'netlify.toml',
        'Dockerfile'
    ]
    
    # List of important file extensions to include
    important_extensions = ['.py', '.json', '.md', '.txt', '.toml', '.yaml', '.yml']
    
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # First gather project root files
        for root, _, files in os.walk('.'):
            # Skip unwanted directories
            if any(x in root for x in ['.git', '__pycache__', 'venv', '.env']):
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                
                # Include if it's a Python file
                if file.endswith(tuple(important_extensions)):
                    zf.write(file_path)
                # Include if it's in our list of important files
                elif file in important_files:
                    zf.write(file_path)
                # Include session files
                elif file.endswith('.session'):
                    zf.write(file_path)
        
        # Also check the temp_repo directory for important files
        if os.path.exists('temp_repo'):
            logger.info("Including files from temp_repo directory")
            for root, _, files in os.walk('temp_repo'):
                # Skip unwanted directories
                if any(x in root for x in ['__pycache__', 'venv']):
                    continue
                    
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Include if it has important extension
                    if file.endswith(tuple(important_extensions)):
                        zf.write(file_path)
                    # Include if it's in our list of important files
                    elif file in important_files:
                        zf.write(file_path)
                    # Include session files
                    elif file.endswith('.session'):
                        zf.write(file_path)
    
    # Log the files included in the zip
    included_files = zf.namelist()
    logger.info(f"Number of files included in backup: {len(included_files)}")
    logger.info(f"Important files included: {[f for f in included_files if os.path.basename(f) in important_files]}")
    
    # Reset the file pointer to the beginning of the buffer
    memory_file.seek(0)
    logger.info("Created backup zip file with all important project files")
    return memory_file

async def send_restart_notification(bot, include_zip=True):
    """Send a notification to admin that the bot has restarted"""
    
    startup_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    # Fancy formatted restart message
    restart_message = f"""
<b>📸 Auto Caption Bot Started Successfully ✨️</b>

<b>⏰ Restart Time:</b> <code>{startup_time}</code>
<b>👥 Total Users:</b> <code>{await bot.db.users.count_documents({})}</code>
<b>📝 Tasks:</b> <code>Pending: {await bot.db.pending_tasks.count_documents({'status': 'pending'})} | Completed: {await bot.db.pending_tasks.count_documents({'status': 'completed'})} | Failed: {await bot.db.pending_tasks.count_documents({'status': 'failed'})}</code>

<b>✅ Bot is now ready to process messages!</b>
<b>🔄 All pending tasks will be processed automatically.</b>

<i>This is an automatic notification sent when the bot restarts.</i>
"""
    
    for admin_id in Bots.ADMIN:
        try:
            if include_zip:
                # Create code backup zip
                backup_file = await create_code_backup()
                
                # Send the backup file with the restart message
                await bot.send_document(
                    chat_id=admin_id,
                    document=backup_file,
                    file_name=f"caption_bot_backup_{startup_time.replace(' ', '_').replace(':', '-')}.zip",
                    caption=restart_message
                )
            else:
                # Just send the message without zip file
                await bot.send_message(
                    chat_id=admin_id,
                    text=restart_message
                )
        except Exception as e:
            logger.error(f"Error sending restart notification to admin {admin_id}: {e}")

async def process_caption_edit_task(bot, task):
    """Process a pending caption edit task"""
    
    try:
        data = task['data']
        chat_id = data['chat_id']
        message_id = data['message_id']
        file_name = data['file_name']
        
        # Get the message
        message = await bot.get_messages(chat_id, message_id)
        
        if not message or not message.media:
            await mark_task_failed(task['_id'], "Message not found or is not media")
            return False
            
        # Get caption format from database or use default
        cap_dets = await chnl_ids.find_one({"chnl_id": chat_id})
        
        if cap_dets:
            cap = cap_dets["caption"]
            replaced_caption = cap.format(file_name=file_name)
        else:
            replaced_caption = Bots.DEF_CAP.format(file_name=file_name)
            
        # Edit the message with the new caption
        try:
            await message.edit(replaced_caption)
            await mark_task_completed(task['_id'])
            return True
        except FloodWait as e:
            # If flood wait is encountered, wait and retry
            await asyncio.sleep(e.x)
            return await process_caption_edit_task(bot, task)
            
    except Exception as e:
        await mark_task_failed(task['_id'], str(e))
        logger.error(f"Error processing caption edit task: {e}")
        return False

async def process_pending_tasks(bot):
    """Process all pending tasks from the database"""
    
    logger.info("Starting to process pending tasks...")
    
    # Get stats before processing
    pending_count = await bot.db.pending_tasks.count_documents({"status": "pending"})
    logger.info(f"Found {pending_count} pending tasks")
    
    if pending_count == 0:
        return
    
    # Process tasks in batches to avoid overloading
    batch_size = 10
    processed = 0
    failed = 0
    
    while True:
        tasks = await get_pending_tasks(batch_size)
        
        if not tasks or len(tasks) == 0:
            break
            
        for task in tasks:
            try:
                task_type = task.get('task_type')
                
                if task_type == 'caption_edit':
                    success = await process_caption_edit_task(bot, task)
                    if success:
                        processed += 1
                    else:
                        failed += 1
                elif task_type == 'test_task':
                    # Handle test tasks - simply mark them as completed
                    logger.info(f"Processing test task: {task['data'].get('message')}")
                    await mark_task_completed(task['_id'])
                    processed += 1
                else:
                    await mark_task_failed(task['_id'], f"Unknown task type: {task_type}")
                    failed += 1
                    
            except Exception as e:
                logger.error(f"Error processing task {task.get('_id')}: {e}")
                try:
                    await mark_task_failed(task['_id'], str(e))
                except Exception as mark_error:
                    logger.error(f"Failed to mark task {task.get('_id')} as failed: {mark_error}")
                failed += 1
                
            # Small delay to avoid hitting rate limits
            await asyncio.sleep(0.5)
            
    logger.info(f"Task processing complete. Processed: {processed}, Failed: {failed}")
    
    # If there were successful tasks, send a notification to admin
    if processed > 0:
        for admin_id in Bots.ADMIN:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"<b>🔄 Processed Pending Tasks</b>\n\n"
                         f"✅ <b>Successfully processed:</b> {processed}\n"
                         f"❌ <b>Failed:</b> {failed}\n\n"
                         f"<i>Tasks were processed after bot restart.</i>"
                )
            except Exception as e:
                logger.error(f"Failed to send task completion notification to admin {admin_id}: {e}")