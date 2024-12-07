from CakeMusic import bot, API_ID, API_HASH
from pyrogram import filters, Client, idle
from pyrogram.types import Message
import os

@bot.on_message(filters.command("clone"))
async def clone(bot: Client, msg: Message):
    """
    Clone command: Clone a Pyrogram session using a provided string session
    and load plugins for the cloned session.
    """
    if len(msg.command) < 2:
        await msg.reply("Usage: `/clone <string_session>`\nSend your Pyrogram2 string session to clone. ❤️")
        return
    
    string_session = msg.command[1]
    
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
