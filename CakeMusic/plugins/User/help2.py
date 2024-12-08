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

# Function to create a Carbonara paste
def create_carbonara_paste(text: str) -> str:
    url = "https://carbonara.solopov.dev/api/cook"
    payload = {
        "code": text,
        "theme": "seti",
        "width": 1000,
    }
    try:
        response = requests.post(url, json=payload)
        
        # Debugging response content
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"

        try:
            data = response.json()
        except ValueError:
            return f"Error: Unexpected response format: {response.text[:200]}"

        if "url" in data:
            return data["url"]
        else:
            return "Error: No URL in the response."
    except requests.RequestException as e:
        return f"Error while creating Carbonara paste: {str(e)}"

# Fallback function to create a Hastebin paste
def create_hastebin_paste(text: str) -> str:
    url = "https://hastebin.com/documents"
    try:
        response = requests.post(url, data=text.encode("utf-8"))
        if response.status_code == 200:
            key = response.json().get("key")
            if key:
                return f"https://hastebin.com/{key}.py"
        return f"Error: {response.status_code} - {response.text}"
    except requests.RequestException as e:
        return f"Error while creating Hastebin paste: {str(e)}"

# Command to show help (list of available plugins)
@app.on_message(filters.command("helpp"))
async def help(client: Client, message: Message):
    if plugin_details:
        help_text = f"""
📚 Help Menu 📚
Below is a list of all available plugins you can use. There are a total of {len(plugin_details)} plugins.
Use `/plugin_details <plugin_number>` to learn more about a specific plugin.

"""
        # Generate plugin rows dynamically
        plugin_list = list(plugin_details.keys())
        rows = [plugin_list[i:i + 10] for i in range(0, len(plugin_list), 10)]

        plugin_number_map = {}
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

        # Try creating a Carbonara paste
        carbonara_url = create_carbonara_paste(help_text.strip())
        if "Error" in carbonara_url:
            # Fallback to Hastebin if Carbonara fails
            hastebin_url = create_hastebin_paste(help_text.strip())
            if "Error" in hastebin_url:
                await message.reply(hastebin_url)  # Show Hastebin error
            else:
                await message.reply(f"Here is the Help Menu (via Hastebin): {hastebin_url}")
        else:
            await message.reply(f"Here is the Help Menu (via Carbonara): {carbonara_url}")
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
