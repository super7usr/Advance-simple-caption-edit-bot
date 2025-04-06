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
    add_pending_task, get_pending_tasks, mark_task_completed, mark_task_failed
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
    await insert(user_id)
    
    # More attractive start message with emojis and better formatting
    start_text = f"""
<b>🤖 Welcome {message.from_user.mention}!</b>

I'm an <b>Advanced Auto-Caption Bot</b> that enhances your channel media with custom captions.

<b>✨ Features:</b>
• 🎬 Automatically add captions to videos
• 🎵 Caption audio files beautifully
• 📄 Format document captions professionally
• 🔄 Process tasks even when offline
• 🔒 Ultra-reliable 24/7 operation

<b>⚙️ Commands:</b>
• <code>/set_caption</code> - Set your custom caption
• <code>/delcaption</code> - Reset to default caption
• <code>/users</code> - Admin only: check user stats
• <code>/broadcast</code> - Admin only: send mass message

<b>💡 Pro Tip:</b> Use <code>{{file_name}}</code> in your caption to include the original filename.

<b>Note:</b> All caption commands work in channels only.
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
    
    await message.reply_photo(
        photo=Bots.BOT_PIC,
        caption=start_text,
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
                cap_dets = await chnl_ids.find_one({"chnl_id": chnl_id})
                try:
                    if cap_dets:
                        cap = cap_dets["caption"]
                        replaced_caption = cap.format(file_name=file_name)
                        await message.edit(replaced_caption)
                    else:
                        replaced_caption = Bots.DEF_CAP.format(file_name=file_name)
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
    await auto_edit_caption(bot, message)

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
  
• <code>/delcaption</code> - Reset to default caption
  Alternatively, use <code>/del_caption</code> or <code>/delete_caption</code>

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
• 🔄 Process tasks even when offline
• 🔒 Ultra-reliable 24/7 operation

<b>⚙️ Commands:</b>
• <code>/set_caption</code> - Set your custom caption
• <code>/delcaption</code> - Reset to default caption
• <code>/users</code> - Admin only: check user stats
• <code>/broadcast</code> - Admin only: send mass message

<b>💡 Pro Tip:</b> Use <code>{{file_name}}</code> in your caption to include the original filename.

<b>Note:</b> All caption commands work in channels only.
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
        # Get tasks counts directly
        pending_count = await bot.db.pending_tasks.count_documents({"status": "pending"})
        completed_count = await bot.db.pending_tasks.count_documents({"status": "completed"})
        failed_count = await bot.db.pending_tasks.count_documents({"status": "failed"})
        total_count = pending_count + completed_count + failed_count
        
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
