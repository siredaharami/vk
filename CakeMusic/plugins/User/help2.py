from pyrogram import Client, filters
from pyrogram.types import Message
from CakeMusic import app
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Dictionary to store plugin details automatically
plugin_details = {}

# Decorator to register plugins automatically
def plugin(name, description):
    def decorator(func):
        plugin_details[name] = description
        return func
    return decorator

# Function to create carbon-style image
def generate_carbon_image(text: str) -> BytesIO:
    # Set font and image size
    font_path = "arial.ttf"  # Replace with your font file
    font_size = 20
    width, height = 800, 1200  # Adjust dimensions based on content
    padding = 20

    # Create an image with white background
    image = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        raise ValueError("Font not found. Please provide a valid font path.")

    # Add text to the image
    text_x, text_y = padding, padding
    lines = text.split("\n")
    for line in lines:
        draw.text((text_x, text_y), line, fill="white", font=font)
        text_y += font_size + 5

    # Crop image to content
    cropped_image = image.crop((0, 0, width, text_y + padding))
    
    # Save to BytesIO object
    output = BytesIO()
    cropped_image.save(output, format="PNG")
    output.seek(0)
    return output

# Command to show help (list of available plugins with numbers as Carbon-style image)
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

        # Generate Carbon-style image
        carbon_image = generate_carbon_image(help_text.strip())
        await message.reply_photo(carbon_image, caption="Here is the Help Menu in Carbon style.")
    else:
        await message.reply("No plugins added yet.")

# Command to show plugin details by number
@app.on_message(filters.command("help "))
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
