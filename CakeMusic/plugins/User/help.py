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
        # Custom help text
        help_text = """
📚 **Help Menu** 📚
Below is a list of all available plugins you can use. Each row contains up to 10 plugins.
Use `/plugin_details <plugin_name>` to learn more about a specific plugin.

"""
        # Generate plugin rows dynamically
        plugin_list = list(plugin_details.keys())
        rows = [plugin_list[i:i + 10] for i in range(0, len(plugin_list), 10)]

        for idx, row in enumerate(rows, start=1):
            help_text += f"\n🛠️ **Plugins Row {idx}:**\n"
            for plugin in row:
                help_text += f"🔧 {plugin}\n"

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

# Example plugins added using the @plugin decorator
@app.on_message(filters.command("example"))
@plugin(
    name="example",
    description="""
**Example Plugin**
- **Command**: /example
- **Description**: This is an example plugin.
- **Usage**: Type /example to see the plugin in action.
"""
)
async def example(client: Client, message: Message):
    await message.reply("Example plugin is active!")
