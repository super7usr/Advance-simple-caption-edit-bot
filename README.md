# Telegram Caption Bot

This is a Telegram bot based on the [super7usr/caption](https://github.com/super7usr/caption) repository. The bot automatically adds captions to media files (photos, videos, documents) sent in Telegram channels.

## Features

- Automatically adds captions to media in your Telegram channels
- Supports customizing caption text with variables like `{file_name}`
- Force subscription feature to ensure users subscribe to your channel
- Admin broadcast capabilities to send messages to all bot users
- Ultra-reliable 24/7 uptime with multi-layer keep-alive mechanism
- Self-healing design with automatic recovery from crashes

## Configuration

The bot requires the following environment variables (already configured):

- `API_ID` and `API_HASH`: Telegram API credentials
- `BOT_TOKEN`: Your Telegram bot token
- `FORCE_SUB`: Username of the channel users must subscribe to
- `DB_URL`: MongoDB connection string
- `ADMIN`: Telegram user ID of the bot admin

## Usage Instructions

### Basic Commands

1. `/start` - Start the bot and see basic information
2. `/set_caption` - Set a custom caption for your media files
3. `/del_caption` - Delete your custom caption 
4. `/see_caption` - View your current caption

### For Admins

1. `/users` - See the number of users who have used the bot
2. `/broadcast` - Send a message to all users
3. `/restart` - Restart the bot

### Adding Captions to Media

1. Add the bot as an administrator to your Telegram channel
2. Ensure the bot has permission to post messages
3. When media is posted in the channel, the bot will automatically add the configured caption

### Custom Caption Variables

You can use the following variables in your custom caption:
- `{file_name}` - Original filename of the media
- `{file_size}` - Size of the file
- `{duration}` - Duration (for videos and audio)

## Implementation Details

This bot runs on Replit with an enhanced 24/7 uptime mechanism that:

1. **Watchdog System**: Monitors the main process and restarts it if it crashes
2. **Telegram Bot**: Processes messages and manages caption functionality
3. **Web Server**: Provides an HTTP endpoint for keep-alive pings
4. **Adaptive Keep-Alive**: Self-pinging system with fallback mechanisms and adaptive timing
5. **Automatic Refresh**: Implements a 24-hour restart cycle to prevent memory leaks
6. **Task Queue System**: Stores tasks when the bot is offline and processes them upon restart

For detailed documentation on the reliability implementation, see the [KEEP_ALIVE.md](KEEP_ALIVE.md) file.
For details on the enhanced reliability features, see the [ENHANCED_RELIABILITY.md](ENHANCED_RELIABILITY.md) file.

## Task Queue System

The bot implements a resilient task queue system that ensures no messages are lost even if the bot goes offline temporarily:

### How It Works

1. When the bot receives a message but cannot process it immediately (e.g., during restart), it's stored in MongoDB
2. When the bot restarts, it automatically processes any pending tasks in the queue
3. The task queue maintains three statuses for tasks: `pending`, `completed`, and `failed`
4. The system includes detailed logging and error handling to track task processing

### Task Queue Utilities

Several utility scripts are provided to manage and monitor the task queue:

1. **process_tasks_manually.py**: Process pending tasks manually with various options
   ```
   # Process all pending tasks
   python process_tasks_manually.py
   
   # Display detailed task statistics
   python process_tasks_manually.py --stats
   
   # Retry failed tasks
   python process_tasks_manually.py --reset-failed
   
   # Clean up old completed tasks
   python process_tasks_manually.py --clean
   ```

2. **task_queue_utility.py**: Provides various task queue management functions
   ```
   # Check current task queue status
   python task_queue_utility.py check
   
   # Add a test task to the queue
   python task_queue_utility.py add-test
   
   # Retry failed tasks
   python task_queue_utility.py retry-failed
   
   # Clean up old completed tasks
   python task_queue_utility.py clean
   ```

3. **force_task_processing.py**: Force process all pending tasks without waiting for the bot
   ```
   python force_task_processing.py
   ```

### Admin Commands for Task Queue

Admins can use the following bot commands to manage the task queue:

1. `/queue_status` - Display the current status of the task queue
2. `/show_failed_tasks` - List recent failed tasks with their error messages

## Troubleshooting

If the bot stops responding:

1. Check the Replit logs for any watchdog or error messages
2. The system should automatically recover within 2-5 minutes in most cases
3. If automatic recovery fails, restart the bot using the Replit "Run" button
4. Verify your MongoDB database is operational
5. Ensure all your environment variables and Telegram credentials are valid

### Task Queue Troubleshooting

If tasks are not being processed:

1. Check the task queue status: `python task_queue_utility.py check`
2. Manually process pending tasks: `python process_tasks_manually.py`
3. Check for database connectivity issues
4. Restart the bot system: `python fix_task_processing.py`
5. View detailed logs: `cat task_processor.log` (if available)

For deployment information, see the [DEPLOYMENT.md](DEPLOYMENT.md) file.

## System Architecture

```
┌─────────────────┐         ┌─────────────────┐
│    watchdog.py  │ monitors │     main.py     │
│ (Process Monitor)├────────→│  (Bot Launcher) │
└─────────────────┘         └────────┬────────┘
                                     │ starts
                                     ▼
┌─────────────────┐         ┌─────────────────┐
│   keep_alive.py │ pings   │     bot.py      │
│ (Uptime Service)│◄────────┤  (Telegram Bot) │
└─────────────────┘         └─────────────────┘
```

For further assistance, contact the repository maintainer or open an issue on GitHub.
