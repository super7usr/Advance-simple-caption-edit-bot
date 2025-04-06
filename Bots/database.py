# (c) @renish_rgi
# Developer ❁✗❍═❰ 🆁︎🅴︎🅽︎🅸︎🆂︎🅷︎ ❱═❍✗❁ 
# Don't Remove Credit 😔
# Telegram Channel @M0VIES_CHANNEL
# Developer @renish_rgi

import motor.motor_asyncio
from config import Bots
import datetime

client = motor.motor_asyncio.AsyncIOMotorClient(Bots.DB_URL)
db = client[Bots.DB_NAME]
chnl_ids = db.chnl_ids
users = db.users
pending_tasks = db.pending_tasks

#insert user data
async def insert(user_id):
    user_det = {"_id": user_id}
    try:
        await users.insert_one(user_det)
    except:
        pass
        
# Total User
async def total_user():
    user = await users.count_documents({})
    return user

async def getid():
    all_users = users.find({})
    return all_users

async def delete(id):
    await users.delete_one(id)
                     
async def addCap(chnl_id, caption):
    dets = {"chnl_id": chnl_id, "caption": caption}
    await chnl_ids.insert_one(dets)

async def updateCap(chnl_id, caption):
    await chnl_ids.update_one({"chnl_id": chnl_id}, {"$set": {"caption": caption}})

# Task Queue System
async def add_pending_task(task_type, data):
    """
    Add a task to the pending queue when the bot is offline.
    
    Parameters:
    task_type: str - Type of task (e.g., 'caption_edit', 'broadcast', etc.)
    data: dict - Task-specific data (e.g., message_id, chat_id, etc.)
    """
    task = {
        "task_type": task_type,
        "data": data,
        "timestamp": datetime.datetime.utcnow(),
        "status": "pending"
    }
    await pending_tasks.insert_one(task)
    return task

async def get_pending_tasks(limit=50):
    """Get a list of pending tasks ordered by timestamp (oldest first)"""
    cursor = pending_tasks.find({"status": "pending"}).sort("timestamp", 1).limit(limit)
    return await cursor.to_list(length=limit)

async def mark_task_completed(task_id):
    """Mark a task as completed after processing"""
    await pending_tasks.update_one(
        {"_id": task_id},
        {"$set": {"status": "completed", "completed_at": datetime.datetime.utcnow()}}
    )

async def mark_task_failed(task_id, error_message):
    """Mark a task as failed with the error message"""
    await pending_tasks.update_one(
        {"_id": task_id},
        {"$set": {
            "status": "failed", 
            "error": error_message,
            "failed_at": datetime.datetime.utcnow()
        }}
    )

async def get_task_stats():
    """Get statistics about pending, completed, and failed tasks"""
    pending_count = await pending_tasks.count_documents({"status": "pending"})
    completed_count = await pending_tasks.count_documents({"status": "completed"})
    failed_count = await pending_tasks.count_documents({"status": "failed"})
    return {
        "pending": pending_count,
        "completed": completed_count,
        "failed": failed_count,
        "total": pending_count + completed_count + failed_count
    }
    
async def get_recent_failed_tasks(limit=5):
    """Get most recent failed tasks with their error messages"""
    cursor = pending_tasks.find(
        {"status": "failed"}, 
        {"data": 1, "task_type": 1, "error": 1, "failed_at": 1}
    ).sort("failed_at", -1).limit(limit)
    
    tasks = []
    async for task in cursor:
        tasks.append(task)
    return tasks
    
async def clear_completed_tasks():
    """Clear all completed tasks from the database (keep the most recent 100)"""
    # First keep the most recent 100 completed tasks
    cursor = pending_tasks.find({"status": "completed"}).sort("updated_at", -1).limit(100)
    keep_ids = []
    async for task in cursor:
        keep_ids.append(task["_id"])
    
    # Delete all other completed tasks
    if keep_ids:
        await pending_tasks.delete_many({
            "status": "completed",
            "_id": {"$nin": keep_ids}
        })
    else:
        await pending_tasks.delete_many({"status": "completed"})
    
    # Return how many were deleted
    return await pending_tasks.count_documents({"status": "completed"})

# Developer ❁✗❍═❰ 🆁︎🅴︎🅽︎🅸︎🆂︎🅷︎ ❱═❍✗❁ 
# Don't Remove Credit 😔
# Telegram Channel @M0VIES_CHANNEL
# Developer @renish_rgi
