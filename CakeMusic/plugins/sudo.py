from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from CakeMusic import bot

# Store sudo users in a set
sudo_users = {OWNER_ID}  # Start with the owner as the default sudo user

# Add Sudo User Command
@bot.on_message(filters.command("addsudo") & filters.user(OWNER_ID))
async def add_sudo(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /addsudo <user_id>")
        return
    
    try:
        user_id = int(message.command[1])
        sudo_users.add(user_id)
        await message.reply_text(f"User {user_id} added as a sudo user.")
    except ValueError:
        await message.reply_text("Invalid user ID. Please provide a numeric user ID.")

# Remove Sudo User Command
@bot.on_message(filters.command("removesudo") & filters.user(OWNER_ID))
async def remove_sudo(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /removesudo <user_id>")
        return
    
    try:
        user_id = int(message.command[1])
        if user_id == OWNER_ID:
            await message.reply_text("You cannot remove yourself as the owner.")
            return

        if user_id in sudo_users:
            sudo_users.remove(user_id)
            await message.reply_text(f"User {user_id} removed from sudo users.")
        else:
            await message.reply_text("This user is not a sudo user.")
    except ValueError:
        await message.reply_text("Invalid user ID. Please provide a numeric user ID.")

# Sudo List Command
@bot.on_message(filters.command("sudolist"))
async def sudo_list(client: Client, message: Message):
    text = "**Sudo Users List:**\n\n"
    for user_id in sudo_users:
        try:
            user = await client.get_users(user_id)
            text += f"- {user.first_name} (`{user.id}`)\n"
        except Exception:
            text += f"- Unknown User (`{user_id}`)\n"
    
    await message.reply_text(text)
