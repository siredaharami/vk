from pyrogram import Client, filters
from pyrogram.types import Message
from CakeMusic import app

# Dictionary to store plugin details automatically
plugin_details = {}

# Register plugin details in a global dictionary
def register_plugin(plugin_name, plugin_description):
    plugin_details[plugin_name] = plugin_description

# Command to show help (list of available plugins)
@app.on_message(filters.command("help"))
async def help(client: Client, message: Message):
    if plugin_details:
        help_text = "Available Plugins:\n\n"
        
        # Add emojis and plugins in two rows
        plugin_list = list(plugin_details.keys())
        row_1 = plugin_list[:5]
        row_2 = plugin_list[5:10]

        # First row of plugins with emojis
        help_text += "🛠️ Plugins Row 1:\n"
        for plugin in row_1:
            help_text += f"🔧 {plugin}\n"
        
        # Second row of plugins with emojis
        help_text += "\n🛠️ Plugins Row 2:\n"
        for plugin in row_2:
            help_text += f"🔨 {plugin}\n"

        # Add photo if you have one
        photo_url = "https://files.catbox.moe/xwygzj.jpg"  # Replace with your actual photo URL
        await message.reply_photo(photo_url, caption=help_text)
    else:
        await message.reply("No plugins added yet.")

# Command to show plugin details by name
@app.on_message(filters.command("plugin_details"))
async def plugin_details_command(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please provide the plugin name.")
        return
    
    plugin_name = message.command[1]
    
    if plugin_name in plugin_details:
        await message.reply(plugin_details[plugin_name])
    else:
        await message.reply(f"No details found for plugin '{plugin_name}'.")

# Example of the Ping plugin
@app.on_message(filters.command("ping"))
async def ping(client: Client, message: Message):
    plugin_name = "ping"
    plugin_description = """
    **Ping Plugin**
    - **Command**: /ping
    - **Description**: This plugin responds with 'Pong!' to check if the bot is alive.
    - **Usage**: Type /ping to check if the bot is responsive.
    """
    register_plugin(plugin_name, plugin_description)
    
    await message.reply("Ping plugin is active!")

# Example of the Song plugin
@app.on_message(filters.command("song"))
async def song(client: Client, message: Message):
    plugin_name = "song"
    plugin_description = """
    **Song Plugin**
    - **Command**: /song <song_name>
    - **Description**: This plugin allows you to search and play songs.
    - **Usage**: Type /song <song_name> to search for a song.
    """
    register_plugin(plugin_name, plugin_description)
    
    await message.reply("Song plugin is active!")

# Example of the Admin plugin
@app.on_message(filters.command("admin"))
async def admin(client: Client, message: Message):
    plugin_name = "admin"
    plugin_description = """
    **Admin Plugin**
    - **Command**: /admin
    - **Description**: This plugin gives admin-like controls, such as banning users or setting permissions.
    - **Usage**: Type /admin to access admin commands.
    """
    register_plugin(plugin_name, plugin_description)
    
    await message.reply("Admin plugin is active!")
    
