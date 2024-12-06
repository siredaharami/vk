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

# Command to show help (list of available plugins with numbers or details)
@app.on_message(filters.command("help"))
async def help(client: Client, message: Message):
    # Check if a number is provided after the command
    if len(message.command) > 1:
        try:
            plugin_number = int(message.command[1])  # Get the plugin number
        except ValueError:
            await message.reply("Invalid plugin number. Please provide a valid number.")
            return

        # Get the plugin details if the number is valid
        if plugin_number > 0 and plugin_number <= len(plugin_details):
            plugin_name = list(plugin_details.keys())[plugin_number - 1]  # Get plugin by number
            plugin_description = plugin_details[plugin_name]
            formatted_description = f"```python\n{plugin_description}\n```"  # Formatting as Python code block
            await message.reply(formatted_description)
        else:
            await message.reply(f"No details found for plugin number '{plugin_number}'.")
    else:
        # Custom help text in Python code format
        help_text = f"""
📚 **Help Menu** 📚
Below is a list of all available plugins you can use. There are a total of {len(plugin_details)} plugins.
Use `/help <plugin_number>` to learn more about a specific plugin.

```python
"""
        # Generate plugin rows dynamically
        plugin_list = list(plugin_details.keys())
        rows = [plugin_list[i:i + 10] for i in range(0, len(plugin_list), 10)]

        plugin_number_map = {}  # Map plugin number to name
        plugin_count = 1

        for idx, row in enumerate(rows, start=1):
            help_text += f"# Plugins Row {idx}:\n"
            for plugin in row:
                help_text += f"# {plugin_count}. {plugin}\n"
                plugin_number_map[plugin_count] = plugin
                plugin_count += 1

        help_text += "```"

        # Save the plugin number map globally
        global plugin_number_map_global
        plugin_number_map_global = plugin_number_map

        # Add photo if you have one
        photo_url = "https://files.catbox.moe/xwygzj.jpg"  # Replace with your actual photo URL
        await message.reply_photo(photo_url, caption=help_text)

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
