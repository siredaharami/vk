from pyrogram import Client, filters
from pyrogram.types import Message
from CakeMusic import app

# Dictionary to store plugin details automatically
plugin_details = {}

# Global variable to keep track of the current plugin being viewed
current_plugin_index = {}

# Decorator to register plugins automatically
def plugin(name, description):
    def decorator(func):
        plugin_details[name] = description.strip()
        return func
    return decorator

# Command to show help (list of available plugins with numbers or specific details)
@app.on_message(filters.command("help"))
async def help(client: Client, message: Message):
    global current_plugin_index

    user_name = message.from_user.first_name or "User"
    user_id = message.from_user.id

    # Check if a number is provided after the command
    if len(message.command) > 1:
        try:
            plugin_number = int(message.command[1])  # Get the plugin number
        except ValueError:
            await message.reply(f"Hey {user_name}, invalid plugin number. Please provide a valid number.")
            return

        # Get the plugin details if the number is valid
        if plugin_number > 0 and plugin_number <= len(plugin_details):
            plugin_name = list(plugin_details.keys())[plugin_number - 1]  # Get plugin by number
            plugin_description = plugin_details[plugin_name]
            
            # Extract commands from the description
            commands = [line.split(":")[1].strip() for line in plugin_description.splitlines() if line.startswith("- **Command**")]
            total_commands = len(commands)
            commands_list = "\n".join(f"- {cmd}" for cmd in commands)

            formatted_description = f"""Hey **{user_name}** 👋, here are the details:

**Plugin Details:**
**Name**: `{plugin_name}`
**Total Commands**: {total_commands}

**Commands List:**
{commands_list}

**Description**:
{plugin_description}
"""
            # Update the current plugin index for the user
            current_plugin_index[message.from_user.id] = plugin_number
            await message.reply(formatted_description)
        else:
            await message.reply(f"Hey {user_name}, no details found for plugin number '{plugin_number}'.")
    else:
        # Custom help text
        help_text = f"""
📚 **Help Menu for {user_name}** 📚
Below is a list of all available plugins. Use `/help <plugin_number>` to view the details of a specific plugin.
"""

        # Generate plugin rows dynamically
        plugin_list = list(plugin_details.keys())
        for idx, plugin in enumerate(plugin_list, start=1):
            help_text += f"{idx}. 🌟 `{plugin}`\n"

        # Send the help menu
        await message.reply(help_text)

# Command to show the next plugin's details
@app.on_message(filters.command("next"))
async def next_plugin(client: Client, message: Message):
    global current_plugin_index

    user_name = message.from_user.first_name or "User"

    user_id = message.from_user.id
    if user_id not in current_plugin_index:
        await message.reply(f"Hey {user_name}, please use `/help <number>` to start viewing plugin details.")
        return

    current_index = current_plugin_index[user_id]
    if current_index < len(plugin_details):
        current_index += 1
        plugin_name = list(plugin_details.keys())[current_index - 1]
        plugin_description = plugin_details[plugin_name]

        # Extract commands from the description
        commands = [line.split(":")[1].strip() for line in plugin_description.splitlines() if line.startswith("- **Command**")]
        total_commands = len(commands)
        commands_list = "\n".join(f"- {cmd}" for cmd in commands)

        formatted_description = f"""Hey **{user_name}** 👋, here are the details:

**Plugin Details:**
**Name**: `{plugin_name}`
**Total Commands**: {total_commands}

**Commands List:**
{commands_list}

**Description**:
{plugin_description}
"""
        current_plugin_index[user_id] = current_index
        await message.reply(formatted_description)
    else:
        await message.reply(f"Hey {user_name}, you are already viewing the last plugin.")

# Command to show the previous plugin's details
@app.on_message(filters.command("back"))
async def back_plugin(client: Client, message: Message):
    global current_plugin_index

    user_name = message.from_user.first_name or "User"

    user_id = message.from_user.id
    if user_id not in current_plugin_index:
        await message.reply(f"Hey {user_name}, please use `/help <number>` to start viewing plugin details.")
        return

    current_index = current_plugin_index[user_id]
    if current_index > 1:
        current_index -= 1
        plugin_name = list(plugin_details.keys())[current_index - 1]
        plugin_description = plugin_details[plugin_name]

        # Extract commands from the description
        commands = [line.split(":")[1].strip() for line in plugin_description.splitlines() if line.startswith("- **Command**")]
        total_commands = len(commands)
        commands_list = "\n".join(f"- {cmd}" for cmd in commands)

        formatted_description = f"""Hey **{user_name}** 👋, here are the details:

**Plugin Details:**
**Name**: `{plugin_name}`
**Total Commands**: {total_commands}

**Commands List:**
{commands_list}

**Description**:
{plugin_description}
"""
        current_plugin_index[user_id] = current_index
        await message.reply(formatted_description)
    else:
        await message.reply(f"Hey {user_name}, you are already viewing the first plugin.")

# Example plugins added using the @plugin decorator
@app.on_message(filters.command("example"))
@plugin(
    name="animation",
    description="""
- **Command**: /dog
- **Command**: /cat
- **Command**: /rat 
- **Description**: This is an example plugin for animations.
- **Usage**: Type /dog or /cat to see the animation commands.
"""
)
async def example(client: Client, message: Message):
    await message.reply("Example plugin is active!")
