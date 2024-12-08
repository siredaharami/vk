import requests
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

# Function to create a paste on Carbonara and get the image URL
def create_carbonara_paste(text: str) -> str:
    url = "https://carbonara.solopov.dev/api/cook"
    payload = {
        "code": text,
        "theme": "seti",  # You can change this theme to other available options
        "lang": "text",
        "font": "Fira Code",  # You can use other fonts available
        "width": 1000,  # Customize the width if needed
        "height": 700,  # Customize the height if needed
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json().get("url")  # Get the URL of the generated image
    else:
        return "Error creating paste."

# Command to show help (list of available plugins with Carbonara link)
@app.on_message(filters.command("help"))
async def help(client: Client, message: Message):
    if plugin_details:
        # Custom help text
        help_text = f"""
📚 Help Menu 📚
Below is a list of all available plugins you can use. There are a total of {len(plugin_details)} plugins.
Use `/plugin_details <plugin_number>` to learn more about a specific plugin.

"""
        # Generate plugin rows dynamically
        plugin_list = list(plugin_details.keys())
        rows = [plugin_list[i:i + 10] for i in range(0, len(plugin_list), 10)]

        plugin_number_map = {}  # Map plugin number to name
        plugin_count = 1

        for idx, row in enumerate(rows, start=1):
            help_text += f"\n🛠️ Plugins Row {idx}:\n"
            for plugin in row:
                help_text += f"{plugin_count}. 🔧 {plugin}\n"
                plugin_number_map[plugin_count] = plugin
                plugin_count += 1

        # Save the plugin number map globally
        global plugin_number_map_global
        plugin_number_map_global = plugin_number_map

        # Create Carbonara paste
        carbonara_url = create_carbonara_paste(help_text.strip())
        if "Error" in carbonara_url:
            await message.reply(carbonara_url)
        else:
            await message.reply(f"Here is the Help Menu: {carbonara_url}")
    else:
        await message.reply("No plugins added yet.")

# Command to show plugin details by number
@app.on_message(filters.command("plugin_details"))
async def plugin_details_command(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please provide the plugin number.")
        return
    
    try:
        plugin_number = int(message.command[1])  # Get the plugin number
    except ValueError:
        await message.reply("Invalid plugin number. Please provide a valid number.")
        return
    
    if plugin_number_map_global.get(plugin_number):
        plugin_name = plugin_number_map_global[plugin_number]
        await message.reply(plugin_details[plugin_name])
    else:
        await message.reply(f"No details found for plugin number '{plugin_number}'.")

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
