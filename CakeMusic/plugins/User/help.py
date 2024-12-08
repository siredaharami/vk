from pyrogram import Client, filters
from pyrogram.types import Message
from CakeMusic import app

# Dictionary to store plugin details automatically
plugin_details = {}

# Decorator to register plugins automatically
def plugin(name, description):
    def decorator(func):
        plugin_details[name] = description
        return func
    return decorator

# Command to show help (list of available plugins)
@app.on_message(filters.command("help"))
async def help(client: Client, message: Message):
    if plugin_details:
        help_text = "Available Plugins:\n\n"
        
        # Split plugins into two rows
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
        photo_url = "https://your_image_url_here.com/photo.jpg"  # Replace with your actual photo URL
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

# Add your plugins here using the @plugin decorator
# Example:
# @app.on_message(filters.command("example"))
# @plugin(
#     name="example",
#     description="""
#     **Example Plugin**
#     - **Command**: /example
#     - **Description**: This is an example plugin.
#     - **Usage**: Type /example to see the plugin in action.
#     """
# )
# async def example(client: Client, message: Message):
#     await message.reply("Example plugin is active!")
