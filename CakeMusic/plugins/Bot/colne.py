from CakeMusic import bot, API_ID, API_HASH
from pyrogram import filters, Client
from pyrogram.types import Message

@bot.on_message(filters.command("clone"))
async def clone(bot: Client, msg: Message):
    """
    Clone command: Clone a Pyrogram session using a provided string session.
    """
    if len(msg.command) < 2:
        await msg.reply("Usage: `/clone <string_session>`\nSend your Pyrogram2 string session to clone. ❤️")
        return
    
    string_session = msg.command[1]
    chat = msg.chat
    
    try:
        reply_msg = await msg.reply("Please wait... Setting up the session. 💌")
        
        # Initialize the client with the provided session string
        client = Client(
            name="ClonedClient",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string_session,
            plugins=dict(root="CakeMusic/plugins")
        )
        
        # Start the client and fetch user details
        await client.start()
        user = await client.get_me()
        
        # Reply with success message
        success_msg = (
            f"🎉 Successfully cloned the session!\n\n"
            f"👤 **User:** {user.first_name}\n"
            f"🆔 **User ID:** {user.id}\n\n"
            f"Enjoy using your cloned session. 💕"
        )
        await reply_msg.edit(success_msg)
    except Exception as e:
        error_msg = f"❌ **ERROR:** `{str(e)}`\nPlease check your session string or try again."
        await msg.reply(error_msg)

    finally:
        if client.is_connected:
            await client.stop()
