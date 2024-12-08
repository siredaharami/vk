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
    
    # Payload for Carbonara API
    payload = {
        "code": text,
        "theme": "seti",  # Example theme
        "width": 1000,    # Optional
    }
    
    try:
        # Send request to Carbonara API
        response = requests.post(url, json=payload)
        
        # Log the response for debugging
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"  # Log the error response
        
        # Ensure response contains valid JSON
        try:
            data = response.json()
        except ValueError:
            return "Error: Invalid JSON response from the server."

        # Return the URL if present
        if "url" in data:
            return data["url"]
        else:
            return "Error: No URL in the response."
    except requests.RequestException as e:
        return f"Error while creating paste: {str(e)}"

# Command to show help (list of available plugins with Carbonara link)
@app.on_message(filters.command("help1"))
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

        # Create Carbonara paste
        carbonara_url = create_carbonara_paste(help_text.strip())
        
        if "Error" in carbonara_url:
            await message.reply(carbonara_url)  # Show detailed error
        else:
            await message.reply(f"Here is the Help Menu: {carbonara_url}")
    else:
        await message.reply("No plugins added yet.")
