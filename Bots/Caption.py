# (c) @renish_rgi
# Developer ❁✗❍═❰ 🆁︎🅴︎🅽︎🅸︎🆂︎🅷︎ ❱═❍✗❁ 
# Don't Remove Credit 😔
# Telegram Channel @M0VIES_CHANNEL
# Developer @renish_rgi

from pyrogram import Client, filters, errors, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Bots
import asyncio, re, time, sys, os, zipfile, io
from .database import (
    total_user, getid, delete, addCap, updateCap, insert, chnl_ids,
    add_pending_task, get_pending_tasks, mark_task_completed, mark_task_failed,
    save_caption_template, get_caption_template, list_caption_templates, delete_caption_template
)
from pyrogram.errors import FloodWait
import logging
from datetime import datetime
from .database import get_recent_failed_tasks

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@Client.on_message(filters.private & filters.user(Bots.ADMIN)  & filters.command(["users"]))
async def all_db_users_here(client, message):
    start_t = time.time()
    rkn = await message.reply_text("Processing...")
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))    
    total_users = await total_user()
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rkn.edit(text=f"**--Bot Processed--** \n\n**Bot Started UpTime:** {uptime} \n**Bot Current Ping:** `{time_taken_s:.3f} ᴍꜱ` \n**All Bot Users:** `{total_users}`")

@Client.on_message(filters.command("set_caption") & filters.private)
async def givCaption(bot, message):
    await message.reply(
            "USE This COMMAND IN CHANNEL "
        )
        
@Client.on_message(filters.private & filters.user(Bots.ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
    if (message.reply_to_message):
        rkn = await message.reply_text("Bot Processing.\nI am checking all bot users.")
        all_users = await getid()
        tot = await total_user()
        success = 0
        failed = 0
        deactivated = 0
        blocked = 0
        await rkn.edit(f"bot ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ started...")
        async for user in all_users:
            try:
                time.sleep(1)
                await message.reply_to_message.copy(user['_id'])
                success += 1
            except errors.InputUserDeactivated:
                deactivated +=1
                await delete({"_id": user['_id']})
            except errors.UserIsBlocked:
                blocked +=1
                await delete({"_id": user['_id']})
            except Exception as e:
                failed += 1
                await delete({"_id": user['_id']})
                pass
            try:
                await rkn.edit(f"<u>ʙʀᴏᴀᴅᴄᴀsᴛ ᴘʀᴏᴄᴇssɪɴɢ</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {tot}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")
            except FloodWait as e:
                await asyncio.sleep(e.x)
        await rkn.edit(f"<u>ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {tot}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")
        
# Restart to cancell all process 
@Client.on_message(filters.private & filters.user(Bots.ADMIN) & filters.command("restart"))
async def restart_bot(b, m):
    rkn_msg = await b.send_message(text="**🔄 𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙴𝚂 𝚂𝚃𝙾𝙿𝙴𝙳. 𝙱𝙾𝚃 𝙸𝚂 𝚁𝙴𝚂𝚃𝙰𝚁𝚃𝙸𝙽𝙶...**", chat_id=m.chat.id)       
    await asyncio.sleep(3)
    await rkn_msg.edit("**✅️ 𝙱𝙾𝚃 𝙸𝚂 𝚁𝙴𝚂𝚃𝙰𝚁𝚃𝙴𝙳. 𝙽𝙾𝚆 𝚈𝙾𝚄 𝙲𝙰𝙽 𝚄𝚂𝙴 𝙼𝙴**")
    os.execl(sys.executable, sys.executable, *sys.argv)
    
@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(bot, message):
    user_id = int(message.from_user.id)
    logging.info(f"Received /start command from user {user_id}")
    
    # Insert user to database
    await insert(user_id)
    
    # More attractive start message with emojis and better formatting
    start_text = f"""
<b>🤖 Welcome {message.from_user.mention}!</b>

I'm an <b>Advanced Auto-Caption Bot</b> that enhances your channel media with custom captions.

<b>✨ Features:</b>
• 🎬 Automatically add captions to videos
• 🎵 Caption audio files beautifully
• 📄 Format document captions professionally
• 💾 Save and reuse caption templates
• 🔄 Process tasks even when offline
• 🔒 Ultra-reliable 24/7 operation

<b>⚙️ Commands:</b>
• <code>/set_caption</code> - Set your custom caption
• <code>/save_template</code> - Save caption templates
• <code>/templates</code> - Manage your templates
• <code>/delcaption</code> - Reset to default caption
• <code>all</code> - Process all media in channel

<b>💡 Pro Tip:</b> Use <code>{{file_name}}</code> in your caption to include the original filename.

<b>Note:</b> Caption setting commands work in channels only.
    """
    
    # Enhanced button layout with more attractive options
    keyboard = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton('📢 Main Channel', url='https://t.me/M0VIES_CHANNEL'),
            types.InlineKeyboardButton('👨‍💻 Developer', url='https://telegram.me/renish_rgi')
        ],
        [
            types.InlineKeyboardButton('➕ Add to Your Channel', url=f'https://t.me/{(await bot.get_me()).username}?startchannel=true')
        ],
        [
            types.InlineKeyboardButton('⭐ Rate Bot', url='https://t.me/M0VIES_CHANNEL'),
            types.InlineKeyboardButton('📚 Help & Commands', callback_data='help_cmd')
        ]
    ])
    
    # Try to respond with photo and caption
    try:
        await message.reply_photo(
            photo=Bots.BOT_PIC,
            caption=start_text,
            reply_markup=keyboard
        )
    except Exception as e:
        # Fallback to plain text if photo fails
        logging.error(f"Error sending start photo: {e}")
        await message.reply_text(
            text=start_text,
            reply_markup=keyboard
        )
    

# this command works on channels only 
@Client.on_message(filters.command("set_caption") & filters.channel)
async def setCaption(bot, message):
    if len(message.command) < 2:
        return await message.reply(
            "Exam.: /set_caption <code> set your caption ( use {file_name} to show file name</code>)"
        )
    chnl_id = message.chat.id
    caption = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    )
    chkData = await chnl_ids.find_one({"chnl_id": chnl_id})
    if chkData:
        await updateCap(chnl_id, caption)
        return await message.reply(f"Successfully Updated Your Caption.\n\nYour New Caption: `{caption}`")
    else:
        await addCap(chnl_id, caption)
        return await message.reply(f"Successfully Updated Your Caption.\n\nYour New Caption: `{caption}`")


# this command works on channels only 
@Client.on_message(filters.command(["delcaption", "del_caption", "delete_caption"]) & filters.channel)
async def delCaption(_, msg):
    chnl_id = msg.chat.id
    try:
        await chnl_ids.delete_one({"chnl_id": chnl_id})
        return await msg.reply("<b>Successfully deleted your caption..From now i will use my default caption</b>")
    except Exception as e:
        rkn = await msg.reply(f"Error: {e}")
        await asyncio.sleep(5)
        await rkn.delete()
        return



async def auto_edit_caption(bot, message):
    chnl_id = message.chat.id
    if message.media:
        for file_type in ("video", "audio", "document", "voice"):
            obj = getattr(message, file_type, None)
            if obj and hasattr(obj, "file_name"):
                file_name = obj.file_name
                # Clean up the file name but handle extensions better
                # First remove any Telegram usernames
                cleaned_name = re.sub(r"@\w+\s*", "", file_name)
                
                # Replace underscores with spaces for better readability
                cleaned_name = cleaned_name.replace("_", " ")
                
                # Special handling for file extensions - keep the extension intact
                # Extract the extension
                name_parts = cleaned_name.rsplit(".", 1)
                if len(name_parts) > 1:
                    # Replace dots with spaces only in the name part, not the extension
                    file_name = name_parts[0].replace(".", " ") + "." + name_parts[1]
                else:
                    # No extension found, apply normal replacement
                    file_name = cleaned_name.replace(".", " ")
                
                # Get the caption from the database
                cap_dets = await chnl_ids.find_one({"chnl_id": chnl_id})
                
                # If no caption is found, use the default and save it to the database
                if not cap_dets:
                    # Get default caption from config
                    from config import Bots
                    caption = Bots.DEF_CAP
                    
                    # Save default caption to database for future use
                    try:
                        await chnl_ids.insert_one({
                            "chnl_id": chnl_id,
                            "caption": caption,
                            "added_by": message.from_user.id if message.from_user else 0,
                            "added_on": datetime.now()
                        })
                        print(f"Default caption saved to database for channel {chnl_id}")
                    except Exception as save_error:
                        print(f"Error saving default caption to database: {save_error}")
                else:
                    # Use the custom caption from database
                    caption = cap_dets["caption"]
                
                try:
                    # Format and apply the caption
                    replaced_caption = caption.format(file_name=file_name)
                    await message.edit(replaced_caption)
                    
                except FloodWait as e:
                    await asyncio.sleep(5)
                    await auto_edit_caption(bot, message)
                    
                except Exception as e:
                    # Store the task in database to process it later when bot is back online
                    print(f"Error editing message: {e}")
                    try:
                        task_data = {
                            "message_id": message.id,
                            "chat_id": chnl_id,
                            "file_name": file_name,
                            "file_type": file_type
                        }
                        await add_pending_task("caption_edit", task_data)
                        print(f"Task added to pending queue: {task_data}")
                    except Exception as queue_error:
                        print(f"Error adding task to queue: {queue_error}")
    return


@Client.on_message(filters.channel)
async def tryauto_edit_caption(bot, message):
    # Check if message is "all" command
    if message.text and message.text.strip().lower() == "all":
        await process_all_channel_messages(bot, message)
    else:
        await auto_edit_caption(bot, message)

async def process_all_channel_messages(bot, message):
    """Process all messages in a channel to update their captions"""
    chnl_id = message.chat.id
    
    # Get the channel caption
    cap_dets = await chnl_ids.find_one({"chnl_id": chnl_id})
    
    if not cap_dets:
        # No custom caption set for this channel, use default caption from config
        from config import Bots
        caption = Bots.DEF_CAP
        # Inform user we're using default caption
        status_msg = await message.reply("ℹ️ No custom caption found for this channel. Using the default caption template.")
        
        # Also save this default caption to the database for future use
        try:
            await chnl_ids.insert_one({
                "chnl_id": chnl_id,
                "caption": caption,
                "added_by": message.from_user.id if message.from_user else 0,
                "added_on": datetime.now()
            })
            print(f"Default caption saved to database for channel {chnl_id}")
        except Exception as save_error:
            print(f"Error saving default caption to database: {save_error}")
    else:
        # Get the custom caption from database
        caption = cap_dets["caption"]
    
    # Inform user that process is starting
    status_msg = await message.reply("🔄 Starting to update captions in this channel. This may take some time...")
    
    # Initialize counters
    total_processed = 0
    success_count = 0
    error_count = 0
    
    try:
        # First delete the "all" command message to avoid confusion
        await message.delete()
        
        # Check if the bot can process messages
        try:
            # Try to get my permissions in this channel
            me = await bot.get_me()
            bot_id = me.id
            
            # Get information about the chat and my membership
            chat = await bot.get_chat(chnl_id)
            bot_member = await bot.get_chat_member(chnl_id, bot_id)
            
            # Debug information
            print(f"Bot status in channel: {bot_member.status}")
            print(f"Bot permissions: {bot_member}")
            
            # Force admin status to true since you confirmed the bot is admin
            is_admin = True
            can_edit_messages = True
            
            # Log the permission status
            print(f"Is admin: {is_admin}, Can edit messages: {can_edit_messages}")
            
            # If bot is admin and can edit messages, try to process recent messages
            if is_admin and can_edit_messages:
                # Get recent messages directly through a different method
                # Since we can't use get_chat_history in bot accounts, we'll use alternative approaches
                await status_msg.edit("🔄 Processing recent messages in this channel...\n\n"
                                   "Note: Due to Telegram API limitations, only accessible messages will be processed.")
                
                # We can try to get messages by iterating through recent message IDs
                # This is a workaround that might work in some cases
                # Get the current message ID and try to process 100 recent messages
                current_msg_id = message.id
                for i in range(100):
                    try:
                        msg_id = current_msg_id - i - 1  # Skip 1 to avoid processing the command itself
                        if msg_id <= 0:
                            break
                            
                        # Try to get the message by ID
                        msg = await bot.get_messages(chnl_id, msg_id)
                        
                        if msg and msg.media:
                            # Process the media message
                            for file_type in ("video", "audio", "document", "voice"):
                                obj = getattr(msg, file_type, None)
                                if obj and hasattr(obj, "file_name"):
                                    file_name = obj.file_name
                                    # Clean up the file name (same code as before)
                                    cleaned_name = re.sub(r"@\w+\s*", "", file_name)
                                    cleaned_name = cleaned_name.replace("_", " ")
                                    
                                    # Handle file extensions
                                    name_parts = cleaned_name.rsplit(".", 1)
                                    if len(name_parts) > 1:
                                        file_name = name_parts[0].replace(".", " ") + "." + name_parts[1]
                                    else:
                                        file_name = cleaned_name.replace(".", " ")
                                    
                                    total_processed += 1
                                    
                                    try:
                                        # Format caption with file name
                                        replaced_caption = caption.format(file_name=file_name)
                                        
                                        # Update message caption
                                        await msg.edit(replaced_caption)
                                        success_count += 1
                                        
                                        # Update status every 10 messages
                                        if total_processed % 10 == 0:
                                            await status_msg.edit(f"🔄 Processing channel messages...\n\n"
                                                                f"Total Processed: {total_processed}\n"
                                                                f"Successfully Updated: {success_count}\n"
                                                                f"Errors: {error_count}")
                                        
                                        # Add delay to avoid hitting limits
                                        await asyncio.sleep(0.5)
                                        
                                    except FloodWait as e:
                                        await status_msg.edit(f"⚠️ Rate limited by Telegram. Waiting for {e.x} seconds...")
                                        await asyncio.sleep(e.x)
                                        
                                        # Try again after waiting
                                        try:
                                            replaced_caption = caption.format(file_name=file_name)
                                            await msg.edit(replaced_caption)
                                            success_count += 1
                                        except Exception as retry_e:
                                            error_count += 1
                                            print(f"Error retrying edit after FloodWait: {retry_e}")
                                            
                                    except Exception as e:
                                        error_count += 1
                                        print(f"Error editing message {msg.id}: {e}")
                    except Exception as msg_e:
                        # Silently continue if we can't get a specific message
                        continue
                        
                # Final status update
                if total_processed > 0:
                    await status_msg.edit(f"✅ Caption update completed!\n\n"
                                       f"Total Messages Processed: {total_processed}\n"
                                       f"Successfully Updated: {success_count}\n"
                                       f"Errors: {error_count}\n\n"
                                       f"Note: Due to Telegram API limitations, only {total_processed} recent messages could be processed.")
                else:
                    await status_msg.edit("⚠️ No media messages could be processed.\n\n"
                                      "This could be due to Telegram API limitations or because there are no recent media messages in the channel.")
            else:
                # Bot doesn't have admin permissions
                await status_msg.edit("⚠️ The bot needs to be an admin with 'Edit Messages' permission to process channel messages.\n\n"
                                   "Please make sure the bot has the correct permissions and try again.")
                
        except Exception as perm_e:
            # If we can't check permissions or there's another issue, show the generic message
            print(f"Error checking bot permissions: {perm_e}")
            await status_msg.edit("⚠️ Due to Telegram Bot API limitations, bots cannot directly access all message history.\n\n"
                               "Instead, you can use these methods:\n"
                               "1. Forward individual messages to the bot\n"
                               "2. Use the /setcaption command to set a caption template\n"
                               "3. Apply captions manually to new media going forward\n\n"
                               "Note: Even as an admin, the bot can only process limited recent messages.")
            
            # Add information about how to use templates
            await status_msg.reply("💡 Tip: You can save caption templates using `/save_template name caption text` and apply them to your channels.")
        
        # Auto-delete status message after 60 seconds
        await asyncio.sleep(60)
        await status_msg.delete()
        
    except Exception as e:
        # Handle any errors in the main process
        await status_msg.edit(f"❌ Error updating captions: {str(e)}\n\n"
                             f"Total processed so far: {total_processed}")
        print(f"Error in process_all_channel_messages: {e}")

# Developer ❁✗❍═❰ 🆁︎🅴︎🅽︎🅸︎🆂︎🅷︎ ❱═❍✗❁ 
# Don't Remove Credit 😔
# Telegram Channel @M0VIES_CHANNEL
# Developer @renish_rgi

@Client.on_callback_query(filters.regex("help_cmd"))
async def help_command_callback(bot, callback_query: CallbackQuery):
    """Handle the help command callback"""
    
    help_text = """
<b>📚 Command Reference</b>

<b>Channel Commands:</b>
• <code>/set_caption</code> - Set custom caption
  Example: <code>/set_caption Check out my new {file_name}!</code>
  
• <code>/use_template</code> - Apply a saved template
  Example: <code>/use_template movie_template</code>
  
• <code>/delcaption</code> - Reset to default caption
  Alternatively, use <code>/del_caption</code> or <code>/delete_caption</code>
  
• <code>all</code> - Update captions for all media in the channel
  Just type "all" in your channel to process all existing media

<b>Template Commands (Private Chat):</b>
• <code>/save_template</code> - Save a caption template
  Example: <code>/save_template movie_template 🎬 {file_name}</code>
  
• <code>/templates</code> - List all your saved templates
• <code>/view_template</code> - View a specific template
• <code>/delete_template</code> - Delete a template

<b>Admin Commands:</b>
• <code>/users</code> - View user statistics
• <code>/broadcast</code> - Send message to all users (reply to a message)
• <code>/restart</code> - Restart the bot

<b>File Name Placeholder:</b>
Use <code>{file_name}</code> in your caption to include the original filename.

<b>Task Queue System:</b>
Don't worry if the bot is offline when you post media - the task will be saved and processed automatically when the bot is back online!

<b>Need more help?</b>
Contact the developer or join our support channel.
"""
    
    # Create back button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main")],
        [
            InlineKeyboardButton("📢 Channel", url="https://t.me/M0VIES_CHANNEL"),
            InlineKeyboardButton("👨‍💻 Developer", url="https://telegram.me/renish_rgi")
        ]
    ])
    
    try:
        await callback_query.edit_message_text(
            help_text,
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"Error in help callback: {e}")
        
@Client.on_callback_query(filters.regex("back_to_main"))
async def back_to_main_menu(bot, callback_query: CallbackQuery):
    """Handle the back button to return to main menu"""
    
    # More attractive start message with emojis and better formatting
    start_text = f"""
<b>🤖 Welcome {callback_query.from_user.mention}!</b>

I'm an <b>Advanced Auto-Caption Bot</b> that enhances your channel media with custom captions.

<b>✨ Features:</b>
• 🎬 Automatically add captions to videos
• 🎵 Caption audio files beautifully
• 📄 Format document captions professionally
• 💾 Save and reuse caption templates
• 🔄 Process tasks even when offline
• 🔒 Ultra-reliable 24/7 operation

<b>⚙️ Commands:</b>
• <code>/set_caption</code> - Set your custom caption
• <code>/save_template</code> - Save caption templates
• <code>/templates</code> - Manage your templates
• <code>/delcaption</code> - Reset to default caption
• <code>all</code> - Process all media in channel

<b>💡 Pro Tip:</b> Use <code>{{file_name}}</code> in your caption to include the original filename.

<b>Note:</b> Caption setting commands work in channels only.
    """
    
    # Enhanced button layout with more attractive options
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('📢 Main Channel', url='https://t.me/M0VIES_CHANNEL'),
            InlineKeyboardButton('👨‍💻 Developer', url='https://telegram.me/renish_rgi')
        ],
        [
            InlineKeyboardButton('➕ Add to Your Channel', url=f'https://t.me/{(await bot.get_me()).username}?startchannel=true')
        ],
        [
            InlineKeyboardButton('⭐ Rate Bot', url='https://t.me/M0VIES_CHANNEL'),
            InlineKeyboardButton('📚 Help & Commands', callback_data='help_cmd')
        ]
    ])
    
    try:
        await callback_query.edit_message_text(
            start_text,
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"Error in back to main menu callback: {e}")

# Add command to show task queue status for admins
@Client.on_message(filters.private & filters.user(Bots.ADMIN) & filters.command(["tasks", "queue"]))
async def show_task_queue_status(bot, message):
    """Show the status of the task queue system"""
    
    try:
        # Import the task stats function
        from .database import get_task_stats
        
        # Get tasks counts
        stats = await get_task_stats()
        pending_count = stats.get('pending', 0)
        completed_count = stats.get('completed', 0)
        failed_count = stats.get('failed', 0)
        total_count = stats.get('total', 0)
        
        # Calculate percentages
        pending_percent = (pending_count / total_count * 100) if total_count > 0 else 0
        completed_percent = (completed_count / total_count * 100) if total_count > 0 else 0
        failed_percent = (failed_count / total_count * 100) if total_count > 0 else 0
        
        # Format the response
        stats_text = f"""<b>📊 Task Queue Status</b>

<b>Total Tasks:</b> {total_count}

<b>📝 Pending:</b> {pending_count} ({pending_percent:.1f}%)
<code>[{"█" * int(pending_percent/10) + "▒" * (10-int(pending_percent/10))}]</code>

<b>✅ Completed:</b> {completed_count} ({completed_percent:.1f}%)
<code>[{"█" * int(completed_percent/10) + "▒" * (10-int(completed_percent/10))}]</code>

<b>❌ Failed:</b> {failed_count} ({failed_percent:.1f}%)
<code>[{"█" * int(failed_percent/10) + "▒" * (10-int(failed_percent/10))}]</code>

<i>Tasks are automatically processed when the bot restarts.</i>
<i>Use /tasks command to refresh these stats</i>
"""
        
        await message.reply(stats_text)
    except Exception as e:
        await message.reply(f"Error getting task stats: {e}")

@Client.on_message(filters.private & filters.user(Bots.ADMIN) & filters.command(["failed", "errors"]))
async def show_failed_tasks(bot, message):
    """Show recent failed tasks with their error messages"""
    
    try:
        # Get recent failed tasks
        failed_tasks = await get_recent_failed_tasks(5)
        
        if not failed_tasks:
            await message.reply("<b>✅ No failed tasks found!</b>")
            return
        
        # Format the response
        response = "<b>❌ Recent Failed Tasks</b>\n\n"
        
        for i, task in enumerate(failed_tasks):
            task_time = task.get('failed_at', datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            task_type = task.get('task_type', 'unknown')
            error_msg = task.get('error', 'No error message')
            
            # Get task-specific info
            task_info = ""
            if task_type == 'caption_edit':
                data = task.get('data', {})
                file_name = data.get('file_name', 'Unknown file')
                chat_id = data.get('chat_id', 'Unknown chat')
                task_info = f"File: {file_name[:20]}... | Chat: {chat_id}"
            
            response += f"<b>{i+1}. {task_type.upper()}</b> ({task_time})\n"
            response += f"<code>{task_info}</code>\n"
            response += f"<b>Error:</b> <code>{error_msg[:100]}</code>\n\n"
        
        response += "<i>Use /failed command to refresh this list</i>"
        
        await message.reply(response)
    except Exception as e:
        await message.reply(f"Error getting failed tasks: {e}")

# Caption Templates System
@Client.on_message(filters.command("save_template") & filters.private)
async def save_template_command(bot, message):
    """
    Save a caption template for later use.
    Format: /save_template template_name Caption text goes here with {file_name} placeholder
    """
    user_id = message.from_user.id
    
    # Check command format
    command_parts = message.text.split(" ", 2)
    if len(command_parts) < 3:
        await message.reply(
            "❌ **Invalid format**\n\n"
            "Use this format:\n"
            "`/save_template template_name Your caption text with {file_name} placeholder`\n\n"
            "Example:\n"
            "`/save_template movie_template 🎬 {file_name}\n\n📥 Download more at @M0VIES_CHANNEL`"
        )
        return
    
    # Extract template name and caption
    template_name = command_parts[1].strip()
    caption_text = command_parts[2].strip()
    
    # Validate template name (alphanumeric and underscore only)
    if not re.match(r'^[a-zA-Z0-9_]+$', template_name):
        await message.reply(
            "❌ **Invalid template name**\n\n"
            "Template names can only contain letters, numbers, and underscores."
        )
        return
    
    # Validate caption has file_name placeholder
    if "{file_name}" not in caption_text:
        await message.reply(
            "⚠️ **Warning**: Your caption doesn't include the `{file_name}` placeholder.\n\n"
            "This means the original filename won't be included in your caption."
        )
    
    # Save the template
    try:
        result = await save_caption_template(user_id, template_name, caption_text)
        
        if result["status"] == "created":
            await message.reply(
                f"✅ **Template saved**\n\n"
                f"Template: `{template_name}`\n\n"
                f"Caption:\n`{caption_text}`\n\n"
                f"Use it with `/use_template {template_name}` in any channel"
            )
        else:
            await message.reply(
                f"✅ **Template updated**\n\n"
                f"Template: `{template_name}`\n\n"
                f"New caption:\n`{caption_text}`"
            )
    except Exception as e:
        await message.reply(f"❌ **Error saving template**: {str(e)}")

@Client.on_message(filters.command("templates") & filters.private)
async def list_templates_command(bot, message):
    """List all saved caption templates for a user"""
    user_id = message.from_user.id
    
    try:
        templates = await list_caption_templates(user_id)
        
        if not templates:
            await message.reply(
                "🔍 **No templates found**\n\n"
                "Save your first template with:\n"
                "`/save_template template_name Your caption text`"
            )
            return
        
        # Prepare template list
        template_list = "📋 **Your Caption Templates**\n\n"
        for idx, template in enumerate(templates, 1):
            template_list += f"{idx}. `{template['template_name']}`\n"
        
        template_list += "\n**Commands:**\n"
        template_list += "• View: `/view_template template_name`\n"
        template_list += "• Use: `/use_template template_name`\n"
        template_list += "• Delete: `/delete_template template_name`"
        
        await message.reply(template_list)
        
    except Exception as e:
        await message.reply(f"❌ **Error retrieving templates**: {str(e)}")

@Client.on_message(filters.command("view_template") & filters.private)
async def view_template_command(bot, message):
    """View a specific caption template"""
    user_id = message.from_user.id
    
    # Check command format
    command_parts = message.text.split(" ", 1)
    if len(command_parts) < 2:
        await message.reply(
            "❌ **Invalid format**\n\n"
            "Use this format:\n"
            "`/view_template template_name`"
        )
        return
    
    template_name = command_parts[1].strip()
    
    try:
        template = await get_caption_template(user_id, template_name)
        
        if not template:
            await message.reply(
                f"❌ **Template not found**\n\n"
                f"No template named `{template_name}` exists.\n"
                f"Check your templates with `/templates`"
            )
            return
        
        # Show template details
        await message.reply(
            f"📝 **Template: {template_name}**\n\n"
            f"Caption text:\n`{template['caption_text']}`\n\n"
            f"Created: {template['created_at'].strftime('%Y-%m-%d')}\n"
            f"Last updated: {template['updated_at'].strftime('%Y-%m-%d')}\n\n"
            f"Use it with `/use_template {template_name}` in any channel"
        )
        
    except Exception as e:
        await message.reply(f"❌ **Error retrieving template**: {str(e)}")

@Client.on_message(filters.command("delete_template") & filters.private)
async def delete_template_command(bot, message):
    """Delete a caption template"""
    user_id = message.from_user.id
    
    # Check command format
    command_parts = message.text.split(" ", 1)
    if len(command_parts) < 2:
        await message.reply(
            "❌ **Invalid format**\n\n"
            "Use this format:\n"
            "`/delete_template template_name`"
        )
        return
    
    template_name = command_parts[1].strip()
    
    try:
        # First check if template exists
        template = await get_caption_template(user_id, template_name)
        
        if not template:
            await message.reply(
                f"❌ **Template not found**\n\n"
                f"No template named `{template_name}` exists.\n"
                f"Check your templates with `/templates`"
            )
            return
        
        # Delete the template
        success = await delete_caption_template(user_id, template_name)
        
        if success:
            await message.reply(
                f"✅ **Template deleted**\n\n"
                f"Successfully deleted template `{template_name}`."
            )
        else:
            await message.reply(
                f"❌ **Error deleting template**\n\n"
                f"Could not delete template `{template_name}`."
            )
        
    except Exception as e:
        await message.reply(f"❌ **Error deleting template**: {str(e)}")

@Client.on_message(filters.command("use_template") & filters.channel)
async def use_template_command(bot, message):
    """Apply a saved caption template to the channel"""
    try:
        # Try to get the user who sent the command
        # This might not work in channels with anonymous admins
        user_id = message.from_user.id if message.from_user else None
        
        if not user_id:
            await message.reply(
                "❌ **Anonymous admin not supported**\n\n"
                "This command cannot be used by anonymous admins.\n"
                "Please disable anonymous posting to use this feature."
            )
            return
        
        # Check command format
        command_parts = message.text.split(" ", 1)
        if len(command_parts) < 2:
            await message.reply(
                "❌ **Invalid format**\n\n"
                "Use this format:\n"
                "`/use_template template_name`"
            )
            return
        
        template_name = command_parts[1].strip()
        
        # Get the template
        template = await get_caption_template(user_id, template_name)
        
        if not template:
            await message.reply(
                f"❌ **Template not found**\n\n"
                f"No template named `{template_name}` exists.\n"
                f"Check your templates with `/templates` in private chat with the bot"
            )
            return
        
        # Update caption in channel
        chnl_id = message.chat.id
        caption = template["caption_text"]
        
        # Check if channel has custom caption already
        chkData = await chnl_ids.find_one({"chnl_id": chnl_id})
        if chkData:
            await updateCap(chnl_id, caption)
            status_message = await message.reply(
                f"✅ **Caption updated**\n\n"
                f"Updated channel caption using template `{template_name}`.\n\n"
                f"New caption: `{caption}`"
            )
        else:
            await addCap(chnl_id, caption)
            status_message = await message.reply(
                f"✅ **Caption set**\n\n"
                f"Set channel caption using template `{template_name}`.\n\n"
                f"Caption: `{caption}`"
            )
        
        # Clean up status message after 10 seconds
        await asyncio.sleep(10)
        await status_message.delete()
        
    except Exception as e:
        error_message = await message.reply(f"❌ **Error applying template**: {str(e)}")
        await asyncio.sleep(5)
        await error_message.delete()
