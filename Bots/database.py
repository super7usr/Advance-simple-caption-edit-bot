# (c) @renish_rgi
# Developer ❁✗❍═❰ 🆁︎🅴︎🅽︎🅸︎🆂︎🅷︎ ❱═❍✗❁ 
# Don't Remove Credit 😔
# Telegram Channel @M0VIES_CHANNEL
# Developer @renish_rgi

import datetime
import sqlite3
import os
import logging
from config import Bots
import json
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up SQLite database
DB_PATH = "instance/telegram_bot.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Create connection function to ensure thread safety
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

# Initialize database tables
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS channel_captions (
        chnl_id INTEGER PRIMARY KEY,
        caption TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pending_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_type TEXT,
        data TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        failed_at TIMESTAMP,
        error TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS caption_templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        template_name TEXT,
        caption_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, template_name)
    )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized")

# Initialize database
init_db()

# Database access functions with async interface for compatibility

# Insert user data
async def insert(user_id):
    # Simplified version without using asyncio.to_thread
    try:
        # Since SQLite operations are generally fast, we can do this directly
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (user_id,))
        conn.commit()
        logger.info(f"User {user_id} inserted or already exists in database")
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error inserting user {user_id}: {e}")
        return False
        
# Total User
async def total_user():
    # Simplified version without using asyncio.to_thread
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        count = result['count'] if result else 0
        conn.close()
        return count
    except Exception as e:
        logger.error(f"Error getting total users: {e}")
        return 0

# Get all user IDs
async def getid():
    # Simplified version without using asyncio.to_thread
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id as _id FROM users")
        # Convert to a list of dicts to match MongoDB interface
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        # Return results directly (we'll handle this better in Python 3.12)
        for row in result:
            yield row
    except Exception as e:
        logger.error(f"Error getting user IDs: {e}")
        yield []

# Delete a user
async def delete(id_dict):
    def _delete():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            user_id = id_dict.get('_id')
            if user_id:
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
        finally:
            conn.close()
    
    await asyncio.to_thread(_delete)
                     
# Add a caption for a channel
async def addCap(chnl_id, caption):
    def _addCap():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO channel_captions (chnl_id, caption) VALUES (?, ?)",
                (chnl_id, caption)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Error adding caption: {e}")
        finally:
            conn.close()
    
    await asyncio.to_thread(_addCap)

async def updateCap(chnl_id, caption):
    def _updateCap():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE channel_captions SET caption = ? WHERE chnl_id = ?",
                (caption, chnl_id)
            )
            if cursor.rowcount == 0:
                # If no rows were updated, the channel wasn't found, so insert it
                cursor.execute(
                    "INSERT INTO channel_captions (chnl_id, caption) VALUES (?, ?)",
                    (chnl_id, caption)
                )
            conn.commit()
        except Exception as e:
            logger.error(f"Error updating caption: {e}")
        finally:
            conn.close()
    
    await asyncio.to_thread(_updateCap)

# Create a class to represent a MongoDB collection for compatibility
class Collection:
    def __init__(self, table_name):
        self.table_name = table_name

    # Helper to access collection from other code
    @property
    def find_one(self):
        if self.table_name == "channel_captions":
            return self.channel_caption_find_one
        elif self.table_name == "caption_templates":
            return self.caption_template_find_one
        else:
            # Default handler
            async def default_find_one(query):
                logger.warning(f"Unimplemented find_one for {self.table_name}: {query}")
                return None
            return default_find_one
    
    async def delete_one(self, query):
        """Delete a document based on query"""
        if self.table_name == "channel_captions":
            try:
                conn = get_connection()
                cursor = conn.cursor()
                chnl_id = query.get("chnl_id")
                if chnl_id:
                    cursor.execute("DELETE FROM channel_captions WHERE chnl_id = ?", (chnl_id,))
                    conn.commit()
                    logger.info(f"Deleted channel caption for channel {chnl_id}")
                    return True
                conn.close()
            except Exception as e:
                logger.error(f"Error deleting from {self.table_name}: {e}")
                return False
        else:
            logger.warning(f"Unimplemented delete_one for {self.table_name}: {query}")
            return False
            
    async def channel_caption_find_one(self, query):
        def _find_one():
            conn = get_connection()
            cursor = conn.cursor()
            try:
                chnl_id = query.get("chnl_id")
                cursor.execute(
                    "SELECT chnl_id, caption FROM channel_captions WHERE chnl_id = ?",
                    (chnl_id,)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
            finally:
                conn.close()
        
        return await asyncio.to_thread(_find_one)
        
    async def caption_template_find_one(self, query):
        def _find_one():
            conn = get_connection()
            cursor = conn.cursor()
            try:
                user_id = query.get("user_id")
                template_name = query.get("template_name")
                cursor.execute(
                    """
                    SELECT id as _id, user_id, template_name, caption_text, 
                           created_at, updated_at 
                    FROM caption_templates 
                    WHERE user_id = ? AND template_name = ?
                    """,
                    (user_id, template_name)
                )
                row = cursor.fetchone()
                if row:
                    result = dict(row)
                    # Convert string timestamps to datetime objects
                    for key in ['created_at', 'updated_at']:
                        if key in result and result[key]:
                            try:
                                result[key] = datetime.datetime.fromisoformat(result[key])
                            except (ValueError, TypeError):
                                pass
                    return result
                return None
            finally:
                conn.close()
        
        return await asyncio.to_thread(_find_one)
        
# Create collections for compatibility
chnl_ids = Collection("channel_captions")
caption_templates = Collection("caption_templates")

# Task Queue System
async def add_pending_task(task_type, data):
    """
    Add a task to the pending queue when the bot is offline.
    
    Parameters:
    task_type: str - Type of task (e.g., 'caption_edit', 'broadcast', etc.)
    data: dict - Task-specific data (e.g., message_id, chat_id, etc.)
    """
    def _add_task():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            data_json = json.dumps(data)
            now = datetime.datetime.utcnow().isoformat()
            cursor.execute(
                """
                INSERT INTO pending_tasks (task_type, data, status, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (task_type, data_json, "pending", now)
            )
            conn.commit()
            task_id = cursor.lastrowid
            
            # Return the task for compatibility
            return {
                "_id": task_id,
                "task_type": task_type,
                "data": data,
                "timestamp": now,
                "status": "pending"
            }
        except Exception as e:
            logger.error(f"Error adding pending task: {e}")
            return None
        finally:
            conn.close()
    
    return await asyncio.to_thread(_add_task)

async def get_pending_tasks(limit=50):
    """Get a list of pending tasks ordered by timestamp (oldest first)"""
    def _get_tasks():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT id as _id, task_type, data, status, created_at as timestamp,
                       completed_at, failed_at, error
                FROM pending_tasks
                WHERE status = 'pending'
                ORDER BY created_at ASC
                LIMIT ?
                """,
                (limit,)
            )
            tasks = []
            for row in cursor.fetchall():
                task = dict(row)
                # Parse the JSON data
                if task.get('data'):
                    try:
                        task['data'] = json.loads(task['data'])
                    except:
                        task['data'] = {}
                tasks.append(task)
            return tasks
        finally:
            conn.close()
    
    return await asyncio.to_thread(_get_tasks)

async def mark_task_completed(task_id):
    """Mark a task as completed after processing"""
    def _mark_completed():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            now = datetime.datetime.utcnow().isoformat()
            cursor.execute(
                """
                UPDATE pending_tasks
                SET status = 'completed', completed_at = ?
                WHERE id = ?
                """,
                (now, task_id)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Error marking task completed: {e}")
        finally:
            conn.close()
    
    await asyncio.to_thread(_mark_completed)

async def mark_task_failed(task_id, error_message):
    """Mark a task as failed with the error message"""
    def _mark_failed():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            now = datetime.datetime.utcnow().isoformat()
            cursor.execute(
                """
                UPDATE pending_tasks
                SET status = 'failed', failed_at = ?, error = ?
                WHERE id = ?
                """,
                (now, error_message, task_id)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Error marking task failed: {e}")
        finally:
            conn.close()
    
    await asyncio.to_thread(_mark_failed)

async def get_task_stats():
    """Get statistics about pending, completed, and failed tasks"""
    def _get_stats():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Count pending tasks
            cursor.execute("SELECT COUNT(*) as count FROM pending_tasks WHERE status = 'pending'")
            pending_count = cursor.fetchone()['count']
            
            # Count completed tasks
            cursor.execute("SELECT COUNT(*) as count FROM pending_tasks WHERE status = 'completed'")
            completed_count = cursor.fetchone()['count']
            
            # Count failed tasks
            cursor.execute("SELECT COUNT(*) as count FROM pending_tasks WHERE status = 'failed'")
            failed_count = cursor.fetchone()['count']
            
            return {
                "pending": pending_count,
                "completed": completed_count,
                "failed": failed_count,
                "total": pending_count + completed_count + failed_count
            }
        finally:
            conn.close()
    
    return await asyncio.to_thread(_get_stats)
    
async def get_recent_failed_tasks(limit=5):
    """Get most recent failed tasks with their error messages"""
    def _get_failed_tasks():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT id as _id, task_type, data, error, failed_at
                FROM pending_tasks
                WHERE status = 'failed'
                ORDER BY failed_at DESC
                LIMIT ?
                """,
                (limit,)
            )
            tasks = []
            for row in cursor.fetchall():
                task = dict(row)
                # Parse the JSON data
                if task.get('data'):
                    try:
                        task['data'] = json.loads(task['data'])
                    except:
                        task['data'] = {}
                tasks.append(task)
            return tasks
        finally:
            conn.close()
    
    return await asyncio.to_thread(_get_failed_tasks)
    
async def clear_completed_tasks():
    """Clear all completed tasks from the database (keep the most recent 100)"""
    def _clear_tasks():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Get IDs of most recent 100 completed tasks
            cursor.execute(
                """
                SELECT id FROM pending_tasks
                WHERE status = 'completed'
                ORDER BY completed_at DESC
                LIMIT 100
                """
            )
            keep_ids = [row['id'] for row in cursor.fetchall()]
            
            # Delete all other completed tasks
            if keep_ids:
                # SQLite doesn't support NOT IN with a large number of values
                # So we use a different approach - delete tasks with IDs less than the minimum keep_id
                min_keep_id = min(keep_ids)
                cursor.execute(
                    """
                    DELETE FROM pending_tasks
                    WHERE status = 'completed' AND id NOT IN ({})
                    """.format(','.join('?' for _ in keep_ids)),
                    keep_ids
                )
            else:
                cursor.execute("DELETE FROM pending_tasks WHERE status = 'completed'")
            
            conn.commit()
            
            # Count remaining completed tasks
            cursor.execute("SELECT COUNT(*) as count FROM pending_tasks WHERE status = 'completed'")
            return cursor.fetchone()['count']
        finally:
            conn.close()
    
    return await asyncio.to_thread(_clear_tasks)

# Caption Template System
async def save_caption_template(user_id, template_name, caption_text):
    """
    Save a caption template for a user.
    
    Parameters:
    user_id: int - The Telegram user ID
    template_name: str - Name for the template
    caption_text: str - The caption template text
    """
    def _save_template():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            now = datetime.datetime.utcnow().isoformat()
            
            # Check if template exists
            cursor.execute(
                """
                SELECT id FROM caption_templates
                WHERE user_id = ? AND template_name = ?
                """,
                (user_id, template_name)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update existing template
                cursor.execute(
                    """
                    UPDATE caption_templates
                    SET caption_text = ?, updated_at = ?
                    WHERE user_id = ? AND template_name = ?
                    """,
                    (caption_text, now, user_id, template_name)
                )
                conn.commit()
                return {
                    "status": "updated",
                    "template": {
                        "user_id": user_id,
                        "template_name": template_name,
                        "caption_text": caption_text,
                        "updated_at": now
                    }
                }
            else:
                # Insert new template
                cursor.execute(
                    """
                    INSERT INTO caption_templates
                    (user_id, template_name, caption_text, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (user_id, template_name, caption_text, now, now)
                )
                conn.commit()
                template_id = cursor.lastrowid
                return {
                    "status": "created",
                    "template": {
                        "_id": template_id,
                        "user_id": user_id,
                        "template_name": template_name,
                        "caption_text": caption_text,
                        "created_at": now,
                        "updated_at": now
                    }
                }
        except Exception as e:
            logger.error(f"Error saving template: {e}")
            return {"status": "error", "error": str(e)}
        finally:
            conn.close()
    
    return await asyncio.to_thread(_save_template)

async def get_caption_template(user_id, template_name):
    """
    Get a specific caption template by name.
    
    Parameters:
    user_id: int - The Telegram user ID
    template_name: str - Name of the template to retrieve
    """
    def _get_template():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT id as _id, user_id, template_name, caption_text,
                       created_at, updated_at
                FROM caption_templates
                WHERE user_id = ? AND template_name = ?
                """,
                (user_id, template_name)
            )
            row = cursor.fetchone()
            if row:
                result = dict(row)
                # Convert string timestamps to datetime objects
                for key in ['created_at', 'updated_at']:
                    if key in result and result[key]:
                        try:
                            result[key] = datetime.datetime.fromisoformat(result[key])
                        except (ValueError, TypeError):
                            pass
                return result
            return None
        finally:
            conn.close()
    
    return await asyncio.to_thread(_get_template)

async def list_caption_templates(user_id):
    """
    List all caption templates for a user.
    
    Parameters:
    user_id: int - The Telegram user ID
    """
    def _list_templates():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT id as _id, user_id, template_name, caption_text,
                       created_at, updated_at
                FROM caption_templates
                WHERE user_id = ?
                ORDER BY template_name
                """,
                (user_id,)
            )
            templates = []
            for row in cursor.fetchall():
                template = dict(row)
                # Convert string timestamps to datetime objects
                for key in ['created_at', 'updated_at']:
                    if key in template and template[key]:
                        try:
                            template[key] = datetime.datetime.fromisoformat(template[key])
                        except (ValueError, TypeError):
                            pass
                templates.append(template)
            return templates
        finally:
            conn.close()
    
    return await asyncio.to_thread(_list_templates)

async def delete_caption_template(user_id, template_name):
    """
    Delete a caption template.
    
    Parameters:
    user_id: int - The Telegram user ID
    template_name: str - Name of the template to delete
    """
    def _delete_template():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                DELETE FROM caption_templates
                WHERE user_id = ? AND template_name = ?
                """,
                (user_id, template_name)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    return await asyncio.to_thread(_delete_template)

# Developer ❁✗❍═❰ 🆁︎🅴︎🅽︎🅸︎🆂︎🅷︎ ❱═❍✗❁ 
# Don't Remove Credit 😔
# Telegram Channel @M0VIES_CHANNEL
# Developer @renish_rgi
